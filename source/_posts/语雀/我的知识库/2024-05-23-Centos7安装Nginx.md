---
layout: post
title: Centos7安装Nginx
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "Grbk@2024"
typora-root-url: ./..
date: 2024-05-23 18:36:32
---
## 一、安装环境

### 1.安装gcc环境
```
yum install -y gcc-c++
```

<!--more-->
### 2.安装pcre库
nginx的http模块使用pcre来解析正则表达式，所以需要在linux上安装pcre库，pcre-devel是使用pcre开发的一个二次开发库。nginx也需要此库。
```
yum install -y pcre pcre-devel
```

### 3.安装zlib库
zlib提供了很多种压缩和解压缩的方式，nginx使用zlib对http包的内容进行gzip，所以需要在Centos上安装zlib库。
```
yum install -y zlib zlib-devel
```

### 4.安装OpenSSL
OpenSSL是一个强大的安全套接字层密码库，囊括主要的密码算法、常用的密钥和证书封装管理功能及SSL协议，并提供丰富的应用程序供测试或其它目的使用。nginx不仅支持http协议，还支持https（即在ssl协议上传输http），所以需要在Centos安装OpenSSL库。
```
yum install -y openssl openssl-devel
```

## 二．下载安装nginx

### 1.官网地址
[https://nginx.org/en/download.html](https://nginx.org/en/download.html)

### 2.下载到本地
```
wget https://nginx.org/download/nginx-1.17.1.tar.gz
```

### 3.解压

```
tar -zxvf nginx-1.17.1.tar.gz
cd nginx-1.17.1
```

### 4.默认配置
```
./configure
```

### 5.可选自定义配置

```
./configure --prefix=/usr/local/nginx --conf-path=/usr/local/nginx/conf/nginx.conf --pid-path=/usr/local/nginx/conf/nginx.pid --lock-path=/var/lock/nginx.lock --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --with-http_gzip_static_module --http-client-body-temp-path=/var/temp/nginx/client --http-proxy-temp-path=/var/temp/nginx/proxy --http-fastcgi-temp-path=/var/temp/nginx/fastcgi --http-uwsgi-temp-path=/var/temp/nginx/uwsgi --http-scgi-temp-path=/var/temp/nginx/scgi --with-http_ssl_module
```

### 6.编译安装

```
make
make install
```

### 7.设置环境变量

```
whereis nginx
ln -s /usr/local/nginx/sbin/nginx  /usr/bin/nginx
nginx -v
```

### 8.配置反向代理等
配置的目录为：
```
/usr/local/nginx
```

## 9.重启脚本
```
利用配置文件启动nginx 命令: nginx -c /usr/local/nginx/conf/nginx.conf
重启服务： service nginx restart
快速停止或关闭Nginx：nginx -s stop
正常停止或关闭Nginx：nginx -s quit
配置文件修改重装载命令：nginx -s reload
```

