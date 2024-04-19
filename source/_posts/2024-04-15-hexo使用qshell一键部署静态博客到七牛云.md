---
title: hexo使用qshell一键部署静态博客到七牛云
tag:
  - hexo
  - 七牛云
categories:
  - 博客
  - hexo
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
abbrlink: 1a485dfe
date: 2024-04-15 18:27:06
top:
---

### 下载qshell下载

https://github.com/qiniu/qshell/releases/download/v2.13.0/qshell-v2.13.0-windows-386.zip

### 配置qshell环境变量

### 添加account

执行qshell account <Your AccessKey> <Your SecretKey> <Your Name> 

### Hexo项目的根目录下创建upload.conf文件

配置

```
{
// 这个地址是根目录地址，不可使用相对路径
"src_dir": "E:\\xx\\github\\person_blog_new\\public",
// 储存空间名称
"bucket": "person-blog-new-hw",
// 是否覆盖
"overwrite" : true,
// 检查新增文件
"rescan_local" : true
}
```

上传 qshell qupload upload.conf

### 一键部署

打开Hexo下的package.json，npm run publish 就可实现一键打包部署到七牛云

```
  "scripts": {
	"publish": "hexo generate && qshell qupload upload.conf"
  }
```

### 参考

https://juejin.cn/post/6844903983857811469