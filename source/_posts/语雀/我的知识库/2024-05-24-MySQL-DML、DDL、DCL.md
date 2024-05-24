---
layout: post
title: MySQL-DML、DDL、DCL
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "Grbk@2024"
typora-root-url: ./..
date: 2024-05-24 10:45:56
---
### DDL（Data Definition Languages）语句：
数据定义语言，这些语句定义了不同的数据段、数据库、表、列、索引等数据库对象的定义。 常用的语句关键字主要包括 create、drop、alter 等，**更多的被数据库管理员（DBA）所使用，一般的开发人员很少使用。** 具体命令有：

- CREATE TABLE：创建数据库表
- ALTER TABLE：更改表结构、添加、删除、修改列长度
- DROP TABLE：删除表
- CREATE INDEX：在表上建立索引
<!--more-->
- DROP INDEX：删除索引


### DML（Data Manipulation Language）语句：
数据操纵语句，用于添加、删除、更新和查询数据库记录，并检查数据完整性， 常用的语句关键字主要包括 insert、delete、udpate 和 select 等。(增添改查），**开发人员日常使用最频繁的操作**。 具体命令有：

- INSERT：添加数据到数据库中
- DELETE：删除数据库中的数据
- UPDATE：修改数据库中的数据
- SELECT：选择（查询）数据


### DCL（Data Control Language）语句：
数据控制语句，用于控制不同数据段直接的许可和访问级别的语句。这些语句定义了数据库、表、字段、用户的访问权限和安全级别，用来控制数据库的访问， **一般也是 DBA 使用**。 具体命令有：

- GRANT：授予访问权限
- REVOKE：撤销访问权限
- COMMIT：提交事务处理
- ROLLBACK：事务处理回退


## 总结：

- DDL：一句话解释：增删改查表信息
- DML：一句话解释：增删改查表数据
- DCL：一句话解释：控制表和库权限
