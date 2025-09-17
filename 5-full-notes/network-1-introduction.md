Time:2025-09-09

Status: 

- [ ] **working** 👨‍💻
- [x] *done*    💻

Tags:[[network]]

## concept

 network
 internet
 host
## category(topology)

bus:fast but easy to broken
star
circle
tree

## 交换网络

电路交换
报文交换:存储转发
分组交换
1. 数据报
2. 虚电路

## 分组交换

时延
首部信息开销

## 网络实例

### internet层级结构

顶级ISP->地区->本地->...

### 构成

网络边缘:host
网络核心:交换机,路由器...
|->路由,转发
## 协议与分层结构

**protocol**

为了数据交换而设置的规则,标准,双方需要共同遵守

include：
1. 语法
2. 语义
3. 时序

why?
  分层结构
  统一标准
  模块独立

---

**layer**

___

**service**

about 连接

面向连接->电话模型
  建立连接
  交换数据
  切断连接

无连接->邮政系统
  携带完整目的地址
  传输无需应答

what is service?
  interface
  primitive->function you call

---

difference between service and protocol?

proto->horizontal
service->vertical

---

**数据单元**

接口数据单元(IDU interface data unit)
  IDU = PDU + ICI
^
|
协议数据单元(PDU)
  PDU = SDU + PCI(protocol control information)
^
|
服务数据单元(SDU)
  原始为了完成用户需求而需要传送的数据

SDU + PCI -> PDU + ICI -> IDU

下层信息=上层信息+包头

---

**data unit name on layer**

物理层:bit
链路层:frame 帧
网络层:packet 包
传输层:segment 报文段
应用层:报文
## reference model

**OSI** open system interconnection

![[2-source-material/images/Pasted image 20250911104226.png]]

*physical*

how to transfer bit on wire

*data link*

成帧:从物理层bits stream中提取完整的帧

*network*

路由(routing)
数据包跨越网络从源设备发送到目的设备
编址->寻径->传递

*transport*

数据从源端口发送到目的端口(process to process)

*session*

应用程序之间建立和维持会话

*presentation*

关注传递信息的语法和语义,管理数据的表示方法,传输的数据结构

*application*

应用层协议->网络服务调用

---

**TCP/IP**

![[2-source-material/images/Pasted image 20250911104906.png]]

*internet and transport*

most significant -> ip & tcp

## 度量单位

bit rate: bit per sec -> bps

bandwidth(带宽):单位时间内某信道能通过的*最高数据率*

PPS(包转发率):packet per second
  交换机或者路由器以包为单位的转发速率
  packet->64 bytes
  线速转发:转发时达到最高速率

Delay(时延):
  传输时延:$d_{trans}=\frac{length(bit)}{R(bit/s)}$,注意数据单位在主机和网络中的不同($2^{20}$->$10^2$)
  传播时延:$d_{prop}=\frac{distance(m)}{c(m/s)}$,某一个bit从一端到另一端的时间
  节点处理时延:$d_{proc}$,路由器收到包之后对包进行的验证等处理工作
  排队时延:$d_{queue}$,包的排队时间

往返时延(RTT Round-Trip Time):
  发送方发送数据开始到收到接收方的确认需要的总时间

时延带宽积:
  *时延带宽积=传播时延x带宽*->按*比特计数*的链路长度
  第一个发送的bit到达中终点时,发送方发送了时延带宽积个bit

吞吐量,有效吞吐量,利用率,丢包率

时延抖动

延迟丢包
## Reference
