Time:2025-11-06

Tags:[distributed](3-tags/distributed.md)

# Introduction

fast 2PC

scalable
on disk
multi-version

transaction key-value store

serializable ACID

mechanism:trongly consistent snapshot reads on  
commodity hardware, using a novel lock-free read proto-  
col.

# Requirements

fast:

1. short OLTP
2. support long-running read-only queries
3. maintain high throughput for both low and high contention workloads

general:

1. unrestricted programming model and API
2. scalability and normal hardware with highest level semantics

# Notes

## 一、核心背景与问题
1. 分布式磁盘数据库困境：用2PC保证原子性则事务慢，不用则语义/扩展性受限；现代数据中心技术（fast RPC、低延迟存储）已降低2PC latency（Azure约150µs），新瓶颈转为“持有锁时从SSD读数据”的竞争。
2. 目标：实现“Fast+General”分布式磁盘事务——短OLTP事务延迟数百µs、高低竞争均高吞吐、支持严格串行化ACID，且无编程模型限制、不依赖专用硬件。

## 二、四大核心技术总结
### 1. 体系结构
- 四大组件协同：Epoch Service（Multi-Paxos维护全局递增epoch，提供序列化点）、KV Service（range分片+Paxos副本，含预取缓冲区，Leader管锁）、Transaction State Store（哈希分片存事务状态，解2PC阻塞）、Client Library（2PC协调+干运行预取）。
- 核心逻辑：事务先干运行预取数据，按序申请锁，并行执行Prepare与读epoch，验证Leader租约后提交，全程保证严格串行化与高可用。

### 2. 快照（Snapshots）
- 基础：多版本管理，VID=⟨epoch（前缀）+事务内计数器（后缀）⟩，删除以墓碑存储。
- 无锁强一致读取：读epoch确定快照点，等待写锁释放后读对应版本，不占锁；可选等待epoch更新保证线性化，垃圾回收按租约epoch区间清理旧版本。
- 价值：支撑长只读查询不干扰读写，为预取/死锁避免提供读写集基础。

### 3. 预取（Prefetching）
- 机制：Client Library通过“干运行”（快照读模拟事务）计算读写集，提前将冷数据加载到KV Service预取缓冲区并pin住，正式执行时直接从内存读。
- 优势：避免锁持有期间SSD IO，无需改用户代码，支持扫描查询；干运行开销可接受，低竞争场景可禁用。

### 4. 死锁避免（Deadlock Avoidance）
- 核心：干运行获读写集后，所有事务按“键升序”申请锁，消除循环等待；借RPC Chains优化锁申请RPC次数。
- 异常：读写集变化时fallback到Wound-Wait，实验中死锁abort率为0，优于传统超时/检测方案。


## 三、最值得借鉴的工作

这篇论文最值得借鉴的是“基于现代数据中心硬件特性（fast RPC、低延迟存储），重构分布式磁盘数据库的核心瓶颈解决思路”——不再局限于优化传统2PC，而是通过“无锁快照读+预取+有序锁”的协同设计，将“锁持有期间的磁盘IO”这一新瓶颈转移到锁申请前，在保证强语义（严格串行化）和通用性的同时，实现高低竞争场景下的高性能，为分布式磁盘数据库平衡“强一致性、高可用、高性能”提供了可落地的技术范式。

# AI summarize
# Reference
