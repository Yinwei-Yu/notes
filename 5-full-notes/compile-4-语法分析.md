Time:2025-10-17

Status: 

- [ ] **working** 👨‍💻
- [x] *done*    💻

Tags:[[3-tags/compile|compile]]

由词法分析的输出生成语法树

任务：
单词如何组成声明和语句
声明和语句如何组成程序
报告不符合语法规则的部分

分析方法：
  自上而下：
  开始符号->最左推导
  树的根节点->构造语法树
  从程序除法->构造源程序
  ![[2-source-material/images/Pasted image 20251017160019.png]]
  自下而上： 从最后的符号串开始规约到初始符号

eg.

![[2-source-material/images/Pasted image 20251017161145.png]]

如果存在:U->a1|a2|a3...
当匹配错误时,需要回溯到出错点->效率低
  ->当文法中出现左递归时，会使分析过程陷入无限循环。

so:消除左递归,避免回溯

## 消除左递归

直接左递归:

采用EBNF
引入新的非终结符,讲左递归改写为右递归
![[2-source-material/images/Pasted image 20251017164202.png]]

---

间接左递归:
代入->改写为直接左递归->消除

## 消除回溯

右侧的各符号串的终结首符号集合两两不相交
后随终结符号集,若本身在最后,则终结符为$.当α->ε时,FISRT集和FOLLOW集不相交

![[2-source-material/images/Pasted image 20251017171430.png]]

---

求FIRST集:

求FOLLOW集

## 递归子程序

对真实推导过程的直接模拟
对每个非终结符号调用一个对应的分析程序
文法产生式->流程图

要求文法:无左递归

简单,过分依赖文法产生式

## 确定的LL(1)分析器


# AI Summarize

## 语法分析概述

### 基本任务
语法分析是编译过程的第二个阶段，接收词法分析器输出的单词序列（token流），构建语法结构。

**核心任务：**
1. **结构识别：** 识别单词如何组成声明、语句等语法单元
2. **程序构建：** 识别声明和语句如何组成完整的程序
3. **错误处理：** 报告不符合语法规则的部分，提供有意义的错误信息

### 分析方法分类

#### 自上而下分析 (Top-Down Parsing)
**工作原理：**
- 从文法的开始符号出发
- 执行最左推导（Leftmost Derivation）
- 从语法树的根节点开始构造
- 模拟从程序出发构造源程序的过程

**特点：**
- 直观，易于理解
- 适合手工实现
- 可能遇到左递归和回溯问题

![[2-source-material/images/Pasted image 20251017160019.png]]

#### 自下而上分析 (Bottom-Up Parsing)
**工作原理：**
- 从输入的单词序列开始
- 逐步规约（Reduce）到文法的开始符号
- 从语法树的叶子节点向根节点构造

**示例推导过程：**
![[2-source-material/images/Pasted image 20251017161145.png]]

## 自上而下分析的问题与解决方案

### 回溯问题 (Backtracking)

**问题描述：**
当文法中存在产生式 $U \rightarrow \alpha_1 | \alpha_2 | \alpha_3 | \dots$ 时，如果选择错误的产生式进行推导，需要回溯到出错点重新选择，导致分析效率低下。

**示例：**
```
E → T + E | T
T → int | int * T | (E)
```
在分析 `int * int` 时，如果错误选择 `T → int`，需要回溯选择 `T → int * T`

### 左递归问题 (Left Recursion)

**问题描述：**
当文法中出现直接或间接左递归时，自上而下分析会陷入无限循环。

**直接左递归形式：**
$A \rightarrow A\alpha | \beta$

**间接左递归形式：**
$A \rightarrow B\alpha$
$B \rightarrow A\beta$

## 文法改造技术

### 消除直接左递归

**EBNF (Extended Backus-Naur Form) 方法：**
引入新的非终结符，将左递归改写为右递归

**转换规则：**
原产生式：$A \rightarrow A\alpha | \beta$
转换后：
$A \rightarrow \beta A'$
$A' \rightarrow \alpha A' | \varepsilon$

![[2-source-material/images/Pasted image 20251017164202.png]]

**具体示例：**
原左递归文法：
```
E → E + T | T
T → T * F | F  
F → (E) | id
```

消除左递归后：
```
E → T E'
E' → + T E' | ε
T → F T'
T' → * F T' | ε
F → (E) | id
```

### 消除间接左递归

**处理步骤：**
1. **代入转换：** 将间接左递归转换为直接左递归
2. **消除左递归：** 应用直接左递归消除方法

**示例：**
原文法：
```
S → A a | b
A → A c | S d | ε
```

代入 S 到 A 的产生式：
```
A → A c | (A a | b) d | ε
  → A c | A a d | b d | ε
```

消除直接左递归：
```
A → b d A' | A'
A' → c A' | a d A' | ε
```

### 消除回溯

**必要条件：**
对于文法中的每个非终结符 A，其所有产生式 $A \rightarrow \alpha_1 | \alpha_2 | \dots | \alpha_n$ 满足：
1. $FIRST(\alpha_i) \cap FIRST(\alpha_j) = \emptyset$（$i \neq j$）
2. 如果 $\alpha_i \rightarrow^* \varepsilon$，则 $FIRST(\alpha_j) \cap FOLLOW(A) = \emptyset$（$j \neq i$）

![[2-source-material/images/Pasted image 20251017171430.png]]

## 集合计算

### FIRST 集计算

**定义：** $FIRST(\alpha)$ 是从 $\alpha$ 可以推导出的所有串的第一个终结符的集合。

**计算规则：**
1. 如果 X 是终结符，则 $FIRST(X) = \{X\}$
2. 如果 X 是非终结符：
   - 对于每个产生式 $X \rightarrow Y_1Y_2\dots Y_k$
   - 将 $FIRST(Y_1)$ 加入 $FIRST(X)$
   - 如果 $Y_1 \rightarrow^* \varepsilon$，继续加入 $FIRST(Y_2)$，依此类推
   - 如果所有 $Y_i \rightarrow^* \varepsilon$，将 $\varepsilon$ 加入 $FIRST(X)$
3. 如果 $X \rightarrow \varepsilon$，将 $\varepsilon$ 加入 $FIRST(X)$

**示例计算：**
```
E → T E'
E' → + T E' | ε
T → F T'  
T' → * F T' | ε
F → (E) | id
```

计算结果：
- $FIRST(F) = \{(, id\}$
- $FIRST(T') = \{*, \varepsilon\}$
- $FIRST(T) = \{(, id\}$
- $FIRST(E') = \{+, \varepsilon\}$
- $FIRST(E) = \{(, id\}$

### FOLLOW 集计算

**定义：** $FOLLOW(A)$ 是可能在某些句型中紧跟在 A 后面的终结符的集合。

**计算规则：**
1. 将 $ 加入 $FOLLOW(S)$，其中 S 是开始符号
2. 如果存在产生式 $A \rightarrow \alpha B \beta$：
   - 将 $FIRST(\beta) - \{\varepsilon\}$ 加入 $FOLLOW(B)$
   - 如果 $\varepsilon \in FIRST(\beta)$，将 $FOLLOW(A)$ 加入 $FOLLOW(B)$
3. 如果存在产生式 $A \rightarrow \alpha B$，将 $FOLLOW(A)$ 加入 $FOLLOW(B)$

**示例计算（续前例）：**
- $FOLLOW(E) = \{\$, )\}$
- $FOLLOW(E') = \{\$, )\}$
- $FOLLOW(T) = \{+, \$, )\}$
- $FOLLOW(T') = \{+, \$, )\}$
- $FOLLOW(F) = \{*, +, \$, )\}$

## 递归下降分析

### 递归子程序法 (Recursive Descent)

**基本思想：**
为每个非终结符编写一个对应的分析子程序，直接模拟推导过程。

**实现要求：**
- 文法必须无左递归
- 需要计算 FIRST 和 FOLLOW 集来指导产生式选择

**文法产生式到流程图的转换示例：**
对于产生式：$A \rightarrow \alpha_1 | \alpha_2 | \dots | \alpha_n$

对应的分析程序结构：
```pseudocode
procedure A;
begin
    if lookahead in FIRST(α₁) then
        分析α₁
    else if lookahead in FIRST(α₂) then
        分析α₂
    ...
    else if lookahead in FOLLOW(A) then
        // 选择ε产生式
    else
        error
end;
```

**优缺点：**
- **优点：** 简单直观，易于实现和调试
- **缺点：** 过分依赖文法产生式，文法变化时代价大，可能产生深度递归

## LL(1) 分析器

### 确定的自上而下分析

**LL(1) 含义：**
- **L:** 从左向右扫描输入
- **L:** 产生最左推导
- **(1):** 向前查看 1 个符号

**预测分析表构造：**
对于每个产生式 $A \rightarrow \alpha$：
1. 对于每个 $a \in FIRST(\alpha)$，将 $A \rightarrow \alpha$ 加入 $M[A,a]$
2. 如果 $\varepsilon \in FIRST(\alpha)$，对于每个 $b \in FOLLOW(A)$，将 $A \rightarrow \alpha$ 加入 $M[A,b]$

**分析算法：**
```pseudocode
初始化栈和输入
将$和开始符号压栈

while 栈非空 do
    if 栈顶是终结符a then
        if 输入符号匹配a then
            弹出栈顶，前移输入指针
        else
            error
    else if 栈顶是非终结符A then
        if M[A,当前输入符号] = A→α then
            弹出A，将α逆序压栈
        else
            error
    else
        error
```

**LL(1) 文法条件：**
1. 文法无左递归
2. 对于每个非终结符 A 和它的任意两个不同产生式 $A \rightarrow \alpha$ 和 $A \rightarrow \beta$：
   - $FIRST(\alpha) \cap FIRST(\beta) = \emptyset$
   - 如果 $\beta \rightarrow^* \varepsilon$，则 $FIRST(\alpha) \cap FOLLOW(A) = \emptyset$

## 术语表

| 术语 | 英文 | 解释 |
|------|------|------|
| 语法分析 | Syntax Analysis | 编译过程的阶段，将单词序列转换为语法结构 |
| 自上而下分析 | Top-Down Parsing | 从开始符号出发，通过推导构建语法树的分析方法 |
| 自下而上分析 | Bottom-Up Parsing | 从输入串开始，通过规约到开始符号的分析方法 |
| 最左推导 | Leftmost Derivation | 每次替换最左边非终结符的推导过程 |
| 回溯 | Backtracking | 分析失败时退回之前状态重新尝试的过程 |
| 左递归 | Left Recursion | 非终结符的直接或间接产生式以自身开头 |
| EBNF | Extended BNF | 扩展的巴科斯范式，支持重复和可选操作符 |
| FIRST集 | FIRST Set | 符号串可能推导出的第一个终结符集合 |
| FOLLOW集 | FOLLOW Set | 可能紧跟在非终结符后的终结符集合 |
| 递归子程序 | Recursive Descent | 为每个非终结符编写递归函数的分析方法 |
| LL(1)分析 | LL(1) Parsing | 向前看一个符号的确定自上而下分析方法 |
| 预测分析表 | Predictive Parsing Table | LL(1)分析中指导产生式选择的二维表 |
| 规约 | Reduce | 自下而上分析中将句柄替换为相应非终结符的操作 |
| 句柄 | Handle | 与某个产生式右部匹配的子串，是可规约的串 |

# Reference
