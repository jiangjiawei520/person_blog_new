---
title: MobaXterm有用配置
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
abbrlink: 
date: 2024-04-31 14:16:00
top:
---

## 关闭自动弹出SFTP

Moba在连接上远程电脑之后，将自动打开左侧的SFTP侧边栏。有时我们并不需要SFTP，同时主窗口是黑色的，SFTP又是白色的，显得有点刺眼，因此可以将自动弹出SFTP功能关闭掉。

在菜单栏点击 「settings」 --> 「Configuration」，在弹出的对话框中选择 「SSH」，再将 「automaticall switch to SSH-browser tab after login」 前面的对勾去掉即可。

![image-20240531145708740](/imgs/image-20240531145708740.png)