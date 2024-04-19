---
layout: post
title: Goindex的魔改版本
tags:
  - 技术分享
categories:
  - 技术分享
abbrlink: '4734e101'
date: 2020-06-17
---

![img](http://jiangjiawei.epizy.com/wp-content/uploads/2020/06/u3207433114120194597fm26gp0.png)

**GoIndex**是一款部署在**Cloudflare Workers**的Google Drive目录索引程序，无需提供服务器，可以直接列出你谷歌网盘的所有文件，同时下载和访问也不需要挂梯子，也可以在线观看某些格式的视频文件。

<!--more-->

原版Github地址：https://github.com/donwa/goindex

原版作者由于某些原因已经删库。

这次主要介绍的是基于原版Goindex的一个魔改版本

Github项目地址 ：https://github.com/Aicirou/goindex-theme-acrou
此魔改版本的特色：

🔐 多盘切换
🔐 Http Basic Auth
🎨 网格视图模式（文件预览）
🎯 分页加载
🌐 I18n（多国语言）
🛠 html渲染
🖥 视频在线播放(mp4,mkv,webm,flv,m3u8)
🚀 拥有更快的速度



开发者demo https://oss.achirou.workers.dev/
快速部署:
此魔改版本同样支持快速部署：
打开[https://goindex-quick-install.glitch.me](https://goindex-quick-install.glitch.me/)
授权并获取授权码
将代码部署到 Cloudflare Workers
关于使用自己的api部署可以查阅项目介绍页的说明，由于本人较懒使用的是快速部署所以就不过多介绍了。
使用个人api部署好处就是安全点，高峰期也不容易爆炸。

查看[https://goindex-quick-install.glitch.me](https://goindex-quick-install.glitch.me/)的源码https://glitch.com/@qianqian1307

作者: 赖小瑜
链接: https://blog.likexy.me/posts/a3ab42cc/