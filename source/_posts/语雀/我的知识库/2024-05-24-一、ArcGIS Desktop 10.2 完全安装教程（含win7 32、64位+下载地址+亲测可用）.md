---
layout: post
title: 一、ArcGIS Desktop 10.2 完全安装教程（含win7 32、64位+下载地址+亲测可用）
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "bk@2024"
typora-root-url: ./..
date: 2024-05-24 10:50:14
---
## 系统环境

win7 32/64位操作系统（Win10本人没有测试，不过留言区有读者反馈也可以安装成功）
## 需要文件

### 1.ArcGIS Desktop 10.2原版安装光盘
### 2.ArcGIS Desktop 10.2补丁文件
<!--more-->
[点击此处下载](http://malagis.com/arcgis-10-2-full-iso-download.html)
说明：上面的文件大约在4G左右，需要找一个网速快的地方下载~

## 0.关闭Windows防火墙 & Windows Defender

如果想安装起来少麻烦，**请关闭Windows防火墙**，关闭方法戳右边链接-->[**安装ArcGIS关闭Window防火墙的方法**](http://malagis.com/install-arcgis-close-windows-firewall.html)
如果是Win7以上的系统，要把 Windows Defender 也关闭，关闭方法--> [**安装ArcGIS关闭 Windows Defender 的方法**](https://malagis.com/install-arcgis-to-close-windows-defender.html)
已经有很多朋友遇到因为Window防火墙引起的问题，保险起见，建议关闭。
## 1.用虚拟光驱或者解压软件将下载下来的ISO文件解压。

![](https://cdn.nlark.com/yuque/0/2021/jpeg/12484160/1615346619487-e8f81a23-93fb-4536-9d53-56f7484a6261.jpeg#averageHue=%23c2b69b&height=324&id=EAVN2&originHeight=324&originWidth=520&originalType=binary&ratio=1&rotation=0&showTitle=false&size=0&status=done&style=none&title=&width=520)
运行ESRI.exe

## 2.安装License Manager

与ArcGIS 10.1的安装不同，10.2不需要安装第3方修改的License Manager，安装原版即可。
![](https://cdn.nlark.com/yuque/0/2021/jpeg/12484160/1615346619724-0d52acff-2551-4002-abb3-3f4da5e3c362.jpeg#averageHue=%23f2efed&height=365&id=V3ZPe&originHeight=365&originWidth=520&originalType=binary&ratio=1&rotation=0&showTitle=false&size=0&status=done&style=none&title=&width=520)
点击红圈里的Setup开始安装，一路默认即可，另如果C盘不是特别小，不建议更改路径（仅仅是建议）。
安装完毕后，启动License Manager，选择停止服务。如图：
![](https://cdn.nlark.com/yuque/0/2021/jpeg/12484160/1615346619696-954b3325-9eba-4154-9383-0a82008f4ef0.jpeg#averageHue=%23e4e2db&height=169&id=hV8N5&originHeight=169&originWidth=519&originalType=binary&ratio=1&rotation=0&showTitle=false&size=0&status=done&style=none&title=&width=519)
## **3.安装**[**ArcGIS**](http://malagis.com/tag/arcgis)** Desktop**

![](https://cdn.nlark.com/yuque/0/2021/jpeg/12484160/1615346619708-7e95d749-b67d-4288-8e42-5d1efe7ec8ce.jpeg#averageHue=%23ede2d6&height=223&id=OTe8L&originHeight=223&originWidth=519&originalType=binary&ratio=1&rotation=0&showTitle=false&size=0&status=done&style=none&title=&width=519)
安装期间一路下一步即可，什么也不用管。
## 4.执行补「破」丁「解」文件

下面就到了关键步骤了，这里提供一种本人亲测可用的方法。
首先打开Lincense10.2的安装目录，我的是：
C:\Program Files (x86)\ArcGIS\License10.2\bin
32位系统的是
C:\Program Files\ArcGIS\License10.2\bin
这里都是指默认目录，如图：
![](https://cdn.nlark.com/yuque/0/2021/jpeg/12484160/1615346619722-6512c0ac-3070-46e9-91b6-bafdcd85b460.jpeg#averageHue=%23d3cfbd&height=423&id=QioWi&originHeight=423&originWidth=498&originalType=binary&ratio=1&rotation=0&showTitle=false&size=0&status=done&style=none&title=&width=498)
将里面的service.txt和ARCGIS.exe重命名（**随便重命名一下就好，名字不要求**，这是比较安全的做法，万一失败可以用其他方法），然后将下载的ArcGIS Desktop 10.2补（po）丁（jie）文件复制进去即可。当然，**直接替换**也可以。
## 5.启动服务

运行License Manager，点击开始即可，如果为了确保成功，可以点击重新读取许可。
![](https://cdn.nlark.com/yuque/0/2021/jpeg/12484160/1615346619512-585ebb66-cf30-4451-a256-fcd66f1038cc.jpeg#averageHue=%23b4c8df&height=222&id=VzlFh&originHeight=222&originWidth=571&originalType=binary&ratio=1&rotation=0&showTitle=false&size=0&status=done&style=none&title=&width=571)
不出意外，就成功了，你可以启动ArcGIS Administrator，查看可用性。
![](https://cdn.nlark.com/yuque/0/2021/jpeg/12484160/1615346619498-3fe02707-3758-489f-9266-28447cf72064.jpeg#averageHue=%23cbc4b6&height=191&id=aplHE&originHeight=191&originWidth=519&originalType=binary&ratio=1&rotation=0&showTitle=false&size=0&status=done&style=none&title=&width=519)
## 6.更改授权地址

打开安装完成后启动ArcGIS Administrator(打开方法开始菜单->所有程序->ArcGIS->ArcGIS Administrator)。
![](https://cdn.nlark.com/yuque/0/2021/jpeg/12484160/1615346620103-1b928391-b51c-45ee-ba21-451d2d242884.jpeg#averageHue=%23f6dc91&height=232&id=awtST&originHeight=232&originWidth=269&originalType=binary&ratio=1&rotation=0&showTitle=false&size=0&status=done&style=none&title=&width=269)
选择ArcInfo浮动版
![](https://cdn.nlark.com/yuque/0/2021/jpeg/12484160/1615346619716-4857f4e2-c28d-4612-a2b0-211cceb21403.jpeg#averageHue=%23eae8e7&height=258&id=jdbHK&originHeight=258&originWidth=500&originalType=binary&ratio=1&rotation=0&showTitle=false&size=0&status=done&style=none&title=&width=500)
同时将图3处，改为localhost，点击确定，关闭 ArcGIS Administrator。不出意外，你已经可以运行ArcMap了。不过此时是英文版本。
![](https://cdn.nlark.com/yuque/0/2021/jpeg/12484160/1615346619707-f77c485a-73cb-4a8d-95ea-8310c421568d.jpeg#height=198&id=t4ivE&originHeight=198&originWidth=363&originalType=binary&ratio=1&rotation=0&showTitle=false&size=0&status=done&style=none&title=&width=363)
## 安装简体中文汉化包

ArcGIS 10.2 汉化方法：

- [ArcGIS 10.2简体中文汉化教程（附下载地址+亲测可用）](http://malagis.com/arcgis-10-2-chinese-simplified-chinese-tutorial.html)
## License无法启动另外2种解决方案

如果使用上述替换文件的方法无法启动License，也可以用下面的2种方法来解决。
我用上述方法成功，如果有未成功的可以用下面提供的几种方法。
### 方法一
打开补（po）丁（jie）文件中的service.txt，修改第3行的
SERVER localhost ANY 27000
将其中的localhost改为this_host，然后执行替换，如果还是不行将localhost改为你的计算机名（注意计算机名中不能有特殊符号，修改方法可以参考[安装ArcGIS修改计算机名](http://malagis.com/installing-arcgis-modify-computer-name.html)）
### 方法二
点击[下载这个文件](http://pan.baidu.com/s/1sjx1TEH)，提取密码：e9y2
运行ArcGIS_KeyGen_modified.exe
![](https://cdn.nlark.com/yuque/0/2021/jpeg/12484160/1615346619722-74b59e70-476b-4b14-97f4-c654d021ae55.jpeg#height=416&id=aIkAz&originHeight=416&originWidth=407&originalType=binary&ratio=1&rotation=0&showTitle=false&size=0&status=done&style=none&title=&width=407)
图中的10.2是无法选择的，手动输入即可。点击all，将生成的内容保存成service.txt；然后将这个service.txt和ArcGIS.exe按照之前的方法执行破解。
## 疑难问题解决

如果 License Manager 服务还是无法启动，可以参考这篇文章：[安装ArcGIS License Manager 服务无法启动的解决方案汇总](http://malagis.com/arcgis-license-manage-cannot-start-solutions.html)
## 其他ArcGIS版本安装方法大全

如果需要安装其他的ArcGIS版本（建议只装一个版本，人要专一不是吗？多版本共存，会有各种问题哦），可以参考下面的文章。

- [ArcGIS 9.3下载安装方法整理](https://malagis.com/arcgis-9-3-downlaod-install.html)
- [ArcGIS Desktop 10.1+ArcEngine10.1完全安装教程1（含下载地址+亲测可用！）](https://malagis.com/arcgis-desktop-arcengine-fully-cracked-installation-tutorial-1.html)
- [ArcGIS Desktop 10.1+ArcEngine10.1完全安装教程2（含下载地址+亲测可用！）](https://malagis.com/arcgis-desktop-arcengine-cracked-installation-tutorial-2.html)
- [ArcGIS Desktop 10.2 完全安装教程（含win7 32/64位+下载地址+亲测可用）](https://malagis.com/arcgis-desktop-10-2-full-installation-tutorial.html)
- [ArcGIS Desktop 10.2.2 完整安装教程（兼容win7/8/10 32/64位+下载地址+亲测可用）](https://malagis.com/arcgis-desktop-10-2-2-full-installation-tutorial.html)
- [ArcGIS Desktop 10.3 安装简明教程（支持32/64位+下载地址+亲测可用）](https://malagis.com/arcgis-desktop-10-3-full-cracked-installation-tutorial-html.html)
- [ArcGIS 10.4.1 Desktop 完整安装教程（含win7/8/10 32/64位+下载地址+亲测可用）](https://malagis.com/arcgis-desktop-10-4-1-full-installation-tutorial.html)
- [ArcGIS 10.5 Desktop 完整安装教程（含win7/8/10 32/64位+下载地址+亲测可用）](https://malagis.com/arcgis-desktop-10-5-full-installation-tutorial.html)
- [ArcGIS 10.6 Desktop 完整安装教程（含win7/8/10 32/64位+下载地址+亲测可用）](https://malagis.com/arcgis-desktop-10-6-full-installation-tutorial.html)
- [ArcGIS 10.7 Desktop 完整安装教程（含win7/8/10 32/64位+下载地址+亲测可用）](https://malagis.com/arcgis-desktop-10-7-full-installation-tutorial.html)
