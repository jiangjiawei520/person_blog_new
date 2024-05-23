---
layout: post
title: oracle知识体系（centos下安装）
tags:
- 语雀
categories:
- [语雀,个人技能体系]
abbrlink: 
password: "Grbk@2024"
typora-root-url: ./..
date: 2024-05-23 18:36:31
---
| 编制人 | 编制内容 | 编制时间 |
| --- | --- | --- |
| 蒋家威 | 新增部署文档初版v1.0 | 2022/1/18 |

## 一、准备工作
### 1、下载安装包
下载Oracle安装包：[linux.x64_11gR2_database_1of2.zip](http://www.oracle.com/technetwork/database/enterprise-edition/downloads/112010-linx8664soft-100572.html) 和 [linux.x64_11gR2_database_2of2.zip](http://www.oracle.com/technetwork/database/enterprise-edition/downloads/112010-linx8664soft-100572.html) ，可以下载到本地，通过ftp服务上传到Linux系统（[参考CentOS7 FTP服务器搭建](http://www.cnblogs.com/xibei666/p/5934659.html)），也可以使用Linux系统的wget命令，下载文件包；
<!--more-->
[https://www.oracle.com/cn/database/enterprise-edition/downloads/oracle-db11g-linux.html](https://www.oracle.com/cn/database/enterprise-edition/downloads/oracle-db11g-linux.html)
### 2、创建用户和用户组
创建运行oracle数据库的系统用户和用户组，用Root账号登录，运行下面指令，创建所需要用户和用户组，[分组原因参考网址](http://www.oracle.com/technetwork/cn/articles/hunter-rac11gr2-iscsi-2-092412-zhs.html#13)
```bash
groupadd oinstall　　　　　　　　　　　　　#创建用户组oinstall
groupadd dba　　      　　　　　　　　　　 #创建用户组dba
useradd -g oinstall -G dba -m oracle　　#创建oracle用户，并加入到oinstall和dba用户组
groups oracle  　　　　　　　　　　　　　　#查询用户组是否授权成功
passwd oracle　　     　　　　　　　　　　 #设置用户oracle的登陆密码，不设置密码，在CentOS的图形登陆界面没法登陆
id oracle                   　　　　　　 #查看新建的oracle用户
```
### 3、创建安装目录
创建oracle数据库安装目录（运行下面指令，创建账号和分配权限）
```bash
 mkdir -p /data/oracle　　#oracle数据库安装目录
 mkdir -p /data/oraInventory　　#oracle数据库配置文件目录
 mkdir -p /data/database　　#oracle数据库软件包解压目录
 cd /data
 ls　　#创建完毕检查一下
 chown -R oracle:oinstall /data/oracle　　#设置目录所有者为oinstall用户组的oracle用户
 chown -R oracle:oinstall /data/oraInventory
 chown -R oracle:oinstall /data/database
```
### 4、修改OS系统标识
　oracle默认不支持CentOS系统安装， 修改文件 /etc/[RedHat](http://www.linuxidc.com/topicnews.aspx?tid=10)-release 内容为RedHat-7
```bash
vi /etc/redhat-release  #修改成红色部分文字
redhat-7
```
### 5、安装软件包
　　安装oracle数据库所需要的软件包，以下是按照需要依赖的安装包，通过 yum install {包名} 来验证是否安装，例如yum install binutils
```bash
binutils-2.23.52.0.1-12.el7.x86_64 
compat-libcap1-1.10-3.el7.x86_64 
gcc-4.8.2-3.el7.x86_64 
gcc-c++-4.8.2-3.el7.x86_64 
glibc-2.17-36.el7.i686 
glibc-2.17-36.el7.x86_64 
glibc-devel-2.17-36.el7.i686 
glibc-devel-2.17-36.el7.x86_64 
ksh
libaio-0.3.109-9.el7.i686 
libaio-0.3.109-9.el7.x86_64 
libaio-devel-0.3.109-9.el7.i686 
libaio-devel-0.3.109-9.el7.x86_64 
libgcc-4.8.2-3.el7.i686 
libgcc-4.8.2-3.el7.x86_64 
libstdc++-4.8.2-3.el7.i686 
libstdc++-4.8.2-3.el7.x86_64 
libstdc++-devel-4.8.2-3.el7.i686 
libstdc++-devel-4.8.2-3.el7.x86_64 
libXi-1.7.2-1.el7.i686 
libXi-1.7.2-1.el7.x86_64 
libXtst-1.2.2-1.el7.i686 
libXtst-1.2.2-1.el7.x86_64 
make-3.82-19.el7.x86_64 
sysstat-10.1.5-1.el7.x86_64
```
　　使用下面指令，检查依赖软件包
```bash
yum install -y binutils-2.* compat-libstdc++-33* elfutils-libelf-0.* elfutils-libelf-devel-* gcc-4.* gcc-c++-4.* glibc-2.* glibc-common-2.* glibc-devel-2.* glibc-headers-2.* ksh-2* libaio-0.* libaio-devel-0.* libgcc-4.* libstdc++-4.* libstdc++-devel-4.* make-3.* sysstat-7.* unixODBC-2.* unixODBC-devel-2.* pdksh*
```
### 6、防火墙设置和selinux
```bash
[root@HikOS ~]# systemctl start firewalld.service     //停止firewall
[root@HikOS ~]# firewall-cmd --zone=public --add-port=1521/tcp --permanent  //开启1521端口
[root@HikOS ~]# firewall-cmd --reload  //重启防火墙
```
### 7、修改内核参数
```bash
vi /etc/sysctl.conf #红色部分是要添加sysctl.conf内容
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.conf.all.rp_filter = 1
fs.file-max = 6815744 #设置最大打开文件数
fs.aio-max-nr = 1048576
kernel.shmall = 2097152 #共享内存的总量，8G内存设置：2097152*4k/1024/1024
kernel.shmmax = 2147483648 #最大共享内存的段大小
kernel.shmmni = 4096 #整个系统共享内存端的最大数
kernel.sem = 250 32000 100 128
net.ipv4.ip_local_port_range = 9000 65500 #可使用的IPv4端口范围
net.core.rmem_default = 262144
net.core.rmem_max= 4194304
net.core.wmem_default= 262144
net.core.wmem_max= 1048576
```
### 8、用户设置限制
对oracle用户设置限制，提高软件运行性能
```bash
vi /etc/security/limits.conf  #红色部分要添加到Limits.conf内容
oracle soft nproc 2047
oracle hard nproc 16384
oracle soft nofile 1024
oracle hard nofile 65536
```
### 9、配置用户的环境变量
```bash
vi /etc/profile #红色部分是要追加bash_profile内容部分
export ORACLE_BASE=/data/oracle #oracle数据库安装目录
export ORACLE_HOME=$ORACLE_BASE/product/11.2.0/db_1 #oracle数据库路径
export ORACLE_SID=orcl #oracle启动数据库实例名
export ORACLE_TERM=xterm #xterm窗口模式安装
export PATH=$ORACLE_HOME/bin:/usr/sbin:$PATH #添加系统环境变量
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/lib:/usr/lib #添加系统环境变量
export LANG=C #防止安装过程出现乱码
export NLS_LANG=AMERICAN_AMERICA.ZHS16GBK  #设置Oracle客户端字符集，必须与Oracle安装时设置的字符集保持一致
```
```bash
[root@HikOS ~]# source /etc/profile    //使上述配置生效
```
### 10、获取安装包、解压安装包
　　获取安装包文件后解压安装包，获取安装包文件的方式，[可通过ftp服务器](http://www.cnblogs.com/xibei666/p/5934659.html)，也可通过wget下载到指定目录，解压方式如下
```bash
unzip linux.x64_11gR2_database_1of2.zip -d /data/database/  #解压文件1
unzip linux.x64_11gR2_database_2of2.zip -d /data/database/  #解压文件2
chown -R oracle:oinstall /data/database/database/　　　　　　 #分配安装文件授权Oracle
```
## 二、Oracle静默安装
### 1、文件配置
**切换用户，使用刚刚创建的oracle用户登录liunx服务器。采用的是静默安装，修改配置文件**。
```
[oracle@HikOS ~]# vim /data/database/database/response/db_install.rsp    
// 修改配置文件如下，安装上述解压时，解压路径就是这样
```
```sql
   oracle.install.option=INSTALL_DB_SWONLY
 　ORACLE_HOSTNAME=pc //使用hostname查看自己的系统版本，然后替换
 　UNIX_GROUP_NAME=oinstall
 　INVENTORY_LOCATION=/data/oracle/oraInventory
 　SELECTED_LANGUAGES=en,zh_CN
 　ORACLE_HOME=/data/oracle/product/11.2.0/db_1
 　ORACLE_BASE=/data/oracle/
 　oracle.install.db.InstallEdition=EE
 　oracle.install.db.DBA_GROUP=dba
 　oracle.install.db.OPER_GROUP=oinstall
 　DECLINE_SECURITY_UPDATES=true
```
### 　2、执行安装过程
```sql
[oracle@HikOS ~]# cd /data/database/database
[oracle@HikOS database]# ./runInstaller -silent -ignorePrereq -ignoreSysPrereqs -responseFile /data/database/database/response/db_install.rsp
```
 安装完成后提示如下界面：
　　![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1620834217209-27374991-8162-4ffe-a8ae-a9ccb65a7f0d.png#height=345&id=kSZwC&originHeight=345&originWidth=902&originalType=binary&ratio=1&size=0&status=done&style=none&width=902)
### 3、安装提示命令
切换成root用户，安装上图显示的提示执行命令
```bash
# 可能只需要执行某一条 如第二条
[root@database ~]# sh /data/oraInventory/orainstRoot.sh
[root@database ~]# sh /data/oracle/product/11.2.0/db_1/root.sh
```
### 4、配置监听
切换成oracle用户，配置监听
```bash
[oracle@oracle ~]# cd /data/database/database/response
[oracle@oracle response]# $ORACLE_HOME/bin/netca /silent /responsefile /data/database/database/response/netca.rsp
```
### 5、查看启动情况
查看1521端口监听是否配置成功
```bash
[oracle@oracle~]# netstat -tnulp | grep 1521
```
### 6、创建数据库，修改配置文件
创建数据库，修改配置文件
```bash
[oracle@HikOS ~]# vim /data/database/database/response/dbca.rsp
# oracle版本，不能更改
RESPONSEFILE_VERSION = "11.2.0"
 
# Description   : Type of operation
OPERATION_TYPE = "createDatabase"
[CREATEDATABASE]
# Description   : Global database name of the database
# 全局数据库的名字=SID+主机域名
# 第三方工具链接数据库的时候使用的service名称
GDBNAME = "orcl.test"
# Description   : System identifier (SID) of the database
# 对应的实例名字
SID = "orcl"
# Description   : Name of the template
# 建库用的模板文件
TEMPLATENAME = "General_Purpose.dbc"
# Description   : Password for SYS user
# SYS管理员密码
SYSPASSWORD = "123456"
# Description   : Password for SYSTEM user
# SYSTEM管理员密码
SYSTEMPASSWORD = "123456"
 
# Description   : Password for SYSMAN user
# SYSMAN管理员密码
SYSMANPASSWORD = "123456"
# Description   : Password for DBSNMP user
# DBSNMP管理员密码
DBSNMPPASSWORD = "123456"
# Description   : Location of the data file's
# 数据文件存放目录
DATAFILEDESTINATION =/data/oracle/oradata
 
# Description   : Location of the data file's
# 恢复数据存放目录
RECOVERYAREADESTINATION=/data/oracle/fast_recovery_area
 
# Description   : Character set of the database
# 字符集，重要!!! 建库后一般不能更改，所以建库前要确定清楚。
# (CHARACTERSET = "AL32UTF8" NATIONALCHARACTERSET= "UTF8")
CHARACTERSET = "ZHS16GBK"
 
# Description   : total memory in MB to allocate to Oracle
# oracle内存1638MB,物理内存2G*80%
TOTALMEMORY = "1638"
```
```bash
[oracle@HikOS ~]# dbca -silent -responseFile /data/database/database/response/dbca.rsp
#会自动删命令记录？二次输入密码确认开始安装
```
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1620834217191-7c18980a-6f77-4597-a419-35d303bdb274.png#height=372&id=WWy5A&originHeight=372&originWidth=692&originalType=binary&ratio=1&size=0&status=done&style=none&width=692)
 显示如上界面后，表示创建成功
## 三、Oracle图形化安装
### 1、命令安装
切换到oracle用户登录系统，使用命令行跳转到data/database/database目录下，输入./runInstaller 调出安装页面；
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1620802088467-7358892d-bba7-406c-b8a7-b2eb034d20e1.png#height=330&id=G0yX1&originHeight=330&originWidth=571&originalType=binary&ratio=1&size=0&status=done&style=none&width=571)
调出安装页面，点击下一步进行安装，我选择仅数据库服务安装
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1620802088693-97520dff-7931-47a2-8b41-c306cbd79d96.png#height=395&id=EhyeG&originHeight=395&originWidth=677&originalType=binary&ratio=1&size=0&status=done&style=none&width=677)
### 2、配置安全更新
这步可将自己的电子邮件地址填写进去（也可以不填写，只是收到一些没什么用的邮件而已）。取消下面的“我希望通过My Oracle Support接受安全更新(W)”。 如图：
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1620802088782-f5dab800-0cad-404b-86b6-5c4be9f5dd66.png#height=596&id=wzlwh&originHeight=596&originWidth=801&originalType=binary&ratio=1&size=0&status=done&style=none&width=801)
### 3、安全选项
直接选择默认创建和配置一个数据库(安装完数据库管理软件后，系统会自动创建一个数据库实例)。 如图：
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1620802088539-c98e5704-84a9-468b-978b-d78e36bf04a5.png#height=592&id=vCNoR&originHeight=592&originWidth=797&originalType=binary&ratio=1&size=0&status=done&style=none&width=797)
### 4、系统类
直接选择默认的桌面类就可以了，图略
### 5、典型安装
重要步骤。建议只需要将Oracle基目录更新下，目录路径不要含有中文或其它的特殊字符。全局数据库名可以默认，且口令密码，必须要牢记。密码输入时，有提示警告，不符合Oracel建议时不用管。 (因Oracel建议的密码规则比较麻烦， 必须是大写字母加小写字母加数字，而且必须是8位以上。麻烦，可以输入平常自己习惯的短小密码即可) 如图：
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1620802088617-d8fe635f-a9c0-43fa-8254-e17970e5702c.png#height=594&id=WmlkA&originHeight=594&originWidth=796&originalType=binary&ratio=1&size=0&status=done&style=none&width=796)
### 6、先决条件检查。 
安装程序会检查软硬件系统是否满足，安装此Oracle版本的最低要求。 直接下一步就OK 了。如图：
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1620802088599-1bfec3b4-a87a-4b99-8c93-6110edff7dc6.png#height=588&id=M9Wf2&originHeight=588&originWidth=790&originalType=binary&ratio=1&size=0&status=done&style=none&width=790)
### 7、概要
安装前的一些相关选择配置信息。 可以保存成文件或不保存文件直接点完成即可，然后开始进行安装，如图：
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1620802088571-e866576a-85f5-4828-b286-023cdb6e4b95.png#height=597&id=OCh26&originHeight=597&originWidth=798&originalType=binary&ratio=1&size=0&status=done&style=none&width=798)	数据库管理软件文件及dbms文件安装完后，会自动创建安装一个实例数据库，数据库的名称默认是前面设置的orcl。如图：
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1620802088603-dc8e066a-30e7-4634-a894-0de965a44593.png#height=476&id=iaJcy&originHeight=476&originWidth=1024&originalType=binary&ratio=1&size=0&status=done&style=none&width=1024)
### 8、设置账户密码
实例数据库创建完成了，系统默认把所有账户都锁定不可用(除sys和system账户可用外)，建议点右边的口令管理，将常用的scott账户解锁并输入密码。 如图：
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1620802088623-1c22aaba-8e22-4e43-a0cb-1fc17acfca09.png#height=541&id=NB4FI&originHeight=541&originWidth=891&originalType=binary&ratio=1&size=0&status=done&style=none&width=891)
解锁scott账户， 去掉前面的绿色小勾，输入密码
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1620802088527-40329381-a1e7-4875-a6af-da4126e8476e.png#height=392&id=vLsYk&originHeight=392&originWidth=594&originalType=binary&ratio=1&size=0&status=done&style=none&width=594)
安装成功，完成即可
## 三、Oracle添加实例
　　安装完成之后，通过netca打开监听配置页面，通过执行dbca命令，启动oracle实例安装界面,一个Oracle服务可以对应多个实例，一个Oracle数据库对应多个表空间和用户名，每个用户名又可管理表空间。
## 四、Oracle登入使用
```sql
使用sqlplus命令登录Oracle，重启服务器
sqlplus  /nolog （登录客户端，不登入用户）
  注： 直接登入用户： sqlplus 用户名/密码 as 权限（如sysdba:管理员权限）
conn user/password as sysdba;  （切换登入用户）
\#再输入startup，回车.这步是启动oracle服务。
startup
重启服务器之后，打开Oracle，提示 ORA-01034: ORACLE not available ORA-27101
　　原因在于未启动服务，操作的方式是：
　　1、启动oracle监听：cmd命令行窗口下，输入lsnrctl start，回车即启动监听；
　　2、采用sqlplus /nolog 登录Oracle服务，连接服务conn /as sysdba，然后startup启动服务
  
1）sqlplus / as sysdba  //管理员登录
#再输入startup，回车.这步是启动oracle服务。
startup
2）创建用户
　　语法：CREATE USER 用户名 IDENTIFIED BY 密码;
　　    CREATE USER username IDENTIFIED BY password;
      eg:CREATE USER oracle IDENTIFIED BY 123456;
3）将刚创建的用户解锁/锁住
　　语法：ALTER USER 用户名 ACCOUNT UNLOCK/LOCK
　　用户解锁
　　　　alter user username account unlock;
　　用户锁住
　　　　alter user username account lock;
4）授予新登陆的用户创建权限:
　　语法：CRANT CREATE SESSION TO 用户名
　　    grant create session to username;
5） 授予新创建的用户数据库管理员权限
　　语法：CRANT DBA TO 用户名;
　　    grant dba to username;
6） 切换到新创建的用户登陆
　　语法：CONNECT 用户名/密码
　　　　connect username/password;
7） 删除用户
　　语法：DROP USER 用户名
　　　　drop user uaernam
    
8）进入Oracle用户
su - oracle

9）以dba身份进入sql语句
sqlplus / as sysdba

10）启动数据库
startup

11）启动监听(关闭监听的命令lsnrctl stop)，退出sql编写界面
lsnrctl start

12）关闭数据库服务，在sql编写界面
shutdown immediate

13）常看当前连接用户的信息 
select * from user_users;

14）查看数据库的启动状态 （查看进程里面有没 有Oracle数据库这个进程）
ps -ef|grep oracle

15）表空间相关命令
Sql语句执行的时候要加上分号
创建表空间：
SQL> create tablespace test_work
datafile'/u01/app/oracle/oradata/abc.dbf'
size 10M AUTOEXTEND ON;

16）查询当前所有的表空间：
select *from DBA_TABLESPACES;

17）分类别查看当前的表空间：
SQL> select tablespace_name,
 file_name,
 round(bytes / (1024 * 1024), 0) total_space（显示出来的数字是以M为单位的）
 from dba_data_files
 order by tablespace_name;

18）删除相应的表空间
drop tablespace xxx including contents and datafiles;

19）查看详细数据文件：
SQL> select file_name,tablespace_name from dba_data_files;

20）扩展表空间 
alter database datafile '/data/oracle/oradata/abc.dbf' resize 20M;

21）查看表空间的名字及文件所在位置
select tablespace_name,
file_id,
file_name,
round(bytes / (1024 * 1024), 0) total_space
from sys.dba_data_files
order by tablespace_name

22）查询当前表空间下使用情况
select a.tablespace_name,
a.bytes / 1024 / 1024 "sum MB",
(a.bytes - b.bytes) / 1024 / 1024 "used MB",
b.bytes / 1024 / 1024 "free MB",
round(((a.bytes - b.bytes) / a.bytes) * 100, 2) "used%"
from (select tablespace_name, sum(bytes) bytes
from dba_data_files
group by tablespace_name) a,
(select tablespace_name, sum(bytes) bytes, max(bytes) largest
from dba_free_space
group by tablespace_name) b
where a.tablespace_name = b.tablespace_name
order by ((a.bytes - b.bytes) / a.bytes) desc;
```
## 五、Redhat下安装Oracle
扩展RedHat下Oracle的安装
　　1、RedHat系统版本尽量使用Desk版本，便于Oracle的界面安装，Oracle安装文件传输到RedHat服务器，可以通过SecureCrt远程客户端完成数据的传输。
　　2、记得配置用户换机下的安装编码，否则oracle安装会出现乱码：
```sql
vi /home/oracle/.bash_profile  #追加配置文件
export LANG=C #防止安装过程出现乱码
export NLS_LANG=AMERICAN_AMERICA.ZHS16GBK  #设置Oracle客户端字符集，必须与Oracle安装时设置的字符集保持一致
```
## 六、安装问题
1、我已经在/etc/sysctl.conf中加入了kernel.sem = 250 32000 100 128，但是安装oracle的时候检测还是告诉我理论值128，实际值为0.
网络上解决方案关闭selinux，但是依然如此。决定忽略该告警，继续下一步安装。
解决方案：修改完/etc/sysctl.conf 必须 sysctl -p /etc/sysctl.conf生效配置文件

2、Error in invoking target 'install' of makefile '/data/oracle/product/11.2.0/db_1/ctx/lib/ins_ctx.mk'. See '/data/oraInventory/logs/installActions2019-06-12_10-53-05AM.log' for details.
解决方案：需下载安装32位版本 yum install glibc-devel.i686

3、Error in invoking target 'agent nmhs' of makefile '/data/oracle/product/11.2.0/db_1/sysman/lib/ins_emagent.mk'. See '/data/oraInventory/logs/installActions2019-06-12_10-53-05AM.log' for details.
解决方案: 保留安装过程，另外开启一个终端窗口，将ins_emagent.mk文件中的 (MK_EMAGENT_NMECTL)更改为$(MK_EMAGENT_NMECTL) -lnnz11，然后在安装过程中点击Retry即可。

4、Oracle开放1521端口 telnet不通解决办法
解决方案：查看Linu主机名和修改主机名
hostname 查看主机名
hostname -i：查看本机对应的IP
修改主机名
vim /etc/sysconfig/network
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1620802088482-a53780b2-0e5e-4ec8-8edf-8210869bcc18.png#height=59&id=cTlNF&originHeight=59&originWidth=333&originalType=binary&ratio=1&size=0&status=done&style=none&width=333)
vim /etc/hosts
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1620802088530-1fc6cab0-6735-4280-89be-dd78710c2322.png#height=74&id=RXhbG&originHeight=74&originWidth=555&originalType=binary&ratio=1&size=0&status=done&style=none&width=555)
修改完成后重启:reboot

5.安装完成实例之后，使用sqlPlus命令链接数据库的时候，提示 could not open parameter file "/data/Oracle/product/11.2/db_1/dbs/initorcl.ora"，这个时候需要将刚刚安装的Oracle实例配置文件（$ORACLE_BASE/admin /数据库名称/pfile目录下的init.ora.012009233838形式的文件）拷贝到/data/Oracle/product/11.2/db_1/dbs目录下
```sql
[oracle@localhost pfile]$ pwd
/data/oracle/admin/MLUCDB/pfile
[oracle@localhost pfile]$ cp init.ora.962016224738 /data/Oracle/product/11.2/db_1/dbs/initorcl.ora
```
6、./runInstaller -silent -ignorePrereq -ignoreSysPrereqs -responseFile /data/database/database/response/db_install.rsp 
必须为绝对路径

7、java.lang.NoClassDefFoundError
```bash
[oracle@pc database]$ ./runInstaller -silent -responseFile /data/database/database/response/db_install.rsp -ignorePrereq
Starting Oracle Universal Installer...
Checking Temp space: must be greater than 120 MB.   Actual 8740 MB    Passed
Checking swap space: must be greater than 150 MB.   Actual 2047 MB    Passed
Preparing to launch Oracle Universal Installer from /tmp/OraInstall2021-05-12_10-51-58PM. Please wait ...
[oracle@pc database]$ Exception in thread "main" java.lang.NoClassDefFoundError
        at java.lang.Class.forName0(Native Method)
        at java.lang.Class.forName(Class.java:164)
        at java.awt.Toolkit$2.run(Toolkit.java:821)
        at java.security.AccessController.doPrivileged(Native Method)
        at java.awt.Toolkit.getDefaultToolkit(Toolkit.java:804)
        at javax.swing.UIManager.initialize(UIManager.java:1262)
        at javax.swing.UIManager.maybeInitialize(UIManager.java:1245)
        at javax.swing.UIManager.getUI(UIManager.java:851)
        at javax.swing.JPanel.updateUI(JPanel.java:104)
        at javax.swing.JPanel.<init>(JPanel.java:64)
        at javax.swing.JPanel.<init>(JPanel.java:87)
        at javax.swing.JPanel.<init>(JPanel.java:95)
        at oracle.sysman.oii.oiif.oiifo.OiifoOCMUI.<init>(OiifoOCMUI.java:125)
        at oracle.sysman.oii.oiif.oiifo.OiifoOCMInterfaceManager.<init>(OiifoOCMInterfaceManager.java:79)
 
 [oracle@pc database]$ unset DISPLAY
```
DISPLAY环境变量的作用
在Linux/Unix 类操作系统上, DISPLAY用来设置将图形显示到何处. 直接登陆图形界面或者登陆命令行界面后使用startx启动图形, DISPLAY环境变量将自动设置为:0.0, 此时可以打开终端, 输出图形程序的名称(比如xclock)来启动程序, 图形将显示在本地窗口上, 在终端上输入printenv查看当前环境变量, 输出结果中有如下内容:
DISPLAY=:0.0
使用xdpyinfo可以查看到当前显示的更详细的信息。

无图形化界面，静默安装，禁用
```bash
设置禁用DISPLAY环境变量
执行：
unset DISPLAY
然后再执行runInstaller.sh，执行成功
```
8、安装过程错误QA(大部分因为db_install.rsp（/data/database/database/response/db_install.rsp ）配置有问题)
```
1）、[FATAL] [INS-32037] The operating system group specified for central inventory (oraInventory) ownership is invalid.
解决：
UNIX_GROUP_NAME=oinstall
INVENTORY_LOCATION=/data/oracle/oraInventory


2）、[FATAL] [INS-35071] Global database name cannot be left blank.
解决：ORACLE_HOSTNAME=oracle1

3）、[FATAL] [INS-35071] Global database name cannot be left blank.
解决：oracle.install.db.config.starterdb.globalDBName=oracle.sunyard

4）、[FATAL] [INS-35175] No value given for the allocated memory of the database
解决：oracle.install.db.config.starterdb.memoryLimit=512

5）、[FATAL] [INS-30004] The ADMIN password entered is invalid.
解决：密码不能带@

6）、[INS-32033]Central Inventory location is not vritable
解决：chown -R oracle:oinstall /data/oracle
　　　chown -R oracle:oinstall /data/oraInventory
　　　chown -R oracle:oinstall /data/database
　　　chown -R oracle:oinstall /data/database/database/

7）、[FATAL] [INS-35341] User is not a member of the following chosen OS groups
解决：
oracle.install.db.DBA_GROUP=dba
oracle.install.db.OPER_GROUP=oinstall

8）、[SEVERE] - Email Address Not Specified"
解决：DECLINE_SECURITY_UPDATES=true
```

9、静默安装中缺少某些包
　　解决方法：在静默安装前，先运行 rpm -q binutils compat-libcap1 compat-libstdc++-33 gcc gcc-c++ glibc glibc-devel ksh libaio libaio-devel libgcc libstdc++ libstdc++-devel libXi libXtst make sysstat unixODBC unixODBC-devel，检查是否所有包都有安装，没有的则先安装好再进行接下来的步骤。

10、开始静默安装后，报错“SEVERE: [FATAL] oracle10: oracle10”
　　这个是静默安装最常见的坑，原因是在etc/hosts 文件中没有添加hostname与ip地址的对应内容。解决方法：vim /etc/hosts，在最下方加入你的ip地址与hostname（例如192.168.1.1 oracle10），保存退出后重新运行runInstaller静默安装命令，就能很快解决问题。
     
11、静默安装后，报错“[INS-08109] Unexpected error occurred while validating inputs at state 'inventoryPage‘”
　　原因是oraInventory的设置出现了问题，oraInventory存放的是Oracle软件安装的目录信息，Oralce的安装升级都需要用到这个目录。解决方案：检查响应文件db_install.rsp，看看INVENTORY_LOCATION是否有设定（自己设定一个目录就好，最好是空目录），然后检查/etc/oraInst.loc文件，加入两行
　　　　　　inventory_loc=/data/app/oracle/oraInventory（在db_install.rsp中设定的oraInventory目录）
　　　　　　inst_group=oinstall
　　保存退出后重新运行静默安装命令，就可以解决问题。参考链接：[http://www.savedba.com/?p=910](http://www.savedba.com/?p=910)
 　
12、安装success后，运行sqlplus报找不到指令
　 这个是新手在使用服务器时候常遇到的问题，可以先尝试下到oracle的bin下运行sqlplus，如果有报缺少包去安装缺少的包即可，能直接运行则说明环境变量配置有问题（要么没配对，要么没有使其永久生效）。解决方案：vim ~/.bash_profile，配置正确的环境变量后source ~/.bash_profile，具体的流程网上非常多，这边就不过多描述。

13、监听启动不了
　 解决方案：先配置监听程序 netca /silent /responsefile /home/oracle/etc/netca.rsp，然后修改监控的ip地址
vi /data/app/oracle/product/11.2.0/db_1/network/admin/listener.ora，重新启动lsnrctl start。
 
　　接下来是一堆连锁坑，很容易接连出现：
 
14、运行sqlplus后，运行报错ERROR:ORA-01034: ORACLE not available
　　解决方案：用 sys as sysdba进入空闲例程，运行startup启动oracle
 
15、运行startup，报错LRM-00109: could not open parameter file '/data/app/oracle/product/11.1.0/db_1/dbs/initORCL.ora（文件名是init+sid）'
　　解决方案：$ORACLE_BASE/admin/(dbname) /pfile目录下的init.ora(.01200923383)文件复制到$ORACLE_HOME/dbs目录下即可.(参考资料:https://www.cnblogs.com/linyfeng/p/7231603.html)。如果进到$ORACLE_BASE后发现没有admin怎么办？静默建库就好，建好以后会自动生成admin目录。
 
16、静默建库语句运行后出现一直清屏的现象
　　解决方案：仔细检查应答文件etc/dbca.rsp是否设置正确，特别是SYSPASSWORD= "PASSWARD"，SYSTEMPASSWORD= "PASSWARD"，SYSMANPASSWORD= "PASSWARD"，DBSNMPPASSWORD= "PASSWARD"这几个被注释的行是否有关闭注释，密码是否有输入正确。修改后保存退出etc/dbca.rsp，重新静默建库：

17、Cannot create directory "/data/oracle/cfgtoollogs/dbca".      
> [oracle@pc response]$ cd /data/oracle/cfgtoollogs/netca/
> netca_OraDb11g_home1-21051211PM5100.log  netca_OraDb11g_home1-21051211PM5207.log  netca_OraDb11g_home1-21051211PM5229.log  trace_OraDb11g_home1-21051211PM5100.log  tr                                                                                  
> Cannot create directory "/data/oracle/cfgtoollogs/dbca".                                                                                                                                                               
> sh: /data/oracle/cfgtoollogs/cpuinfo.txt: Permission denied                                                                                                                                                             
> sh: /data/oracle/cfgtoollogs/swapinfo.txt: Permission denied                                                                                                                                                           /etc/inittab does not seem to contain default runlevel information.                                                                                                                                                 sh: /data/oracle/cfgtoollogs/usrgrpinfo.txt: Permission denied   

切换到root用户,对/data/oracle/cfgtoollogs授权
> chmod 774 /data/oracle/cfgtoollogs/


17、Linux下Oracle中SqlPlus时上下左右键乱码问题的解决办法
window下的sqlplus可以通过箭头键，来回看历史命令，用起来非常的方便。
但是在Linux下，会出现各种乱码，非常不方便，如下图所示，每次打错一个字符就需要重新打一遍。
**解决办法：**rlwrap 可以用来支持Oracle下sqlplus历史命令的回调功能，提高效率。
**解决过程：**
**1、首先下载rlwrap和readline；**    
```bash
readline-6.3.tar.gz
rlwrap-0.30.tar.gz
```
**2、安装readline包**
```bash
tar -zxvf readline-6.3.tar.gz 
   cd readline-6.3
   ./configure
   make
   make install
```
**3、安装rlwrap**    
```bash
tar -zxvf rlwrap-0.30.tar.gz
  cd rlwrap-0.30
  ./configure
```
  18、出现问题：You need the GNU readline library(ftp://ftp.gnu.org/gnu/readline/ ) to build this program!
解决办法：yum install readline*，执行后出现如下问题
```bash
 Error Downloading Packages:
  readline-static-6.0-4.el6.x86_64: failure: Packages/readline-static-6.0-4.el6.x86_64.rpm from base: [Errno 256] No more mirrors to try.
  ncurses-libs-5.7-4.20090207.el6.x86_64: failure: Packages/ncurses-libs-5.7-4.20090207.el6.x86_64.rpm from base: [Errno 256] No more mirrors to try.
  readline-devel-6.0-4.el6.x86_64: failure: Packages/readline-devel-6.0-4.el6.x86_64.rpm from base: [Errno 256] No more mirrors to try.
  ncurses-devel-5.7-4.20090207.el6.x86_64: failure: Packages/ncurses-devel-5.7-4.20090207.el6.x86_64.rpm from base: [Errno 256] No more mirrors to try.
  ncurses-base-5.7-4.20090207.el6.x86_64: failure: Packages/ncurses-base-5.7-4.20090207.el6.x86_64.rpm from base: [Errno 256] No more mirrors to try.
```
   如果这些包安装失败,可以到官网上找这些包下载独立安装,安装无误后,在一次尝试:
   **可以从这个网址进行下载 **，包很全：   [http://ftp.riken.jp/Linux/centos/6/os/x86_64/Packages/](http://ftp.riken.jp/Linux/centos/6/os/x86_64/Packages/)    （需要翻墙）
**  安装下载的依赖包：**
```bash
rpm -ivh  --force readline-static-6.0-4.el6.x86_64.rpm  ncurses-libs-5.7-4.20090207.el6.x86_64.rpm readline-devel-6.0-4.el6.x86_64.rpm  ncurses-devel-5.7-4.20090207.el6.x86_64.rpm  ncurses-base-5.7-4.20090207.el6.x86_64.rpm
```
然后再尝试安装rlwrap：
```bash
./configure
make
make install
```
**使用方法：**
1、首先配置一些信息，在root用户下的/etc/profile中添加以下信息： 
```bash
alias sqlplus='/usr/local/rlwrap/bin/rlwrap sqlplus'  (添加命令)
  alias sqlplus='rlwrap sqlplus'       （去除每次都需要输入rlwrap的麻烦）
  alias rman='rlwrap rman'
```
2、source /etc/profile 后切换回oracle就可以使用了
