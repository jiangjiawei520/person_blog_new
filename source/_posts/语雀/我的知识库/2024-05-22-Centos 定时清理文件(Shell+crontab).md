
    layout: post
    title: Centos 定时清理文件(Shell+crontab)
    tags:
    - 语雀
    categories:
    - [语雀,我的知识库]
    abbrlink: 
    date: 2024-05-22 17:28:46
    
## 需求
最近有个需求，就是rsync每次同步的数据量很多，但是需要保留的数据库bak文件
保留7天就够了，所以需要自动清理文件夹内的bak文件



find /usr/local/tomcat/data-integration/logs/1/  -name "*.txt"  -exec rm -rf {} \;
## 解决方案
利用shell脚本来定期删除文件夹内的任务
<!--more-->
## 1、创建shell文件
```bash
[root@zabbix script]# vim backup_sql_clean.sh 
#!/bin/sh 
find /data1/backup/KDKDA\$AGKDPAYKT/XNAKSD/FXUIJ -mtime +10 -name "*.bak" -exec rm -rf {} \;
```
**参数说明：**
/data1/backup/KDKDA\$AGKDPAYKT/XNAKSD/FXUIJ  #这个是文件的路径path
-mtime +10 #这个是保留的天数，10就是10天
-name "*.bak"  #这个是要删除文件的名称，这边加后缀就是删除这个类型的文件
其他的是Linux的命令

## 2、设置shell文件权限
```bash
[root@zabbix script]# chown 777 backup_sql_clean.sh
```

### 3、设置crontab周期执行
crontab命令用于设置周期性被执行的指令
crontab相关命令说明：[https://www.cnblogs.com/Sungeek/p/9561833.html](https://www.cnblogs.com/Sungeek/p/9561833.html)
```bash
[root@zabbix /]# crontab -e 0 0 * * 7 /data/script/backup_sql_clean.sh
```

## 4、启动crond进程
crond的概念和crontab是不可分割的。crontab是一个命令，常见于Unix和类Unix的操作系统之中，用于设置周期性被执行的指令。
该命令从标准输入设备读取指令，并将其存放于“crontab”文件中，以供之后读取和执行。而crond正是它的守护进程。
```bash
[root@zabbix /]# systemctl status crond.service #查看crond状态
[root@zabbix /]# systemctl start crond.service #启动crond服务
[root@zabbix /]# systemctl restart crond.service #重启crond服务
```
