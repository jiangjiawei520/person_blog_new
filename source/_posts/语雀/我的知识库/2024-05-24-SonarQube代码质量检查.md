---
layout: post
title: SonarQube代码质量检查
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "Grbk@2024"
typora-root-url: ./..
date: 2024-05-24 10:45:56
---
服务端

◆进入条件：

    1、准备Java环境，这里略去配置

    2、需要安装MySQL (支持数据库种类见sonar.properties)，这里略去配置
<!--more-->

    3、sonar [https://docs.sonarqube.org](https://docs.sonarqube.org)

◆数据库配置：

     1、创建sonar数据库

     2、选择conf/sonar.properties文件，配置数据库设置，默认已经提供了各类数据库的支持，这里选择MySQL数据库，默认已经准备了支持各种数据库，只需将MySQL注释部分去掉，顺便改了sonarQube的端口sonar.web.port=1011
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1624516094902-c9d08d2d-1346-4a80-9abd-f9e2d1c3836e.png#align=left&display=inline&height=481&originHeight=481&originWidth=1335&size=0&status=done&style=none&width=1335)

> sonar.jdbc.url=jdbc:mysql://localhost:1010/sonar?useUnicode=true&characterEncoding=utf8&rewriteBatchedStatements=true&useConfigs=maxPerformance
> sonar.jdbc.driver=com.mysql.jdbc.Driver
> sonar.jdbc.username=root
> sonar.jdbc.password=root

◆sonar

将下载的soar安装包后，解压，随意放置一个地方

   注：JDK的环境和系统环境，要对应，我是windows系统，JDK位64位，选windows-x86-64

进入bin目录后，点击SonarStart.bat，页面输入http://localhost:1011/，进入页面，配置成功

客户端

前面已经说了客户端可以通过IDE插件、Sonar-Scanner插件、Ant插件和Maven插件方式进行扫描分析，这一节先记录Sonar-Scanner扫描

◆下载sonar-scanner解压，将bin文件加入环境变量path中如我的路径E:\sonar\sonar-scanner\bin将此路径加入path中
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1624516124418-522513d2-e65c-4d18-8fcd-f50c511deb64.png#align=left&display=inline&height=444&originHeight=444&originWidth=404&size=0&status=done&style=none&width=404)

◆修改sonar scanner配置文件， conf/sonar-scanner.properties。根据数据库使用情况进行取消相关的注释即可,同时需要添加数据库用户名和密码信息，即配置要访问的sonar服务和mysql服务器地址
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1624516129045-89785bbe-9ea5-4d75-9df4-ad1b0f8cb4b1.png#align=left&display=inline&height=515&originHeight=515&originWidth=897&size=0&status=done&style=none&width=897)

◆创建sonar-project.properties文件，以java工程为例在工程根目录下新建立一个sonar-project.properties配置文件
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1624516133044-0c204240-13c9-4626-b1d4-38cb80de43ac.png#align=left&display=inline&height=156&originHeight=156&originWidth=464&size=0&status=done&style=none&width=464)

◆开始scanner，只需三步，即可完成

  1、打开CMD命令行，

  2、cd进入你的工作空间，某个工程的代码路径，

  3、敲入sonar-scanner，即可进行分析

◆结果展示，分析完后进入http://localhost:1011/，projectKey点击你分析的工程，查看分析结果




一 . SonarQube代码质量检查工具简介
Sonar (SonarQube)是一个开源平台，用于管理源代码的质量.

Sonar 不只是一个质量数据报告工具，更是代码质量管理平台。

支持Java, C#, C/C++, PL/SQL, Cobol, JavaScrip, Groovy 等等二十几种编程语言的代码质量管理与检测。
Sonar可以从以下七个维度检测代码质量，而作为开发人员至少需要处理前5种代码质量问题。

> 1. 不遵循代码标准
>   sonar可以通过PMD,CheckStyle,Findbugs等等代码规则检测工具规范代码编写。
> 2. 潜在的缺陷
>   sonar可以通过PMD,CheckStyle,Findbugs等等代码规则检测工具检 测出潜在的缺陷。
> 3. 糟糕的复杂度分布
>   文件、类、方法等，如果复杂度过高将难以改变，这会使得开发人员 难以理解它们, 且如果没有自动化的单元测试，对于程序中的任何组件的改变都将可能导致需要全面的回归测试。
> 4. 重复
>   显然程序中包含大量复制粘贴的代码是质量低下的，sonar可以展示 源码中重复严重的地方。
> 5. 注释不足或者过多
>   没有注释将使代码可读性变差，特别是当不可避免地出现人员变动 时，程序的可读性将大幅下降 而过多的注释又会使得开发人员将精力过多地花费在阅读注释上，亦违背初衷。
> 6. 缺乏单元测试
>   sonar可以很方便地统计并展示单元测试覆盖率。
> 7. 糟糕的设计

>   通过sonar可以找出循环，展示包与包、类与类之间的相互依赖关系，可以检测自定义的架构规则 通过sonar可以管理第三方的jar包，可以利用LCOM4检测单个任务规则的应用情况， 检测藕合。


通过以下介绍SonarQube的安装、使用说明。

为什么要选择sonarQube?
个人使用之后认为 : sonarQube的优势如下(相比于阿里编码规约这种市面上常见类似软件):

1. 更加优秀的图形化界面

基本上通过界面就可以对自己项目的代码状况一目了然

2. 可以查询出其它软件难以定位到的问题

比如 : 可能导致空指针异常的问题 (对象在进行使用前没有加空的判断)
       可能导致内存泄漏的问题, 在try catch 块里面,直接使用e.printStackTrace()将堆栈信息打印到内存的
       可能导致的漏洞 : 成员变量使用public定义的
       还有诸如 : 流等未关闭或者是非正常关闭都能够检测出来!
       功能非常强大!!

二. 安装：
2.1 安装SonarQube web server
1.  首先确保安装了jdk1.8 +
2.  到此链接 [https://www.sonarqube.org/downloads/](https://www.sonarqube.org/downloads/)
下载sonalqube(下载社区版,是开源的),
我下载的是当前最新版本 7.3 
并解压,解压完之后的目录如下 :


3. 到解压目录的bin\windows-x86-64(我的是64位的)目录下:
双击StartSonar.bat文件 启动SonarQube

4. 到浏览器界面,输入 : http://localhost:9000 
// 能够进入界面证明安装成功

2.2 安装数据库
1. 版本要求:

在conf目录下的sonar.properties文件下:
有这样一行配置 : 
#----- MySQL >=5.6 && < 8.0

所以, mysql版本过高的话,要降级!! 比如说我... 用的就是8.0.11版本的

附 : mysql 8.0.11 版本卸载
1. 关闭mysql服务 
net stop mysql
2. 删除mysql
sc delete mysql
3. 删除mysql的目录文件, 我直接把mysql安装目录整个删除了
4. 将mysql的环境变量清空

然后在下载安装一个合适版本的即可

2. 为sonarqube 创建一个数据库
create database 数据库名;  

3. 创建sonarqube用户并进行授权

CREATE USER 'username'@'host' IDENTIFIED BY 'password'; // 创建用户并设置密码
// username 为创建的用户名
host为对应的主机地址,本地就是localhost
password为设置的密码

GRANT ALL ON *.* TO '用户名'@'localhost'; //对用户进行授权操作

4. 修改SonarQube配置文件,添加Mysql相关配置
sonar.jdbc.url=jdbc:mysql://localhost:3306/sonarqube?useUnicode=true&characterEncoding=utf8&rewriteBatchedStatements=true&useConfigs=maxPerformance&useSSL=false
sonar.jdbc.username=用户名  // 刚刚创建的sonarQube用户
sonar.jdbc.password=密码   // 创建用户对应的密码
sonar.sorceEncoding=UTF-8 // 设置编码格式为UTF-8

2.3 重新启动服务端
1. 退出 SonarQube 服务端
在之前弹出的cmd窗口执行ctrl + c,
弹出来的提示选择Y,退出SonarQube服务

2.  双击StartSonar.bat文件, 重新启动SonarQube
这次因为要进行数据库的初始化操作,所以需要的时间可能稍微久一点

3. 启动成功后,浏览器输入 : http://localhost:9000 进入界面

4. 登录 

点击界面右上角的登录按钮, 进行登录 :
初始的账户名 : admin
初始的密码  :  admin

如上 , SonarQube的安装已经OK!

附 : 一些关键配置的修改,如 主机地址,context,端口号等:
通常情况下使用默认的配置即可!
文件 /conf/sonar.properties
#sonar.web.host=0.0.0.0 
#sonar.web.context=
#sonar.web.port=9000

三. 使用
3.1. 安装必要的插件 (最重要的是汉化包)
点击 导航栏的 config, 选择应用市场
搜索 Chinese pack, 点击install进行安装

安装成功后, 重启 SonarQube !

如下图 : 进入到了很友好的中文界面!
进入主页后，默认为英文页面。安装中文插件可以让页面以中文显示。
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1624513975044-b9f622c6-5120-4468-967a-89bd29b69536.png#align=left&display=inline&height=946&originHeight=946&originWidth=1920&size=0&status=done&style=none&width=1920)
若上述方法安装中文插件安装不上，可以单独进行插件的安装。首先找到插件，点击HomePage进入插件主页。
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1624513986377-7b865475-b3ad-4faa-aee7-16c69e619a79.png#align=left&display=inline&height=484&originHeight=570&originWidth=1413&size=0&status=done&style=none&width=1200)根据合适的Sonar版本，选择适合的中文插件版本。我的是Sonar 6.5 选择1.17版本。点击图中标出的链接进行选择下载。
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1624514010576-e9cd270b-e233-45b7-973b-04d688a6006b.png#align=left&display=inline&height=782&originHeight=782&originWidth=1480&size=0&status=done&style=none&width=1480)


进入链接后，点击Tags，进行版本选择。
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1624514014671-c2261716-ad12-4720-91b7-9f12773a1674.png#align=left&display=inline&height=929&originHeight=929&originWidth=1662&size=0&status=done&style=none&width=1662)


找到指定版本后点击进入详情页面，进行jar包下载。
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1624514019004-80a06857-185f-4e11-b9b0-ed23d8e6b347.png#align=left&display=inline&height=557&originHeight=557&originWidth=1227&size=0&status=done&style=none&width=1227)


将下载后的jar包，传到Sonar目录中的\extensions\plugins下
![](https://cdn.nlark.com/yuque/0/2021/png/12484160/1624514022885-79b0e274-0264-45ac-8bba-d137b1a322a8.png#align=left&display=inline&height=321&originHeight=321&originWidth=717&size=0&status=done&style=none&width=717)
重新启动Sonar。

3.2. 开始分析项目代码源代码
我是使用maven的方式进行分析
1
3.2.1 编辑maven 的settings.xml文件
 位置 $MAVEN_HOME/conf 
或者是 ~/.m2 
找到对应的位置添加以下配置代码：
我的maven版本是3.5.4 对应的文件是settings.xml
版本低一点的对应的文件可能是setting.xml
1
2
3
4
5
<settings>
	<pluginGroups>
  <pluginGroup>org.sonarsource.scanner.maven</pluginGroup>
	</pluginGroups>
	<profiles>
  <profile>
  	<id>sonar</id>
  	<activation>
    <activeByDefault>true</activeByDefault>
  	</activation>
  	<properties>
    <!-- Optional URL to server. Default value is http://localhost:9000 -->
    <sonar.host.url>
      http://localhost:9000
    </sonar.host.url>
  	</properties>
  </profile>
  </profiles>
</settings>
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
其中sonar.host.url 值就是 上文启动的sonar 服务器地址。
1
3.2.2 对maven项目进行分析
到项目所在的文件路径下: 

使用命令提示符或者是power shell执行 如下命令: 
mvn org.sonarsource.scanner.maven:sonar-maven-plugin:3.2:sonar

出现: BUILD SUCCESS 标识之后
刷新界面查看 :
1
2
3
4
5
6
7
3.3 配置分析参数
强制参数：
   
1. Server
  sonar.host.url  http://localhost:9000
2. Project Configuration
  sonar.projectKey    	Maven   <groupId>:<artifactId>
  sonar.sources      Maven 默认的源码路径
   
可以配置的参数：
1. Project identity
  sonar.projectName        项目名称
  sonar.projectversion  项目版本
 	
2. Authentication
  sonar.login                  分析该项目的用户名称
  sonar.password                分析该项目的用户密码
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
3.4. 程序员用户使用说明
SonarQube Web管理者通过配置和设置以下参数值对项目源代码进行：

复杂度、覆盖率、文档、重复、问题、可维护性、可靠性、安全性、大小等约束和规范。

sonar中的质量阈管理以下内容。

               复杂度
    	复杂度
    	复杂度/类
    	复杂度/文件
    	复杂度/方法
    覆盖率
    	分支覆盖
    	集成测试的新分支覆盖
    	新代码的分支覆盖率
    	覆盖率
    	新集成测试覆盖
    	新覆盖率
    	集成测试分支覆盖
    	集成测试覆盖
    	集成测试覆盖行
    	集成测试未覆盖分支
    	集成测试未覆盖行
    	代码覆盖率
    	集成测试的新行覆盖
    	新代码覆盖率
    	代码行
    	集成测试的新行覆盖
    	覆盖的新代码
    	总体分支覆盖率
    	总体新分支覆盖率
    	总体覆盖率
    	总体新覆盖率
    	总体代码覆盖率
    	总体新代码覆盖率
    	总体覆盖的新行数
    	总体未覆盖分支
    	总体未覆盖的新分支
    	总体未覆盖代码
    	总体未覆盖新行数
    	单元测试忽略数
    	未覆盖分支
    	集成测试未覆盖的新分支
    	未覆盖新分支
    	未覆盖的代码
    	集成测试未覆盖的行
    	未覆盖的新代码
    	单元测试持续时间
    	单元测试错误数
    	单元测试失败数
    	单元测试成功 (%)
    	单元测试数
    文档
    	注释行
    	注释 (%)
    	公共API
    	公共注释的API (%)
    	公共未注释的API
    重复
    	重复块
    	重复文件
    	重复行
    	重复行(%)
    问题
    	阻断违规
    	确认问题
    	严重违规
    	误判问题
    	提示违规
    	违规
    	主要违规
    	次要违规
    	新阻断违规
    	新严重违规
    	新提示违规
    	新违规
    	新主要违规
    	新次要违规
    	开启问题
    	重开问题
    	不修复的问题
    可维护性
    	新代码的技术债务
    	坏味道
    	达到可维护性A级所需的工作
    	新增坏味道
    	技术债务
    	技术债务比率
    	新代码技术债务比率
    	Management
    	Burned budget
    	Business value
    	Team size
    可靠性
    	Bugs
    	新增Bugs
    	可靠性修复工作
    	新代码的可靠性修复工作
    安全性
    	新增漏洞
    	安全修复工作
    	新代码的安全修复工作
    	漏洞
    大小
    	类
    	目录
    	文件
    	方法
    	生成的行数
    	生成的代码行数
    	行数
    	代码行数
    	项目
    	语句
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
3.5管理员使用手册
3.5.1 管理员配置管理
配置管理内容有：

配置
权限
项目
系统


3.5.2 管理员配置管理–系统
包含两部分内容分别为：

更新中心

系统信息

3.5.2.1 更新中心
方便管理插件、安装插件。


3.5.2.2 系统信息
系统信息就是现实SonarQube安装环境的配置变量和系统配置路径。

如下部分截图：


3.5.3 管理员配置管理–项目管理
包含两部分内容分别为：

SonarQube项目管理

SonarQube后台任务

3.5.3.1 SonarQube项目管理
创建、编辑、修改、删除(批量)SonarQube项目


3.5.3.2. SonarQube后台任务


3.5.4 管理员配置管理–权限管理
权限管理内容包含：

用户
群组
全局权限
项目权限
权限模板
3.5.4.1. 用户


3.5.4.2. 群组


3.5.4.3. 全局权限


3.5.4.4. 项目权限


3.5.4.5. 权限模板


3.5.5 管理员配置管理–配置管理
配置管理模块又包含以下管理：

通用设置(重点介绍)
Custom Metrics(自定义指标)
默认仪表盘
3.5.5.1 通用配置
管理的模块有：

Java：配置检查的java源文件及静态代码检查规范检查
SCM：配置软件控制器。上文已经提到的配置项。比如：svn、git等等
SonarJs：雷同java文件检查、
技术债务：
授权
排除
权限
通用
3.5.5.2 通用配置–技术债
名词解释技术债：

维基百科上的解释：维基百科上的解释

此处配置决定和影响项目仪表盘显示、影响数据库数据。


3.5.5.3 通用配置–排除
可以配置通配符排除一下影响代码项目：

代码覆盖率
检查文件
重复行数代码
issues
具体配置请参考具体配置项目。



3.5.5.4 通用配置–通用
有以下配置项目：

通用

对比视图

数据库清理器

界面外观

邮件

重复
交叉项目重复检测
问题

四 .参考资料
使用 Sonar 进行代码质量管理
SonarQube官方文档
安装最新版本SonarQube环境要求
SonarQube是什么
SonarQube代码质量管理平台安装与使用
通过sonar了解你的项目
SonarQube7.3安装和使用说明
