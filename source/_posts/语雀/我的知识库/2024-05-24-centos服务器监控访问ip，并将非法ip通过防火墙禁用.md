---
layout: post
title: centos服务器监控访问ip，并将非法ip通过防火墙禁用
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "bk@2024"
typora-root-url: ./..
date: 2024-05-24 10:50:14
---
## 使用iftop查看访问ip
我们在shell直接输入iftop,有可能会提示我们无此命令，这时我们需要安装iftop
### 安装iftop
yum install iftop -y
如图：
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639360763735-85e75f61-9d31-4f2d-aacb-ab7ef249d1cb.png#clientId=uc5ab3970-6abd-4&from=paste&id=u3c74bd95&originHeight=410&originWidth=644&originalType=url&ratio=1&size=23799&status=done&style=none&taskId=ubb4c90b9-3b95-40b6-ae44-ca6bf0efb89)
### 效果
<!--more-->
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639360763708-7b82b075-3cf8-49a0-b49d-f99db67e57df.png#clientId=uc5ab3970-6abd-4&from=paste&id=u9883dcca&originHeight=381&originWidth=651&originalType=url&ratio=1&size=16443&status=done&style=none&taskId=u59b64888-7162-4f3b-bd06-b38d147b579)
# Centos7开放或限制IP和端口
**开放或限制端口**
> #单个端口开放

> firewall-cmd --zone=public --add-port=80/tcp --permanent

> #每次修改都要重新载入

> firewall-cmd --reload

> #移除开放的端口则端口会被限制

> firewall-cmd --zone=public --remove-port=80/tcp --permanent

> firewall-cmd --reload

> 

> #批量开放端口

> firewall-cmd --zone=public --add-port=2000-2100/tcp --permanent

> firewall-cmd --reload

> #批量限制

> firewall-cmd --zone=public --remove-port=2000-2100/tcp --permanent

> firewall-cmd --reload


**查看开放的端口**
> #查看所有开放成功的端口

> firewall-cmd --zone=public --list-ports

> #查看端口是否开放成功

> firewall-cmd --zone=public --query-port=80/tcp


开放或者限制IP访问
> #允许指定IP访问80端口，如果要限制 accept改为reject

> firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.1.100" port protocol="tcp" port="80" accept"

> firewall-cmd --reload

> 

> #允许内网访问80端口，如果要限制 accept改为reject

> firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.1.0/24" port protocol="tcp" port="80" accept"

> firewall-cmd --reload

> 

> #查看已经添加的规则

> firewall-cmd --zone=public --list-rich-rules

> #删除修改已经添加的规则

> vi /etc/firewalld/zones/public.xml

> firewall-cmd --reload


**firewall启用禁用**
> #开启

> systemctl start  firewalld

> #查看状态

> systemctl status firewalld

> #开机启动

> systemctl enable firewalld

> #禁用

> systemctl disable firewalld

> #停用

> systemctl stop firewalld

> 

