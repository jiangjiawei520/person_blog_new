---
layout: post
title: 查看centos的CPU、内存、磁盘空间
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "Grbk@2024"
typora-root-url: ./..
date: 2024-05-23 18:36:32
---
```plsql
查看物理CPU个数
cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l

查看内存占用
free -h

<!--more-->
查看磁盘使用详情
df -h

centos版本信息
cat /etc/redhat-release
uname -a

mysql版本查询
/usr/local/mysql/bin/mysql --version
```
