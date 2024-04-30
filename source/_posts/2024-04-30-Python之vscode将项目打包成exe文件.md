---
title: Python之vscode将项目打包成exe文件
tag:
  - python
categories:
  - python
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
abbrlink: b12f19ab
date: 2024-04-30 15:06:40
top:
---

#### 操作步骤

##### 1、打开VSCode并打开你的Python项目。

##### 2、在VSCode终端中安装`pyinstaller`：

```
pip install pyinstaller
```

##### 3、运行以下命令使用`pyinstaller`将Python项目打包成exe文件：

```
pyinstaller -F your_script.py --name=my_program
```

##### 其中`your_script.py`是你的Python脚本的文件名；my_program为生成的应用名称

##### 4、打包完成后，在你的项目目录中会生成一个`dist`文件夹，里面包含了打包后的可执行文件。

>   ****请注意，使用`pyinstaller`打包成exe文件时可能会遇到一些依赖项缺失或路径问题，你可能需要进行一些额外的配置。另外，如果你的项目有一些特殊的资源文件（如图片、配置文件等），你也需要确保这些资源文件能够被正确地打包进exe文件中。**** 

<!--more-->

#### 演示步骤

##### 1、打开VSCode并打开你的Python项目。

<img alt="" height="1200" src="/imgs/32340822a74047e3b51c3b9ad858c991.png" width="1200">

##### 2、在VSCode终端中安装`pyinstaller`：

```
pip install pyinstaller

```

##### <img alt="" height="1200" src="/imgs/423ed294b3064d28a988a77164cda1c2.png" width="1200">

>   我之前已经安装过了，所以显示的是下面的样子。 


<img alt="" height="1200" src="/imgs/b927321e516844f698be54e6cdcf02b8.png" width="1200">

##### 3、运行以下命令使用`pyinstaller`将Python项目打包成exe文件：  

```
pyinstaller -F your_script.py
```

<img alt="" height="1200" src="/imgs/d79d52bdf321469bbea4c2e19fc3b5ea.png" width="1200">

>   **打包完成 ** 


<img alt="" height="1200" src="/imgs/5969cef4ca4b49b1a4926b6925a54546.png" width="1200">

<img alt="" height="136" src="/imgs/22b6e1d144724b49be931c552ff5ad3c.png" width="706">

##### 4、打包完成后，在你的项目目录中会生成一个`dist`文件夹，里面包含了打包后的可执行文件。 

<img alt="" height="174" src="/imgs/7b171c11fb2f454b9c8bfe6785ed4ebc.png" width="391"> 

<img alt="" height="228" src="/imgs/86d32b54438641af876a1343e62de693.png" width="391">

<img alt="" height="372" src="/imgs/f7d9e2f5ed42439d92fc66ce6f4c212e.png" width="859">

#### 测试

>   **运行成功** 


<img alt="" height="784" src="/imgs/6e9b480bf7564e7583a33fb6e2d63eb6.png" width="1176">

<img alt="" height="253" src="/imgs/48f9f74d673c4a60a49ad9106ce8dd08.png" width="265">