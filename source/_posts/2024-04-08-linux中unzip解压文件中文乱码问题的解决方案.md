---
title: linux中unzip解压文件中文乱码问题的解决方案
tag:
  - linux
categories:
  - linux
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
abbrlink: 67e26b88
date: 2024-04-08 15:54:33
top:
---

### 原因

在windows上压缩的文件，是以系统默认编码中文来压缩文件。由于zip文件中没有声明其编码，所以linux上的unzip一般以默认编码解压，中文文件名会出现乱码。  
虽然2005年就有人把这报告为bug, 但是info-zip的官方网站没有把自动识别编码列入计划，可能他们不认为这是个问题。Sun对java中存在N年的zip编码问题，采用了同样的处理方式。

### 解决问题：

第一种：通过unzip行命令解压，指定字符集

```bash
unzip -O GBK xxx.zip (用GBK, GB18030也可以)
```
