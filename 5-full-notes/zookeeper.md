Time:2025-10-26

Status: 

- [ ] **working** 👨‍💻
- [x] *done*    💻

Tags:[[3-tags/distributed|distributed]]

# Introduction

zookeeper是一个面向大型分布式系统的开源分布式协调服务。它将复杂的分布式一致性服务封装起来，对外提供可靠的原语集，来简化分布式应用的开发。让开发者可以专注于应用的开发，而不是将大量精力花在处理分布式的一致性等问题上。

zookeeper暴露的接口具有共享寄存器的无等待特性，并带有类似于分布式文件系统缓存失效的事件驱动机制，以提供一个简单但强大的协调服务。

zookeeper保证每个client级别的FIFO执行的操作顺序。

---

zookeeper实现的是一个coordination kernel，而不是运行在服务器上的协调服务。

zookeeper的api操作简单的无等待数据对象，像在文件树上一样。

zookeeper保证client级别的FIFO，以及写入操作的线性一致性。

zookeeper采用流水线架构，天生支持FIFO，而FIFO又为client提供了异步处理的能力。

为保证更新操作满足线性一致性，zookeeper采用leader-based原子广播协议-zab。主要面向读操作。

client缓存信息十分重要，以leader为例，缓存了leader信息client不再需要每次向zookeeper询问。zookeeper提供watch机制来使client在配置发生变化时及时更新。

# zookeeper service

client通过zookeeper提供的client库api来访问zookeeper服务，该库还管理client与zookeeper之间的网络连接。

## overview

抽象结构：
zookeeper将数据抽象为对象节点（znode
znode采用树状层级结构组织，类似文件系统
znode用于存储元数据信息；除临时节点外，都可以有子节点
znode可以带有顺序号或者时间戳，来表明client操作的顺序

znode类型：
regular：由client显示创建和删除
ephemeral：client创建这些节点后，要么显示删除，要么当session断联后由zookeeper自动删除

watch机制：
及时通知状态变化，避免客户端轮询
一次触发，与会话绑定
只通知发生变化，不包含变化内容

session：
客户端与zookeeper建立连接时，具有一个关联超时时间
当timeout或者zk检测到客户端故障时，session断开
客户端可在 ZK 集群内**透明切换服务器**，会话**持久存在**于切换过程中

## Client API

### 1. 核心 API 操作 (Requests)

| API 方法 | 核心功能 (Keywords) | 特殊参数/标志 (Flags) |
| :--- | :--- | :--- |
| **create** | **创建 ZNode**，存储数据。| `path`, `data`, `flags` (Regular/Ephemeral, Sequential) |
| **delete** | **删除 ZNode**。| `path`, **`version` (条件删除)** |
| **exists** | **检查 ZNode 是否存在**。| `path`, **`watch` (设置监视)** |
| **getData** | **获取数据和元数据**（含版本）。| `path`, **`watch`** (仅当节点存在时生效) |
| **setData** | **写入数据**。| `path`, `data`, **`version` (条件写入)** |
| **getChildren** | **获取子节点名称列表**。| `path`, **`watch` (监视子节点变化)** |
| **sync** | **等待待处理更新**传播到当前服务器。| `path` (目前忽略), **强制同步，确保读取最新数据**。|

### 2. API 调用模式 (Invocation Modes)

| 模式 | 特点 | 适用场景 |
| :--- | :--- | :--- |
| **Synchronous (同步)** | **阻塞 (Blocks)** 直到操作完成。| 单个操作，无并发任务。|
| **Asynchronous (异步)** | **非阻塞**，支持**多个未完成操作**和**并行任务**。| 高并发、高性能场景。|
| **Callback Guarantee** | 客户端保证**回调按顺序 (In order)** 执行。| 确保异步操作结果的有序处理。|

### 3. 设计原则与特性 (Design Principles)

| 特性 | 说明 (Keywords) | 优势 |
| :--- | :--- | :--- |
| **无句柄 (No Handles)** | 请求包含**完整路径 (Full path)**，无 `open()`/`close()`。| **简化 API**，消除服务器端额外状态维护。|
| **条件更新 (Conditional Updates)** | `delete` 和 `setData` 接受 **`expected version`**。| 实现**原子性**操作 (Compare-and-Swap)。版本不匹配则失败。|
| **无版本检查** | 版本号设为 **-1**。| 强制执行操作，不检查版本。|

## zookeeper guarantees

### 1. 基本有序性保证 (Basic Ordering Guarantees)

| 保证名称 | 核心机制/定义 | 影响/优势 |
| :--- | :--- | :--- |
| **Linearizable Writes (A-线性化)** | 所有**更新（Update）**操作都是**可线性化**的（Serializable and respect precedence）。| 提供**强一致性**。满足 A-线性化的系统也满足线性化。|
| **A-Linearizability** | 允许客户端有**多个未完成的异步操作**，但强制保证 **FIFO Client Order**。| 实现了强一致性下的**异步操作并行**。|
| **FIFO Client Order** | **单个客户端**发出的所有请求（读/写）将按**发送顺序**执行。| 允许客户端进行**高效的异步管道化 (Pipelining)** 操作。|
| **读操作优化** | **仅更新请求（Writes）是 A-线性化**。读请求（Reads）可由**本地副本处理**。| 实现读性能的**线性扩展 (Scale linearly)**，支持读密集型负载。|

---

### 2. 保证的交互应用：原子配置更新 (Atomic Configuration Update Scenario)

| 协调挑战 | 解决方案（“Ready ZNode”机制） | 依赖的保证 |
| :--- | :--- | :--- |
| **防止使用部分配置** | 新 Leader：`Delete /ready` $\rightarrow$ **批量更新配置** $\rightarrow$ `Create /ready`。| **FIFO Client Order**：确保 $\rightarrow$ 严格按顺序执行。|
| **故障时不使用无效配置** | **线性化写**：若进程看到 `Create /ready`，则**必然**看到了之前的所有配置更新。若 Leader 在 `Create /ready` 前失败，进程看不到 `ready`，即知配置未完成。| **Linearizable Writes** |
| **防止并发读取旧配置** | **Watch 通知顺序**：客户端监视 `ready` 节点。Watch 通知事件**保证在**客户端看到新的状态之前被发送。| **通知有序性**：客户端在收到变更通知前不会读取新配置。|
| **性能提升** | Leader 将 5000 个更新请求**异步管道化**提交，将 10 秒操作缩短至 < 1 秒。| **FIFO Client Order**（允许异步 Pipelining）|

---

### 3. 跨通道同步与 `sync` 原语 (Cross-Channel Synchronization and `sync`)

| 潜在问题 | 核心机制 | 依赖的保证 |
| :--- | :--- | :--- |
| **跨通道数据不一致** | 客户端 A 通过 ZK 更新配置，并通过**非 ZK 通道**通知客户端 B 读取。若 B 连接的 ZK 副本落后，B 可能读到旧配置。| ZK 快速读导致**不保证读操作的先例顺序**（Precedence Order）。|
| **强制最新读取** | 客户端 B 在读取配置前，先调用 **`sync(path)`**，然后紧跟 `read`。| **FIFO Client Order** + **`sync`** |
| **`sync` 实现细节** | `sync` 是**异步**执行，并在 Leader 处被排序。它强制 Follower 在处理该 `read` 前，应用所有**已提交的**待处理写请求。| 不需原子广播，只需 Leader 将 `sync` 放在队列末尾。|

---

### 4. 活性与持久性 (Liveness and Durability)

| 保证类型 | 核心内容 | 依赖条件 |
| :--- | :--- | :--- |
| **Liveness (活性/可用性)** | 服务将保持**可用 (Available)**。| **多数 (Majority)** 的 ZooKeeper 服务器处于活跃通信状态。|
| **Durability (持久性)** | 成功响应的变更请求**将持久化 (Persists)**。| 只要**法定数量 (Quorum)** 的服务器最终能够恢复，变更就不会丢失。|

## 原语应用示例

### 核心理念：ZooKeeper 作为内核 (Coordination Kernel)

*   **实现者：** 所有高级原语（Locks, Barriers, etc.）**完全在客户端实现**，ZooKeeper 服务本身对此一无所知。
*   **基础：** 依赖 ZooKeeper 的**有序性保证**（高效推理系统状态）和 **Watches**（高效等待事件）。

### 1. 配置管理 (Configuration Management)

| 目的 | 机制 | ZK 特性 |
| :--- | :--- | :--- |
| **动态更新** | 配置存储在 ZNode $z_c$ 中。| **ZNode Data** |
| **通知机制** | 进程启动时 `read` $z_c$ 并设置 **`watch=true`**。| **Watches** |
| **更新流程** | $z_c$ 更新 $\rightarrow$ 客户端被通知 $\rightarrow$ 客户端**再次读取**新配置并**重新设置 Watch**。| **Watches** (一次性触发) |

### 2. 组成员管理 (Group Membership)

| 目的 | 机制 | ZK 特性 |
| :--- | :--- | :--- |
| **群组表示** | 专用 ZNode $z_g$ 代表群组。| **ZNode Path** |
| **成员注册/存活** | 每个成员在 $z_g$ 下**创建 Ephemeral Child ZNode**（可带 `SEQUENTIAL` 保证唯一命名）。| **Ephemeral ZNode** |
| **故障检测/清理**| 成员进程失败 $\rightarrow$ Ephemeral ZNode **自动删除**。| **Session-Bound Lifetime** |
| **监控群组** | 进程**监视** $z_g$ 的子节点变化，收到通知后刷新子节点列表。| **Watches on Children** |

### 3. 分布式锁 (Simple Locks without Herd Effect) - 推荐的实现

| 目的 | 机制/流程 | ZK 特性 |
| :--- | :--- | :--- |
| **请求排队** | 客户端 `create` **EPHEMERAL | SEQUENTIAL** ZNode $n$ 在锁父节点 $l$ 下。| **Ephemeral + Sequential** |
| **获取锁** | 检查 $n$ 是否是 $l$ 下的**最小顺序号**子节点。| **Sequential Ordering** |
| **高效等待** | 非最小节点**只监视**排在自己**前面紧邻**的那个节点 $p$ 的删除事件。| **Watches** |
| **避免羊群效应** | 节点 $p$ 删除时**只唤醒** $n$ 对应的**一个**客户端。| **Watches (One-to-One)** |
| **容错释放** | 持有锁客户端崩溃 $\rightarrow$ Ephemeral ZNode $n$ **自动删除**。| **Ephemeral ZNode** |
| **释放锁** | 客户端显式 `delete(n)`。| **Delete API** |

### 4. 读/写锁 (Read/Write Locks)

| 目的 | 机制 | 区别点 |
| :--- | :--- | :--- |
| **写锁** | 创建 **`/write-` + SEQUENTIAL | EPHEMERAL** 节点 $n$，只有 $n$ 为最小节点时获得锁。| **与 Simple Lock 相同**（只更改命名）。|
| **读锁** | 创建 **`/read-` + SEQUENTIAL | EPHEMERAL** 节点 $n$。| **等待条件不同：** 进程只需等待**所有顺序号比自己小的 `/write-` 节点**被删除即可获得锁。|
| **羊群效应** | 当写锁节点被删除时，所有等待读锁的客户端被唤醒是**期望行为**（因为读锁是共享的）。| **Watches (One-to-Many)** |

### 5. 双重屏障 (Double Barrier)

| 目的 | 阶段 | 机制 | ZK 特性 |
| :--- | :--- | :--- | :--- |
| **整体同步**| 屏障 ZNode $b$。| $b$ 的子节点代表在屏障内的成员。| **ZNode Path + Children** |
| **进入** | 成员在 $b$ 下**创建子节点**（注册）。| 检查子节点数量是否**超过阈值**。| **Children List** |
| **进入等待** | 进程监视**“Ready”子节点**的存在。| **Watches on Exists** |
| **退出** | 成员**删除**自己的子节点（注销）。| 检查子节点数量是否**为零**（所有完成）。| **Delete API** |
| **退出等待** | 进程监视**特定子节点**的消失。| **Watches on Delete** |

# zookeeper implementation

### 总体架构与组件

ZooKeeper 通过在组成服务的每台服务器上复制数据来实现高可用性。

#### 1. 故障模型
- 假设服务器以**崩溃**（crashing）方式失效，且这些故障的服务器随后可能恢复。

#### 2. 高级组件（High-Level Components）
- **请求处理器 (Request Processor)：** 接收到请求后，对其进行预处理以准备执行。这一步会计算出应用该请求后的服务器状态是什么，并将请求转化为幂等的事务。
- **协议组件 (Agreement Protocol)：**
    - 针对**写请求**（需要服务器间协调），使用**原子广播**协议（Zab 的实现）进行协调。
    - **读请求**则不需要该协议。
- **ZooKeeper 数据库 (ZooKeeper Database)：** 在所有服务器副本上**完全复制**。

#### 3. 请求处理流程
- **写请求：** `服务器接收` -> `请求处理器预处理` -> `原子广播协议协调` -> `提交更改到 ZooKeeper 数据库`。
- **读请求：** `服务器接收` -> `简单读取本地数据库状态` -> `生成响应`。

### 复制数据库结构与持久化

#### 1. 数据库结构
- **存储介质：** 一个**内存数据库**，包含整个数据树。
- **Znode 限制：** 树中的每个 znode 默认存储**最大 1MB** 的数据（该值可配置）。

#### 2. 可恢复性与持久化（WAL 与快照）
- **日志记录：** 为了可恢复性，更新操作会**高效地记录到磁盘**。
- **强制写入：** 在将更改应用到内存数据库之前，必须**强制将写入操作提交到磁盘介质**。
- **写入预写日志 (WAL)：** 维护一个已提交操作的重放日志（即**预写日志，Write-Ahead Log**），用于恢复。
- **周期性快照：** 定期生成内存数据库的快照。

### 原子广播协议 (Zab) 与一致性保证

所有更新 ZooKeeper 状态的请求都通过 **Zab** 协议进行协调。

#### 1. Leader-Follower 机制
- **写请求转发：** 所有更新状态的请求都转发给**唯一的服务器**，称为 **Leader**。
- **Leader 职责：** Leader 执行请求，并通过 Zab 协议向其他服务器（**Followers**）广播状态更改。
- **客户端响应：** 接收客户端请求的服务器，在**交付**（deliver）相应的状态更改后，向客户端响应。

#### 2. Quorum 机制与容错
- Zab 默认使用**简单多数仲裁**（simple majority quorums）来决定提案。
- **容错能力：** 对于 $2f + 1$ 台服务器，可以容忍 $f$ 台服务器的故障。

#### 3. 性能与处理管线
- **高吞吐量：** ZooKeeper 试图保持请求处理管线（pipeline）充满，可能同时有数千个请求处于处理管线的不同部分。

#### 4. Zab 的强化有序性保证
由于状态更改依赖于先前状态更改的应用，Zab 提供了比常规原子广播更强的有序保证：
1. **Leader 内部顺序：** Leader 广播的更改，将以发送时的顺序交付。
2. **跨 Leader 顺序：** 在一个 Leader 广播其自身的更改之前，来自**先前 Leader** 的所有更改必须交付给该已确立的 Leader。

#### 5. 简化实现与性能优化
- **传输层：** 使用 **TCP** 作为传输，利用网络维护消息顺序，简化了实现。
- **Leader 统一：** Zab 选出的 Leader 即为 ZooKeeper Leader，同一进程负责创建事务并提议事务。
- **日志复用：** 用于跟踪提案的日志同时作为内存数据库的**预写日志**，避免了消息两次写入磁盘。

#### 6. 幂等性与消息重传
- **正常操作：** Zab 正常情况下按序且恰好交付一次消息。
- **恢复重传：** 由于 Zab 不永久记录每个已交付消息的 ID，恢复期间可能会**重传**消息。
- **幂等事务：** ZooKeeper 使用**幂等事务**，只要按顺序交付，多次交付是可接受的。
- **重传要求：** ZooKeeper 要求 Zab 至少重传**从上次快照开始以来**所有已交付的消息。

### 模糊快照 (Fuzzy Snapshots) 与恢复机制

#### 1. 快照必要性
- 恢复：从崩溃中恢复时，如果重放所有已交付消息，耗时将非常长。
- 解决方案：使用**周期性快照**，只需重传**从快照开始以来**的消息。

#### 2. 模糊快照的特点
- **非锁定：** 快照被称为**模糊快照（fuzzy snapshots）**，因为它**不会锁定** ZooKeeper 状态来进行快照。
- **过程：** 以**深度优先扫描**方式，原子性地读取每个 znode 的数据和元数据，并写入磁盘。
- **结果状态：** 最终的模糊快照可能**不对应**于 ZooKeeper 在任何时间点的有效状态，因为它可能应用了在快照生成期间交付的部分状态更改。

#### 3. 基于幂等性的恢复示例
由于状态更改是幂等的，它们可以被应用两次，只要按顺序应用即可。

**示例：**
1. **初始状态：** `/foo` 的值为 `f1`，版本为 1；`/goo` 的值为 `g1`，版本为 1。
2. **状态更改流（Stream of State Changes）：**
    - `<SetDataTXN, /foo, f2, 2>`
    - `<SetDataTXN, /goo, g2, 2>`
    - `<SetDataTXN, /foo, f3, 3>`
3. **最终有效状态：** `/foo` 的值为 `f3`，版本为 3；`/goo` 的值为 `g2`，版本为 2。
4. **模糊快照记录状态（可能无效）：** 快照可能记录 `/foo` 的值为 `f3`，版本为 3；`/goo` 的值为 `g1`，版本为 1（这是一个**无效状态**）。
5. **恢复过程：** 如果服务器崩溃并使用此快照恢复，然后 Zab **按序重传**上述三条状态更改，则最终状态将与崩溃前的服务状态一致。

### 客户端-服务器交互与一致性保障

#### 1. 客户端连接与请求顺序
- **连接：** 客户端仅连接到**一台**服务器。
- **请求处理顺序：** ZooKeeper 服务器以 **FIFO 顺序**处理来自客户端的请求。

#### 2. 写请求处理与 Watch
- **处理顺序：** 服务器按序处理写请求，且**不并发**处理其他写或读请求。
- **Watch 通知：** 在处理写请求时，服务器会发送并清除对应于该更新的任何 Watch 通知。
- **通知保证：** 这确保了**严格的通知连续性**（strict succession of notifications）。通知是**本地**处理的，只有客户端连接的服务器才跟踪和触发该客户端的通知。

#### 3. 读请求处理（Fast Reads）
- **本地处理：** 读请求在每个服务器上**本地处理**。
- **高性能：** 实现了出色的读取性能（仅为本地服务器上的内存操作，**无磁盘活动或协议运行**）。这是实现以读取为主的工作负载（read-dominant workloads）高性能的关键。
- **zxid 标记：** 每个读请求都使用一个 **zxid** 进行标记，该 zxid 对应于服务器**见到的最新事务**，定义了读请求相对于写请求的**偏序关系**（partial order）。

#### 4. 读一致性问题与 `sync` 原语
- **快速读取的弊端：** **不保证先行顺序**（precedence order），即读操作可能返回**陈旧值**（stale value），即使对同一 znode 的最新更新已提交。
- **`sync` 机制：** 为需要先行顺序的应用提供了 `sync` 原语。
    - **使用方式：** 客户端调用 `sync` 后跟 `read` 操作。
    - **保证：** 保证给定的读操作返回**最新的更新值**。
    - **实现：** `sync` 异步执行，并被 Leader 安排在所有待处理的写操作**之后**到达该服务器的本地副本。
    - **Leader 检查与空事务：** 为了使 `sync` 工作，Follower 必须确保 Leader 仍然是 Leader。
        - **有待处理事务：** 服务器不怀疑 Leader。
        - **待处理队列为空：** Leader 需要发送一个**空事务**（null transaction）来提交，并将 `sync` 安排在该事务之后。
        - **当前实现优化：** 超时设置使得 Leader 在 Follower 放弃它之前意识到自己不再是 Leader，因此**不会发出空事务**（在 Leader 有负载时可避免额外的广播流量）。

#### 5. Session 管理与 Durability 保证
- **响应信息：** 响应（包括无活动时的心跳消息）包含响应相关的 **zxid**。
- **客户端连接新服务器：**
    - 新服务器通过检查客户端的 `last zxid` 与自身的 `last zxid`，确保其对 ZooKeeper 数据的视图**至少与客户端的视图一样新**。
    - 如果客户端的视图比服务器**更新**，服务器将**不会重新建立会话**，直到它**追上**（caught up）为止。
- **耐久性 (Durability) 保证：** 客户端只看到已复制到**多数** ZooKeeper 服务器的更改，因此客户端一定能找到一个具有最新系统视图的服务器。

#### 6. 客户端会话故障检测
- **超时机制：** ZooKeeper 使用超时机制来检测客户端会话故障。
- **故障确定：** 如果在会话超时时间内，**没有其他服务器**从客户端会话接收到任何信息，则 Leader 确定发生故障。
- **客户端心跳逻辑（Session Timeout 为 $s$ 毫秒）：**
    - 闲置超过 **$s/3$ 毫秒**后，客户端发送心跳消息。
    - 如果超过 **$2s/3$ 毫秒**未收到服务器响应，客户端切换到新的 ZooKeeper 服务器重新建立会话。

## Reference

[[2-source-material/papers/zookeeper.pdf|zookeeper]]