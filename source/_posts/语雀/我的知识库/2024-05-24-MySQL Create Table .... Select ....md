---
layout: post
title: MySQL Create Table .... Select ...
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "Grbk@2024"
typora-root-url: ./..
date: 2024-05-24 10:45:56
---

改为分两步执行即可，第一步建表，第二步插数据：
 create table xxxx like xxxx
insert into xxxx select *from xxxx
