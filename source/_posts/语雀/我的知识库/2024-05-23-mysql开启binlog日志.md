---
layout: post
title: mysql开启binlog日志
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "Grbk@2024"
typora-root-url: ./..
date: 2024-05-23 18:36:32
---
## 介绍
binlog是二进制日志文件，Mysql的binlog日志作用是用来记录mysql内部增删改查等对mysql数据库有更新的内容的记录（对数据库的改动），对数据库的查询select或show等不会被binlog日志记录;主要用于数据库的主从复制以及增量恢复。
mysql的binlog日志必须打开log-bin功能才能生存binlog日志
> -rw-rw---- 1 mysql mysql   669 8月  10 21:29 mysql-bin.000001
> -rw-rw---- 1 mysql mysql   126 8月  10 22:06 mysql-bin.000002
> -rw-rw---- 1 mysql mysql 11799 8月  15 18:17 mysql-bin.000003

<!--more-->
## 1、登录mysql之后使用下面的命令查看是否开启binlog
show variables like 'log_%';
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1640573777339-661bed4b-0a3b-48f2-8375-b350cfe546c1.png#clientId=uc5408318-c919-4&from=paste&id=ue8a65a7c&originHeight=432&originWidth=669&originalType=url&ratio=1&size=25037&status=done&style=none&taskId=u1d971cb7-461f-42f5-837b-4271bc15399)
## 2、编辑配置文件
vi /etc/my.cnf
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1640573823223-5e3e15e2-cc03-4060-91df-a8a647394925.png#clientId=uc5408318-c919-4&from=paste&id=ubeb6cd45&originHeight=49&originWidth=312&originalType=url&ratio=1&size=2095&status=done&style=none&taskId=uaa8f72a5-eafc-45c9-bcfa-1ee45a090f7)
## 3、打开MySQL的log-bin功能
> #单个结点的id
> server_id=2
> #指定binlog日志文件的名字为mysql-bin，以及其存储路径
> log_bin = /var/lib/mysql/mysql-bin
> #binlog模式
> binlog_format = ROW
> expire_logs_days = 30

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1640573929053-60fe0861-a9e0-4918-82de-c30d8adb14b9.png#clientId=uc5408318-c919-4&from=paste&id=udf5f3bfe&originHeight=394&originWidth=723&originalType=url&ratio=1&size=27426&status=done&style=none&taskId=ufd95750b-332a-4639-88f1-d82ae018a4c)
## 4、重启mysql服务
systemctl restart mysqld
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1640573929016-8a7551f7-381c-4b0c-9647-6957a78e6008.png#clientId=uc5408318-c919-4&from=paste&id=ube5a4d20&originHeight=50&originWidth=406&originalType=url&ratio=1&size=2485&status=done&style=none&taskId=u6fe675a1-ac1b-489f-a458-54e122bf5d6)
## 5、再次查看binlog开启状态
再次使用命令show variables like 'log_%';进行查看，为ON表明binlog开启
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1640573929060-b7ac5fbe-abe1-4e5a-b2d8-b531e08a2522.png#clientId=uc5408318-c919-4&from=paste&id=u5552d9ad&originHeight=451&originWidth=719&originalType=url&ratio=1&size=27523&status=done&style=none&taskId=ua0843e60-33bf-4cf5-9114-5d13599fec7)
## 6、日志
在该路径下会生成mysql-bin.000001 mysql-bin.000002这样的文件
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1640573929077-36c82e30-595b-47fb-bf36-c72ec0c5316d.png#clientId=uc5408318-c919-4&from=paste&id=u051fe7a7&originHeight=305&originWidth=739&originalType=url&ratio=1&size=30712&status=done&style=none&taskId=uf6fa7a4d-446f-4609-b589-a4c7613b9d9)
## 补充
### Mysqlbinlog解析工具
 Mysqlbinlog功能是将Mysql的binlog日志转换成Mysql语句，默认情况下binlog日志是二进制文件，无法直接查看。
 Mysqlbinlog参数

| 参数 | 描述 |
| --- | --- |
| -d | 指定库的binlog |
| -r | 相当于重定向到指定文件 |
| --start-position--stop-position | 按照指定位置精确解析binlog日志（精确），如不接--stop-positiion则一直到binlog日志结尾 |
| --start-datetime--stop-datetime | 按照指定时间解析binlog日志（模糊，不准确），如不接--stop-datetime则一直到binlog日志结尾 |

备注：myslqlbinlog分库导出binlog，如使用-d参数，更新数据时必须使用use database。
例：解析ceshi数据库的binlog日志并写入my.sql文件
> #mysqlbinlog -d ceshi mysql-bin.000003 -r my.sql

Row模式下解析binlog日志
> #mysqlbinlog --base64-output="decode-rows" -v mysql-bin.000001

使用位置精确解析binlog日志
> #mysqlbinlog mysql-bin.000003 --start-position=100  --stop-position=200 -r my.sql

### MySQL binlog的三种工作模式
 **（1）Row level**
 日志中会记录每一行数据被修改的情况，然后在slave端对相同的数据进行修改。
 优点：能清楚的记录每一行数据修改的细节
 缺点：数据量太大
 **（2）Statement level（默认）**
 每一条被修改数据的sql都会记录到master的bin-log中，slave在复制的时候sql进程会解析成和原来master端执行过的相同的sql再次执行
 优点：解决了 Row level下的缺点，不需要记录每一行的数据变化，减少bin-log日志量，节约磁盘IO，提高新能
 缺点：容易出现主从复制不一致
** （3）Mixed（混合模式）**
 	结合了Row level和Statement level的优点
### MySQL企业binlog模式的选择

1. 互联网公司使用MySQL的功能较少（不用存储过程、触发器、函数），选择默认的Statement level
2. 用到MySQL的特殊功能（存储过程、触发器、函数）则选择Mixed模式
3. 用到MySQL的特殊功能（存储过程、触发器、函数），又希望数据最大化一直则选择Row模式
