---
layout: post
title: hexo 插件hexo-git-backup实现对文章的备份
tags:
  - hexo
categories:
  - [博客,hexo]
typora-root-url: ./..
password: 
date: 2024-03-29
abbrlink: a8dc1525
---

一篇关于Hexo博客的备份与恢复的，用的是一个插件：[hexo-git-backup](https://github.com/coneycode/hexo-git-backup)，Hexo官网的插件里搜不到，这个插件发布在了GitHub上，关于安装使用官方也给了很简洁易懂的说明文档。

## 备份

### 安装插件

如果你的Hexo版本是2.x.x（查看Hexo版本可使用命令：`hexo version`）在终端中使用如下命令安装：

```crystal
$ npm install hexo-git-backup@0.0.91 --save
```

如果你的Hexo版本是3.x.x**及后续版本**，则使用如下命令安装：

```auto
$ npm install hexo-git-backup --save
```

<!--more-->

## 插件升级

如果你是通过 `--save`安装的，那么升级之前你必须先删除旧的版本：

```auto
npm remove hexo-git-backup
npm install hexo-git-backup --save
```

### 新建GitHub仓库

新建一个 GitHub 仓库用来备份博客（具体操作不再赘述）

复制仓库ＳＳＨ链接备用，此处需确保你的电脑已通过SSH连接到 GitHub ，具体操作可参考 [GitHub 官方帮助文档](https://help.github.com/en/articles/connecting-to-github-with-ssh)。

## 插件配置

在博客根目录下的 `_config.yml` 文件中配置插件：

```auto
backup:
    type: git
    repository:
       github: git@github.com:xxx/xxx.git,branchName
       gitcafe: git@github.com:xxx/xxx.git,branchName
```

#### 配置说明：

如果你想连同主题一起备份，在 `_config.yml` 文件中添加主题名即可：

```auto
backup:
    type: git
    theme: coney,landscape,xxx
    repository:
       github: git@github.com:xxx/xxx.git,branchName
       gitcafe: git@github.com:xxx/xxx.git,branchName
```

**注意：如果你选择了备份主题例如landscape，那么landscape主题文件夹下的 themes/landscape/.git 文件就会被删除**

如果你想自定义 commit 信息，添加一行 `message: update xxx` 即可：

```auto
backup:
    type: git
    message: update xxx
    repository:
       github: git@github.com:xxx/xxx.git,branchName
       gitcafe: git@github.com:xxx/xxx.git,branchName
```

## 插件使用

现在就可以使用以下命令备份你的博客到GitHub了

```
hexo b 或者 hexo backup
```

博客备份至此就已经结束！安全起见可以每次 `hexo d` 的时候同步 `hexo b` 备份一下博文。

## 恢复

有时候换了另一台电脑或者另一个系统环境下，想要写博客就不得不把博客文件迁移过去，这一部分是关于博客的迁移，接上文使用 hexo-git-backup 插件的情况下（其他方法备份的博客原理类似）。

### 安装Hexo

根据 Hexo 官网说明安装 Hexo 即可

附上官网地址：[https://hexo.io/zh-cn/](https://hexo.io/zh-cn/)

要部署博客到 GitHub 还需要安装插件：

```auto
$ npm install --save hexo-deployer-git
```

### 恢复博客

下载或者 clone 前文所述备份的博客到本地任意位置，复制备份文件夹内所有文件到新安装的博客目录下，重复文件保留备份的即可。

至此博客迁移已完成，可以”三部曲“测试一下是否迁移成功：

```crystal
$ hexo clean
$ hexo g
$ hexo s
```

## **操作过程可能遇到的问题**

### 如何忽略一些文件

​	根目录下配置.gitignore文件：

```
.DS_Store
Thumbs.db
db.json
*.log
node_modules/
public/
.deploy*/
```

**注意，如果你之前克隆过theme中的主题文件，那么应该把主题文件中的.git文件夹删掉，因为git不能嵌套上传，最好是显示隐藏文件，检查一下有没有，否则上传的时候会出错，导致你的主题文件无法上传，这样你的配置在别的电脑上就用不了了。**



### **如何配置`SSH`**

找到`id_rsa.pub`文件，一般在`C:\Users\Administrator\.ssh`这个目录下，复制`id_rsa.pub`内容，打开`gitee/github`的`SSH`公钥，然后填写进去。

如果你之前已经有绑定过本电脑的`SSH`到`github`，那么就不需要再绑定一次了。还没绑定的或者提交失败的，可以重新绑定以此，操作如图，也是将`id_rsa.pub`文件内容填写到这里。

![](/imgs/v2-7f0b49856fcbbacc47e0d887d49ebe87_b.jpg)

![](/imgs/v2-9a01ad00be24e1864f687cf1ed562a55_b.jpg)

### **`hexo b`失败**

**github成功，gitee失败**

可能是`SSH`的公钥还没有绑定到`gitee`，可以试试把根目录下的`.git`目录删掉再提交一次，删掉`不`需要`git init`

![](/imgs/v2-73ba04474814111811d69e29b4eeeae9_b.jpg)

**提交成功**

![](/imgs/v2-ebaa161639e43296a326cc71e8a0f2d0_b.jpg)

#### **原因一：`.git`文件夹存在**

​	目录下有`.git`文件夹，删掉`.git`文件夹即可

![](/imgs/v2-8719fc6b1d86b1031fd2bdbf95c915f1_b.jpg)

​	删掉重新提交(hexo b)

#### **原因二：本地仓库和远程仓库没有连上**

**可以试试添加远程链接**

```bash
 git remote add backup-gitee git@gitee.com:Lilbai518/backup-blog.git
 git remote add backup-github git@github.com:0000rookie/backup-blog.git
```

**添加完检查一下**

```bash
 $ git remote -v
 gitee   git@gitee.com:Lilbai518/backup-blog.git (fetch)
 gitee   git@gitee.com:Lilbai518/backup-blog.git (push)
 githu   git@github.com:0000rookie/backup-blog.git (fetch)
 githu   git@github.com:0000rookie/backup-blog.git (push)
```

**重新提交试试**

## 可能遇到的错误

### **Could not read from remote repository.**

今天在备份博客的时候，突然报错了，然后重新生成公钥，放到Gitee和GitHub上，重新hexo b就好了

**错误**

![](/imgs/v2-b05b78c8692cc702f0cb9c298db807a7_b.jpg)

**生成新的公钥**

```bash
 ssh-keygen -t rsa -C "aa134***@gmail.com"
```

**删除目录下的.git文件夹**

![](/imgs/v2-2206d4e24b294de5679390b20606f85a_b.jpg)

**将公钥放到Github和Gitee上**

将改文件`C:\Users\用户名\.ssh\id_rsa.pub`复制公钥到Gitee和GitHub

**重新部署**

不需要初始化本地仓库`git init`，直接使用`hexo b`就行，因为我们在博客根目录下的`_config.yml`已经添加我们的仓库地址了。

```yaml
 backup:
   type: git
   theme: butterfly
   message: 这是我的博客文件
   repo:
     github: git@github.com:***地址.git,main
     gitee: git@gitee.com:***地址.git,master
```
