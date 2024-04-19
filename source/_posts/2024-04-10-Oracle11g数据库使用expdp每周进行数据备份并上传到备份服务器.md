---
title: Oracle11g数据库使用expdp每周进行数据备份并上传到备份服务器
tag:
  - oracle
categories:
  - [linux,oracle]
article_type: 0
no_word_count: false
no_toc: false
no_date: false
no_declare: false
no_reward: false
no_comments: false
no_share: false
no_footer: false
mathjax: false
typora-root-url: ./..
abbrlink: fc083848
date: 2024-04-10 10:47:01
top:
---

## 1.看看数据库情况

### 1.1先看了下表空间情况，生产环境表空间大概90G，用了才一半不到

​	查看所有表空间及使用情况

```
SELECT
　　B.FILE_NAME 物理文件名,
　　B.TABLESPACE_NAME 表空间名称,
　　B.BYTES/1024/1024 大小M,
　　(B.BYTES-SUM(NVL(A.BYTES,0)))/1024/1024 已使用M,
　　SUBSTR((B.BYTES-SUM(NVL(A.BYTES,0)))/(B.BYTES)*100,1,5) 使用率
FROM DBA_FREE_SPACE A,DBA_DATA_FILES B
WHERE A.FILE_ID=B.FILE_ID
GROUP BY B.TABLESPACE_NAME,B.FILE_NAME,B.BYTES
ORDER BY B.TABLESPACE_NAME;
```

![](/imgs/2022062810410290.jpg)

## 2.数据库备份

### 2.1登陆数据库

```
[root@]$ sqlplus / as sysdba
```
<!--more-->


### 2.2创建逻辑目录

执行这个操作并不会在Linux中创建/opt/data\_backup这个文件，最后需要手动去创建该文件才能进行备份。

```
SQL> create directory back_dir as '/opt/backup'
SQL> select * from dba_directories; #查看所有逻辑目录,看是否创建成功
```



### 2.3给数据库用户文件操作权限#dbuser为数据库用户名，更具实际情况更改

```
Grant read,write on directory back_dir to dbuser;
```



### 2.3创建物理目录

```
[root@]$ mkdir -p /opt/backup #-p 确保目录名称存在，不存在的就建一个，可使用参数创建多级目录
```



### 2.4备份数据库

```
[root@]$ expdp dbuser/passwd@192.168.110.9:1521/orcl dumpfile=dbback.dmp log=log.log directory=back_dir schemas=cbyxy
```

exedp有很多参数，这里是用到的一些解释  
dbuser/passwd@192.168.110.9:1521/orcl #导出用户名/密码@数据库IP/数据库SID  
dumpfile=导出的文件名.dmp  
log=导出过程的日志名.log  
directory=备份放的路径名,用的之前的逻辑目录名  
schemas=要备份的数据库用户名字  
FULL=y #加上意思为导出整个数据库就不需要schemas参数了  
也可以按表空间导出TABLESPACES=  
表名导出TABLES=  
等等还有很多参数自行了解

## 3.shell脚本实现自动备份

```
#!/bin/bash
#导入环境变量，根据具自己实际情况填写
export ORACLE_BASE=/home/oracle/app
export ORACLE_HOME=$ORACLE_BASE/oracle/product/11.2.0/dbhome_1
export PATH=$ORACLE_HOME/bin:$PATH
export LOCAL_IP=192.168.110.183:1521
export BACKUP_USER_IP_DIR=root@192.168.110.187:/opt/   #备份服务器的用户，ip，保存地址
export ORACLE_USER_NAME=system #数据库的用户密码根据实际情况填写，备份整个库最好使用system或sys管理员用户
export ORACLE_USER_PASSWD=Abc123556..
export ORACLE_SID=orcl #不知道可以使用Oracle用户执行echo $ORACLE_SID，或者SQL> SELECT instance_name FROM v$instance
export DATA_DIR=/opt/backup   #与数据库中的逻辑地址相同,用来储存备份文件
export DELTIME=`date -d "7 days ago" +%Y%m%d` # -d "7 days ago" 为获取七天前的日期,以日期命名方便任务自动删>除
export BAKUPTIME=`date +%Y%m%d` #备份日期年月日
export NLS_LANG=AMERICAN_AMERICA.ZHS16GBK #定义语言地域和字符集属性的环境变量，根据自己数据库情况修改
mkdir -p $DATA_DIR
echo "Starting bakup..."
echo "Backup file path $DATA_DIR/$BAKUPTIME.dmp"
expdp $ORACLE_USER_NAME/$ORACLE_USER_PASSWD@$LOCAL_IP/$ORACLE_SID dumpfile=$BAKUPTIME.dmp log=$BAKUPTIME.log directory=expdp full=y
echo "backup file success..."
tar -zcvPf $DATA_DIR/$BAKUPTIME.tar.gz $DATA_DIR/$BAKUPTIME.dmp --remove-files ##-P：指定绝对路径 --remove-files :打包后删除原文件
echo "tar the file backup successfully"
echo "scp to":$BACKUP_IP
scp $DATA_DIR/$BAKUPTIME.tar.gz $BACKUP_USER_IP_DIR #远程服务器防火墙有限制scp端口需要加：-P 端口号
rm -f $DATA_DIR/$DELTIME.log #删除之前的备份
echo "Bakup completed."
```

![](/imgs/2022062810410391.png)

## 4.添加定时任务

```
[root@ ]$ crontab -e
```

添加行：

\* 1 \* \* 6 /opt/back.sh #每个星期的星期六早上执行备份任务

0 0 1 * * /opt/back.sh #每个月的1号凌晨12点执行备份任务

```
*    *    *    *    *
-    -    -    -    -
|    |    |    |    |
|    |    |    |    +----- 星期中星期几 (0 - 6) (星期天 为0)
|    |    |    +---------- 月份 (1 - 12) 
|    |    +--------------- 一个月中的第几天 (1 - 31)
|    +-------------------- 小时 (0 - 23)
+------------------------- 分钟 (0 - 59)
```



## 5.参考文章

[https://www.cnblogs.com/xwdreamer/p/3511047.html](https://www.cnblogs.com/xwdreamer/p/3511047.html)  
[https://www.cnblogs.com/farmer-y/p/5888432.html](https://www.cnblogs.com/farmer-y/p/5888432.html)  
[https://blog.csdn.net/weixin\_41607523/article/details/110817646](https://blog.csdn.net/weixin_41607523/article/details/110817646)  
[https://blog.csdn.net/XUEYUTIANQI/article/details/113976558](https://blog.csdn.net/XUEYUTIANQI/article/details/113976558)

