> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/R66-y2colMgKD6ubRAvDPw)

![](https://mmbiz.qpic.cn/mmbiz_png/MqgA8Ylgeh6JV2fOEySyiappfbYgBWJcW2atRlSeZe1vmcfSj7Zq1SpFIfASl0EpckZCe81UZ2iawq3lArdSLqhg/640?wx_fmt=png&from=appmsg&wxfrom=5&wx_lazy=1&tp=webp#imgIndex=0)

![](https://mmbiz.qpic.cn/mmbiz_jpg/1JuKibm2ZBZU6IZGCdciawtWib5Vr9hJxtx6lG46pqIn2NrdH8KqicQNliaTUKh91Z3z6juY9MOsTtzNS6u95XVafibg/640?wx_fmt=other&wxfrom=5&wx_lazy=1&tp=webp#imgIndex=1)

**小分块不如大分块，动态 JSON 更适合复杂场景业务落地。**

**![](https://mmbiz.qpic.cn/mmbiz_jpg/1JuKibm2ZBZU6IZGCdciawtWib5Vr9hJxtxYjAzXhItHpzypIGiac9KmcqPr4fEJ2sTw5pDNlGcCFBZMTJh1VU0KEQ/640?wx_fmt=other&wxfrom=5&wx_lazy=1&tp=webp#imgIndex=2)**

沃尔沃汽车是全球知名汽车制造商，所有的战略决策都依赖于高效的数据洞察。

在此背景下，沃尔沃战略部门需要构建基于向量检索的 多模态 AI 文档检索系统，支撑 300-400MB 文档（约 70 万 - 100 万向量嵌入）稳定处理，适配部门级日均 10-20 次查询场景。

其对文档检索系统的要求如下：

体验侧，需足够精准、能够处理各种多模态数据、支持元数据动态管理、检索透明化监控能力，且支持自托管与托管服务迁移。

成本侧，需要初始投入可控（低于云厂商）、运营成本与使用量挂钩、规模化扩展时成本增长可预测。

开发维护侧，则需要提供完善文档与案例降低开发难度，支持定制化开发，且维护成本低、升级平滑。

针对以上需求，要怎么选型，技术落地有哪些坑？这是沃尔沃的选型与技术部署心得。

01 
---

如何选型
----

知识库检索系统的核心是向量数据库，沃尔沃选择先以单机模式部署在自托管虚拟机上。

但在分析 PDF、PowerPoint、Excel、Word 及嵌入图表 / 图像的再被的海量非结构化企业文档时，包括云厂商 AI 搜索服务在内的多数企业级工具，或准确性不足，或成本过高、定制化能力弱。

比如云服务厂商，采用 “固定托管费 + 按使用量计费” 的模式，仅 100MB 数据每月就要花费 250 美元，且大部分成本来自运行时间费用，而非实际查询费用。对于一个日均查询量仅 10-20 次的部门级系统而言，若将该方案推广至生产环境，从财务角度看是不可持续的。

紧随其后，沃尔沃花了一个月调研了市场上几乎所有主流向量数据库产品。但很快发现，这些产品要么是极客专属，要么文档过于简洁，但企业落地，在 API 接口和性能之外，更需要清晰的实操指南：怎么做文档预处理、如何选择 embedding 模型、如何部署可用于生产环境的流程。

最终有三款向量数据库进入候选名单：Milvus、Pinecone 和 ChromaDB。

ChromaDB 最早被排除，核心原因在于可扩展性有限。

紧随其后，排除的是 Pinecone。Milvus 和 Pinecone 在测试环节表现不相上下，但是落地实践之后，往往网络配置，embedding 模型搭配会极大影响实际表现，Milvus 的优势在于，提供了非常详细的落地指导，保证生产环境的高效稳定运行。

此外，对于 Milvus 的选型，沃尔沃也没选择比较新的 PyMilvus v2 SDK 及其内置的 embedding 集成功能，而是选择了 SDK v1 中基于 collection 的旧版本，从而保证团队能够设计详细的元数据结构，并明确定义每种文档的存储、索引和检索方式。

在企业文档本身杂乱且不统一的情况下，这种精细化的模式管理至关重要。

而性能上，该系统在峰值时足够处理约 300-400MB 的文档，对应约 70 万至 100 万个 embedding，与消费级 AI 工作负载相比，这个规模可能较小，但对于部门级工作负载而言恰到好处。

此外，针对格式繁多的非结构化数据，Milvus 支持的字段类型多达 64 种，这让沃尔沃不仅能存储嵌入向量，还能存储丰富的元数据 —— 从文档类型、来源到部门级分类等关键信息，覆盖全面。面对元数据无法适配预定义模式（schema）的情况，还能通过动态 JSON 字段解决这一问题，让团队灵活应对新文档类型与不断变化的需求，无需重构现有数据库。

02 
---

RAG 搭建过程中的经验与教训
---------------

知识库的本质是 RAG。

而对 RAG 来说，除了 LLM 提示词撰写技巧之外，影响其工作质量的核心有二：chunking 和 embedding。

其中，embedding 环节，一些特殊行业往往会选择在开源 embedding 模型基础上进行微调改造。

而 chunking 环节，沃尔沃面临的第一个问题就是怎么定分块大小。

市面上大多数 RAG 流程依赖小尺寸分块，比如许多云厂商的向量搜索服务通常默认 256 或 512 个 token。理由是，他们觉得较短的片段能带来更高的精度。

但事实是，分块太小，反而导致语义上下文丢失，逻辑断裂。

因此沃尔沃选择 1024 个 token 的大尺寸分块，保留一定的检索精度的同时，更注重检索结果的逻辑性、上下文完整性。从而为后续的 rerank 质量和大模型的判断环节，提供更高效的信息。

03
--

 改造成果与展望
--------

相比云厂商的 AI 搜索服务，基于自托管 Milvus 的部署方案不仅性能和表现更优，并且让沃尔沃的数据库支出减少了近 90%，省掉了不必要的固定的运行时间和存储费用。对于日均查询量适中的系统而言，可以带来 10 倍的成本效率提升。

除成本和性能外，沃尔沃汽车尤为看重 Milvus 的透明性。借助 Milvus，团队可以直接查看集合（collection）、查询存储的向量，以及数据库内部存储的数据。

这种透明性使得结果验证、准确性跟踪和检索质量的持续优化变得简单。

相比许多向量数据库将数据查看功能隐藏在复杂的定制工具之后，而 Milvus 通过其模型上下文协议（MCP）客户端和交互式 UI，提供了内置的可视化能力，使可观测性的成本极大降低。

未来，沃尔沃还将把业务从 Milvus 逐渐迁移到商业化的 Zilliz Cloud（Milvus 的商业化托管服务），并将这套系统推广至质量部门。数据类型上，也会从非结构化数据扩展到半结构化数据，将其与 PostgreSQL 和 Snowflake 中的数据集成，将文本文档与结构化指标（如财务记录、质量数据）相关联。

阅读推荐

[放弃 ES+Mongo，如何用 Milvus 一套系统搞定千万用户视频检索 * 关键词](https://mp.weixin.qq.com/s?__biz=MzUzMDI5OTA5NQ==&mid=2247510704&idx=1&sn=c5d89d724106a2fa079d0d11e7d9193b&scene=21#wechat_redirect)

[DeepSeek-OCR 解读：视觉如何成为长上下文压缩的新思路](https://mp.weixin.qq.com/s?__biz=MzUzMDI5OTA5NQ==&mid=2247510651&idx=1&sn=3270e92eddacf80916fe5fa6432167c4&scene=21#wechat_redirect)

[比 LangChain 强在哪？Parlant × Milvus 动态规则告别 agent 失控](https://mp.weixin.qq.com/s?__biz=MzUzMDI5OTA5NQ==&mid=2247510602&idx=1&sn=06f1b37b3339cb6dba414182d9619341&scene=21#wechat_redirect)

[多少做 RAG 的人，连分词都搞不定? Milvus Analyzer 指南](https://mp.weixin.qq.com/s?__biz=MzUzMDI5OTA5NQ==&mid=2247510534&idx=1&sn=be6f029a2fda69a85ccf96b30d38a8a8&scene=21#wechat_redirect)

[大模型贵，小模型蠢！vLLM+Milvus + 智能路由，无痛降本 50%](https://mp.weixin.qq.com/s?__biz=MzUzMDI5OTA5NQ==&mid=2247510510&idx=1&sn=f9cf589db0990265872cbebcbe7940bd&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_png/MqgA8Ylgeh5OzgygOxg4CIjUuFvGuMfcFUuOJwfp2fe1pg50tjrAWF5C9TzVKFt2D98sGjguIcPEI3TCcMPrDQ/640?wx_fmt=png&from=appmsg&wxfrom=5&wx_lazy=1&tp=webp#imgIndex=6)

![](https://mmbiz.qpic.cn/mmbiz_png/MqgA8Ylgeh4ek0GU1Snpd5xyiahZAUvz7DbjIGcGrDrbxqVsqlzTMhllbNJR9UIE3QF35qrwNmAkv9wW1gEcK6A/640?wx_fmt=png&from=appmsg&wxfrom=5&wx_lazy=1&tp=webp#imgIndex=6)