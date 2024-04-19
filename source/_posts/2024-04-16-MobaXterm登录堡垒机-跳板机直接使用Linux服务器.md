title: MobaXterm登录堡垒机/跳板机直接使用Linux/Windows服务器
tag:
  - MobaXterm
  - shell
categories:
  - linux
  - shell
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
abbrlink: 81cbb71e
tags:
  - MobaXterm
  - shell
author: ''
date: 2024-04-16 09:16:00
top:
---
## 前言

xshell很好用，但是没找到正式版本，公司不允许使用，看了网上的一些资料，发现MobaXterm是比较好的替代产品,，使用MobaXterm登录堡垒机/跳板机直接使用Linux服务器。

## 安装mobaxterm

### 版本

v21.0

### 链接

官网的免费版本：
https://mobaxterm.mobatek.net/download-home-edition.html
直接portable edition就可以了。

![在这里插入图片描述](/imgs/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0l2X3p6eQ==,size_16,color_FFFFFF,t_70.png)

<!--more-->

## 登录堡垒机/跳板机Linux服务器

### 登录方法

#### 输入自己的信息



session-->SSH，新增《创建或者管理凭据》![image-20240416092314200](/imgs/image-20240416092314200.png)

![在这里插入图片描述](/imgs/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0l2X3p6eQ==,size_16,color_FFFFFF,t_70-1713230457868-3.png)

新建凭据

点击新建new，创建凭据；
name：随意填
username：就是你的用户名（你在公司的账户，一般是姓名拼音，大公司是拼音后还有个序号）
password：就是你用户名对应的密码；

![在这里插入图片描述](/imgs/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0l2X3p6eQ==,size_16,color_FFFFFF,t_70-1713230507195-10.png)

![image-20240416092428250](/imgs/image-20240416092428250.png)

点击最下方的确认按钮，保存



### 登录堡垒机/跳板机

登录口令是这个
ssh -p XX username@ip

所以下图的
remote host ：你的堡垒机ip
specify username: 此处会出现上一步你填的name，勾选，登录的时候会自动替换成你上面写的username。
port：需要注意的是这个端口号记得改，我发现我的堡垒机登录的端口号是80，之前没改，所以一直没成功。（linux端口正常是22）

![image-20240416092633347](/imgs/image-20240416092633347.png)

直接点击ok
一部分小伙伴会直接弹出窗口，让你输入二次验证password（密码），那么直接将堡垒机的二次密码输入即可；

#### 选择服务器

​	二次密码验证后，将会需要选择需要登陆的服务器。



二次验证：

![image-20240416095323455](/imgs/image-20240416095323455.png)

服务器选择，然后输入服务器的账号密码，即可正常使用，复制粘贴正常。（只会显示linux机器）

![image-20240416095439359](/imgs/image-20240416095439359.png)

#### 注意

复制了堡垒机的密码，你看看ctrl v能不能用，不能用的话，直接鼠标右键一下，密码就可以粘贴上来了，因为密码不显示，所以这块不知道自己粘贴上了没有，大家多试几次即可



## 登录堡垒机/跳板机Windows服务器

​	

session-->SSH，新增《创建或者管理凭据》![image-20240416092314200](/imgs/image-20240416092314200.png)

![image-20240416094738825](/imgs/image-20240416094738825.png)

新建凭据

点击新建new，创建凭据；
name：随意填
username：就是你的用户名（你在公司的账户，一般是姓名拼音，大公司是拼音后还有个序号）
password：就是你用户名对应的密码；

![在这里插入图片描述](/imgs/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0l2X3p6eQ==,size_16,color_FFFFFF,t_70-1713230507195-10.png)

![image-20240416092428250](/imgs/image-20240416092428250.png)

点击最下方的确认按钮，保存



### 登录堡垒机/跳板机


remote host ：你的堡垒机ip
specify username: 此处会出现上一步你填的name，勾选，登录的时候会自动替换成你上面写的username。
port：需要注意的是这个端口号记得改,使用Windows的远程端口，我发现我的堡垒机登录的端口号是63333，之前没改，所以一直没成功。（Windows端口正常是63333或者默认的3389）

![image-20240416094827124](/imgs/image-20240416094827124.png)

直接点击ok
一部分小伙伴会直接弹出窗口，让你输入二次验证password（密码），那么直接将堡垒机的二次密码输入即可；



#### 选择服务器

​	二次密码验证后，将会需要选择需要登陆的服务器。



二次验证：

![image-20240416095102158](/imgs/image-20240416095102158.png)

服务器选择，然后输入服务器的账号密码，即可正常使用，复制粘贴正常。（只会显示Windows机器）

![image-20240416095210062](/imgs/image-20240416095210062.png)