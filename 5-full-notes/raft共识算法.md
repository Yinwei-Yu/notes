Time:2025-10-14

Status: 

- [ ] **working** 👨‍💻
- [x] *done*    💻

Tags:[[3-tags/distributed|distributed]]

# replicated state machines

复制状态机用于解决分布式系统中的容错问题。

采用复制日志的方式实现。（同样的起始状态，同样的输入->同样的结果）

![[2-source-material/images/Pasted image 20251014090339.png]]

具体工作:client向server发起请求,server将此请求设置到log列表中,通过共识算法与其他server交流,当此log被大多数server复制后,server应用此log,返回client.

共识算法的工作为:保持复制日志的一致性

共识算法通常有如下性质:

1. 在非拜占庭情况下,保证安全性(日志一致性),如网络导致的包丢失,重复,乱序等.这意味着,共识算法无法解决某一个server发送恶意信息的情况.
2. 只要大多数服务器可用,共识算法就可以正常工作(2f+1台机器的容错上限为f)
3. 不依赖时钟进行同步
4. 普遍情况下,只要大多数server复制了log,log便可应用,一两个缓慢的server不会拖慢整体

# Raft basics

raft将共识问题分为三个子问题:

1. leader选举
2. 日志复制
3. 安全性保证

在任意时刻,一个server处于三种状态之一:

1. leader
2. candidate
3. follower

任何时刻,整个集群中,有且只有一个leader,这一点在后面会谈到如何实现.

**follower**的工作十分简单:他们不发出任何request,只简单的回复来自candidate和leader的信息.**leader**处理所有来自client的request(如果一个client联系了follower,follower转发给leader).**candidate**用来选举新的leader.

他们的转换关系为:启动时,所有server都为follower.当一个follower发现超过election time后没有收到leader的心跳信息,则开启新的term,发起选举,变为candidate.candidate在选举时间结束后仍没有收到leader的信息,则继续保持选举,若收到,则变为follower.一个candidate收到多数server的投票后,转换为leader.leader发现一个server的term大于自己后,转换为follower.

![[2-source-material/images/Pasted image 20251014091948.png]]

raft将时间划分为任意长度的term(任期).每个任期伴随着一个唯一的递增整数.每个任期开始时,集群会进行选举,从candidate选出一个leader.如果产生split vote,该term没有leader,会进入下一个term,重新开始选举.

![[2-source-material/images/Pasted image 20251014092120.png]]

不同的服务器可能在不同的时间观察到term信息,因此可能出现leader过期的情况.因此term起到一个逻辑时钟的效果,每个server存储一个current term号,随着时间单调递增.当server之间交互时,会交换彼此的任期号,如果一个server发现自己任期号小于其他的,则更新为更大的值.如果一个candidate或者leader发现自己的term过期了,则立刻回退为follower状态.如果一个server收到一个过期term的server的请求,则拒绝该请求.

Raft使用到两个RPC.

RequestVote RPC在选举阶段由candidate发起,AppendEntries RPC只能由leader发送,用于复制log,也用作心跳.RPC过期的话,则server重发.server并行发送RPC.

在讨论leader选举,日志复制,安全性,首先介绍raft保证的性质:

1. election safety:在一个term内,最多只有一个leader
2. leader append-only:一个leader从不覆写或者删除自己的log,只append新的entry.
3. log matching:如果两个log有相同的index和term,那么在给定index前的所有entry都相同
4. leader completeness:如果一个log entry在一个term内被**committed**,那么该entry在之后的所有term中,都会在leader的log中
5. state machine safety:如果一个server把某个index的log entry应用到状态机上(committed),那么该index处不会有其他的log entry

# Leader election

raft采用心跳机制来触发leader选举.当server启动时,均为follower状态.一个server只要收到来自leader或者candidate的message,就保持follower状态.leader周期性地发送心跳(不包含log entry的appendEntriesRPC),来维持自己的地位.如果一个follower在election timeout后,没有收到信息,就假设没有可见的leader,它发起选举.

follower发起选举的过程是:

1. 增加自己current term
2. 转换为candidate
3. 给自己投票
4. 并行向其他集群中的server发送RPC

一个candidate持续处理该状态直到下面三个事件之一发生:

1. 赢得选举
2. 其他server成为leader
3. 超时,而且没有leader产生.

*赢得选举*:当candidate收到集群中大多数server的vote后,赢得选举.每个server最多给一个candidate投票,采用先到先得的方式.保证了最多只有一个candidate可以赢得选举.当一个candidate赢得选举后,它向其他server发送心跳,声明自己的leader地位,避免新的选举

*其他server成为leader*:在candidate等待vote的时候,可能收到其他server的心跳信息,即当选leader声明.如果其term大于等于当前candidate的term,则candidate变为follower;否则,candidate拒绝此rpc,保持candidate状态

*超时*:如果多个follower同时成为candidate,则会产生split vote,因为没有candidate获得大多数server的投票,这种情况下,会产生election timeout,并开始新一轮的选举.最坏情况下,这种情况会持续发生.解决方式是:使用随机election timeouts.每个server随机在150-300ms内选取election timeouts.

# Log replication

当leader被选举后,它开始处理client的请求,每个client请求包含一个command, leader将该command追加到自己的log中作为一个new entry.然后向其他server发送AppendEntries RPC,当该log被大多数server复制后,leader commit此log.如果一个server因为网络问题没有成功复制,则leader无限重复发送.

Log entry的组织形式为:一个状态机命令,一个term号.同时,一个entry还有一个index,决定其在log中的位置.

Raft保证,一个committed的entry会持久化,最终每个server上都会将该entry应用到状态机.当大多数server复制了一个entry后,leader commit此entry,并且也会commit所有之前的log entries,包括其他leader创建的entries.当发生leader更换后,需要额外的规则,下面会讨论.leader会维护一个自己一直的最高的将要被commit的index号,并在AppendEntries RPCs中包含此号.当follower发现一个log entry被committed后,会把该entry应用到自己的状态机中.

Raft保证下面两个性质,共同构成了log matching的性质:

1. 如果两个不同log中的entries有相同的index和term,那么他们存储的command相同(也就是说不同server的log中,同一个位置,同一任期的log entry是一样的)
2. 同样的条件下,在当前这个相同的index前的所有entries都相同.

第一个性质:leader在一个给定的term和index下,只会创建一个唯一的entry.

第二个性质:依靠AppendEntries RPC检查,leader在log中包含新entry之前的那一个entry的index和term.如果follower的log中没有这个index和term的entry,则follower拒绝该新entry.这个consistency check是一个递归的步骤.

当一切正常时,leader和follower的log是一致的.leader宕机可能会导致log的不一致(old leader还没来得及复制它的全部日志),当频繁发生时,可能导致follower缺少leader中的entry,也可能包含leader中没有的entry.

Raft的解决方式是:leader强制follower的log和自己相同.即:如果follower的log和自己有冲突,则覆写follower的log.

步骤:

1. 找到leader和follower相同的log entry
2. 删除follower中该entry后的部分
3. leader发送该点后的所有entry

这些步骤仅通过AppendEntries RPC完成.leader为每个follower维护一个nextIndex ,代表leader将要发送给follower的下一个entry的index.当一个candidate当选leader后,他把所有follower的nextIndex设置为它log的最后一位的下一个数字.

如果follower的log和leader不相同,则AppendEntries RPC返回失败,leader会递减nextIndex再发送,这样持续下去,就会找到matching point.找到后,追加日志信息(注意,这里是追加matching point后的全部日志,不是一条一条地追加)

这种机制让leader不需要额外的机制就可以保证一致性.leader永远不覆写或者删除自己的日志.

# Safety

上述机制不能保证每个server的状态机按照相同的顺序执行相同的命令.

比如说:一个follower在leader commit log entry时宕机了,但是之后它又被选举为leader,这会导致已经commit的记录丢失.

## Election restriction

Raft中log entry只有一个流向:leader to follower

在选举阶段,一个candidate必须包含所有已经committed的log entries才能够被选举.一个candidate必须和集群中的大多数交流来获得选票,意味着每个committed entry一定会在至少一个server中有.

RequestVote RPC有一个机制:RPC包含candidate的log信息,如果voter发现自己的log**更新**,则拒绝投票.

*更新*:两个log比较,如果最后一个entry的term不同,term大的更新.如果term相同,则谁的log更长谁更新

## Committing entries from previous terms

leader知道一个entry被committed,如果该entry被大多数server复制.如果leader在commit之前挂了,后来的leader会尝试完成复制该entry.但是,一个leader不能立刻提交前一个任期内的entry,即使被大多数server复制.它只能在自己的任期内,在下一次提交时,顺带地把前一个term的entry提交了.一个例子如下:

![[2-source-material/images/Pasted image 20251014120834.png]]

S1开始是leader,复制了index 2.在b时刻,s1宕机,s5接管(s3,s4投票),在index 2 收到一个不同的entry.c时刻,s5宕机,s1重新当选为leader(s2,s3,s4投票),开始term4,并继续复制index 2的entry,此时index 2的entry已经在大多数server上了,但是还没s1还没来的及提交index 3,就又宕机了.然后s5再次成为leader,复制自己的entry,这会覆写index 2处的日志.

如果s1在成为leader并复制了大多数entry后就在提交4之前提交2,那么会导致已提交的entry被覆写,造成不安全.

Raft的解决方案是:leader只能提交当前term的entry.根据log matching性质,此前的entry也会匹配.

## Follower and candidate crashes

follower或者candidate宕机后,rpc会失效,Raft无限重试.

如果一个server收到了rpc并执行完成后宕机了,没有发送返回信号,当它重启时,由于Raft的rpc是幂等的,所以没影响.

## Timing and availability

在election timeout,传播时延(broadcastTime)和MTBF(mean time between failures)之间,需要有大小关系:

$$
broadcastTime \ll electionTimeout \ll MTBF
$$

很好理解,rpc信号必须要在超时之前收到,否则会一直选举.

Raft要求把信息存储到底层存储中,所以broadcast time通常为0.5ms-20ms
election timeout在10ms-500ms之间.MTBF通常为几个月.

# Log Compaction

日志不能无限增长.采用snapshot来压缩日志

snapshot当前状态到磁盘,然后删除该点前的所有日志

![[2-source-material/images/Pasted image 20251019155313.png]]

压缩了日志1-5的结果

每个server做自己的snapshot,包括当前的状态机状态,以及一些元信息.

leader需要偶尔向落后的follower发送snapshot,这种情况只在follower很慢,或者新server加入的情况.

leader使用一个新的RPC来发送snapshot--InstallSnapshot.

当follower收到snapshot后,做:
1. 如果snapshot中有follower中没有的新信息,follower抛弃自己的所有日志,应用snapshot.
2. 如果snapshot是follower日志的一个前缀,则压缩snapshot部分,后继保持

影响snapshot的性能因素:

1. server必须决定何时进行snapshot,太短浪费磁盘IO,太久导致日志过大,而且增加重启时应用日志的时间.*策略是选择一个固定size,日志达到此size后,进行压缩*
2. 写snapshot会耗费大量时间,我们不希望这对普通操作造成延迟,*采用写时复制*来优化.

# Client interaction

client开始先向随机的server发送请求,如果对方不是leader,则请求被转发给leader,并且通知client leader的ip.

为防止出现,leader提交了client的请求,但是在回复client前宕机,导致client重发,同一命令执行两次的情况,规定每个client的操作需要加上序列号.

只读操作也需要额外操作来防止读取到过期数据,这出现在网络分区中old leader并不知道新leader已经产生的情况下.

1. leader必须拥有所有已提交的entries信息,但是在其term开始时,他不能确定哪些是已提交的entries哪些不是,所以,leader在其term开始时,需要进行一个空提交(no-op),来提交其前面的日志.

2. leader在执行只读操作前,需要和集群大多数交换心跳信息来确认自己的leader地位.这是Raft想要实现线性一致性的要求,毫无疑问降低了性能.在实际中需要做trade-off,基本选择准确性换性能

# AI Summarize

## 1. 复制状态机 (Replicated State Machines - RSM)

**核心思想：**
通过复制日志的方式，在分布式系统中实现容错。基本原理是：如果所有服务器从相同的初始状态开始，并以相同的顺序处理相同的输入（日志条目），那么它们将达到相同的最终状态。

**工作流程：**
1.  客户端向服务器发起请求。
2.  服务器将请求作为日志条目添加到其本地日志中。
3.  服务器通过共识算法与其他服务器通信，将该日志条目复制到大多数服务器。
4.  一旦日志条目被大多数服务器复制（即“已提交”），服务器将其应用到本地状态机。
5.  服务器向客户端返回响应。

**共识算法的目标：** 维护所有服务器上复制日志的一致性。

**Raft 共识算法的性质：**
1.  **安全性 (Safety)：** 在非拜占庭（Byzantine）故障模型下，保证日志的一致性（即使存在网络分区、包丢失、重复或乱序）。它不处理服务器发送恶意信息的情况。
2.  **可用性 (Availability)：** 只要大多数服务器可用，共识算法就能正常工作。在拥有 $2f+1$ 台机器的集群中，最多可以容忍 $f$ 台机器的故障。
3.  **无时钟依赖：** Raft 不依赖精确的时钟同步。
4.  **高效性：** 通常情况下，一旦日志条目被大多数服务器复制，就可以被应用，少数缓慢的服务器不会拖慢整体进度。

## 2. Raft 基本概念

Raft 将共识问题分解为三个子问题：
1.  **Leader 选举 (Leader Election)**
2.  **日志复制 (Log Replication)**
3.  **安全性保证 (Safety)**

### 2.1 服务器状态

在任何时刻，服务器都处于以下三种状态之一：
*   **Follower (跟随者)：** 被动接收来自 Leader 或 Candidate 的信息，不主动发起通信。
*   **Candidate (候选者)：** 参与 Leader 选举过程。
*   **Leader (领导者)：** 处理所有客户端请求，并负责复制日志到其他服务器。

**状态转换：**
*   **启动时：** 所有服务器都是 Follower。
*   **Follower → Candidate：** 当 Follower 在一个“选举超时”（election timeout）时间内没有收到 Leader 的心跳（AppendEntries RPC）时，它会增加自己的任期号（term），转变为 Candidate，并开始新的选举。
*   **Candidate → Leader：** 当 Candidate 在选举超时内收到集群中大多数服务器的投票后，它赢得选举，转变为 Leader。
*   **Candidate → Follower：**
    *   收到一个来自新 Leader 的 AppendEntries RPC（如果新 Leader 的任期号大于等于 Candidate 的当前任期号）。
    *   选举超时后仍未赢得选举，且没有新的 Leader 出现，则可能重新开始选举。
*   **Leader → Follower：** 当 Leader 发现存在一个任期号大于自己的服务器时，它会立即退回 Follower 状态。

### 2.2 任期 (Term)

*   Raft 将时间划分为任意长度的“任期”（term），每个任期由一个唯一的递增整数标识。
*   每个任期开始时，集群会进行一次选举，尝试选出一个 Leader。
*   如果选举出现“票数分裂”（split vote），则该任期可能没有 Leader，选举将进入下一个任期。
*   **任期号 (Current Term)：** 每个服务器存储一个 `currentTerm` 号，它会随着时间单调递增。当服务器之间通信时，会交换任期号。
    *   如果一个服务器发现自己的任期号小于收到的任期号，它会更新自己的任期号为较大的值。
    *   如果一个 Candidate 或 Leader 发现自己的任期号已过期（收到来自其他服务器的更大任期号），它会立即回退到 Follower 状态。
    *   如果服务器收到一个来自过期任期（小于自身 `currentTerm`）的请求，它会拒绝该请求。

### 2.3 RPC 通信

Raft 使用两种 RPC：
*   **RequestVote RPC：** 由 Candidate 在选举阶段发起，用于请求其他服务器的投票。
*   **AppendEntries RPC：**
    *   由 Leader 发送，用于复制日志条目到 Follower。
    *   也用作心跳机制，以维持 Leader 的地位。
    *   如果 RPC 因超时而失败，服务器会重试。服务器会并行发送 RPC 给集群中的其他服务器。

### 2.4 Raft 保证的性质

1.  **Election Safety (选举安全)：** 在任何一个任期内，最多只有一个 Leader 被选举出来。
2.  **Leader Append-Only (Leader 追加日志)：** Leader 永远不会覆盖或删除自己日志中的条目，只会追加新的条目。
3.  **Log Matching (日志匹配)：** 如果两个日志在某个索引位置具有相同的任期号，那么从该索引开始之前的所有日志条目都必须相同。
4.  **Leader Completeness (Leader 完整性)：** 如果一个日志条目在一个任期内被提交（committed），那么该条目在之后的所有任期中，都将出现在 Leader 的日志中。
5.  **State Machine Safety (状态机安全)：** 如果一个服务器将某个索引位置的日志条目应用到其状态机上（即该条目已被提交），那么该服务器不会再将其他任何日志条目应用到该索引位置。

## 3. Leader 选举 (Leader Election)

*   **心跳机制：** Leader 周期性地向所有 Follower 发送心跳（AppendEntries RPC，不包含日志条目），以维持其 Leader 地位。
*   **选举超时 (Election Timeout)：** 如果一个 Follower 在一个选举超时时间内没有收到来自 Leader 或 Candidate 的消息，它会假设当前没有可用的 Leader，并触发一次新的选举。
*   **选举过程：**
    1.  Follower 增加自己的 `currentTerm`。
    2.  将自己转变为 Candidate 状态。
    3.  给自己投票。
    4.  并行向集群中的其他服务器发送 `RequestVote RPC`。
*   **Candidate 的持续状态：** Candidate 持续其状态直到以下三者之一发生：
    *   **赢得选举：** 当 Candidate 收到集群中大多数服务器的投票后，它赢得选举。
        *   **投票规则：** 每个服务器在一个任期内最多只能给一个 Candidate 投票，采用“先到先得”的原则。这保证了最多只有一个 Candidate 能赢得选举。
        *   赢得选举后，Candidate 立即转变为 Leader，并开始向其他服务器发送心跳，以声明其 Leader 地位并阻止新的选举。
    *   **其他服务器成为 Leader：** 在等待投票期间，Candidate 可能收到其他服务器成为 Leader 的心跳（AppendEntries RPC）。
        *   如果该 Leader 的任期号大于等于 Candidate 的当前任期号，Candidate 会转变为 Follower。
        *   否则（Leader 的任期号小于 Candidate 的任期号），Candidate 会拒绝该 RPC，并保持 Candidate 状态。
    *   **选举超时且无 Leader 产生：** 如果 Candidate 在选举超时时间内没有赢得选举，也没有收到其他 Leader 的消息，它会进入下一个任期，并开始新一轮选举。
*   **解决票数分裂 (Split Vote)：**
    *   当多个 Follower 同时成为 Candidate 时，可能出现票数分裂，导致没有 Candidate 获得大多数投票。
    *   这种情况会导致选举超时，并开始新一轮选举。
    *   **随机化 Election Timeout：** 为了解决这种情况可能持续发生的问题，Raft 要求每个服务器随机选择一个选举超时时间（通常在 150-300ms 之间）。这大大降低了多个服务器同时成为 Candidate 的概率，并加速了选举过程。

## 4. 日志复制 (Log Replication)

*   **Leader 处理请求：** 一旦 Leader 被选举出来，它就开始处理客户端的请求。每个请求包含一个状态机命令。
*   **追加日志条目：** Leader 将客户端命令追加到自己的日志中，形成一个新的日志条目（Log Entry）。每个条目包含命令、当前任期号以及在日志中的索引位置。
*   **发送 AppendEntries RPC：** Leader 向所有 Follower 发送 `AppendEntries RPC`，包含新的日志条目。
*   **提交日志条目 (Commit)：** 当一个日志条目被大多数服务器复制后，Leader 将该条目标记为“已提交”（committed）。Leader 会维护一个“最高已提交索引”（`commitIndex`），并将其包含在 `AppendEntries RPC` 中发送给 Follower。
*   **Follower 应用日志：** 当 Follower 收到 `AppendEntries RPC` 并发现其中的日志条目已被 Leader 提交后，它会将该条目应用到自己的状态机中。
*   **持久化：** Raft 保证已提交的日志条目是持久化的，并且最终会应用到所有服务器的状态机上。
*   **Log Matching 性质的保证：**
    1.  **唯一性：** Leader 在一个给定的任期和索引下，只会创建一个唯一的日志条目。
    2.  **一致性检查：** `AppendEntries RPC` 包含前一个日志条目的索引和任期号。如果 Follower 的日志在该索引位置没有匹配的条目，它会拒绝该 RPC。这个检查是递归的，直到找到匹配点。
*   **处理日志不一致：**
    *   当 Leader 宕机后重启，或者频繁发生 Leader 切换时，可能导致 Follower 的日志与 Leader 不一致（Follower 可能缺少 Leader 中的条目，或包含 Leader 中没有的条目）。
    *   **Raft 的强制同步机制：** Leader 通过强制覆盖 Follower 的日志来解决不一致问题。
        *   Leader 为每个 Follower 维护一个 `nextIndex`，表示下一个要发送给该 Follower 的日志条目的索引。
        *   当 Leader 被选举后，它会将所有 Follower 的 `nextIndex` 初始化为自己日志的最后一个条目索引加一。
        *   如果 `AppendEntries RPC` 因日志不匹配而失败，Leader 会递减 `nextIndex` 并重试，直到找到匹配点。
        *   一旦找到匹配点，Leader 会将该点之后的所有日志条目发送给 Follower，强制覆盖 Follower 中不匹配的部分。
*   **Leader 不修改日志：** Leader 永远不会修改或删除自己的日志条目。

## 5. 安全性保证 (Safety)

### 5.1 Election Restriction (选举限制)

*   **单向日志流：** Raft 的日志条目只从 Leader 流向 Follower。
*   **投票资格：** 为了保证日志的完整性，一个 Candidate 只有在包含所有已提交（committed）的日志条目时，才有资格被选举为 Leader。
*   **RequestVote RPC 中的日志信息：** `RequestVote RPC` 会包含 Candidate 的日志信息（最后一个条目的任期号和索引）。
    *   **投票规则：** 如果投票者（voter）发现自己的日志比 Candidate 的日志“更新”（即拥有更多已提交的条目），则拒绝投票。
    *   **日志更新判断：**
        *   如果两个日志的最后一个条目任期号不同，则任期号较大的日志被认为是更新的。
        *   如果最后一个条目的任期号相同，则日志更长的被认为是更新的。

### 5.2 Committing Entries from Previous Terms (提交前任期日志)

*   **问题：** 如果 Leader 在提交某个日志条目（例如索引为 2 的条目）之前宕机，并且后续选举产生了新的 Leader（例如，新的 Leader 提交了它自己任期内的条目，例如索引为 3 的条目），那么旧 Leader 尝试提交的索引 2 的条目可能会被新 Leader 覆盖，导致已提交的记录丢失。
*   **Raft 的解决方案：** Leader 只能提交**当前任期内**的日志条目。
    *   当 Leader 提交了当前任期内的某个条目（例如索引为 4 的条目）后，根据 Log Matching 性质，所有之前的条目（包括前任期内的条目，如索引 2 和 3）也会被隐式地匹配和提交。
    *   **空提交 (No-op)：** 为了确保在 Leader 刚上任时，能够确定哪些旧日志条目已被提交，Raft 要求 Leader 在其任期开始时，先进行一次“空提交”（no-op）操作。这个空提交会提交它自己日志中所有在它成为 Leader 之前就已经被大多数服务器复制的条目。
    *   **只读操作的安全性：** 为了防止在网络分区中，旧 Leader（不知道新 Leader 已产生）执行只读操作时读取到过期数据，Raft 要求 Leader 在执行只读操作前，必须先与集群中的大多数服务器进行心跳通信，以确认自己仍然是 Leader。这保证了线性一致性，但会降低性能。

### 5.3 Follower and Candidate Crashes (跟随者和候选者崩溃)

*   **RPC 重试：** 如果 Follower 或 Candidate 崩溃，发送给它们的 RPC 会失败。Raft 会无限重试这些 RPC，直到服务器恢复。
*   **幂等性：** 如果一个服务器在执行完 RPC 并发送响应之前崩溃，重启后由于 Raft 的 RPC 是幂等的，不会产生影响。

### 5.4 Timing and Availability (时序与可用性)

*   **关键时序关系：** 为了保证 Raft 的稳定运行和可用性，需要满足以下时序关系：
    $$
    broadcastTime \ll electionTimeout \ll MTBF
    $$
    *   `broadcastTime` (RPC 传播时间)：必须远小于选举超时时间，以确保心跳能在超时前到达。通常为 0.5ms - 20ms。
    *   `electionTimeout` (选举超时时间)：必须远小于服务器平均故障间隔时间（MTBF），以确保在服务器发生故障前能完成选举。通常为 10ms - 500ms。
    *   `MTBF` (Mean Time Between Failures)：服务器平均故障间隔时间，通常为数月。
*   **持久化存储：** Raft 要求将信息（如日志条目、任期号、投票记录）存储到底层持久化存储中，以确保在服务器重启后数据不丢失。这使得 `broadcastTime` 通常非常接近于 0。

## 6. 日志压缩 (Log Compaction)

*   **问题：** 日志会随着时间的推移无限增长，占用大量存储空间。
*   **解决方案：快照 (Snapshot)**
    *   服务器将当前状态机状态以及相关的元数据（如最后已提交的日志索引和任期号）持久化到磁盘。
    *   然后，删除该快照点之前的所有日志条目。
*   **快照过程：**
    *   每个服务器独立执行快照操作。
    *   **Leader 发送快照：** 当 Follower 严重落后于 Leader，或者有新服务器加入集群时，Leader 会使用 `InstallSnapshot RPC` 向 Follower 发送快照。
    *   **Follower 应用快照：**
        1.  如果快照包含 Follower 本地日志中没有的新信息，Follower 会丢弃自己的所有日志，并应用快照。
        2.  如果快照是 Follower 日志的前缀，则 Follower 会保留快照部分之后的内容，并应用快照。
*   **快照性能影响与优化：**
    1.  **快照时机选择：** 需要权衡快照频率。太频繁会增加磁盘 I/O 开销；太久会导致日志过大，增加服务器重启时应用日志的时间。通常采用固定日志大小策略，达到阈值后进行压缩。
    2.  **写时复制 (Copy-on-Write)：** 为了避免写快照操作对普通操作造成延迟，可以采用写时复制技术来优化。

## 7. 客户端交互 (Client Interaction)

*   **请求路由：**
    1.  客户端首先向集群中的**任意服务器**发送请求。
    2.  如果该服务器不是 Leader，它会将请求**转发给 Leader**，并通知客户端 Leader 的 IP 地址。
    3.  客户端随后将请求发送给 Leader。
*   **防止重复执行：**
    *   为了防止 Leader 在提交了客户端请求但回复客户端之前宕机，导致客户端重发请求而造成同一命令被执行两次的情况，Raft 为每个客户端操作引入了**序列号 (Serial Number)**。
    *   Leader 会跟踪每个客户端的最后一个已执行序列号，并只执行序列号大于该值的请求。
*   **只读操作的安全性：**
    *   只读操作（如查询状态机状态）也需要额外的机制来防止读取到过期数据，尤其是在网络分区和旧 Leader 仍然活跃的情况下。
    *   **Raft 的解决方案（线性一致性）：**
        1.  **Leader 必须拥有所有已提交的日志条目：** Leader 在其任期开始时，通过一次空提交（no-op）来确保其日志中的所有条目都被提交。
        2.  **Leader 确认 Leader 身份：** 在执行只读操作前，Leader 必须与集群中的大多数服务器交换心跳信息，以确认自己仍然是 Leader。
    *   **性能权衡：** Raft 实现的线性一致性虽然保证了数据的准确性，但会降低性能。在实际应用中，通常需要在准确性和性能之间做出权衡，例如选择牺牲部分一致性来换取更高的吞吐量。

## 术语表

| 术语 | 英文 | 定义 | 应用/解释 |
|---|---|---|---|
| **复制状态机** | Replicated State Machine (RSM) | 分布式系统中通过复制日志实现容错的一种模型。所有节点从相同初始状态开始，按相同顺序处理相同输入，达到相同状态。 | 容错分布式系统的基础模型。 |
| **日志条目** | Log Entry | 存储在复制日志中的一条记录，包含状态机命令、任期号和索引位置。 | Raft 中传递状态变更的基本单位。 |
| **共识算法** | Consensus Algorithm | 分布式系统中，使所有节点就某个值或状态达成一致的算法。 | 保证分布式系统数据一致性和容错性的核心。 |
| **拜占庭故障** | Byzantine Fault | 节点可能发送任意错误信息，甚至恶意信息，表现行为不可预测。 | Raft 假设的是非拜占庭故障（如网络问题、节点崩溃）。 |
| **Leader 选举** | Leader Election | 在分布式集群中，通过特定机制选出一个节点作为 Leader 的过程。 | Raft 的核心子问题之一，保证集群有且只有一个 Leader。 |
| **日志复制** | Log Replication | 将 Leader 的日志条目同步到其他 Follower 服务器的过程。 | Raft 的核心子问题之一，保证数据一致性。 |
| **安全性** | Safety | 保证分布式系统不出现不一致状态的性质。 | Raft 保证日志一致性、状态机一致性等。 |
| **可用性** | Availability | 保证系统在部分节点故障时仍能正常工作的性质。 | Raft 只要大多数节点可用即可工作。 |
| **任期** | Term | Raft 时间划分的基本单位，由递增整数标识，每个任期开始时进行一次选举。 | 用于区分不同时期，解决 Leader 过期问题。 |
| **选举超时** | Election Timeout | Follower 在未收到 Leader 心跳后触发选举的时间间隔。 | 用于检测 Leader 失联并启动选举。 |
| **票数分裂** | Split Vote | 在选举中，没有 Candidate 获得足够多的选票，导致该任期无 Leader 产生。 | 通过随机化选举超时来解决。 |
| **RPC** | Remote Procedure Call | 远程过程调用，用于服务器之间的通信。 | Raft 使用 RequestVote RPC 和 AppendEntries RPC。 |
| **RequestVote RPC** | RequestVote RPC | Candidate 发起，用于请求投票的 RPC。 | 选举阶段的关键通信。 |
| **AppendEntries RPC** | AppendEntries RPC | Leader 发起，用于复制日志条目和发送心跳的 RPC。 | 日志复制和心跳机制的核心。 |
| **已提交 (Committed)** | Committed | 指一个日志条目已被大多数服务器复制，并保证最终会被应用到所有服务器的状态机上。 | Raft 中日志状态的重要里程碑。 |
| **状态机** | State Machine | 接收命令并改变状态的抽象模型。 | 复制状态机的核心组成部分。 |
| **日志匹配** | Log Matching | 保证两个日志在相同索引和任期下，其内容及之前的条目都相同的性质。 | Raft 的核心性质之一，用于同步日志。 |
| **Leader 完整性** | Leader Completeness | 保证在一个任期内被提交的日志条目，在后续任期中也一定存在于 Leader 的日志中。 | Raft 的核心性质之一。 |
| **状态机安全** | State Machine Safety | 保证一个服务器一旦将某个日志条目应用到状态机，就不会再应用其他条目到该索引位置。 | Raft 的核心性质之一。 |
| **快照** | Snapshot | 将当前状态机状态和相关元数据持久化到磁盘，并删除之前的日志条目，以压缩日志。 | 用于管理日志增长，节省存储空间。 |
| **序列号** | Serial Number | 客户端请求中附加的编号，用于防止重复执行。 | 解决 Leader 提交请求后宕机导致重复执行的问题。 |
| **线性一致性** | Linearizability | 一种强一致性模型，保证所有操作看起来是按某个全局顺序串行执行的。 | Raft 在处理只读操作时追求的目标，但可能影响性能。 |
| **MTBF** | Mean Time Between Failures | 平均故障间隔时间。 | 衡量系统可靠性的指标，用于指导 Raft 的时序设计。 |
| **广播时间** | Broadcast Time | RPC 消息在集群中传播所需的时间。 | Raft 时序设计中的关键参数。 |
| **空提交 (No-op)** | No-op (No Operation) | Leader 在任期开始时执行的一个特殊提交操作，用于提交其之前的日志条目。 | 保证 Leader 完整性，尤其是在 Leader 刚上任时。 |
# Reference

[[2-source-material/papers/raft.pdf|raft]]