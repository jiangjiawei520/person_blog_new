---
layout: post
title: nginx与fastdfs的配置
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "Grbk@2024"
typora-root-url: ./..
date: 2024-05-23 18:36:32
---
[https://blog.csdn.net/qq_41946543/article/details/102811191?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.control](https://blog.csdn.net/qq_41946543/article/details/102811191?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.control)
 
首先我们需要一台服务器，这里我用的是VM虚拟机，ISO是CentOS7，使用XShell操作终端，Xshell、虚拟机和CentOS的安装我就不赘述啦，直接进入正题。
我们进入linux后使用下面的命令查看下当前的ip
ip addr(ifconfig)
找到你的网卡名称对应的inet后面的ip，我这里的是192.168.1.103，找到了记录一下先，后面我们会用到
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1611906852052-71cfa5aa-1bff-4af6-9c46-b9682ff81d0e.png#align=left&display=inline&height=83&originHeight=238&originWidth=1183&status=done&style=none&width=415)
<!--more-->
安装编译环境
yum install git gcc gcc-c++ make automake autoconf libtool pcre pcre-devel zlib zlib-devel openssl-devel wget vim -y
 
创建数据存储目录
mkdir /home/fdfs_storage/files
 
切换到安装目录准备下载安装包
cd /usr/local/
 
**安装libfatscommon**
git clone [https://github.com/happyfish100/libfastcommon.git](https://github.com/happyfish100/libfastcommon.git) --depth 1
 
进入文件
cd libfastcommon/
 
编译安装
./make.sh && ./make.sh install
 
完成后回到上一层目录
cd ../
 
**安装FastDFS**
git clone [https://github.com/happyfish100/fastdfs.git](https://github.com/happyfish100/fastdfs.git) --depth 1
 
进入文件
cd fastdfs/
 
编译安装
./make.sh && ./make.sh install
 
配置文件准备
cp /usr/etc/fdfs/tracker.conf.sample /etc/fdfs/tracker.conf cp /usr/etc/fdfs/storage.conf.sample /etc/fdfs/storage.conf cp /usr/etc/fdfs/client.conf.sample /etc/fdfs/client.conf #客户端文件，测试用 cp /usr/local/fastdfs/conf/http.conf /etc/fdfs/ #供nginx访问使用 cp /usr/local/fastdfs/conf/mime.types /etc/fdfs/ #供nginx访问使用
 
注意：如果提示"无法获取某某某，没有那个文件或目录"，那么就把cp后面的/usr去掉，直接从/etc开始写
返回上一级目录
cd ../
 
**安装fastdfs-nginx-module**
注意版本匹配问题： 下载地址为：[https://github.com/happyfish100/fastdfs-nginx-module/releases](https://github.com/happyfish100/fastdfs-nginx-module/releases) 我这里选择 V1.20 版本和fastDFS5.12版本匹配。
[https://github.com/happyfish100/fastdfs-nginx-module/archive/V1.20.zip](https://github.com/happyfish100/fastdfs-nginx-module/archive/V1.20.zip)
git clone [https://github.com/happyfish100/fastdfs-nginx-module.git](https://github.com/happyfish100/fastdfs-nginx-module.git) --depth 1
 
cp /usr/local/fastdfs-nginx-module/src/mod_fastdfs.conf /etc/fdfs
 
返回上一级目录
cd ../
 
**安装nginx**
下载nginx压缩包
wget [http://nginx.org/download/nginx-1.15.4.tar.gz](http://nginx.org/download/nginx-1.15.4.tar.gz)
 
解压
tar -zxvf nginx-1.15.4.tar.gz
 
进入解压后的文件夹
cd nginx-1.15.4/
 
添加fastdfs-nginx-module模块
./configure --add-module=/usr/local/fastdfs-nginx-module/src/ --prefix=/usr/local/nginx_fdfs
 
* prefix是指定nginx要安装的路径
* add-module指定fastDFS的nginx模块的源代码路径
编译安装
make && make install
 
**tracker配置**
vim /etc/fdfs/tracker.conf
 
需要修改的内容如下
port=22122  # tracker服务器端口（默认22122,一般不修改） # 这里原本为base_path=/home/yuqing/fastdfs，将他改为如下base_path=/home/fdfs_tracker  # 存储日志和数据的根目录
 
 
保存退出
 
**storage配置**
vim /etc/fdfs/storage.conf
 
需要修改的内容如下
port=23000  # storage服务端口（默认23000,一般不修改） # 这里原本为base_path=/home/yuqing/fastdfs，将他改为如下 base_path=/home/fdfs_storage  # 数据和日志文件存储根目录 # 这里原本为base_path0=/home/yuqing/fastdfs，将他改为如下  store_path0=/home/fdfs_storage  # 第一个存储目录 # 这里可能会存在两条相同的配置，注释掉一条即可，然后ip改成最开始让记录下来的你的ip，这里因为我的是192.168.1.103，所以我改成了这个 tracker_server=192.168.1.103:22122  # tracker服务器IP和端口 http.server_port=8888  # http访问文件的端口(默认8888,看情况修改,和nginx中保持一致)
 
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1611906852603-bb7fa3a1-32ec-402b-90b4-7ddf8065475f.png#align=left&display=inline&height=50&originHeight=88&originWidth=728&status=done&style=none&width=415)
**client测试**
vim /etc/fdfs/client.conf
 
需要修改的内容如下
# 这里也是改成与之前相同的 base_path=/home/fdfs_client# 这里也可能存在两条，注释掉一条即可，ip改成自己的ip tracker_server=192.168.1.103:22122    #tracker服务器IP和端口
 
保存退出
 
**启动**
不关闭防火墙的话无法使用
systemctl stop firewalld.service # 关闭防火墙 systemctl disable firewalld.service #重启后防火墙不会自启动
 
启动storage服务
 
/etc/init.d/fdfs_storaged start chkconfig fdfs_storaged on #重启后会自启动storage服务或者/usr/bin/fdfs_storaged /etc/fdfs/storage.conf restart
 
启动tracker服务
/usr/bin/fdfs_trackerd /etc/fdfs/tracker.conf restart
 
查看资源管理器
ps -ef | grep fdfs
 
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1611906853105-90454d62-e090-4ba7-9eb0-fd361140639f.png#align=left&display=inline&height=43&originHeight=122&originWidth=1185&status=done&style=none&width=415)
此时有包含fdfs或者以fdfs打头的进程有这两个，说明进程启动成功了
**测试**
使用Xftp连接CentOS
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1611906853627-57df7877-3303-4104-8518-60be42264fef.png#align=left&display=inline&height=529&originHeight=705&originWidth=494&status=done&style=none&width=371)
连接成功后可以随便放一张图片到CentOS里面去，以便测试
回到root文件夹下
cd ~
 
# /root/111.png是刚才用来测试的存放的图片的路径/usr/bin/fdfs_test /etc/fdfs/client.conf upload /root/111.jpg
 
 
得到一串路径
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1611906854119-37287eca-4346-47ff-8cd4-191628b7af73.png#align=left&display=inline&height=25&originHeight=62&originWidth=1039&status=done&style=none&width=415)
复制这串路径，保存一下，待会儿会用到
**配置nginx访问**
vim /etc/fdfs/mod_fastdfs.conf
 
需要修改的内容如下
# 原本为false 改为  true url_have_group_name=true store_path0=/home/fdfs#原本为tracker_server=tracker:22122 改为如下，ip为自己的ip tracker_server=192.168.1.103:22122
 
 
保存并退出
配置nginx.config
vim /usr/local/nginx/conf/nginx.conf
 
添加如下配置
server {     listen       8888;    ## 该端口为storage.conf中的http.server_port相同     server_name  localhost;     location ~/group[0-9]/ {         ngx_fastdfs_module;     }     error_page   500 502 503 504  /50x.html;     location = /50x.html {     root   html;     } }
 
保存并退出
测试ngnix
/usr/local/nginx/sbin/nginx -t
启动nginx
/usr/local/nginx/sbin/nginx
 
重启nginx
/usr/local/nginx/sbin/nginx -s reload
随后，在你的浏览器地址栏上输入：192.168.1.103:8080（这里的ip为你自己的ip），就能够与访问到nginx的欢迎页面了！
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1611906854629-70048fd6-5a5c-4176-8658-7b80d983e08d.png#align=left&display=inline&height=154&originHeight=257&originWidth=692&status=done&style=none&width=415)
还没有完！还有最后一步测试，将之间记录的图片的路径拷贝到192.168.1.103:8080的后面，变成192.168.1.103:8080/group1/M00/00/···.png就能够访问到你的图片啦！
 
在浏览器访问上传的文件当遇到400错误，检查配置/etc/fdfs/mod_fastdfs.confurl_have_group_name=true该配置表示访问路径中是否需要带有group1，改为true表示路径中需要有group1
 
