---
layout: post
title: CentOS7安装MySQL（完整版）
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "Grbk@2024"
typora-root-url: ./..
date: 2024-05-23 18:36:32
---
在CentOS中默认安装有MariaDB，这个是MySQL的分支，但为了需要，还是要在系统中安装MySQL，而且安装完成之后可以直接覆盖掉MariaDB。

 

1 下载并安装MySQL官方的 Yum Repository
[root@localhost ~]# wget -i -c [http://dev.mysql.com/get/mysql57-community-release-el7-10.noarch.rpm](http://dev.mysql.com/get/mysql57-community-release-el7-10.noarch.rpm)
 
<!--more-->

  使用上面的命令就直接下载了安装用的Yum Repository，大概25KB的样子，然后就可以直接yum安装了。

[root@localhost ~]# yum -y install mysql57-community-release-el7-10.noarch.rpm
 

之后就开始安装MySQL服务器。

[root@localhost ~]# yum -y install mysql-community-server
这步可能会花些时间，安装完成后就会覆盖掉之前的mariadb。
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1617872449590-4cde6b30-a47f-4ff6-afa1-6187d956159f.png#align=left&display=inline&height=181&originHeight=181&originWidth=477&size=0&status=done&style=none&width=477)


至此MySQL就安装完成了，然后是对MySQL的一些设置。

2 MySQL数据库设置
  首先启动MySQL

 

  

 

[root@localhost ~]# systemctl start  mysqld.service
  查看MySQL运行状态，运行状态如图：

 

[root@localhost ~]# systemctl status mysqld.service

![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1617872455293-3a4281f8-2701-4bd4-baad-e038d28a7145.png#align=left&display=inline&height=244&originHeight=244&originWidth=646&size=0&status=done&style=none&width=646)
此时MySQL已经开始正常运行，不过要想进入MySQL还得先找出此时root用户的密码，通过如下命令可以在日志文件中找出密码：

[root@localhost ~]# grep "password" /var/log/mysqld.log
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1617872469882-8a310b1d-3937-411c-a757-86bed68d09d4.png#align=left&display=inline&height=46&originHeight=46&originWidth=719&size=0&status=done&style=none&width=719)

  如下命令进入数据库：

[root@localhost ~]# mysql -uroot -p
输入初始密码（是上面图片最后面的 no;e!5>>alfg），此时不能做任何事情，因为MySQL默认必须修改密码之后才能操作数据库：

mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'new password';
其中‘new password’替换成你要设置的密码，注意:密码设置必须要大小写字母数字和特殊符号（,/';:等）,不然不能配置成功

 

3 开启mysql的远程访问
执行以下命令开启远程访问限制（注意：下面命令开启的IP是 192.168.0.1，如要开启所有的，用%代替IP）：

grant all privileges on *.* to 'root'@'192.168.0.1' identified by 'password' with grant option;
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1617872489697-fff29df4-3cb1-4c6f-980b-069d221feeae.png#align=left&display=inline&height=51&originHeight=51&originWidth=759&size=0&status=done&style=none&width=759)

然后再输入下面两行命令

mysql> flush privileges; 
mysql> exit

![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1617872495003-194e7e45-0919-4430-9350-dbc5554b485f.png#align=left&display=inline&height=80&originHeight=80&originWidth=463&size=0&status=done&style=none&width=463)
 

4 为firewalld添加开放端口
添加mysql端口3306和Tomcat端口8080

[root@localhost ~]# firewall-cmd --zone=public --add-port=3306/tcp --permanent
[root@localhost ~]# firewall-cmd --zone=public --add-port=8080/tcp --permanent
然后再重新载入

[root@localhost ~]# firewall-cmd --reload
 
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1617872498778-fd00478f-3089-4c25-abb5-441539e76645.png#align=left&display=inline&height=121&originHeight=121&originWidth=586&size=0&status=done&style=none&width=586)


 

5 更改mysql的语言
首先重新登录mysql，然后输入status：



 

可以看到，绿色箭头处不是utf-8
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1617872511949-200330c2-6d0c-40d4-bdbc-94c8741f7c07.png#align=left&display=inline&height=60&originHeight=60&originWidth=335&size=0&status=done&style=none&width=335)
 

因此我们先退出mysql，然后再到、etc目录下的my.cnf文件下修改一下文件内容
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1617872511949-200330c2-6d0c-40d4-bdbc-94c8741f7c07.png#align=left&display=inline&height=60&originHeight=60&originWidth=335&size=0&status=done&style=none&width=335)


进入文件后，新增四行代码：
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1617872521678-ede6bf2a-4e52-40f6-8e97-f1bf211fea9a.png#align=left&display=inline&height=634&originHeight=634&originWidth=713&size=0&status=done&style=none&width=713)


保存更改后的my.cnf文件后，重启下mysql，然后输入status再次查看，你就会发现变化啦
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1617872526571-17623932-2a78-4523-8be0-7af89d783b0c.png#align=left&display=inline&height=338&originHeight=338&originWidth=637&size=0&status=done&style=none&width=637)





                                           
