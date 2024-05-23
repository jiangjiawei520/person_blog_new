---
ayout: post
title: MySQL Create Table .... Select ...
tags:
  - 语雀
categories:
  - - 语雀
    - 我的知识库
abbrlink: fe00b06a
password: Grbk@2024
date: 2024-05-23 16:24:15
---

改为分两步执行即可，第一步建表，第二步插数据：
 create table xxxx like xxxx
insert into xxxx select *from xxxx
