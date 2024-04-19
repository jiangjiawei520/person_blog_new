---
layout: post
title: 'AutoRclone教程:如何突破Google Drive每日750G限制？'
tags:
  - 技术分享
categories:
  - 技术分享
abbrlink: e2b959ee
date: 2020-07-11
---



## AutoRclone可以干什么？

可以方便快捷地：

- 从Google Drive到Team Drive
- 从Team Drive到Google Drive
- 从本地到 Team Drive，
- 从公共分享目录到 Team Drive，
- 再或者从 Team Drive 到 Team Drive。

换句话说，就是实现 Team Drive，Google Drive，本地之间的互拷，以及把分享的文件复制到，或者说真正地转存到自己想要的地方。

<!--more-->

## 说明

- 以下，我们将Google Drive简称GD，将Team Drive简称TD，将服务账号(Service Account)简称为SA。
  何为文件夹/文件/TD的id？
- 例如，文件夹/文件/TD的网址为`drive.google.com/drive/u/0/folders/10y_9ucYQyvfxuexDKiOY2pp1CXlXy`
  那么，它的id即为`10y_9ucYQyvfxuexDKiOY2pp1CXlXy`。如果出现形如 的后缀，请务必删除。

```
大致步骤:
先建立自己的团队盘:谷歌团队无限盘申请
管理地址：https://drive.google.com/drive/u/0/shared-drives
1、安装Python及主程序：Python、Rclone(https://rclone.org/downloads/)、AutoClone(https://github.com/xyou365/AutoRclone)、科学工具
2、生成SA
3、管理SA
4、开始运行
```

## 步骤1 相关依赖

### 安装Python。

对于 Win­dows 系统来说，[在此](https://www.python.org/downloads/)找到你的安装包，直接下载并运行即可。
对于 Linux 系统来说，一般自带 Python，你可以试试输入 python 或者 python3 看看有没有反应，如果有，请继续下一步。
如果没有，则 De­bian/​Ubuntu 输入

```
apt update
apt install python3-pip git screen -y
```

Cen­tOS 输入

```
yum update
yum install python3-pip git screen -y
```

### Windows安装python依赖及主程序

进入 [AutoRclone](https://github.com/xyou365/AutoRclone) 的 Github 项目页，然后点击屏幕右边的绿色 Clone or Down­load 下载代码，如图所示。

[![img](http://panoan.top/usr/uploads/2020/03/289240866.png#vwid=1020&vhei=338)](http://panoan.top/usr/uploads/2020/03/289240866.png#vwid=1020&vhei=338)

接着你需要下载[Rclone](https://rclone.org/downloads/)，选择合适的Windows系统即可。
之后需要将Rclone添加进环境变量。

##### Windows 10 和 Windows 8

1. 在“搜索”中，搜索以下内容并进行选择：控制面板
2. 单击高级系统设置链接。
3. 单击环境变量。在系统变量部分中，找到并选择 PATH 环境变量。单击编辑。如果 PATH 环境变量不存在，请单击新建。
4. 在编辑系统变量（或新建系统变量）窗口中，指定 PATH 环境变量的值。单击确定。通过单击确定关闭所有剩余窗口。

##### Windows 7

1. 在桌面上右键单击计算机图标。
2. 从上下文菜单中选择属性。
3. 单击高级系统设置链接。
4. 单击环境变量。在系统变量部分中，找到并选择 PATH 环境变量。单击编辑。如果 PATH 环境变量不存在，请单击新建。
5. 在编辑系统变量（或新建系统变量）窗口中，指定 PATH 环境变量的值。单击确定。通过单击确定关闭所有剩余窗口。

##### Windows XP

1. 选择开始，再选择控制面板。双击系统，然后选择高级选项卡。
2. 单击环境变量。在系统变量部分中，找到并选择 PATH 环境变量。单击编辑。如果 PATH 环境变量不存在，请单击新建。
3. 在编辑系统变量（或新建系统变量）窗口中，指定 PATH 环境变量的值。单击确定。通过单击确定关闭所有
   注意：
4. PATH 环境变量的值即为你所安装的Rclone的目录，如你的Rclone.exe在目录D:\Rclone\Rclone.exe， 则你的 PATH 环境量的值即为D:\Rclone
5. 设置完成后请按组合键Win+R，输入cmd并回车以打开命令提示符，输入rclone，若返回很长的一串文字，则表示已经设置成功。
6. 在以下的运行中，每次运行cmd均需设置代理。代理方法不能在此讲述，请自行搜索。
7. 欲检验是否成功代理，下载[curl](https://curl.haxx.se/download.html)并安装Windows版本，同样设置环境变量，输入`curl https://www.google.com`若出现html的等字样，则表示已成功设置代理。

假设我们已经下载好并且解压好的 Au­toR­clone 在目录 D:/Au­toR­clone 下
在命令行中，输入

```
cd D:/AutoRclone
pip3 install -r requirements.txt
```

Win­dows 中可能显示为 D:\Au­toR­clone，即斜杠方向相反。无需刻意选择，在 cmd 中，两者都是可行的。
此举是为了使你的命令行在 D:/​Au­toR­clone 下进行相关操作。(形象化的说法：先把你的大刀移到 Au­toR­clone 面前！)

### Linux安装python依赖及主程序

#### 对于Debian/Ubuntu系统

只需输入如下命令：

```
sudo apt-get install screen git && curl https://rclone.org/install.sh | sudo bash
sudo git clone https://github.com/xyou365/AutoRclone && cd AutoRclone && sudo pip3 install -r requirements.txt
```

#### 对于CentOS系统

输入

```
yum install curl
yum install screen
yum install git
curl https://rclone.org/install.sh | sudo bash
sudo git clone https://github.com/xyou365/AutoRclone && cd AutoRclone && sudo pip3 install -r requirements.txt
```

## 步骤2 生成SA

### 为什么要生成SA呢？

我们每一个账户都有 750G 的限制，Au­toR­clone 目的在于当一个账号限额达到之后，切换至下一个。
服务账户就是这样的账户，在服务账户的帮助下我们无需大量创建 Google 账户来达到切换的目的。
你可以把服务账户理解为你的小兵，小兵有了，自然不需要一个又一个的将军了。

```
*提示 timeout 踩了好久好久的坑（Shadowsocks）
pathon3只能使用http请求
用这个来测试是否已经出去了。
curl -vv http://www.google.com
首先 set 一个变量只能set一项 已经规定http_proxy=http了 就不能 规定http_proxy=socks5
所以通常我只用下面两项
set http_proxy=http://127.0.0.1:1080
set https_proxy=http://127.0.0.1:1080
最后 路由器的http_proxy不是7890 ，强行在cmd规定http_proxy，也会报错。
```

### 如何生成Service Account

#### 开启Drive API

首先开启 [Drive API](https://developers.google.com/drive/api/v3/quickstart/python) 并将 cre­den­tials.json 保存到你的 Au­toR­clone 目录下面，如图所示

[![img](https://img.vim-cn.com/46/a41db9c3b2b25ef86f5c55db3778544d854580.jpg#vwid=740&vhei=601)](https://img.vim-cn.com/46/a41db9c3b2b25ef86f5c55db3778544d854580.jpg#vwid=740&vhei=601)

DOWNLOAD键你总该认识吧！

**以下步骤如果输入 python3 没有反应，请输入 python 或者 py3**
如果你之前没创建过项目，直接运行

```
python3 gen_sa_accounts.py --quick-setup 5
```

- 创建6个项目（项目0到项目5）
- 开启相关的服务
- 创建600个service accounts（6个项目，每个项目100个）
- 将600个service accounts的授权文件下载到accounts文件夹下面

#### 创建Service Account

如果你已经有 N 个项目，现需要创建新的项目并在新的项目中创建 ser­vice ac­counts，直接运行

```
python3 gen_sa_accounts.py --quick-setup 2 --new-only
```

- 额外创建2个项目（项目N+1到项目N+2）
- 开启相关的服务
- 创建200个service accounts（2个项目，每个项目100个）
- 将200个service accounts的授权文件下载到accounts文件夹下面

如果你想用已有的项目来创建 ser­vice ac­counts（不创建新的项目），直接运行

```
python3 gen_sa_accounts.py --quick-setup -1
```

注意这会覆盖掉已有的 ser­vice ac­counts
顺利完成后，Au­toR­clone 文件下面的 ac­counts 文件夹下会有很多的 json 文件。

***推荐使用\*** `python3 gen_sa_accounts.py --quick-setup 1`***一个项目 = 100 个 sa=750GB\*100=75T，一天 75T 足够了\***
**并且，随意创建多个项目的话，需要一个月后才能删除，且每个账户均有项目个数上限。**

## 步骤3 管理SA

好了，现在你已经创建好了 SA (你的小兵们)。
你可以在 [Google APIs](https://console.developers.google.com/apis/dashboard) 看到你的项目及 SA。
注意：

1. 每个项目里有100个SA
2. 点击此处可以看到你某个项目下的SA的秘钥及地址
3. 点击此处可以看到你的全部项目
4. 有的人可能想问，怎么我只有两个项目200个SA，却有500个json？
   那是因为你浏览项目的时候需要点击“全部”。

[![img](http://panoan.top/usr/uploads/2020/03/3556380987.png#vwid=235&vhei=126)](http://panoan.top/usr/uploads/2020/03/3556380987.png#vwid=235&vhei=126)

有两种方式可以管理你的 SA。

### 方法一：直接加入团队盘

此方法极度不推荐，仅对本地上传比较方便。**极度不推荐！**
将 ser­vice ac­counts 加入到源 Team Drive

```
python3 add_to_team_drive.py -d SharedTeamDriveSrcID
```

将 ser­vice ac­counts 加入到目标 Team Drive

```
python3 add_to_team_drive.py -d SharedTeamDriveDstID
```

### 方法二：利用Group管理

我们这里用到了 Google Groups。

> Of­fi­cial lim­its to the mem­bers of Team Drive (Limit for in­di­vid­u­als and groups di­rectly added as mem­bers is 600).
> 每个 Google Group 只能添加 600 个账户

### 对于G Suite管理员

按照[官方步骤](https://developers.google.com/admin-sdk/directory/v1/quickstart/python)开启 Di­rec­tory API，将生成的 json 文件保存到 cre­den­tials 文件下。
在[控制面版](https://support.google.com/a/answer/33343?hl=en)里面创建一个群组，创建好你会获得一个类似域名邮箱的地址 sa@your­do­main.com
利用 API 将 ser­vice ac­counts 加入 Google Groups

```
python3 add_to_google_group.py -g sa@yourdomain.com
```

其中 `sa@yourdomain.com` 中的 sa 可以为你想要的任何名称。
如果想看参数的具体含义，直接运行 python3 ad­d_­to_­google_­group.py -h

### 对于普通Google账号

直接创建一个 [Google Group](https://groups.google.com/) 然后手动地将 ser­vice ac­counts 对应的邮箱地址（可以在步骤三中的注意 2 处找到，复制下来到 ex­cel 里整理一下即可）挨个加进去。但每次只能加 10 个（以英文逗号 “,” 作为两个邮箱之间的间隔），每 24 小时只能加 100 个。
group 有一个邮箱地址，请牢记，接下来需要用到

## 步骤四：开始运行

你的准备工作已经全部做好。开始运行吧！

#### 拷贝

```
python3 rclone_sa_magic.py -s SourceID -d DestinationID -dp DestinationPathName -b 1 -e 600
```

如果想看参数的具体含义，直接运行 `python3 rclone_sa_magic.py -h`
`-b` 是你开始的 SA，`-e` 是你结束的 SA。比如我今天已经把前十个的限额用满了，那我 `-b 11` 即可。
每个服务账号的限额在二十四小时后重置。
特别地，如果想多开，请用 – p 参数给不同的复制任务指定不同的端口
如果发现拷贝内容明显少于源 Team Drive 里面的内容，那么你可能碰到 Bug 了，请给上运行参数再加上 `--disable_list_r`
如果你一开始就碰到了

```
Failed to rc: connection failed: Post http://localhost:5572/core/stats: dial tcp :5572: connectex: No connection could be made because the target machine actively refused it.
```

那么可能是权限或者路径导致 Rclone 任务都没跑起来，请观察日志文件 log_r­clone.txt，并请先将 Au­toR­clone 目录下的 rclone.conf 复制到 Rclone 目录下，并结合如下简单命令检查出原因 `rclone --config rclone.conf size --disable ListR src001:`，`rclone --config rclone.conf size --disable ListR dst001:`

#### 上传

```
python3 rclone_sa_magic.py -sp YourLocalPath -d DestinationID -dp DestinationPath
```