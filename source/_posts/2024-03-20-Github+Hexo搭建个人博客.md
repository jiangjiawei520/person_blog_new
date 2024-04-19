---
layout: post
title: Github+Hexo搭建个人博客
tags:
  - hexo
  - git
categories:
  - [博客,hexo]
abbrlink: dbfe91e4
typora-root-url: ./..
date: 2024-03-20
---

# **一、下载安装 git ，Node**

Node下载地址：https://nodejs.org/en/

Git：https://git-scm.com/

# **二、安装，配置 Hexo**

​	Hexo官方文档：https://hexo.io/zh-cn/docs/

## 安装

 	前面已经安装了Git和Node.js，然后用npm，安装Hexo
 	
 	找个文件夹，右键“git bash here”,打开git控制台

```bash
npm install -g hexo-cli
```

<!--more-->

## 配置

  	新建博客文件夹（例如：G:\07Blog\Linton_Blog），进入Linton_Blog文件夹，输入以下命令行

```bash
hexo init
npm install
npm install hexo-deployer-git --save
```

 	新建完成后，Linton_Blog的文件夹下的目录：

```tex
├── _config.yml #配置信息
├── package.json
├── scaffolds
├── source
| ├── _drafts
| └── _posts #博客内容
└── themes #主题
```

注意1：如果出现 hexo not command类似的报错，说明hexo的环境变量没有设置或是Node.js版本过低

# **三、本地启动Hexo**

```
$ hexo g # 生成页面

$ hexo s #启动本地服务器,这一步之后就可以通过http://localhost:4000 查看
```

![image-20240320092656930](/imgs/image-20240320092656930-1711088546748-93-1711091521465-43.png)

浏览器输入：http://localhost:4000/；显示如下：

![img](/imgs/wps1-1711088546749-95.jpg)



# **四、将Hexo部署到GitHub上**

##  **注册GitHub账户**

##  **创建仓库**

![image-20240320092914963](/imgs/image-20240320092914963-1711088546749-97.png)

![image-20240320092920984](/imgs/image-20240320092920984-1711088546749-99.png)



## 发布为pages页面

​	点击setting > pages选项

 ![img](/imgs/4893b9c8849c4820bac2efefa5ea66b2-1711088546749-101.png)

​	为站点创建入口文件。 GitHub Pages 将查找 index.html、index.md 或 README.md 文件，作为站点的入口文件。
如果发布源是分支和文件夹，则入口文件必须位于源分支上源文件夹的顶层。 例如，如果发布源是 main 分支上的 /docs 文件夹，则入口文件必须位于名为 main 的分支上的 /docs 文件夹。
​	如果发布源是 GitHub Actions 工作流，则部署的项目必须在项目的顶层包含入口文件。 可以选择使用 GitHub Actions 工作流在工作流运行时生成入口文件，而不是将入口文件添加到存储库。 

​	在Github Pages页面中，可以选择将仓库的哪个分支的哪个文件夹作为网站的根目录发布到Github page中：最后点击Save按钮即可

![img](/imgs/471c7dc6c5f7419d94a05488ed2d6f72-1711088546749-103.png)

 	然后静静等待差不多10分钟左右，再刷新页面，即可看到一个访问网站的提示：然后点击Visit sate 即可访问自己的网站了：

![img](/imgs/b58f440f14a546f28d988d35718c4ec2-1711088546749-105.png)

​	网站中展示的内容，就是你仓库里面的  index.html、index.md 或 README.md 文件，会挨个查找，优先使用找到的那个文件作为展示内容


## 选择自定义主题

​	可以看到“https://linton6.github.io/linton.github.io/”，这个是GitHub给你提供的自定义博客样式，在没有部署Hexo前，你可以点开看看，也是一个博客，可以在下面的choose a theme 旋转主题。部署Hexo后，点击这个链接，就是你刚才在本地运行Hexo的那个页面了

![img](/imgs/wps2-1711088546749-107.jpg) 

![img](/imgs/wps3-1711088546749-109.jpg) 

  	我的页面在没部署前，如下图。待会看下部署完后的页面，做下对比

![img](/imgs/wps4-1711088546749-111.jpg)

## **使用Hexo deploy 部署到GitHub**

###   **1）编辑根目录下_config.yml文件**

```bash
# Deployment
## Docs: https://hexo.io/docs/deployment.html
deploy:
  type: git
  repo: git@github.com:linton6/linton.github.io.git # 这里的网址填你自己的
  branch: master
```

 

**注意：在配置所有的_config.yml文件时（包括theme中的），在所有的冒号:后边都要加一个空格，否则执行hexo命令会报错。**

### **2）添加SSH Key 到GitHub**

```
cd ~/.ssh 
ls                   #此时会显示一些文件
mkdir key_backup
cp id_rsa* key_backup
rm id_rsa*           #以上三步为备份和移除原来的SSH key设置
ssh-keygen -t rsa -C "邮件地址@youremail.com" #生成新的key文件,邮箱地址填你的Github地址
#Enter file in which to save the key (/Users/your_user_directory/.ssh/id_rsa):<回车就好>
#接下来会让你输入密码
```



### **3）进入GitHub首页**

### ![img](/imgs/wps5-1711088546749-113.jpg)![img](/imgs/wps6-1711088546749-115.jpg)

###  **4）点击New SSHKey**

   	然后找到当前用户目录下C:\Users\用户名\ .ssh id_rsa.pub文件以文本方式打开。打开之后全部复制到key中

![img](/imgs/wps7-1711088546749-117.jpg) 

### **5）测试一下是否成功**

```bash
ssh -T git@github.com
```

   如果提示：You've successfully authenticated, but GitHub does not provide shell access. 说明你连接成功了

### **6）设置用户信息：**

```bash
$ git config --global user.name "恰克与飞鸟"          #给自己起个用户名，可以不用时Git的名称
$ git config --global user.email  "649557938@qq.com"  #填写Git的邮箱
```

### **7）部署到GitHub上**

```
hexo d
```

   部署完以后，会发现自己的GitHub这个项目的代码已经更新为你本地的文件！

Enter passphrase for key '/c/Users/Administrator/.ssh/id_rsa':输入密码

### **8）此时再次刷新git网址**

  （我的是https://linton6.github.io/linton.github.io/），就可以看到自己的博客了，可以对比下看看，两个页面访问的都是同一个地址

![img](/imgs/wps8-1711088546749-119.jpg)![img](/imgs/wps9-1711088546749-121.jpg) 

  会发现，现在这个页面没有主题，需要进行下一步设置

### **9）加载博客样式文件**   

  需要修改_config.yml文件中的url地址和根目录

  url：是github Page给我们分配的网址

  root：是搭建该博客的仓库名

![img](/imgs/wps10-1711088546749-123.jpg) 

  这样就可以加载样式文件了

### **10)重新部署到github**

```
hexo clean

hexo g

hexo d
```

  访问网址，如下

![img](/imgs/wps11-1711088546749-125.jpg) 

  好了，自定义的博客已经搭建完毕，后期可以对博客的主题，样式，上传博客等再做教程~

#  四、常见问题

## 1、LF will be replaced by CRLF the next time Git touches it

**问题**：windows平台进行 git add 时，控制台打印警告

解决：适用于Windows系统，且只在Windows上开发的情况。在提交、检出时不会对CRLF/LF换行符进行转换

```
#提交检出均不转换
git config --global core.autocrlf false
```





参考博客：

0.https://hexo.io/zh-cn/docs

1.https://blog.csdn.net/u014385892/article/details/80196115

2.https://blog.csdn.net/dazhaodai/article/details/73730069

3.http://blog.sina.com.cn/s/blog_a03baecd0102xp7i.html

4.https://blog.csdn.net/xudailong_blog/article/details/78762262

5.https://www.jianshu.com/p/8681ab76da08

6.https://www.cnblogs.com/liuxianan/p/build-blog-website-by-hexo-github.html 这个挺全

参考：

https://www.cnblogs.com/MJyaaatou/p/9355648.html

https://blog.csdn.net/lw545034502/article/details/90696872

Hexo-Github-备份：

https://zhuanlan.zhihu.com/p/619003000

Github+Hexo博客增添相册功能：

https://blog.csdn.net/cungudafa/article/details/104378416

Hexo+Github实现相册功能：

https://blog.csdn.net/u013082989/article/details/70162293/

【Hexo】GitHub+Typora写博客+图片上传：

https://blog.csdn.net/Qxiaofei_/article/details/124629908