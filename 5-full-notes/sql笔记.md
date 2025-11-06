Time:2025-11-03

Tags:[[3-tags/sql]] [[3-tags/database]]

# 概述

sql是访问和处理关系型数据库的计算机标准语言.

wiki:
SQL，Structured Query Language，结构化查询语言.是一种特定目的编程语言，用于管理关系数据库管理系统（RDBMS），或在关系流数据管理系统（RDSMS）中进行流处理。

why database?

方便存储与管理数据,程序员不需要关注数据存储的细节

---

数据模型

- 层次模型
- 网状模型
- 关系模型

![](2-source-material/images/Pasted%20image%2020251103093920.png)

关系模型胜出,简单理解且有数学理论支撑

---

数据类型

|名称|类型|说明|
|---|---|---|
|INT|整型|4字节整数类型，范围约+/-21亿|
|BIGINT|长整型|8字节整数类型，范围约+/-922亿亿|
|REAL|浮点型|4字节浮点数，范围约+/-1038|
|DOUBLE|浮点型|8字节浮点数，范围约+/-10308|
|DECIMAL(M,N)|高精度小数|由用户指定精度的小数，例如，DECIMAL(20,10)表示一共20位，其中小数10位，通常用于财务计算|
|CHAR(N)|定长字符串|存储指定长度的字符串，例如，CHAR(100)总是存储100个字符的字符串|
|VARCHAR(N)|变长字符串|存储可变长度的字符串，例如，VARCHAR(100)可以存储0~100个字符的字符串|
|BOOLEAN|布尔类型|存储True或者False|
|DATE|日期类型|存储日期，例如，2018-06-22|
|TIME|时间类型|存储时间，例如，12:20:59|
|DATETIME|日期和时间类型|存储日期+时间，例如，2018-06-22 12:20:59|

此外,还有一些不常用的数据类型,以及不同数据库支持的特定数据类型

主流数据库:

1. 商用:Oracle
2. 开源:MySql
3. 桌面数据库:微软Access
4. 嵌入式数据库:Sqlite

---

DDL:data definition language
DML:data manipulation language
DQL:data query language

SQL语句大写以示突出,表名字段小写

# 关系模型

## 主键

主键用于唯一标识数据表中的每一行数据

主键应该是全局唯一的,主键不应该和业务相关

一般将主键命名为id,主键不能为空

主键类型一般有:

1. 自增整数类型:数据库自动为每一个字段分配一个自增整数
2. 全局唯一GUID(UUID):全局唯一字符串作为主键,算法保证任意时间生成的字符串不同

一般使用BIGINT作为主键类型

---

联合主键

关系型数据库允许多个字段结合在一起作为唯一标识

但是引入复杂度,一般不使用

## 外键

外键用来实现一对多,多对多的关系映射:

| id  | name | other columns... |
| --- | ---- | ---------------- |
| 1   | 小明   | ...              |
| 2   | 小红   | ...              |

|id|name|other columns...|
|---|---|---|
|1|一班|...|
|2|二班|...|

一个班级->多个学生

在学生表里增加一个班级id

|id|class_id|name|other columns...|
|---|---|---|---|
|1|1|小明|...|
|2|1|小红|...|
|5|2|小白|...|

通过class_id,学生表与班级表关联起来,class_id称为外键

外键通过定义外键约束实现:

```mysql
ALTER TABLE students
ADD CONSTRAINT fk_class_id
FOREIGN KEY (class_id)
REFERENCES classes (id);
```

---

多对多关系由两个一对多实现

`teachers`表：

|id|name|
|---|---|
|1|张老师|
|2|王老师|
|3|李老师|
|4|赵老师|

`classes`表：

|id|name|
|---|---|
|1|一班|
|2|二班|

中间表`teacher_class`关联两个一对多关系：

|id|teacher_id|class_id|
|---|---|---|
|1|1|1|
|2|1|2|
|3|2|1|
|4|2|2|
|5|3|1|
|6|4|2|

---

一对一

一个表的记录一一映射到另一个表的记录

一个大表可以拆分为两个小表,区分经常查询和不经常查询的数据

## 索引

索引用来加速查询

索引的效率取决于数据是否散列,如果列数据存在大量相同值,则索引效率不高

对某列创建唯一索引,可以保证唯一性

索引透明

```sql
ALTER TABLE students
ADD INDEX idx_score(score);
```

```sql
ALTER TABLE students
ADD INDEX idx_name_score(name,score);
```

```sql
ALTER TABLE students
ADD UNIQUE INDEX uni_name(name);
```

# SQL语句

## 查询

*取表中的所有数据*

```sql
SELECT * FROM table_name;
```

---

*条件查询*

```sql
SELECT * FROM table_name WHERE 条件;
```

条件:布尔表达式

|条件|表达式举例1|表达式举例2|说明|
|---|---|---|---|
|使用=判断相等|score = 80|name = 'abc'|字符串需要用单引号括起来|
|使用>判断大于|score > 80|name > 'abc'|字符串比较根据ASCII码，中文字符比较根据数据库设置|
|使用>=判断大于或相等|score >= 80|name >= 'abc'||
|使用<判断小于|score < 80|name <= 'abc'||
|使用<=判断小于或相等|score <= 80|name <= 'abc'||
|使用<>判断不相等|score <> 80|name <> 'abc'||
|使用LIKE判断相似|name LIKE 'ab%'|name LIKE '%bc%'|%表示任意字符，例如'ab%'将匹配'ab'，'abc'，'abcd'|

条件组合:

AND,OR,NOT

NOT优先级最高

使用括号组合优先级

---

*投影查询:只查询某些列数据*

```sql
SELECT id,score FROM table_name;
```

使用AS关键字创建别名(也可以不用)

```sql
SELECT id,score AS points FROM table_name;
-- or
SELECT id,score points FROM table_name;
```

---

*排序*

使用`ORDER BY`子句

```sql
SELECT id,name,score FROM students ORDER BY score;
```

使用`DESC`(descend缩写)来降序排列

```sql
SELECT id,name,score FROM students ORDER BY score DESC;
```

按照score排序后有相同两行数据,这两行数据间也需要排序,则在ORDER BY后再加一个列名

ORDER BY需要放到条件语句之后

---

*分页查询*

为防止一次性查询数据量过大,使用分页查询加快速度

假设数据量总数为100

```sql
SELECT * FROM students
LIMIT 10 OFFSET 20
```

LIMIT M OFFSET N 表示:

限制一页查询有几个数据(pagesize),从第几个数据开始显示

`OFFSET = pageSize*(pageIndex-1)`

这样计算出的OFFSET表示完整显示第pageIndex页的数据

---

*聚合查询:使用函数快速计算结果*

统计总数 COUNT

```sql
SELECT COUNT(id) AS boys
FROM students
WHERE score >= 80 AND gender='M'
```

其他的一些聚合函数:

|函数|说明|
|---|---|
|SUM|计算某一列的合计值，该列必须为数值类型|
|AVG|计算某一列的平均值，该列必须为数值类型|
|MAX|计算某一列的最大值|
|MIN|计算某一列的最小值|

若WHERE没有匹配的任何行,则COUNT返回0,其他四个函数返回NULL

---

*分组聚合*

`GROUP BY`子句将查询按照某字段进行分类聚合

分组聚合的显示列表中,只能放入不会有多个的字段,比如name就不行,因为满足分组条件的可能有多个name

---

*多表查询*

查询两个表的数据,结果是两个表的笛卡尔积

可以使用别名来简化操作:

```sql
SELECT 
    s.id AS sid,
    s.name,
    s.score,
    s.gender,
    c.id AS cid,
    c.name AS cname
FROM
    students AS s,
    classes AS c;
```

---

*连接查询*

想要在表1的结果上拼接表2的结果

```sql
SELECT s.id,s.name,s.class_id,c.name AS class_name,s.gender,s.score
FROM student AS s
INNER JOIN classes AS c
ON s.class_id = c.id;
```

步骤:

1. 确认主表数据
2. 确定要连接的表,`INNER JOIN <表名>`
3. 确定连接条件,`ON <条件>`
4. 可选加上WHERE,ORDER BY等子句

四种JOIN类型

![](2-source-material/images/Pasted%20image%2020251103111801.png)

第四个:是选出两个表各自里面的全部数据,一个表中而另一表中没有的使用NULL

## 插入

```sql
INSERT INTO table_name (字段1,字段2,字段3...) VALUES(值1,值2,值3...)
-- eg.
INSERT INTO students (name,score,gender) VALUES('小明',91,'M')
```

为何不增加id?->id在建表时被设置为自增主键

INSER字段顺序不必和表相同,但是VALUES顺序需要和字段顺序相同
VALUES处可插入多个数据

## 更新数据

```sql
UPDATE <表名>
SET <字段1> = <值1>,<字段2> = <值2>
WHERE id=1;
```

其中,SET语句后可以使用表达式:

```sql
UPDATE students SET score=score+10 WHERE score<80;
```

**update可以不使用where语句,但是有很大风险!**

建议在update前先select确定结果正确

## 删除数据

```sql
DELETE FROM <表名> WHERE ...;
```

如果WHERE不匹配,则不删除任何数据

如果没有WHERE,则删除整个表

# 事务

## read uncommitted

隔离级别最低的事务,可能读到未committed的数据,如果另一个事务回滚,则读到的就是脏数据:

```plain
mysql> select * from students;
+----+-------+
| id | name  |
+----+-------+
|  1 | Alice |
+----+-------+
1 row in set (0.00 sec)
```

然后，分别开启两个MySQL客户端连接，按顺序依次执行事务A和事务B：

|时刻|事务A|事务B|
|---|---|---|
|1|SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;|SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;|
|2|BEGIN;|BEGIN;|
|3|UPDATE students SET name = 'Bob' WHERE id = 1;||
|4||SELECT * FROM students WHERE id = 1;|
|5|ROLLBACK;||
|6||SELECT * FROM students WHERE id = 1;|
|7||COMMIT;|
则事务B前后两次读取的数据不一致

## read committed

一个事务不会读到另一个事务未提交的数据,但是会发生不可重复读的问题:

在一个事务内多次读取同一数据,在事务未结束时,其他事务修改该数据,则读取数据不一致

```plain
mysql> select * from students;
+----+-------+
| id | name  |
+----+-------+
|  1 | Alice |
+----+-------+
1 row in set (0.00 sec)
```

然后，分别开启两个MySQL客户端连接，按顺序依次执行事务A和事务B：

|时刻|事务A|事务B|
|---|---|---|
|1|SET TRANSACTION ISOLATION LEVEL READ COMMITTED;|SET TRANSACTION ISOLATION LEVEL READ COMMITTED;|
|2|BEGIN;|BEGIN;|
|3||SELECT * FROM students WHERE id = 1; -- Alice|
|4|UPDATE students SET name = 'Bob' WHERE id = 1;||
|5|COMMIT;||
|6||SELECT * FROM students WHERE id = 1; -- Bob|
|7||COMMIT;|

## repeatable read

一个事务可能遇到幻读的问题

幻读指的是,在一个事务中,第一次查询某个数据发现没有,但是当试图更新这条数据时,却发生了成功,再次读取,存在.

也就是说,repeatable read通过某种机制保证了一个事务中的读取读到的都是事务开始时的数据.但是如果过程中发生了数据的修改,则该保证失效

```plain
mysql> select * from students;
+----+-------+
| id | name  |
+----+-------+
|  1 | Alice |
+----+-------+
1 row in set (0.00 sec)
```

然后，分别开启两个MySQL客户端连接，按顺序依次执行事务A和事务B：

|时刻|事务A|事务B|
|---|---|---|
|1|SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;|SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;|
|2|BEGIN;|BEGIN;|
|3||SELECT * FROM students WHERE id = 99; -- empty|
|4|INSERT INTO students (id, name) VALUES (99, 'Bob');||
|5|COMMIT;||
|6||SELECT * FROM students WHERE id = 99; -- empty|
|7||UPDATE students SET name = 'Alice' WHERE id = 99; -- 1 row affected|
|8||SELECT * FROM students WHERE id = 99; -- Alice|
|9||COMMIT;|

## Serializable

所有事务依次进行,不会并行,安全性最高

但是由于事务串行执行,所以性能大大下降

# 其他语句

## select distinct

一个列可能包含多个重复值，如果希望仅列出不同的值，则使用distinct

```sql
SELECT DISTINCT c1,c2
FROM table_name;
```

## select top

限制返回的结果的行数,类似limit

```mysql
SELECT c1,c2
FROM table_name
LIMIT number;
```

```postgresql
SELECT c1,c2
FROM table_name
LIMIT number;
```

```sql server
SELECT TOP number|percent column1, column2, ...
FROM table_name;
```
number|percent：指定返回的行数或百分比。
- `number`：具体的行数。
- `percent`：数据集的百分比

## LIKE

LIKE用于WHERE指定列的搜索模式,通常和通配符%,_ 一起使用

```sql
SELECT c1,c2
FROM table_name
WHERE column_name LIKE pattern;
```

通配符:
%:匹配任意字符(包括零个)
_ :匹配单个字符

## 通配符

| 通配符                                     | 描述            |
| --------------------------------------- | ------------- |
| %                                       | 替代 0 个或多个字符   |
| _                                       | 替代一个字符        |
| [_charlist_]                            | 字符列中的任何单一字符   |
| [^_charlist_]  <br>或  <br>[!_charlist_] | 不在字符列中的任何单一字符 |

## IN

在where中指定搜索出来的值要匹配某个值

```sql
SELECT column1, column2, ...
FROM table_name
WHERE column IN (value1, value2, ...);
```

其中,value1和value2是数据库中的值

## BETWEEN

选取介于两个值之间的数据范围内的值,可以是数值,文本,日期等

```sql
SELECT column1, column2, ...
FROM table_name
WHERE column BETWEEN value1 AND value2;
```

value1:范围起始
value2:范围截止

可以和IN,NOT等联合使用:

```sql
SELECT * FROM table
WHERE c1 NOT BETWEEN v1 AND v2
```

```sql
SELECT * FROM WebsitesWHERE (alexa BETWEEN 1 AND 20)AND country NOT 
 IN ('USA', 'IND');
```

## UNION

用于链接两个SELECT的结果,每个SELECT语句必须具有相同数量的列,且数据类型相似

```sql
SELECT c1,c2
FROM table1
UNION
SELECT c1,c2
FROM table2;
```

UNION会默认去重,如要保留重复记录,使用UNION ALL

## CREATE DATABASE

```sql
CREATE DATABASE dbname;
```

## 约束

约束用于规定表中的数据规则

在创建表时规定或者创建后修改(ALTER TABLE)

```sql
CREATE TABLE table_name
(
    column_name1 data_type(size) constraint_name,
    column_name2 data_type(size) constraint_name,
    column_name3 data_type(size) constraint_name,
    ....
);
```

在 SQL 中，我们有如下约束：

- **NOT NULL** - 指示某列不能存储 NULL 值。
- **UNIQUE** - 保证某列的每行必须有唯一的值。
- **PRIMARY KEY** - NOT NULL 和 UNIQUE 的结合。确保某列（或两个列多个列的结合）有唯一标识，有助于更容易更快速地找到表中的一个特定的记录。
- **FOREIGN KEY** - 保证一个表中的数据匹配另一个表中的值的参照完整性。
- **CHECK** - 保证列中的值符合指定的条件。
- **DEFAULT** - 规定没有给列赋值时的默认值。
- **INDEX** - 用于快速访问数据库表中的数据。

# AI summarize

## 概述

SQL（Structured Query Language，结构化查询语言）是访问和处理关系型数据库的计算机标准语言。它是一种特定目的编程语言，用于管理关系数据库管理系统（RDBMS），或在关系流数据管理系统（RDSMS）中进行流处理。

### 为什么需要数据库？
数据库提供了以下优势：
- **数据持久化**：数据不会因为程序关闭而丢失
- **数据共享**：多个应用可以同时访问同一数据集
- **数据一致性**：通过事务机制保证数据的完整性和一致性
- **数据安全**：提供权限管理和数据备份恢复机制
- **数据独立性**：程序员不需要关注数据存储的物理细节，专注于业务逻辑

### 数据模型发展历程

**层次模型**：采用树状结构组织数据，适合表示一对多关系，但查询复杂
**网状模型**：采用图结构组织数据，能表示多对多关系，但结构复杂
**关系模型**：采用二维表格组织数据，基于集合论和谓词逻辑，具有坚实的数学理论基础

关系模型胜出的原因：
- 结构简单直观，易于理解
- 有严格的数学理论支撑（关系代数）
- 数据独立性高
- 标准化程度高

### 数据类型详解

| 名称 | 类型 | 说明 | 存储空间 | 范围/示例 |
|------|------|------|----------|-----------|
| INT | 整型 | 4字节整数类型 | 4字节 | -2,147,483,648 到 2,147,483,647 |
| BIGINT | 长整型 | 8字节整数类型 | 8字节 | -9,223,372,036,854,775,808 到 9,223,372,036,854,775,807 |
| REAL | 浮点型 | 单精度浮点数 | 4字节 | 约 ±3.4E+38，精度约7位小数 |
| DOUBLE | 浮点型 | 双精度浮点数 | 8字节 | 约 ±1.7E+308，精度约15位小数 |
| DECIMAL(M,N) | 高精度小数 | 精确小数类型 | 可变 | M为总位数，N为小数位数，DECIMAL(20,10)表示20位总数，10位小数 |
| CHAR(N) | 定长字符串 | 固定长度字符串 | N字节 | 总是存储N个字符，不足补空格 |
| VARCHAR(N) | 变长字符串 | 可变长度字符串 | 实际长度+1/2字节 | 最多存储N个字符，按实际长度存储 |
| BOOLEAN | 布尔类型 | 逻辑值 | 1字节 | TRUE/FALSE |
| DATE | 日期类型 | 日期值 | 3字节 | '2018-06-22' |
| TIME | 时间类型 | 时间值 | 3字节 | '12:20:59' |
| DATETIME | 日期时间类型 | 日期和时间 | 8字节 | '2018-06-22 12:20:59' |

**其他重要数据类型**：
- TEXT：长文本数据
- BLOB：二进制大对象
- ENUM：枚举类型
- SET：集合类型

### 主流数据库系统

1. **商用数据库**：
   - Oracle：功能最强大的商业数据库，适合大型企业应用
   - SQL Server：微软的商业数据库，与Windows生态系统深度集成
   - DB2：IBM的商业数据库，适合大型事务处理

2. **开源数据库**：
   - MySQL：最流行的开源数据库，性能优秀，社区活跃
   - PostgreSQL：功能最丰富的开源数据库，支持高级特性
   - MariaDB：MySQL的分支，完全兼容MySQL

3. **桌面数据库**：
   - Microsoft Access：适合小型应用和个人使用
   - SQLite：嵌入式数据库，零配置，单文件存储

4. **嵌入式数据库**：
   - SQLite：轻量级，无服务器，适合移动应用和嵌入式系统
   - H2：Java编写的内存数据库，适合测试和开发

### SQL语言分类

- **DDL（Data Definition Language）**：数据定义语言，用于定义和管理数据库对象
  - CREATE、ALTER、DROP、TRUNCATE
- **DML（Data Manipulation Language）**：数据操作语言，用于操作数据
  - INSERT、UPDATE、DELETE
- **DQL（Data Query Language）**：数据查询语言，用于查询数据
  - SELECT
- **DCL（Data Control Language）**：数据控制语言，用于权限管理
  - GRANT、REVOKE
- **TCL（Transaction Control Language）**：事务控制语言
  - COMMIT、ROLLBACK、SAVEPOINT

**命名规范**：
- SQL关键字使用大写
- 表名和字段名使用小写
- 使用下划线分隔单词

## 关系模型

### 主键（Primary Key）

主键是表中唯一标识每一行数据的列或列组合。

**主键特性**：
- **唯一性**：主键值必须唯一，不能重复
- **非空性**：主键值不能为NULL
- **稳定性**：主键值不应随时间变化
- **简洁性**：主键应该简单明了

**主键选择策略**：

1. **自增整数类型**：
   - 优点：简单、高效、占用空间小
   - 缺点：在分布式系统中可能产生冲突
   - 示例：`id BIGINT AUTO_INCREMENT PRIMARY KEY`

2. **全局唯一GUID/UUID**：
   - 优点：全局唯一，适合分布式系统
   - 缺点：占用空间大（16字节），索引效率较低
   - 示例：`id CHAR(36) PRIMARY KEY DEFAULT UUID()`

3. **自然主键**：
   - 使用业务中有唯一性的字段作为主键
   - 一般不推荐，因为业务规则可能变化

**最佳实践**：
- 主键列通常命名为`id`
- 使用`BIGINT`类型以避免整数溢出
- 避免使用业务相关字段作为主键

### 联合主键（Composite Primary Key）

联合主键使用多个列的组合来唯一标识表中的每一行。

**示例**：
```sql
CREATE TABLE order_items (
    order_id BIGINT,
    product_id BIGINT,
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);
```

**优缺点**：
- **优点**：在某些场景下更符合业务逻辑
- **缺点**：
  - 外键引用复杂
  - 索引效率可能较低
  - 应用代码处理复杂

**使用场景**：
- 多对多关系的中间表
- 历史数据表
- 日志表

### 外键（Foreign Key）

外键用于建立表与表之间的关联关系，实现数据完整性约束。

**一对一关系**：
```sql
-- 用户表
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100)
);

-- 用户详情表
CREATE TABLE user_profiles (
    user_id BIGINT PRIMARY KEY,
    full_name VARCHAR(100),
    birth_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**一对多关系**：
```sql
-- 部门表
CREATE TABLE departments (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- 员工表
CREATE TABLE employees (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department_id BIGINT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
```

**多对多关系**：
```sql
-- 学生表
CREATE TABLE students (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- 课程表
CREATE TABLE courses (
    id BIGINT PRIMARY KEY,
    title VARCHAR(200) NOT NULL
);

-- 选课关系表
CREATE TABLE student_courses (
    student_id BIGINT,
    course_id BIGINT,
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

**外键约束操作**：
```sql
-- 添加外键约束
ALTER TABLE child_table
ADD CONSTRAINT fk_name
FOREIGN KEY (child_column) 
REFERENCES parent_table(parent_column)
ON DELETE CASCADE
ON UPDATE CASCADE;
```

**外键约束选项**：
- `ON DELETE CASCADE`：父表记录删除时，子表相关记录自动删除
- `ON DELETE SET NULL`：父表记录删除时，子表外键设为NULL
- `ON DELETE RESTRICT`：阻止删除父表记录（默认）
- `ON UPDATE CASCADE`：父表主键更新时，子表外键同步更新

### 索引（Index）

索引是帮助数据库高效获取数据的数据结构，类似于书籍的目录。

**索引类型**：

1. **B-Tree索引**：最常用的索引类型，适合范围查询和精确查找
2. **哈希索引**：适合等值查询，不支持范围查询
3. **全文索引**：适合文本内容的搜索
4. **空间索引**：适合地理空间数据

**创建索引示例**：
```sql
-- 单列索引
CREATE INDEX idx_score ON students(score);

-- 多列复合索引
CREATE INDEX idx_name_score ON students(name, score);

-- 唯一索引
CREATE UNIQUE INDEX uni_email ON users(email);

-- 前缀索引（字符串类型）
CREATE INDEX idx_name_prefix ON students(name(10));
```

**索引选择原则**：
- **高选择性列**：列中不同值较多的列适合建索引
- **查询频繁的列**：经常出现在WHERE条件中的列
- **外键列**：提高连接查询性能
- **排序和分组列**：经常用于ORDER BY和GROUP BY的列

**不适合建索引的情况**：
- 数据量小的表
- 频繁更新的列
- 区分度低的列（如性别、状态标志）
- 很少用于查询条件的列

**索引的代价**：
- 占用存储空间
- 降低数据插入、更新、删除的速度
- 维护成本

## SQL语句

### 查询语句

#### 基本查询
```sql
-- 查询所有列
SELECT * FROM employees;

-- 查询特定列
SELECT id, name, salary FROM employees;

-- 使用表别名
SELECT e.id, e.name, e.department 
FROM employees AS e;
```

#### 条件查询
**比较运算符**：
```sql
-- 等于
SELECT * FROM products WHERE price = 100;

-- 不等于
SELECT * FROM products WHERE price <> 100;
SELECT * FROM products WHERE price != 100;

-- 大于/小于
SELECT * FROM products WHERE price > 100;
SELECT * FROM products WHERE price < 100;

-- 范围查询
SELECT * FROM products WHERE price BETWEEN 50 AND 200;

-- 空值检查
SELECT * FROM employees WHERE department_id IS NULL;
SELECT * FROM employees WHERE department_id IS NOT NULL;
```

**逻辑运算符**：
```sql
-- AND 运算符
SELECT * FROM employees 
WHERE salary > 5000 AND department = 'IT';

-- OR 运算符  
SELECT * FROM employees
WHERE department = 'IT' OR department = 'HR';

-- NOT 运算符
SELECT * FROM employees
WHERE NOT department = 'IT';

-- 复杂条件组合
SELECT * FROM employees
WHERE (salary > 5000 AND department = 'IT') 
   OR (salary > 8000 AND department = 'Sales');
```

**LIKE模糊查询**：
```sql
-- % 通配符：匹配任意字符（包括零个字符）
SELECT * FROM customers WHERE name LIKE '张%';    -- 张开头
SELECT * FROM customers WHERE name LIKE '%技术%'; -- 包含"技术"
SELECT * FROM customers WHERE name LIKE '%公司';  -- 以"公司"结尾

-- _ 通配符：匹配单个字符
SELECT * FROM products WHERE code LIKE 'A_C%';   -- 第二个字符为任意字符

-- 转义特殊字符
SELECT * FROM files WHERE name LIKE '%100\%%' ESCAPE '\';
```

#### 投影查询
```sql
-- 选择特定列
SELECT id, name, salary FROM employees;

-- 使用列别名
SELECT 
    id AS employee_id,
    name AS employee_name,
    salary * 12 AS annual_salary
FROM employees;

-- 使用表达式
SELECT 
    name,
    salary,
    salary * 0.1 AS bonus,
    salary * 1.1 AS total_compensation
FROM employees;
```

#### 排序查询
```sql
-- 单列排序
SELECT * FROM products ORDER BY price;

-- 降序排序
SELECT * FROM products ORDER BY price DESC;

-- 多列排序
SELECT * FROM employees 
ORDER BY department ASC, salary DESC;

-- 使用表达式排序
SELECT * FROM products 
ORDER BY (price * stock_quantity) DESC;

-- NULL值排序处理
SELECT * FROM employees 
ORDER BY commission_pct IS NULL, commission_pct DESC;
```

#### 分页查询
**不同数据库的分页语法**：

**MySQL**：
```sql
SELECT * FROM products 
ORDER BY id
LIMIT 10 OFFSET 20;  -- 第3页，每页10条

-- 简化写法
SELECT * FROM products 
ORDER BY id
LIMIT 20, 10;  -- OFFSET, LIMIT
```

**PostgreSQL**：
```sql
SELECT * FROM products 
ORDER BY id
LIMIT 10 OFFSET 20;
```

**SQL Server**：
```sql
SELECT * FROM products 
ORDER BY id
OFFSET 20 ROWS 
FETCH NEXT 10 ROWS ONLY;
```

**Oracle**：
```sql
SELECT * FROM (
    SELECT t.*, ROWNUM rn FROM (
        SELECT * FROM products ORDER BY id
    ) t WHERE ROWNUM <= 30
) WHERE rn > 20;
```

**分页计算公式**：
```
OFFSET = pageSize × (pageIndex - 1)
```

#### 聚合查询
**常用聚合函数**：

| 函数 | 说明 | 示例 |
|------|------|------|
| COUNT | 统计行数 | `COUNT(*)`, `COUNT(column)` |
| SUM | 求和 | `SUM(salary)` |
| AVG | 求平均值 | `AVG(salary)` |
| MAX | 求最大值 | `MAX(salary)` |
| MIN | 求最小值 | `MIN(salary)` |
| GROUP_CONCAT | 连接字符串 | `GROUP_CONCAT(name)` |

**聚合查询示例**：
```sql
-- 基本统计
SELECT 
    COUNT(*) AS total_employees,
    AVG(salary) AS avg_salary,
    MAX(salary) AS max_salary,
    MIN(salary) AS min_salary
FROM employees;

-- 条件统计
SELECT 
    COUNT(*) AS high_salary_count
FROM employees 
WHERE salary > 10000;

-- 注意：COUNT(column)不统计NULL值
SELECT 
    COUNT(*) AS total_count,          -- 统计所有行
    COUNT(commission_pct) AS has_commission_count  -- 只统计非NULL
FROM employees;
```

#### 分组聚合
```sql
-- 按部门分组统计
SELECT 
    department,
    COUNT(*) AS employee_count,
    AVG(salary) AS avg_salary,
    MAX(salary) AS max_salary
FROM employees
GROUP BY department;

-- 多列分组
SELECT 
    department,
    job_title,
    COUNT(*) AS count,
    AVG(salary) AS avg_salary
FROM employees
GROUP BY department, job_title;

-- HAVING子句：对分组结果过滤
SELECT 
    department,
    AVG(salary) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 5000;

-- WHERE和HAVING的区别
SELECT 
    department,
    AVG(salary) AS avg_salary
FROM employees
WHERE hire_date > '2020-01-01'  -- 先过滤行
GROUP BY department
HAVING AVG(salary) > 5000;      -- 再过滤分组
```

#### 多表查询
```sql
-- 笛卡尔积（谨慎使用）
SELECT 
    e.id AS emp_id,
    e.name AS emp_name,
    d.id AS dept_id, 
    d.name AS dept_name
FROM employees e, departments d;

-- 等值连接
SELECT 
    e.id AS emp_id,
    e.name AS emp_name,
    d.name AS dept_name
FROM employees e, departments d
WHERE e.department_id = d.id;

-- 使用表别名简化
SELECT 
    e.id,
    e.name,
    d.name AS department_name,
    m.name AS manager_name
FROM employees e, departments d, employees m
WHERE e.department_id = d.id
  AND e.manager_id = m.id;
```

#### 连接查询
**INNER JOIN**：
```sql
-- 内连接：只返回两个表都匹配的记录
SELECT 
    e.id,
    e.name,
    d.name AS department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.id;
```

**LEFT JOIN**：
```sql
-- 左外连接：返回左表所有记录，右表不匹配的显示NULL
SELECT 
    e.id,
    e.name,
    d.name AS department_name
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id;
```

**RIGHT JOIN**：
```sql
-- 右外连接：返回右表所有记录，左表不匹配的显示NULL
SELECT 
    e.id,
    e.name,
    d.name AS department_name
FROM employees e
RIGHT JOIN departments d ON e.department_id = d.id;
```

**FULL OUTER JOIN**：
```sql
-- 全外连接：返回两个表的所有记录
SELECT 
    e.id,
    e.name,
    d.name AS department_name
FROM employees e
FULL OUTER JOIN departments d ON e.department_id = d.id;
```

**自连接**：
```sql
-- 查询员工及其经理
SELECT 
    e.name AS employee_name,
    m.name AS manager_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

**多表连接**：
```sql
-- 连接多个表
SELECT 
    e.name AS employee_name,
    d.name AS department_name,
    p.name AS project_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.id
INNER JOIN employee_projects ep ON e.id = ep.employee_id
INNER JOIN projects p ON ep.project_id = p.id;
```

### 插入语句

```sql
-- 插入单条记录
INSERT INTO employees (name, department, salary, hire_date)
VALUES ('张三', '技术部', 8000, '2023-01-15');

-- 插入多条记录
INSERT INTO employees (name, department, salary, hire_date)
VALUES 
    ('李四', '销售部', 6000, '2023-02-01'),
    ('王五', '技术部', 9000, '2023-02-15'),
    ('赵六', '人事部', 5500, '2023-03-01');

-- 插入查询结果
INSERT INTO employee_archive (id, name, department, salary)
SELECT id, name, department, salary
FROM employees
WHERE hire_date < '2020-01-01';

-- 使用DEFAULT值
INSERT INTO products (name, price, create_time)
VALUES ('新产品', 100.00, DEFAULT);

-- 插入时忽略重复键
INSERT IGNORE INTO unique_table (id, name)
VALUES (1, '测试');
```

### 更新语句

```sql
-- 更新单条记录
UPDATE employees 
SET salary = 10000, title = '高级工程师'
WHERE id = 1;

-- 批量更新
UPDATE employees 
SET salary = salary * 1.1  -- 涨薪10%
WHERE department = '技术部';

-- 使用子查询更新
UPDATE employees 
SET salary = (
    SELECT AVG(salary) 
    FROM employees 
    WHERE department = '技术部'
)
WHERE id = 5;

-- 多表更新
UPDATE employees e
JOIN departments d ON e.department_id = d.id
SET e.salary = e.salary * 1.05
WHERE d.name = '销售部';

-- 条件更新
UPDATE products 
SET 
    price = CASE 
        WHEN stock_quantity > 100 THEN price * 0.9  -- 库存多打9折
        WHEN stock_quantity < 10 THEN price * 1.1   -- 库存少加价10%
        ELSE price
    END,
    update_time = NOW();
```

**更新注意事项**：
- 始终使用WHERE条件，避免全表更新
- 更新前先用SELECT验证条件
- 在事务中执行重要更新
- 备份重要数据

### 删除语句

```sql
-- 删除特定记录
DELETE FROM employees 
WHERE id = 1;

-- 条件删除
DELETE FROM employees 
WHERE department = '临时部门' 
  AND hire_date < '2020-01-01';

-- 使用子查询删除
DELETE FROM employees 
WHERE department_id IN (
    SELECT id FROM departments 
    WHERE status = '关闭'
);

-- 多表删除
DELETE e, d
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE d.name = '已解散部门';

-- 清空表（不可恢复）
TRUNCATE TABLE log_table;
```

**删除与TRUNCATE的区别**：
- DELETE是DML操作，可以回滚，逐行删除
- TRUNCATE是DDL操作，不可回滚，直接清空表
- DELETE会触发触发器，TRUNCATE不会
- DELETE会记录日志，TRUNCATE不记录

## 事务

事务是数据库操作的基本单位，保证一组操作要么全部成功，要么全部失败。

### ACID特性

- **原子性（Atomicity）**：事务中的所有操作要么全部完成，要么全部不完成
- **一致性（Consistency）**：事务执行前后，数据库处于一致状态
- **隔离性（Isolation）**：并发事务之间相互隔离
- **持久性（Durability）**：事务提交后，修改永久保存

### 事务隔离级别

#### READ UNCOMMITTED（读未提交）

**特点**：
- 隔离级别最低
- 可能读取到其他事务未提交的数据（脏读）
- 性能最好，但数据一致性最差

**示例场景**：
```sql
-- 事务A
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
-- 此时事务A未提交

-- 事务B  
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN;
SELECT balance FROM accounts WHERE id = 1; -- 可能读到未提交的修改

-- 如果事务A回滚，事务B读到的就是脏数据
```

**问题**：脏读、不可重复读、幻读

#### READ COMMITTED（读已提交）

**特点**：
- 只能读取已提交的数据
- 解决脏读问题
- 但存在不可重复读问题

**示例场景**：
```sql
-- 事务A
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN;
SELECT balance FROM accounts WHERE id = 1; -- 读取1000

-- 事务B
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;  
BEGIN;
UPDATE accounts SET balance = 900 WHERE id = 1;
COMMIT;

-- 事务A再次读取
SELECT balance FROM accounts WHERE id = 1; -- 读取900，前后不一致
```

**问题**：不可重复读、幻读

#### REPEATABLE READ（可重复读）

**特点**：
- 保证在同一事务中多次读取同一数据的结果一致
- 解决不可重复读问题
- 但存在幻读问题

**示例场景**：
```sql
-- 事务A
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
SELECT COUNT(*) FROM accounts WHERE type = 'SAVING'; -- 返回5

-- 事务B
INSERT INTO accounts (type, balance) VALUES ('SAVING', 1000);
COMMIT;

-- 事务A再次统计
SELECT COUNT(*) FROM accounts WHERE type = 'SAVING'; -- 仍然返回5
-- 但尝试插入时会发现主键冲突
```

**MySQL的解决方案**：使用多版本并发控制（MVCC）

#### SERIALIZABLE（串行化）

**特点**：
- 最高的隔离级别
- 所有事务串行执行
- 解决所有并发问题
- 性能最差

**示例场景**：
```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
-- 所有操作串行执行
SELECT * FROM accounts;
UPDATE accounts SET balance = balance + 100;
COMMIT;
```

### 事务控制语句

```sql
-- 开始事务
BEGIN;
START TRANSACTION;

-- 提交事务
COMMIT;

-- 回滚事务
ROLLBACK;

-- 设置保存点
SAVEPOINT point1;

-- 回滚到保存点
ROLLBACK TO point1;

-- 释放保存点
RELEASE SAVEPOINT point1;
```

### 死锁处理

```sql
-- 设置死锁超时时间
SET innodb_lock_wait_timeout = 50;

-- 查看死锁信息
SHOW ENGINE INNODB STATUS;

-- 避免死锁的策略
-- 1. 按相同顺序访问表
-- 2. 使用较低的隔离级别
-- 3. 减少事务执行时间
-- 4. 使用索引减少锁的范围
```

## 其他SQL语句

### SELECT DISTINCT

```sql
-- 去除重复值
SELECT DISTINCT department FROM employees;

-- 多列去重
SELECT DISTINCT department, job_title FROM employees;

-- 与聚合函数结合
SELECT COUNT(DISTINCT department) FROM employees;
```

### 限制结果集

**MySQL/PostgreSQL**：
```sql
SELECT * FROM products LIMIT 10;
SELECT * FROM products LIMIT 10 OFFSET 20;
```

**SQL Server**：
```sql
SELECT TOP 10 * FROM products;
SELECT TOP 10 PERCENT * FROM products;
```

**Oracle**：
```sql
SELECT * FROM products WHERE ROWNUM <= 10;
```

### 模式匹配

**LIKE操作符**：
```sql
-- 基本模式匹配
SELECT * FROM customers WHERE name LIKE '张%';

-- 多个通配符组合
SELECT * FROM products WHERE name LIKE '%手机%保护%';

-- 字符列表匹配
SELECT * FROM users WHERE name LIKE '[张李王]%';  -- 张、李、王开头

-- 排除字符列表
SELECT * FROM users WHERE name LIKE '[^张李王]%'; -- 非张、李、王开头

-- 转义特殊字符
SELECT * FROM files WHERE path LIKE '/home/%\%%' ESCAPE '\';
```

### IN操作符

```sql
-- 值列表
SELECT * FROM employees 
WHERE department IN ('技术部', '销售部', '人事部');

-- 子查询结果
SELECT * FROM products 
WHERE category_id IN (
    SELECT id FROM categories 
    WHERE parent_id = 1
);

-- NOT IN
SELECT * FROM employees 
WHERE department NOT IN ('临时部门', '测试部门');
```

### BETWEEN操作符

```sql
-- 数值范围
SELECT * FROM products 
WHERE price BETWEEN 50 AND 200;

-- 日期范围
SELECT * FROM orders 
WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31';

-- 字符串范围
SELECT * FROM employees 
WHERE name BETWEEN 'A' AND 'M';

-- NOT BETWEEN
SELECT * FROM products 
WHERE price NOT BETWEEN 100 AND 500;
```

### 集合操作

**UNION**：
```sql
-- 合并结果集（去重）
SELECT name FROM current_employees
UNION
SELECT name FROM former_employees;

-- 保留所有记录（包括重复）
SELECT name FROM table1
UNION ALL
SELECT name FROM table2;

-- 多个UNION
SELECT name FROM table1
UNION
SELECT name FROM table2  
UNION
SELECT name FROM table3;
```

**INTERSECT（交集）**：
```sql
-- 两个查询的交集
SELECT name FROM employees
INTERSECT
SELECT name FROM managers;
```

**EXCEPT/MINUS（差集）**：
```sql
-- SQL Server/PostgreSQL
SELECT name FROM all_employees
EXCEPT
SELECT name FROM current_employees;

-- Oracle
SELECT name FROM all_employees
MINUS
SELECT name FROM current_employees;
```

### 数据库操作

```sql
-- 创建数据库
CREATE DATABASE company;

-- 指定字符集和排序规则
CREATE DATABASE company 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 查看数据库
SHOW DATABASES;

-- 选择数据库
USE company;

-- 删除数据库
DROP DATABASE old_company;

-- 修改数据库
ALTER DATABASE company CHARACTER SET utf8;
```

### 约束详解

#### NOT NULL约束
```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

#### UNIQUE约束
```sql
CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    sku VARCHAR(50) UNIQUE,  -- 列级约束
    name VARCHAR(100),
    CONSTRAINT uk_product_sku UNIQUE (sku)  -- 表级约束
);

-- 复合唯一约束
CREATE TABLE employee_contacts (
    employee_id BIGINT,
    contact_type VARCHAR(20),
    contact_value VARCHAR(100),
    UNIQUE (employee_id, contact_type)
);
```

#### PRIMARY KEY约束
```sql
CREATE TABLE departments (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- 复合主键
CREATE TABLE order_items (
    order_id BIGINT,
    item_id BIGINT,
    quantity INT,
    PRIMARY KEY (order_id, item_id)
);
```

#### FOREIGN KEY约束
```sql
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    customer_id BIGINT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

#### CHECK约束
```sql
CREATE TABLE employees (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100),
    salary DECIMAL(10,2),
    age INT,
    CONSTRAINT chk_salary CHECK (salary > 0),
    CONSTRAINT chk_age CHECK (age >= 18 AND age <= 65)
);
```

#### DEFAULT约束
```sql
CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2) DEFAULT 0.00,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'ACTIVE'
);
```

#### 索引约束
```sql
-- 创建索引
CREATE INDEX idx_employee_name ON employees(name);
CREATE INDEX idx_employee_dept_salary ON employees(department, salary);

-- 唯一索引
CREATE UNIQUE INDEX uk_user_email ON users(email);

-- 全文索引
CREATE FULLTEXT INDEX ft_product_desc ON products(description);

-- 删除索引
DROP INDEX idx_employee_name ON employees;
```

## 常见SQL命令速查表

| 类别 | 命令 | 语法示例 | 说明 |
|------|------|----------|------|
| **数据库操作** | CREATE DATABASE | `CREATE DATABASE dbname;` | 创建数据库 |
| | USE | `USE dbname;` | 选择数据库 |
| | DROP DATABASE | `DROP DATABASE dbname;` | 删除数据库 |
| **表操作** | CREATE TABLE | `CREATE TABLE tablename (col1 type, col2 type);` | 创建表 |
| | ALTER TABLE | `ALTER TABLE tablename ADD col type;` | 修改表结构 |
| | DROP TABLE | `DROP TABLE tablename;` | 删除表 |
| | TRUNCATE TABLE | `TRUNCATE TABLE tablename;` | 清空表数据 |
| **数据查询** | SELECT | `SELECT col1, col2 FROM table;` | 查询数据 |
| | DISTINCT | `SELECT DISTINCT col FROM table;` | 去重查询 |
| | WHERE | `SELECT * FROM table WHERE condition;` | 条件查询 |
| | ORDER BY | `SELECT * FROM table ORDER BY col;` | 排序查询 |
| | GROUP BY | `SELECT col, COUNT(*) FROM table GROUP BY col;` | 分组查询 |
| | HAVING | `SELECT col FROM table GROUP BY col HAVING condition;` | 分组条件 |
| **数据操作** | INSERT | `INSERT INTO table (col1, col2) VALUES (val1, val2);` | 插入数据 |
| | UPDATE | `UPDATE table SET col1=val1 WHERE condition;` | 更新数据 |
| | DELETE | `DELETE FROM table WHERE condition;` | 删除数据 |
| **连接查询** | INNER JOIN | `SELECT * FROM t1 INNER JOIN t2 ON condition;` | 内连接 |
| | LEFT JOIN | `SELECT * FROM t1 LEFT JOIN t2 ON condition;` | 左外连接 |
| | RIGHT JOIN | `SELECT * FROM t1 RIGHT JOIN t2 ON condition;` | 右外连接 |
| | FULL JOIN | `SELECT * FROM t1 FULL JOIN t2 ON condition;` | 全外连接 |
| **集合操作** | UNION | `SELECT col FROM t1 UNION SELECT col FROM t2;` | 并集 |
| | UNION ALL | `SELECT col FROM t1 UNION ALL SELECT col FROM t2;` | 并集(保留重复) |
| | INTERSECT | `SELECT col FROM t1 INTERSECT SELECT col FROM t2;` | 交集 |
| | EXCEPT | `SELECT col FROM t1 EXCEPT SELECT col FROM t2;` | 差集 |
| **约束** | PRIMARY KEY | `CREATE TABLE t (id INT PRIMARY KEY);` | 主键约束 |
| | FOREIGN KEY | `FOREIGN KEY (col) REFERENCES table(col);` | 外键约束 |
| | UNIQUE | `CREATE TABLE t (col INT UNIQUE);` | 唯一约束 |
| | NOT NULL | `CREATE TABLE t (col INT NOT NULL);` | 非空约束 |
| | CHECK | `CREATE TABLE t (col INT CHECK (col>0));` | 检查约束 |
| | DEFAULT | `CREATE TABLE t (col INT DEFAULT 0);` | 默认值 |
| **事务控制** | BEGIN | `BEGIN;` | 开始事务 |
| | COMMIT | `COMMIT;` | 提交事务 |
| | ROLLBACK | `ROLLBACK;` | 回滚事务 |
| | SAVEPOINT | `SAVEPOINT name;` | 设置保存点 |
| **索引** | CREATE INDEX | `CREATE INDEX idx_name ON table(col);` | 创建索引 |
| | DROP INDEX | `DROP INDEX idx_name ON table;` | 删除索引 |
| **视图** | CREATE VIEW | `CREATE VIEW viewname AS SELECT ...;` | 创建视图 |
| | DROP VIEW | `DROP VIEW viewname;` | 删除视图 |
| **权限管理** | GRANT | `GRANT privilege ON table TO user;` | 授权 |
| | REVOKE | `REVOKE privilege ON table FROM user;` | 撤销权限 |

## 总结

本笔记详细介绍了SQL的各个方面，从基础概念到高级特性，涵盖了：

1. **SQL基础**：数据类型、数据库系统、语言分类
2. **关系模型**：主键、外键、索引的原理和应用
3. **查询技术**：各种查询语句的详细用法和最佳实践
4. **数据操作**：增删改操作的完整语法和注意事项
5. **事务管理**：ACID特性、隔离级别、并发控制
6. **高级特性**：约束、集合操作、模式匹配等

掌握这些知识可以帮助你高效地使用SQL进行数据库开发和管理，构建稳定可靠的数据库应用。
# Reference
