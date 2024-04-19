---
layout: post
title: 更新github仓库、hexo仓库
tags:
  - hexo
  - git
categories:
  - [博客,hexo]
abbrlink: d9bb6d3f
date: 2024-03-19
---

## 更新github仓库

首先切换到你的本地仓库中更新的项目目录

可以在用Git Bash用cd命令切换，也可以直接右键项目点击git bash here

```bash
//首次时
git config --global user.name "你的名字或昵称"
git config --global user.email "你的邮箱"
//当天第一次时（初始化）
git init
//每次更新代码时add 和commit
git status //查看仓库状态
git add . //用于更新所有代码
git commit -m "first commit"  （first commit 本次提交的内容）
git remote add origin https://github.com/852172891/test3.git //重新添加远程仓库地址，地址换成你建的项目的地址
git pull origin master --allow-unrelated-histories //正常需要把远程仓库和本地同步，消除差异
git push -u origin master  //将本地仓库的代码提交到github的仓库远程仓库的master主干，这一句执行的时候 可能需要输入你的 github 账号 和密码

其他
git clone https://github.com/852172891/test3.git //fork他人模板
git remote -v                                  //查看远程仓库详细信息，可以看到仓库名称
git remote remove orign                      //删除orign仓库（如果把origin拼写成orign，删除错误名称仓库）


git branch new_branch    //新建分支
git push -u origin new_branch       // 推送本地分支到远程仓库，并设置跟踪关系
git checkout 分支名 // 切换分支
git branch -a   //查询所有分支
git branch -d branch_name //删除本地分支
git push origin --delete branch_name  //删除远程分支
```

注：如果是多人合作开发的话，需要在第四步之后先使用 >git pull 拉取当前分支的最新代码

## 更新hexo仓库

首先切换到你的本地仓库中更新的项目目录

```bash
hexo init //新建目录初始化为hexo，再拉取代码
hexo clean //清除指定文件夹的效果
hexo g //生成页面
hexo s //发布服务
hexo d //将hexo发布到GitHub上
```

