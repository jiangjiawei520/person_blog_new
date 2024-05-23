---
layout: post
title: 启动报错 Failed to start Login Service
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "Grbk@2024"
typora-root-url: ./..
date: 2024-05-23 18:36:32
---
之前由于误删passwd文件，导致系统重新启动的时候，卡在加载界面不动，按ctrl+1切换到代码界面，发现很多报错，其中多次出现Failed to start Login Service。下面分享一下解决这个bug的方法：
  首先我们开机进入如下界面：
![](https://cdn.nlark.com/yuque/0/2023/png/12484160/1702108546251-33820bf6-2bb0-4f26-a7a1-8b6291a063b1.png#averageHue=%23060606&clientId=ub689e6b3-58f2-4&from=paste&id=uc02716c2&originHeight=300&originWidth=466&originalType=url&ratio=1&rotation=0&showTitle=false&status=done&style=none&taskId=uc775ac75-5be3-4ed3-8102-a4a20a51f37&title=)
  在进入上面这个界面后，按e进入如下界面
![](https://cdn.nlark.com/yuque/0/2023/png/12484160/1702108571359-eb2175ea-bda4-48bd-a538-58a9ca1328ca.png#averageHue=%23100e0e&clientId=u710a28e1-bd75-4&from=paste&id=u4a8ab6c3&originHeight=328&originWidth=894&originalType=url&ratio=1&rotation=0&showTitle=false&status=done&style=none&taskId=u10a60692-b4c6-498d-b3e8-530a9cba2c6&title=)
  将红框中的ro改成rw rd.break，(不是rw init=/bin/bash)然后按ctrl+x，稍等一会就会进入单用户模式。
![](https://cdn.nlark.com/yuque/0/2023/png/12484160/1702108576307-bd635145-fe34-48cd-a29f-7182ae15fb52.png#averageHue=%23101010&clientId=u710a28e1-bd75-4&from=paste&id=uacf0536a&originHeight=35&originWidth=588&originalType=url&ratio=1&rotation=0&showTitle=false&status=done&style=none&taskId=u16cda3ef-6093-45d5-97c3-01f7ce7fe8a&title=)
<!--more-->
  然后修改根路径，在sh-4.2#后面逐步执行
  chroot /sysroot
  cp /etc/passwd- /etc/passwd
  cp /etc/shadow- /etc/passwd
  完成后，输入vi /etc/sysconfig/selinux修改此文件，将selinux项修改为selinux = disabled。按Esc再输入:wq回车就保存好了文件。再连续输入两次exit，返回到单用户模式，再输入exec /sbin/init重启即可进入系统

