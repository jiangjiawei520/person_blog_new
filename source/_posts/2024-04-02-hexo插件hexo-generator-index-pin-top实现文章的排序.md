---
title: hexo插件hexo-generator-index-pin-top实现文章的排序
tags: 
	- hexo
categories:
  - [博客,hexo]
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
top: 
typora-root-url: ./..
abbrlink: 3225ac4f
date: 2024-04-02 09:19:33
---

# hexo如何修改: 文章排序

hexo默认情况下以编写时间的先后来排序，后写的后出现

按照以下方法可为文章添加top属性来排序

首先在cmd中输入以下命令

首先要切入hexo所在的文件夹，否则生成页面会报错

```
npm uninstall hexo-generator-index --save
npm install hexo-generator-index-pin-top --save
```

然后在文章当中添加top属性即可

数字越大，排在越上面

![img](/imgs/3285662-20240208155353623-1901434418.png)
