
    layout: post
    title: canal+mysql+zookeeper+rocketmq
    tags:
    - 语雀
    categories:
    - [语雀,我的知识库]
    abbrlink: 
    date: 2024-05-22 17:28:46
    
实现监控数据库更新记录监控，配合rocketmq完成消息队列存量数据推送
### 安装配置MySQL
新建数据库和表用于业务模拟，这里不介绍安装步骤了，如未安装过MySQL，自行查阅MySQL详细的安装步骤；
安装完MySQL后，做基本的设置配置
```bash
# 登录mysql
root@ops04:/root #mysql -uroot -p123456
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
<!--more-->
Your MySQL connection id is 442523
Server version: 5.7.29 MySQL Community Server (GPL)

Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
# 增加canal用户并配置权限
mysql> GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'canal'@'%' IDENTIFIED BY 'canal';
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> quit;
Bye
# 修改MySQL配置文件，增添binlog相关配置项
root@ops04:/root #vim /etc/my.cnf
[mysqld]
#skip-grant-tables
#binlog
server-id=1
log-bin=mysql-bin
binlog_format=row
binlog-do-db=gmall
```
新建一个gmall库，库其实都可以，只要和上方配置文件中对应即可
重启MySQL：
```bash
root@ops04:/root #mysql -V
mysql  Ver 14.14 Distrib 5.7.29, for Linux (x86_64) using  EditLine wrapper
root@ops04:/root #systemctl status mysqld
● mysqld.service - MySQL Server
   Loaded: loaded (/usr/lib/systemd/system/mysqld.service; enabled; vendor preset: disabled)
   Active: active (running) since Wed 2021-05-26 09:30:25 CST; 2 months 22 days ago
     Docs: man:mysqld(8)
           http://dev.mysql.com/doc/refman/en/using-systemd.html
 Main PID: 32911 (mysqld)
   Memory: 530.6M
   CGroup: /system.slice/mysqld.service
           └─32911 /usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld.pid

May 26 09:30:18 ops04 systemd[1]: Starting MySQL Server...
May 26 09:30:25 ops04 systemd[1]: Started MySQL Server.
root@ops04:/root #
root@ops04:/root #systemctl restart mysqld
root@ops04:/root #
```
【注意】：在新增了binlog配置后，重启MySQL服务后，在**存储目录(位置可能不一样)**下会有相关的binlog文件，格式如下
```bash
root@ops04:/var/lib/mysql #ll | grep mysql-bin
-rw-r----- 1 mysql mysql     1741 Aug 17 14:27 mysql-bin.000001
-rw-r----- 1 mysql mysql       19 Aug 17 11:18 mysql-bin.index
```
验证canal用户登录：
```bash
root@ops04:/root #mysql -ucanal -pcanal -e "show databases"
mysql: [Warning] Using a password on the command line interface can be insecure.
+--------------------+
| Database           |
+--------------------+
| information_schema |
| gmall              |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
root@ops04:/root #

```
在gmall库中新建表，并插入一些样例数据做测试：
```bash
CREATE TABLE `canal_test` (
  `体温` varchar(255) DEFAULT NULL,
  `身高` varchar(255) DEFAULT NULL,
  `体重` varchar(255) DEFAULT NULL,
  `文章` varchar(255) DEFAULT NULL,
  `日期` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `canal_test`(`体温`, `身高`, `体重`, `文章`, `日期`) VALUES ('36.5', '1.70', '180', '4', '2021-06-01');
INSERT INTO `canal_test`(`体温`, `身高`, `体重`, `文章`, `日期`) VALUES ('36.4', '1.70', '160', '8', '2021-06-02');
INSERT INTO `canal_test`(`体温`, `身高`, `体重`, `文章`, `日期`) VALUES ('36.1', '1.90', '134', '1', '2021-06-03');
INSERT INTO `canal_test`(`体温`, `身高`, `体重`, `文章`, `日期`) VALUES ('37.3', '1.70', '110', '14', '2021-06-04');
INSERT INTO `canal_test`(`体温`, `身高`, `体重`, `文章`, `日期`) VALUES ('35.7', '1.70', '133', '0', '2021-06-05');
INSERT INTO `canal_test`(`体温`, `身高`, `体重`, `文章`, `日期`) VALUES ('36.8', '1.90', '200', '6', '2021-06-06');
INSERT INTO `canal_test`(`体温`, `身高`, `体重`, `文章`, `日期`) VALUES ('37.5', '1.70', '132', '25', '2021-06-07');
INSERT INTO `canal_test`(`体温`, `身高`, `体重`, `文章`, `日期`) VALUES ('35.7', '1.70', '160', '2', '2021-06-08');
INSERT INTO `canal_test`(`体温`, `身高`, `体重`, `文章`, `日期`) VALUES ('36.3', '1.80', '131.4', '9', '2021-06-09');
INSERT INTO `canal_test`(`体温`, `身高`, `体重`, `文章`, `日期`) VALUES ('37.3', '1.70', '98.8', '4', '2021-06-10');

```
### 安装rocketmq+ zookeeper
查询rocketmq和zookeeper各端口集群运行状态：
```bash
wangting@ops03:/opt/module >ssh ops01 'sudo netstat -tnlpu| grep -E "9876|2181"'
tcp6       0      0 :::9876                 :::*                    LISTEN      42305/java          
tcp6       0      0 :::2181                 :::*                    LISTEN      41773/java          

```
## 安装部署canal
阿里的canal项目地址为：https://github.com/alibaba/canal，下载链接可以在github页面点击右边的release查看各版本下载，建议有精力可以多查阅阿里首页的热门项目，有很多项目越来越受欢迎。
### 下载安装包
```bash
# 下载安装包
wangting@ops03:/opt/software >wget https://github.com/alibaba/canal/releases/download/canal-1.1.5/canal.deployer-1.1.5.tar.gz
wangting@ops03:/opt/software >ll | grep canal
-rw-r--r-- 1 wangting wangting  60205298 Aug 17 11:23 canal.deployer-1.1.5.tar.gz

```
### 解压安装
```bash
# 新建canal解压目录【注意】: 官方项目解压出来没有顶级canal目录，所以新建个目录用于解压组件
wangting@ops03:/opt/software >mkdir -p /usr/local/
wangting@ops03:/opt/software >tar -xf canal.deployer-1.1.5.tar.gz -C /usr/local/

```
### 修改canal主配置
```bash
# 修改canal主配置文件
wangting@ops03:/usr/local/canal/ >cd conf/
wangting@ops03:/usr/local//canal/conf >ll
total 28
-rwxrwxr-x 1 wangting wangting  319 Apr 19 15:48 canal_local.properties
-rwxrwxr-x 1 wangting wangting 6277 Apr 19 15:48 canal.properties
drwxrwxr-x 2 wangting wangting 4096 Aug 17 13:49 example
-rwxrwxr-x 1 wangting wangting 3437 Apr 19 15:48 logback.xml
drwxrwxr-x 2 wangting wangting 4096 Aug 17 13:49 metrics
drwxrwxr-x 3 wangting wangting 4096 Aug 17 13:49 spring
# 改动如下相关配置： zk | 同步策略目标方式 | kafka
wangting@ops03:/usr/local/canal/conf >vim canal.properties 
canal.ip = 192.168.132.128
canal.zkServers = 192.168.132.128:2181
canal.serverMode = rocketMQ
#canal.mq.servers = 191.168.132.128:9876;192.168.132.129:9876
canal.mq.servers = 192.168.132.129:9876;192.168.132.128:9876
```
### 修改canal的实例配置- (mysql to rocketmq)
```bash
# 配置实例相关配置：canal可以启多实例，一个实例对应一个目录配置，例如把example目录复制成xxx，把xxx目录下的配置改动启动，就是一个新实例
wangting@ops03:/opt/module/canal/conf >cd example/
wangting@ops03:/opt/module/canal/conf/example >ll
total 4
-rwxrwxr-x 1 wangting wangting 2106 Apr 19 15:48 instance.properties
# 注意11.8.38.86:3306需要改成自己环境的mysql地址和端口，其次用户名密码改成自己环境的，topic自定义一个
wangting@ops03:/opt/module/canal/conf/example >vim instance.properties 
canal.instance.master.address=192.168.132.128:3306
canal.instance.dbUsername=canal
canal.instance.dbPassword=canal
canal.mq.topic=test_canal
canal.mq.partitionsNum=3
```
### 启动canal
```bash
./startup.sh
```
### 验证结果
```bash
# 插入数据时，有数据监控
tail -fn 500 logs/example/meta.log 
# 运行正常时，不报错
tail -fn 500 logs/example/example.log 
  2022-06-17 19:55:39.993 [destination = example , address = /192.168.132.128:3306 , EventParser] WARN  c.a.o.c.p.inbound.mysql.rds.RdsBinlogEventParserProxy - ---> find start position successfully, EntryPosition[included=false,journalName=mysql-bin.000002,position=812555,serverId=1,gtid=,timestamp=1655466709000] cost : 508ms , the next step is binlog dump

# 显示正常running
tail -fn 500 logs/canal/canal.log 
  2022-06-17 19:55:37.666 [main] INFO  com.alibaba.otter.canal.deployer.CanalController 	- ## start the canal server[192.168.132.128(192.168.132.128):11111]
  2022-06-17 19:55:39.299 [main] INFO  com.alibaba.otter.canal.deployer.CanalStarter - ## the canal server is running now ......
^C

```
按照预期，如果现在成功的监测了ops04上MySQL中gmall库，那么在gmall库中的表如有数据改动，那么控制台会有信息输出实时同步更新到前台
当前表内数据：
![image.png](https://cdn.nlark.com/yuque/0/2022/png/12484160/1655467974439-54078d81-6f6a-4dee-850b-095715fe0c8c.png#clientId=u0cc1c07e-8fc4-4&from=paste&id=u3ea9bbc2&originHeight=446&originWidth=627&originalType=url&ratio=1&rotation=0&showTitle=false&size=40140&status=done&style=none&taskId=ue224fa51-df6f-4d47-9d2b-25f58f33f8f&title=)
改动表中的数据观察控制台输出：
![image.png](https://cdn.nlark.com/yuque/0/2022/png/12484160/1655467974387-693bf4d4-3ca3-4107-9d3f-a2566e5ca31d.png#clientId=u0cc1c07e-8fc4-4&from=paste&id=u4c33370d&originHeight=376&originWidth=518&originalType=url&ratio=1&rotation=0&showTitle=false&size=33367&status=done&style=none&taskId=u79bcd2e3-d9e7-48b5-b66a-1cefae6b7a6&title=)
