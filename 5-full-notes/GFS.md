Time:2025-10-26

Status: 

- [ ] **working** 👨‍💻
- [x] *done*    💻

Tags:[[3-tags/distributed|distributed]]

## Introduction

谷歌面对TB,FB级的数据,开发了GFS文件系统,它可以运行在商业级硬件之上,将硬件故障视为常态。

GFS相对于传统文件系统，提出了以下几个不同的观点：

1. 商用级硬件发生故障被视为常态而不是意外。为此，GFS应该具备监控，错误检测，容错，自动恢复能力
2. 有很多GB级和KB级的文件需要处理，前者不利于IO，后者不利于管理。需要重新设计文件存储
3. 许多文件的修改是追加式的，而不是随机写。
4. 同时设计应用和文件系统API对整体系统的灵活性有利

## Design Overview

### 假设

1. 系统建立在商业级硬件之上，经常发生错误
2. 系统存储的大文件数量不多，多数为100MB，GB级别
3. 两种读：大规模流式读取和小规模随机读取
4. 两种写：大型追加式顺序写，支持随机写，但是不做优化
5. 需要高效支持良定的并行追加语义
6. 高带宽比低延迟更重要

### Interface

常用api：

```
create,delete,open,close,read,write
```

此外，GFS还支持额外两个API：

`snapshot，record append`

### Architecture

GFS采用三级架构：master节点，负责配置信息流；chunkservers，负责存储文件；client，负责和chunkservers交互执行文件操作。

![[2-source-material/images/Pasted image 20251026143147.png]]

文件切分为固定大小的chunk，通常为64MB，每个chunk有一个全局唯一的64位chunk handle，这个handle由master授予并管理。每个chunk在chunkserver作为linux文件存储，通常有三个备份。

master节点管理所有的文件系统元数据。包括命名空间，访问权，文件到chunk的映射，以及每个chunk当前的位置。此外，还包括如租约管理，垃圾回收，孤儿chunk等。master定期通过心跳来管理chunkserver。

client从master处获得元信息，从chunkserver处处理数据。

**客户端不缓存文件数据**，但会缓存 Chunk 位置等元数据。chunkserver靠linux的缓存机制来缓存数据信息。

### 单master

设计简单
master便于管理chunkserver
需要最小化通过master的IO
  client不向master请求数据，只向master请求指定文件的chunk位于的chunkserver的位置
  client缓存此信息
  client访问数据的流程：
1. 客户端将文件路径和字节偏移量转换为 Chunk 索引。
2. 客户端向 Master 发送文件路径和 Chunk 索引。
3. Master 返回对应的 Chunk 句柄和副本位置。
4. 客户端以文件路径和 Chunk 索引为键缓存此信息。
5. 客户端选择一个副本，通常是最接近的。
6. 客户端向该副本发送请求。
7. 请求中包含 Chunk 句柄和字节范围。
8. 同—Chunk 的后续读取无需再与 Master 交互。
9. 缓存信息过期或文件重开时才需再次交互。
10. 客户端通常会请求多个相邻 Chunk 的信息。
11. Master 会附带紧随其后的 Chunk 信息。
12. 额外信息减少了未来的客户端-Master 交互。

### Chunk Size

chunk size选定为64MB，存储为linux file，只有在需要时文件大小才会被扩展。
更大的chunk size有以下几个优势：

1. 减少了client与master交互的次数
2. client更有可能在同一个chunk上完成各种操作，通过一个持续稳定的TCP连接来减少了网络开销
3. 减少了存储在master的元数据大小，使得元数据可以存储在master的内存中

缺点：
小文件由少量 Chunk 组成。存储这些 Chunk 的 ChunkServer 可能成为热点。如果很多客户端访问同一文件会发生热点。

**空间浪费问题**：即使采用了延迟空间分配，如果大量小文件都只占用一个 64MB Chunk 的极小部分，也会导致 ChunkServer 磁盘空间在物理上被大量闲置（尽管在逻辑上 Chunk 的大小是动态的，但 Master 的元数据管理单元是 64MB 的 Chunk）。
    
实际中热点不是主要问题。因为应用多是顺序读取大型多 Chunk 文件。
    
批量队列系统初次使用时确实产生了热点。一个可执行文件被写为单 Chunk 文件。该文件被数百台机器同时启动。少数 ChunkServer 被数百个请求压垮。我们通过提高可执行文件的复制因子解决。批处理系统也错开了应用启动时间。潜在长期方案是允许客户端相互读取数据。

### Metadata

master存储三种元数据：file和chunk名字空间，文件到chunk的映射，每个chunk replica的位置。元数据都存储在master的内存中。前两者也通过operation log持久化到磁盘上。后者不需要，因为可以向chunkserver通信获得。

#### In-Memory Data Structure

1. 操作迅速
2. 利于周期性扫描，方便实现gc，re-replication，chunk migration

问题：内存空间不够用咋办？-> 论文中指出每个chunk只需要不到64kb的空间for metadata。
但是随着发展，现在这已经成为了问题。目前，GFS已被更成熟的系统替代。

#### Chunk Locations

Master 节点并不会持久化记录哪个 ChunkServer 拥有某个 Chunk 的副本。它只是在系统启动时通过轮询的方式，向所有 ChunkServer 询问这份信息。此后，Master 就能保持信息的最新状态，因为所有 Chunk 的放置操作都由它控制，并且它会通过定期的心跳（HeartBeat）消息来持续监控 ChunkServer 的状态。

#### Operation Log

操作日志记录了关键元数据的历史变更。它是GFS 的唯一持久化元数据记录。它充当了定义并发操作顺序的逻辑时间线。文件、Chunk 及其版本由创建时的逻辑时间唯一标识。

操作日志必须可靠存储。元数据变更只有在持久化后才能对客户端可见。否则整个文件系统或最新操作会丢失。因此，日志被复制到多台远程机器上。Master 仅在本地和远程都将记录刷新到磁盘后才响应客户端。Master 会批量处理多条日志记录后才进行刷新。批量处理减少了刷新和复制对系统整体吞吐量的影响。

Master通过重放操作日志来恢复文件系统状态。为最小化启动时间，日志必须保持较小。Master 在日志增长到一定大小时会创建检查点（Checkpoint）。 Master 可以通过加载最新的本地检查点并重放之后的少量日志来恢复。检查点是紧凑的 B-tree 格式。它可以直接映射到内存用于命名空间查找。这进一步加快了恢复速度并提高了可用性。

由于创建检查点需要时间，Master 的内部状态允许在不延迟传入修改的情况下创建新的检查点。Master 会切换到一个新的日志文件。它在一个独立线程中创建新的检查点。新检查点包含切换之前的所有修改。对于一个拥有数百万文件的集群，创建过程大约只需要一分钟。检查点完成后会被写入本地和远程磁盘。

恢复只需要最新的完整检查点和后续的日志文件。旧的检查点和日志文件可以删除，但会保留一些以防灾难。检查点过程中发生的失败不会影响正确性。因为恢复代码可以检测并跳过不完整的检查点。

### Consistency Model

GFS采用relaxed consistency model

#### GFS保证

文件命名空间的操作是原子的

file region的state取决于操作的类型和操作是否成功，GFS定义了以下几个一致性模型：

![[2-source-material/images/Pasted image 20251026151210.png]]

consistent：所有client不论从哪个replica读取数据，其读取到的数据都是一样的。
defined：一致，且客户端可以看到写入的内容。

并发写是consistent的但是不是defined的，因为GFS没有对不同chunk的写入顺序做出要求。

GFS保证append操作是原子的，即至少写入成功一次。

在一系列成功操作后，被修改文件保证是defined的。

client cache有过期时间，防止读到过期数据

数据丢失只有在全部丢失时才会发生，且会返回client清晰的错误信息，而不是返回错误数据

## 系统交互

### lease and mutation order

每个修改会发生在所有的replica上，使用租约来做这个mutation order的维护。master给所有的replica的chunk的其中一个一个lease，这个chunk被称为primary。它pick一个顺序，其他replication执行操作时，按照这个顺序来。

lease的租约通常为60s。但是，只要修改操作在进行，primary可以请求增加lease时间，通过心跳来实现。master会在执行某些操作时，收回lease。即使断开连接，master也可以在租约过期后分发新的lease。

![[2-source-material/images/Pasted image 20251026161644.png]]

上图解释了client发起写入请求的步骤：

1. client从master处获得持有lease的chunkserver，以及其他replicas的位置。如果没有，那么master分发一个lease。
2. master回复，client缓存信息。
3. client将数据推送到所有replicas。这个推送不一定是primary最先，一般通过IP地址来推送至最近的chunkserver。采用流水线的方式。chunkserver收到数据后先用LRU缓存，不应用。
4. 当所有replica都收到数据后，client向primary发送写请求。primary指定一个写入顺序，然后应用。
5. primary把写入请求转发给replicas
6. replicas回复primary
7. primary回复client，如果写入在replicas上发生错误，primary回复中包含此错误信息。

如果一个写太大，GFS client会切分。但是并发写可能会产生overwriten的问题。

### Data Flow

**数据流与控制流分离**

采用线性网络拓扑

每个机器将数据传送给最近的机器，使用ip地址

采用流水线

### Atomic Record Appends

在上述写入流程中多一个步骤：

当primary收到client的追加写入请求后：检查是否导致chunk超过64MB。

1. 超过：填充当前chunk，通知replicas do so。返回client在下一个chunk上写入。（通常限制一个追加的体积不超过chunk的1/4）
2. 没超过：应用

如果某一个replica的操作失败，client重试，导致第一次成功的那些chunk重复。GFS不保证byte级别的一致性。

### Snapshot

snapshot对文件或者目录树做即刻的copy

使用标准 copy-on-write 技术。当master收到snapshot请求后：收回leases，写入操作日志，应用日志-复制一份元信息。

当snapshot创建后的第一次一个client想要修改一个chunk C。master注意到C的引用计数大于1，则先推迟返回client，通知所有拥有chunk C的chunkserver新建一个C'，master把lease给一个C’，然后返回client

## Master Operation

master的大多数操作耗时，希望这些操作不会推迟其他操作。因此允许多任务并行，使用锁来管理namespace。

### Namespace & Locking

GFA的文件系统没有目录可以列出所有文件，不支持别名。GFS将namespace表示为一个路径到元信息的查找表。namespace tree中的每个node都有自己的读写锁。

示例：

> Each master operation acquires a set of locks before it runs. Typically, if it involves /d1/d2/.../dn/leaf, it will acquire read-locks on the directory names / d1, / d1/d2, ..., /d1/d2/.../dn, and either a read lock or a write lock on the full pathname /d1/d2/.../dn/leaf. Note that leaf may be a file or directory depending on the operation.

此机制允许同一目录的并发操作。

读写锁为lazy allocated，一旦不使用就删除。

锁按照一致的顺序获得，避免死锁。

### Replica Placement

replica不仅需要分布在不同的机器上，而且这些机器需要位于不同的机架上。
有两个目的：

1. 最大化数据可靠性与可用性
2. 最大化网络带宽利用率

### Creation,Re-replication,Rebalancing

标题为chunk replicas创建的三个原因

*creates：*

choose where to place the initial empty replicas:

1. 放在低于平均磁盘利用率（意味着磁盘空间足）的chunkserver上
2. 最小化在每个chunkserver上的**最近创建数**，因为最近创建一个chunk意味着将来会有大量的写流量
3. 分散在不同机架上

*re-replicas:*

当可用replicas数量少于设定值时触发。

需要重复制的chunk的优先级有几个考虑因素：

1. 它离设置值差几个：设定为3，则1的优先级大于2
2. 先复制live files，后复制属于被删除file的chunk
3. 阻塞client的优先级高

新replica的位置选择和create相同。为了避免clone流量阻塞client请求流量，master限制集群和每个chunkserver的clone操作数。每个chunkserver限制花在clone上的带宽

*rebalance:*

检查当前分布，移动replicas来获得更均衡的分布。而且这个过程是逐步进行的，防止大量的流量冲垮一个新的chunkserver。

### Garbage Collection

当文件删除后，GFS不会立刻释放空间，而是在GC阶段释放，both the file and chunk levels

#### Mechanism

一个文件被删除后，master log这个操作。将文件命名为包含删除时间戳的隐藏文件名。当GC扫描时，移除删除时间大于三天的文件。并移除内存中的元信息。

master识别孤儿chunk（无法从任何一个file到达的chunk），并删除这些chunk的元数据。master通过询问每个chunkserver都包含哪些chunk来做到这一点。

#### 优缺点

1. 简单可靠
2. 将空间释放操作融合为master后台的定期任务，因此该操作是batch的
3. 只有master相对空闲时才会做此工作，master更能回复client的请求
4. 防止不可逆删除

劣势：
1. 空间不足时不利于用户微调
2. 重复创建和删除文件的应用不能立刻利用空间

解决方案：当一个被删除的文件再次被删除时，加快空间释放。允许用户指定某些chunk不进行复制，且删除是立刻进行的

### 过期数据检测

对每个chunk，master维护一个version number来区分最新数据和过期数据

当master授予lease时，增加该chunk的版本号，通知最新replicas。master和replicas都将版本号记录在持久状态中。

当一个宕机的chunkserver重启并报告chunk信息和版本号时，master发现过期数据，在GC阶段回收过期数据，在回收前，master忽略过期数据，也不会向client报告该chunk的位置。

作为安全性保证，mastet在返回clientchunk的位置信息时，也会携带版本号。

如果master看到比自己高的版本号，它假设这是由于当它授予lease时宕机了，接受更高的版本号作为最新版本号。

## 容错与监控

### 高可用

*fast recovery：*

任何错误导致的宕机都在几秒内重启

*chunk replication:*

每个chunk都在不同机架上的不同机器上复制多份。当chunkserver网络失联或者checksum检测失败时，master re-replica此chunk。

*Master Replication：*

master的状态也通过复制来实现可靠性。其操作日志在多台机器上复制。一个操作只有在所有远程机器和本地都写入磁盘后，才会被认为成功，并应用到状态机上。

client使用权威名来寻找master，这是一个DNS别名，当master转移到其他机器后会被修改。

**影子 Master 的作用**

影子 Master 提供了对文件系统的只读访问。即使主 Master 宕机，它仍能提供服务。它们是影子，而非镜像，因为它们可能稍微落后于主 Master。通常延迟只有几分之一秒。它们提高了非活跃修改文件或可接受轻微过期结果的应用的读取可用性。由于文件内容是从 ChunkServer 读取的，应用不会读取到过期的文件内容。在短时间内可能过期的是文件元数据，例如目录内容或访问控制信息。

**影子 Master 的同步机制**

为了保持信息同步，影子 Master 会读取不断增长的操作日志副本。它会应用与主 Master 完全相同的变更序列到其数据结构。与主 Master 一样，它在启动时轮询 ChunkServer 以获取 Chunk 副本位置。之后它会不频繁地进行此操作，并通过频繁的心跳消息监控 ChunkServer 状态。它仅依赖于主 Master来获取副本位置更新。这些更新是主 Master 决定创建和删除副本的结果。
### 数据完整性

chunkserver通过checksum来保持数据完整性。

每个chunk被划分为64KB的blocks。每个block有一个关联的32位checksum。checksum保存在内存中，也通过log进行持久化。

*对于读*，chunkserver验证读范围内数据的checksum。如果不匹配，则返回请求者错误，请求者向其他chunkserver请求，同时通知master自己数据损坏，master复制其他replica的信息，当复制完成后，master指示有着损坏数据的chunkserver删除他的replica

checksum不影响读性能，一方面因为读通常跨越多个block，checksum占比小。另一方面，client会尽可能将读操作按照block对齐。另外checksum查找和比较都是在chunkserver本地完成的，不需要走IO

*对于append写*，checksum计算被高度优化。

GFS只关注两个区域：
1. 最后一部分校验和块，可能被append覆盖，需要重新计算其checksum。
2. 由于append而产生的全新的block

GFS不会验证最后一部分校验和是否合法，因为如果非法，则计算出的新校验和也是非法的，在读的时候一样会被发现。

*对于随机写*，可能覆写chunk中已经存在的内容。

首先需要验证范围内第一个和最后一个block的checksum，否则新的校验和可能掩盖原有的错误。之所以是第一个和最后一个，是因为只有这两个block中会包含旧数据+新数据，如果不验证且旧数据部分正好出错，那么无法通过新的校验和检测出来。

在chunkserver空闲时，会扫描并验证不活跃chunk的校验和，这可以检测到不常被读取的chunk的错误，并通知master更新。这可以防止一个不活跃但是错误的chunk replica欺骗master使其认为它对一个chunk具有足够的有效复制。


## Reference

[[2-source-material/papers/gfs.pdf|gfs]]