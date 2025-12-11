---
title: 2025-12-11-解决国内github.com打不开的最最最准确方法
tag:
  - Windows
  - github
categories:
  - Windows
  - github
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
date: 2025-12-11 12:49:09
top:
---

**1、打开网站 https://tool.chinaz.com/dns/，在 A 类型填写 github.com，点击按钮【立即检测】。**
![img](/imgs/1048776-20240730145926241-1656021786.png)

<!--more-->

**2、下拉，看到如下界面。**
![img](/imgs/1048776-20240730150118606-1855982215.png)



**3、随便复制一个 IP 地址，打开 C:\Windows\System32\drivers\etc 目录下的 host.ics 文件**

![img](/imgs/1048776-20240730150339791-1717021422.png)



**4、在该文件里增加一行 20.205.243.166   github.com。**
![img](/imgs/1048776-20240730150502498-394955352.png)



**5、win+R  打开 CMD 执行 ipconfig/flushdns 命令。**
![img](/imgs/1048776-20240730150803526-294460616.png)

**6. 再次访问 github.com 是不是就能打开了**

