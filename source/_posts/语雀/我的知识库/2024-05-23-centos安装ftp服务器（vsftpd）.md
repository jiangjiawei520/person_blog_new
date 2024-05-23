---
ayout: post
title: centos安装ftp服务器（vsftpd）
tags:
  - 语雀
categories:
  - - 语雀
    - 我的知识库
abbrlink: a8e4c409
password: Grbk@2024
date: 2024-05-23 16:24:15
---
## 一、安装
1、安装
```bash
yum -y install vsftpd
```
2、修改配置，去掉匿名登录：

```bash
<!--more-->
vim /etc/vsftpd/vsftpd.conf
anonymous_enable=YES
改为：
anonymous_enable=NO
```

3、启动服务：
```bash
vim /etc/vsftpd/vsftpd.conf #修改配置文件
```
![](https://cdn.nlark.com/yuque/0/2022/png/12484160/1654149793962-5ed39d98-95ca-43dd-9313-62e17da6184b.png#clientId=ub2f24126-6648-4&from=paste&id=uf1196c65&originHeight=298&originWidth=663&originalType=url&ratio=1&rotation=0&showTitle=false&status=done&style=none&taskId=u8396fb81-a00f-4292-aee7-ab3c9948fdb&title=)

```bash
systemctl start vsftpd
```
4、修改vsftpd的pam认证模块
```bash
vim /etc/pam.d/vsftpd 
#/etc/pam.d下的文件存放的各个命令的pam模块的配置
auth required pam_shells.so
改成
auth required pam_nologin.so
```
5、关闭 SELinux：
临时修改：
```bash
setenforce 0
```
永久生效：
```bash
sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config
grep -v "^#" /etc/selinux/config | grep "SELINUX="
```
6、设置ftp用户密码，第一步安装的时候已经创建了ftp用户（nologin）
```bash
passwd ftp
```
7、可以用ftp用户和密码进行登录了
方法一：直接输入ftp加ip地址
```bash
ftp 192.168.xxx.xxx
```
方法二：直接输入ftp，进入ftp服务后输入open加ip地址
```bash
open 192.168.xxx.xxx
```
#输入用户；输入密码
![image.png](https://cdn.nlark.com/yuque/0/2022/png/12484160/1654149870284-3c9f995a-770d-412d-aaaa-634627ee675e.png#clientId=ub2f24126-6648-4&from=paste&id=u043e4d55&originHeight=359&originWidth=678&originalType=url&ratio=1&rotation=0&showTitle=false&size=29080&status=done&style=none&taskId=ud1e0fdd0-0980-4a7d-8cb7-2336ccfcc35&title=)


## Linux中关闭SELinux的方法
1、临时关闭：输入命令setenforce 0，重启系统后还会开启。
2、永久关闭：输入命令vi /etc/selinux/config，将SELINUX=enforcing改为SELINUX=disabled，然后保存退出。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/12484160/1654149902904-9a1f50eb-9c63-4f65-9c0b-aa8a55e3eccb.png#clientId=ub2f24126-6648-4&from=paste&id=uc886f6e8&originHeight=54&originWidth=365&originalType=url&ratio=1&rotation=0&showTitle=false&size=3395&status=done&style=none&taskId=ua6618f47-6578-40ea-9f49-5718c1c6172&title=)
![image.png](https://cdn.nlark.com/yuque/0/2022/png/12484160/1654149902946-2b6f3b6f-dea3-4720-b67e-c2ef468faeb0.png#clientId=ub2f24126-6648-4&from=paste&id=u89f74be4&originHeight=238&originWidth=539&originalType=url&ratio=1&rotation=0&showTitle=false&size=14329&status=done&style=none&taskId=u88a379c7-a8a4-43b4-a340-6aa68e0cf03&title=)

## 三、问题
#### 550 Failed to change directory及553 Could not creat file
排查思路：
1.查看ftp上传路径是否从根目录开始
个人遇到的情况是，需求方提供的ftp地址存在隐藏目录，需求方提供的ftp地址为：ftp://xx.xx.xxx.xxx/xxx/input,这个地址可以正常访问，只不过没有显示根目录，于是询问ftp服务器搭建人员，权限正常，selinux服务也已关闭，结果还是出现553，然后和ftp搭建人员核对的下目录，发现根目录没有在地址中显示，于是将根目录添加到路径中，问题解决，真实路径为：ftp://xx.xx.xxx.xxx/home/userftp/xxx/input，各位小伙伴可以自行查看自己的根路径。

2.查看权限问题及selinux服务是否关闭
详细解决方案参考下方连接：
[权限问题及selinux服务是否关闭](https://blog.csdn.net/nigar_/article/details/103053052)
