---
layout: post
title: Centos8无法执行update的解决办法（Failed to download metadata for repo ‘AppStream’）
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "bk@2024"
typora-root-url: ./..
date: 2024-05-24 10:50:14
---
### 问题起因
因[Centos8](https://so.csdn.net/so/search?q=Centos8&spm=1001.2101.3001.7020)软件源(yum)官方已经停止维护，无法连接官方的软件源，因此需要修改yum.repos.d来改变软件源
![](https://cdn.nlark.com/yuque/0/2023/png/12484160/1701221414479-40e6fe7f-f1aa-410d-9a96-5a75d3d9d8af.png#averageHue=%23100e0e&clientId=u6a1e8d57-99ae-4&from=paste&id=u966146f1&originHeight=121&originWidth=505&originalType=url&ratio=1&rotation=0&showTitle=false&status=done&style=none&taskId=u8c709112-9c7a-430f-9389-c90c8c2b437&title=)
### 处理办法
按照顺序输入下列命令即可
#### 进入/etc/yum.repos.d目录
```bash
<!--more-->
cd /etc/yum.repos.d
```
#### 修改源链接
```
sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
```
#### 要将之前的mirror.centos.org 改成 vault.centos.org
```
sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
```

#### 更新软件源
```
sudo yum update 
```
![](https://cdn.nlark.com/yuque/0/2023/png/12484160/1701221485272-b646d908-cb9d-4d39-af60-8b524ef1d428.png#averageHue=%23060503&clientId=u6a1e8d57-99ae-4&from=paste&id=u0278c5f3&originHeight=112&originWidth=706&originalType=url&ratio=1&rotation=0&showTitle=false&status=done&style=none&taskId=u224fb611-29d0-4254-9093-25ce5cdf04b&title=)
