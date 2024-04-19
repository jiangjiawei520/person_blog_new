---
title: hexo博客之使用github Actions将自动构建并发布静态源码
tag:
  - hexo
  - github
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
typora-root-url: ./..
abbrlink: 2af8072d
date: 2024-04-19 14:16:26
top:
---

## 自动构建并发布

​	github的action功能，可以使用这个功能代替手工的发布操作。在 GitHub Actions 的仓库中自动化、自定义和执行软件开发工作流程。 您可以发现、创建和共享操作以执行您喜欢的任何作业（包括 CI/CD），并将操作合并到完全自定义的工作流程中。

### 正文

首先建立一个Git仓库，这里不再赘述

这里我采用了sshkey的形式来进行仓库的操作

### 生成ssh密钥

```
ssh-keygen -t rsa -C YourCount@example.com
```

### 打开git仓库,添加部署用的私钥

​	注意添加的secret名称需要唯一，不能于本账号的其他仓库的重复，不然会导致失败。

> setting->secrets->add new secret

[![ePo2EwfZirp9h31](/imgs/ePo2EwfZirp9h31.png)](https://i.loli.net/2020/04/16/ePo2EwfZirp9h31.png)

<!--more-->

### 添加权限验证的公钥

​	在个人账号的设置里面设置，只用设置一次就行，如果之前设置过，可以跳过本步骤。

> setting->deploy keys->add deploy key

[![UK1lDvTx5PZBM2m](/imgs/UK1lDvTx5PZBM2m.png)](https://i.loli.net/2020/04/16/UK1lDvTx5PZBM2m.png)

至此我们的仓库准备工作就已经完成

## 编写action发布文件

> action->set up a new workflow file

可以看到下方有很多发布模板供我们选择

此次我们自己来进行编写

[![LHfVB3gmRvQ18se](/imgs/LHfVB3gmRvQ18se.png)](https://i.loli.net/2020/04/16/LHfVB3gmRvQ18se.png)



```
name: auto publish #发布名称

on:  
  push: #触发方式
    branches: 
      - master #触发分支

jobs: #脚本内容
  build-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v1
    - run: npm ci
    - run: npm install vuepress
    - run: npm run build
    - run: cp CNAME .vuepress/dist/ #指定gitpage的自定义域名
    
    - name: Deploy
      uses: peaceiris/actions-gh-pages@v2.5.0
      env:
        ACTIONS_DEPLOY_KEY: ${{secrets.ACCESS_TOKEN}} #这里引用的是刚才生成的私钥
        PUBLISH_BRANCH: gh-pages #发布到的分支
        PUBLISH_DIR: .vuepress/dist #需要发布的内容
```

下面我们每次对master分支的推送都会触发该发布流程

该发布流程会自动构建vuepress项目并把生成的文件发布到当前项目的gh-pages分支下

## 自动构建并发布到另一仓库

​	新的需求 **自动构建后发布到不同的仓库**。

### 正文

我们直接新建一个yml发布文件

在系统给我们生成的文件中我们可以看到基础语法的介绍

这里我结合自己的理解标注一下

在进行解读之前我们先了解一下基本概念

### 基本术语

- workflow (工作流程)
- job (任务) 一个workflow可以由多个不同的job组成
- step (步骤) 每个job可以由多个step来组成
- action(动作) 每个step又可以由多个action来组成

### Action市场

由于持续集成大家的需求大部分可能都是相同的操作

所以github建立了一个Action市场

使得每个人编写的Action脚本都可以被其他人来引用

这就使得当我这种彩笔小白想要使用这些功能的时候而不用写出很复杂的脚本

而这整个持续集成的过程也就成为了不同的Action相组合的产物

使用方法也很简单，只需要使用`uses`关键字直接引用别人的库即可

```
uses userName/repoName
```

### 结合模板

然后我们来结合系统生成的基础模板来进行基本的解读



```
# This is a basic workflow to help you get started with Actions

name: CI  # 构建流程的名称


on: #触发该流程的方式
  push:
    branches: [ master ]  #触犯该流程的分支
  pull_request:
    branches: [ master ]

jobs:
  # 该任务当前仅包含了一个任务  名称是build
  build:    
    runs-on: ubuntu-latest #任务锁运行的工作环境

    # 该任务所包含的步骤
    steps:
    # 步骤所依赖的操作库 这里引用了官方发布的git操作库 目的是拉取当前库的代码
    - uses: actions/checkout@v2

    # 这里是一个单行命令的模板
    - name: Run a one-line script
      run: echo Hello, world!

    # 这里是一个多行命令的模板
    - name: Run a multi-line script
      run: |
        echo Add other actions to build,
        echo test, and deploy your project.
```

### 用已有的库进行持续集成(当前库构建发布到另外的库)

到这里我们就可以开始进行自己的Action的组装了

首先我们先找一个有发布到其他Git库功能的Action

我们可以在github的市场搜索自己需要的Action

[![MFcPRLTway742pE](/imgs/MFcPRLTway742pE.png)](https://i.loli.net/2020/04/17/MFcPRLTway742pE.png)

这里我使用的是`s0/git-publish-subdir-action@master`

点开这个库的主页我们可以在下方看到该库的使用说明

这里就不在赘述了



```
name: AutoBuild

on:
  push:
    branches: [ OneKeyVip-master ]
  pull_request:
    branches: [ OneKeyVip-master ]
jobs:
  
  build:
    name: build
    runs-on: ubuntu-latest    
    steps:    
    - uses: actions/checkout@v2    
    - name: npm install
      run: |
        npm install
        npm ci
    - name: npm build
      run: |
       npm run build
       cp README.MD ./publish/README.MD #可选
       cp CHANGELOG ./publish/CHANGELOG #可选

    - name: publish
      uses: s0/git-publish-subdir-action@master
      env:
        REPO: 目标库
        BRANCH: 目标分支
        FOLDER: 要发布的内容所在的文件夹        
        SSH_PRIVATE_KEY: ${{ secrets.publish }}
```

## 常见问题

### Repository not found.

```
$ hexo b
INFO  Validating config
INFO  Start backup: git
On branch master
nothing to commit, working tree clean
ERROR: Repository not found.
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
INFO  Backup done: git
```

删除.git目录，重新执行hexo b



检查添加命令：

```
检查已有分支
git remote -v
gitee   git@gitee.com:jiangjiawei520172/person_blog_new.git (fetch)
gitee   git@gitee.com:jiangjiawei520172/person_blog_new.git (push)
github  git@github.com:jiangjiawei520/person_blog_new.git (fetch)
github  git@github.com:jiangjiawei520/person_blog_new.git (push)
github_source   git@github.com:jiangjiawei520/person_blog_new_source.git (fetch)
github_source   git@github.com:jiangjiawei520/person_blog_new_source.git (push)

如无gitee、github_source则添加，github未启动（查询站点根目录_config.yml配置文件backup下的repository参数）
git remote add gitee/github/github_source git@xxx.git	
```

