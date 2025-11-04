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


# Reference
