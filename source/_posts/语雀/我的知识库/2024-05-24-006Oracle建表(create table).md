---
layout: post
title: 006Oracle建表(create table)
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "Grbk@2024"
typora-root-url: ./..
date: 2024-05-24 10:45:56
---
# Oracle建表(create** table)**
Oracle表是Oracle数据库的核心，是存储数据的逻辑基础。Oracle表是一个二维的数据结构，有列字段和对应列的数据构成一个数据存储的结构。可以简单看成行和列的二维表，列代表着Oracle字段（column），行代表着一行数据（即一条数据记录）。

## Oracle字段数据类型
常用的Oracle列字段的数据类型如下：

| **数据类型
<!--more-->

** | **类型解释

** |
| --- | --- |
| VARCHAR2(length)

 | 字符串类型：存储可变的长度的字符串，length:是字符串的最大长度，默认不填的时候是1，最大长度不超过4000。

 |
| CHAR(length)

 | 字符串类型：存储固定长度的字符串，length:字符串的固定长度大小，默认是1，最大长度不超过2000。

 |
| NUMBER(a,b)

 | 数值类型：存储数值类型，可以存整数，也可以存浮点型。a代表数值的最大位数：包含小数位和小数点，b代表小数的位数。例子：
number(6,2)，输入123.12345，实际存入：123.12 。
number(4,2)，输入12312.345，实际春如：提示不能存入，超过存储的指定的精度。

 |
| DATA

 | 时间类型：存储的是日期和时间，包括年、月、日、时、分、秒。例子：
内置函数sysdate获取的就是DATA类型

 |
| TIMESTAMP

 | 时间类型：存储的不仅是日期和时间，还包含了时区。例子：
内置函数systimestamp获取的就是timestamp类型

 |
| CLOB

 | 大字段类型：存储的是大的文本，比如：非结构化的txt文本，字段大于4000长度的字符串。

 |
| BLOB

 | 二进制类型：存储的是二进制对象，比如图片、视频、声音等转换过来的二进制对象

 |

## **create table语句**
Oracle数据库建表是通过create table命令来执行的，通过[Oracle用户](http://www.oraclejsq.com/article/010100133.html)这一章节我们创建了一个Student用户，现在我们可以在student用户下创建一个stuinfo(学生信息表)来讲解create table 命令的使用。

案例1：创建stuinfo（学生信息表）
```plsql
-- Create table
create table STUDENT.stuinfo
(
  stuid      varchar2(11) not null,--学号：'S'+班号（7位数）+学生序号（3位数）(1)
  stuname    varchar2(50) not null,--学生姓名
  sex        char(1) not null,--性别
  age        number(2) not null,--年龄
  classno    varchar2(7) not null,--班号：'C'+年级（4位数）+班级序号（2位数）
  stuaddress varchar2(100) default '地址未录入',--地址 (2)
  grade      char(4) not null,--年级
  enroldate  date,--入学时间
  idnumber   varchar2(18) default '身份证未采集' not null--身份证
)
tablespace USERS --(3)
  storage
  (
    initial 64K
    minextents 1
    maxextents unlimited
  );
-- Add comments to the table 
comment on table STUDENT.stuinfo --(4)
  is '学生信息表';
-- Add comments to the columns 
comment on column STUDENT.stuinfo.stuid -- (5)
  is '学号';
comment on column STUDENT.stuinfo.stuname
  is '学生姓名';
comment on column STUDENT.stuinfo.sex
  is '学生性别';
comment on column STUDENT.stuinfo.age
  is '学生年龄';
comment on column STUDENT.stuinfo.classno
  is '学生班级号';
comment on column STUDENT.stuinfo.stuaddress
  is '学生住址';
comment on column STUDENT.stuinfo.grade
  is '年级';
comment on column STUDENT.stuinfo.enroldate
  is '入学时间';
comment on column STUDENT.stuinfo.idnumber
  is '身份证号';
```
代码解析：
（1）处： not null 表示学号字段（stuid）不能为空。
（2）处：default 表示字段stuaddress不填时候会默认填入‘地址未录入’值。
（3）处：表示表stuinfo存储的表空间是users，storage表示存储参数：区段(extent)一次扩展64k，最小区段数为1，最大的区段数不限制。
（4）处：comment on table 是给表名进行注释。
（5）处：comment on column 是给表字段进行注释。

通过上面crate table命令创建了stuinfo学生信息表后，还可以给表添加相应的约束来保证表数据的准确性。比如：学生的年龄不能存在大龄的岁数，可能是错误数据、性别不能填入不是1（男）、2（女）之外的数据等。

案例2：stuinfo（学生信息表）添加约束
```plsql
-- Create/Recreate primary, unique and foreign key constraints 
alter table STUDENT.STUINFO
  add constraint pk_stuinfo_stuid primary key (STUID);
  --把stuid当做主键，主键字段的数据必须是唯一性的（学号是唯一的）
  
-- Create/Recreate check constraints 
alter table STUDENT.STUINFO
  add constraint ch_stuinfo_age
  check (age>0 and age<=50);--给字段年龄age添加约束，学生的年龄只能0-50岁之内的
  
alter table STUDENT.STUINFO
  add constraint ch_stuinfo_sex
  check (sex='1' or sex='2');
  
alter table STUDENT.STUINFO
  add constraint ch_stuinfo_GRADE
  check (grade>='1900' and grade<='2999');
```
