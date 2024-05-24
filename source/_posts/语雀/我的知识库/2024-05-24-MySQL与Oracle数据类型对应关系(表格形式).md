---
layout: post
title: MySQL与Oracle数据类型对应关系(表格形式)
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "bk@2024"
typora-root-url: ./..
date: 2024-05-24 10:50:14
---
MySQL与Oracle两种数据库在工作中，都是用的比较多的数据库，由于MySQL与Oracle在数据类型上有部分差异，在我们迁移数据库时，会遇上一定的麻烦
# MySQL与Oracle数据库数据类型的对应关系
## 一、二种数据库中的表现形式
| 说明 | mysql | oracle |
| --- | --- | --- |
| 变长字符串 | VARCHAR[0-65535]
定义长度默认按字符长度计算，如果是GBK编码的汉字将占用2个字节 | VARCHAR2[1-4000]
<!--more-->
VARCHAR是VARCHAR2的同义词
定义默认按字节长度计算 |
| 整数 | TINYINT(-128-127)
SMALLINT(-32768-32767)
MEDIUMINT(-8388608-8388607)
INT(-2147483648-2147483647)
BIGINT(-9223372036854775808-9223372036854775807)  | 无专用类型，
TINYINT可以用NUMBER(3,0)代替
SMALLINT可以用NUMBER(5,0)代替
MEDUIMINT可以用NUMBER(7,0)代替

INT可以用NUMBER(10,0)代替

BIGINT可以用NUMBER(20,0)代替

ORACLE中有SMALLINT,INT,INTEGER类型，不过这是NUMBER(38,0)的同义词 |
| 数值类型 | DECIMAL[1-65[,0-30]]
NUMERIC是DECIMAL的同义词 | NUMBER 可表示数范围： 1*10^-130至1*10^126
NUMBER([1-38][,-84-127])

DECIMAL、NUMERIC、DEC是NUMBER的同义词 |
| 浮点型 | FLOAT(D,M) | oracle10g开始增加BINARY_FLOAT类型
10g以前无专用类型，可以用NUMBER代替
ORACLE中有FLOAT和REAL类型，不过这是NUMBER的同义词 |
| 双精度浮点型 | DOUBLE(D,M) | oracle10g开始增加BINARY_DOUBLE类型
10g以前无专用类型，可以用NUMBER代替
ORACLE中有DOUBLE PRECISION类型，不过这是NUMBER的同义词 |
| 位类型 | BIT(1-64) | 无 |
| 日期类型 | DATE，3字节存储，只存储日期，没有时间，支持范围是[1000-01-01]至[9999-12-31]
TIME，3字节存储，只存储时间，没有日期，支持范围是[-838:59:59]至[838:59:59]
DATETIME，占8字节存储，可表示日期和时间，支持范围是[1000-01-01 00:00:00]至[9999-12-31 23:59:59]
TIMESTAMP，占4字节存储，可表示日期和时间，范围是[1970-01-01 00:00:00]至[2038-01-19 03:14:07] | DATE类型
7字节存储，可表示日期和时间，支持范围是[-4712-01-01 00:00:00]至[9999-12-31 23:59:59] |
| 高精度日期 | 5.6.4以前不支持小数秒精度
5.6.4开始TIME,DATETIME,TIMESTAMP支持，最多可以6位小数秒，也就是微秒级别 | TIMESTAMP[0-9]
占用空间7-11个字节，当小数秒精度为0时与DATE类型相同，小数秒最高精度可达9位，也就是纳精度 |
| 年份 | YEAR，1字节存储，只存储年份，支持范围是[1901]至[2155] | 无对应类型，可以用NUMBER(3,0)代替 |
| 定长字符串 | CHAR[0-255]，定义长度默认按字符长度计算，最大保存255字符 | CHAR[1-2000]
定义默认按字节长度计算 |
| 无符号说明 | 支持，用于数值类型 | 不支持 |
| 大字符串，一般用于存储文本文件或超大描述及备注类信息 | TINYTEXT 最大支持255个字节
TEXT最大支持65535个字节
MEDIUMTEXT最大支持16MB个字节
LONGTEXT最大支持4GB字节

字段不支持默认值 | 支持(CLOB)
oracle10g以前最大支持4GB个字节
oracle10g开始最大支持4GB个数据块，数据块大小为2KB-32KB
oracle还有一个LONG类型，是早期的存储大字符串类型，最大支持2GB字节,现已不推荐使用 |
| 二进制对象，一般用于存储文件或图片数据 | TINYBLOB 最大支持255个字节
BLOB最大支持65535个字节
MEDIUMBLOB最大支持16MB个字节
LONGBLOB最大支持4GB字节

字段不支持默认值 | 支持(BLOB)
oracle10g以前最大支持4GB个字节

oracle10g开始最大支持4G个数据块，数据块大小为2KB-32KB
oracle还有一个LONG RAW类型，是早期的存储二进制类型，最大支持2GB字节,现已不推荐使用 |
| 二进制信息 | BINARY(0-255)，定长
VARBINARY(0-65535)，变长 | RAW(1-2000) |
| 枚举类型 | ENUM(v1,v2,v3,...),最多65535个元素 | 不支持 |
| 集合类型 | SET(v1,v2,v3,...)，最多64个元素 | 不支持 |
| 国际化字符集类型，较少使用 | 无，MYSQL可以对每个字段指定字符编码 | 支持
NCHAR(1-2000)
NVARCHAR(1-4000)
NCLOB |
| 外部文件指针类型 | 不支持 | 支持
文件大小最大4GB
文件名称最长255字符 |
| 
 | 不支持 | 支持 |
| 
 | 不支持 | 支持 |
| 自动增长类型 | 支持
使用简单 | 不支持
一般使用SEQUENCE解决，用法与自增类型差别较大，使用较复杂，但能实现非常灵活的应用，包括字符自增主键、全局主键等等 |
| 
 | 不支持函数和表达式
TEXT和BLOB字段类型不支持默认值 | 支持函数和表达式 |
| 
 | 支持，例如，把emp表的id字段顺序放在name字段后面：
alter table emp modify column id varchar(20) after name; | 不支持，只能重建表或字段 |
| 虚拟字段是一个逻辑字段定义，其结果值通常是一个表达式，并在表中存储物理值，不占用空间，主要用于简化查询逻辑。比如有一个商品销售表有单价和数量两个字段，那可以建一个虚拟字段金额，其表达式=单价*数量 | 不支持 | 11g支持，例：
create table sales
(
id       number,
quantity number,
price    number,
amount   GENERATED always as (quantity*price) virtual
); |
| 
 | INNODB 最大1000个字段
所有字段总定义长度不能超过65535字节
所有固定长度字段的总长度不超过半个数据块大小(数据块大小一般为16K) | 最大1000个字段 |

## 二、二种数据库常见数据类型对应关系
| 编号 | ORACLE | MYSQL | 注释 |
| --- | --- | --- | --- |
| 1 | NUMBER | int / DECIMAL | DECIMAL就是NUMBER(10,2)这样的结构INT就是是NUMBER(10)，表示整型；
MYSQL有很多类int型，tinyint mediumint bigint等，不同的int宽度不一样 |
| 2 | Varchar2（n） | varchar(n) |  |
| 3 | Date | DATATIME | 日期字段的处理
MYSQL日期字段分DATE和TIME两种，ORACLE日期字段只有DATE，包含年月日时分秒信息，用当前数据库的系统时间为 SYSDATE, 精确到秒，或者用字符串转换成日期型函数TO_DATE(‘2001-08-01','YYYY-MM-DD')年-月-日 24小时:分钟:秒的格式YYYY-MM-DD HH24:MI:SS TO_DATE()还有很多种日期格式, 可以参看ORACLE DOC.日期型字段转换成字符串函数TO_CHAR(‘2001-08-01','YYYY-MM-DD HH24:MI:SS')

日期字段的数学运算公式有很大的不同。MYSQL找到离当前时间7天用 DATE_FIELD_NAME ＞ SUBDATE（NOW（），INTERVAL 7 DAY）ORACLE找到离当前时间7天用 DATE_FIELD_NAME ＞SYSDATE - 7;

MYSQL中插入当前时间的几个函数是：NOW()函数以`'YYYY-MM-DD HH:MM:SS'返回当前的日期时间，可以直接存到DATETIME字段中。CURDATE()以'YYYY-MM-DD'的格式返回今天的日期，可以直接存到DATE字段中。CURTIME()以'HH:MM:SS'的格式返回当前的时间，可以直接存到TIME字段中。例：insert into tablename (fieldname) values (now())

而oracle中当前时间是sysdate |
| 4 | INTEGER | int / INTEGER | Mysql中INTEGER等价于int |
| 5 | EXCEPTION | SQLEXCEPTION  | 详见<<2009001-eService-O2MG.doc>>中2.5 Mysql异常处理 |
| 6 | CONSTANT VARCHAR2(1) | mysql中没有CONSTANT关键字 | 从ORACLE迁移到MYSQL,所有CONSTANT常量只能定义成变量 |
| 7 | TYPE g_grp_cur IS REF CURSOR; | 光标 : mysql中有替代方案 | 详见<<2009001-eService-O2MG.doc>>中2.2 光标处理 |
| 8 | TYPE unpacklist_type IS TABLE OF VARCHAR2(2000) INDEX BY BINARY_INTEGER; | 数组: mysql中借助临时表处理
或者直接写逻辑到相应的代码中，
直接对集合中每个值进行相应的处理 | 详见<<2009001-eService-O2MG.doc>>中2.4 数组处理 |
| 9 | 自动增长的序列 | 自动增长的数据类型 | MYSQL有自动增长的数据类型，插入记录时不用操作此字段，会自动获得数据值。ORACLE没有自动增长的数据类型，需要建立一个自动增长的序列号，插入记录时要把序列号的下一个值赋于此字段。 |
| 10 | NULL | NULL | 空字符的处理
MYSQL的非空字段也有空的内容，ORACLE里定义了非空字段就不容许有空的内容。按MYSQL的NOT NULL来定义ORACLE表结构, 导数据的时候会产生错误。因此导数据时要对空字符进行判断，如果为NULL或空字符，需要把它改成一个空格的字符串。 |

## 三、二种数据库差异比较之基本语法
| 编号 | 类别 | ORACLE | MYSQL | 注释 |
| --- | --- | --- | --- | --- |
| 1 | 变量的声明方式不同 | li_index NUMBER := 0 | DECLARE li_index INTEGER DEFAULT 0 | 1. mysql 使用DECLARE定义局部变量. 
定义变量语法为:  DECLARE var_name[,...] type [DEFAULT value] 要给变量提供一个默认值，需要包含一个DEFAULT子句。值可以被指定为一个表达式，不需要为一个常数。如果没有DEFAULT子句，初始值为NULL。    |
| 2 | 变量的赋值方式不同 | lv_inputstr := iv_inputstr | SET lv_inputstr = iv_inputstr | 1. oracle变量赋值使用:=  
mysql 使用赋值使用set关键字. 将一个值赋给一个变量时使用"=".  |
| 3 | 跳出（退出）语句不同 | EXIT; | LEAVE procedure name; | 1. oracle: 如果exit语句在循环中就退出当前循环.如果exit语句不再循环中,就退出当前过程或方法. 
Mysql: 如果leave语句后面跟的是存储过程名,则退出当前存储过程. 如果leave语句后面跟的是lable名. 则退出当前lable. 

 |
|  |  | while 条件 loop
exit;
end loop; | label_name:while 条件 do
leave label_name;
end while label_name; |  |
| 4 | 定义游标 | TYPE g_grp_cur IS REF CURSOR;

 | DECLARE cursor_name CURSOR FOR SELECT_statement; | oracle可以先定义游标,然后给游标赋值. 
mysql定义游标时就需要给游标赋值. Mysql定义游标出自 Mysql 5.1 参考手册20.2.11.1.声明光标. |
| 5 | 定义数组 | TYPE unpacklist_type IS TABLE OF VARCHAR2(2000) INDEX BY BINARY_INTEGER; | 可以使用临时表代替oracle数组, 也可以循环拆分字符来替代oracle数组. | 目前可以使用临时表来代替oracle数组. 
详见<<2009002-OTMPPS-Difficult Questions-0001.doc>>中2.4 Mysql数组处理部分 |
| 6 | 注释方式不同 |  "-- message"  或 "/** ….  */" 或"/* ….  */" | "-- message"  或 "/* ….  */" 或 "#" | mysql注释来自  MySQL 5.1参考手册 9.5. 注释语法, 建议同oracle一样, 单行用--, 多行/* */ |
| 7 | 自带日期时间函数格式不同 | Oracle时间格式：yyyy-MM-dd hh:mi:ss | Mysql时间格式：%Y-%m-%d %H:%i:%s | 1. MYSQL日期字段分DATE和TIME两种. 
ORACLE日期字段只有DATE，包含年月日时分秒信息. 
2. mysql中取当前系统时间为now()函数,精确到秒. 
oracle中取当前数据库的系统时间为SYSDATE, 精确到秒. |
| 8 | 日期加减 | 当前时间加N天: sysdate+N
当前时间减N天: sysdate-N | 日期相加: date_add(now(), INTERVAL 180 DAY)
日期相减: date_sub('1998-01-01 00:00:00', interval '1 1:1:1' day_second) |  |
| 9 | 字符串连接符不同 | result  := v_int1&#124;&#124;v_int2; | set result =concat(v_int1,v_int2); | 
1. oracle使用&#124;&#124;连接字符串,也可以使用concat函数. 但Oracle的concat函数只能连接两个字符串.
Mysql使用concat方法连接字符串. MySQL的concat函数可以连接一个或者多个字符串,如
mysql> select concat('10');   结果为: 10.
mysql> select concat('11','22','33','aa'); 结果为: 112233aa
2. "&#124;&#124;"在Mysql是与运算 |
| 10 | 定义游标不同 | CURSOR l_bk_cur IS
SELECT B.BK_HDR_INT_KEY, B.BK_NUM
FROM ES_SR_DTL_VRB A, ES_BK_HDR B
WHERE A.BK_HDR_INT_KEY = B.BK_HDR_INT_KEY
AND b.BK_STATUS != ES_BK_PKG.g_status_can
AND A.SR_HDR_INT_KEY = ii_sr_hdr_int_key; | DECLARE l_bk_cur CURSOR
FOR SELECT B.BK_HDR_INT_KEY, B.BK_NUM
FROM ES_SR_DTL_VRB A, ES_BK_HDR B
WHERE A.BK_HDR_INT_KEY = B.BK_HDR_INT_KEY
AND b.BK_STATUS != ES_BK_PKG.g_status_can
AND A.SR_HDR_INT_KEY = ii_sr_hdr_int_key;

 | 详见<<2009002-OTMPPS-Difficult Questions-0001.doc>>中2.2 Mysql游标处理部分 |
| 11 | 事务回滚 | ROLLBACK; | ROLLBACK; | oracle和mysql中使用方法相同 |
| 12 | GOTO语句 | GOTO check_date; | GOTO check_date; | oracle和mysql中使用方法相同 |

以上就是MySQL与Oracle数据类型对应关系的全部内容了
