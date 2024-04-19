---
layout: post
title: hexo 插件hexo-blog-encrypt 实现对文章的加密
tags:
  - hexo
categories:
  - [博客,hexo]
date: 2024-03-21
abbrlink: ef718547
typora-root-url: ./..
---

## 下载插件

```
npm install --save hexo-blog-encrypt
```

## 快速使用

文章配置里面添加（不启用密码的话password设为空或者不写）

```
---
title: Hello World
date: 2020-12-18 20:44:18
password: (填写你想设置的密码)
abstract: 这里有东西被加密了，需要输入密码查看哦。
message: 您好，这里需要密码。
wrong_pass_message: 抱歉，这个密码看着不太对，请再试试。
wrong_hash_message: 抱歉，这个文章不能被纠正，不过您还是能看看解密后的内容。
---
```

## 按标签设置密码

在博客根目录下的_config.xml中添加:

```
encrypt: # hexo-blog-encrypt
  abstract: 这里有东西被加密了，需要输入密码查看哦。
  message: 您好, 这里需要密码.
  tags:
  - {name: tagName, password: 密码A}
  - {name: tagName, password: 密码B}
  template: <div id="hexo-blog-encrypt" data-wpm="{{hbeWrongPassMessage}}" data-whm="{{hbeWrongHashMessage}}"><div class="hbe-input-container"><input type="password" id="hbePass" placeholder="{{hbeMessage}}" /><label>{{hbeMessage}}</label><div class="bottom-line"></div></div><script id="hbeData" type="hbeData" data-hmacdigest="{{hbeHmacDigest}}">{{hbeEncryptedData}}</script></div>
  wrong_pass_message: 抱歉, 这个密码看着不太对, 请再试试.
  wrong_hash_message: 抱歉, 这个文章不能被校验, 不过您还是能看看解密后的内容.
```

## 应用

![image-20240320163358836](/imgs/image-20240320163358836-1711088473591-24.png)

## 配置优先级

文章信息头 > _config.yml (站点根目录下的) > 默认配置
