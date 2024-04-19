---
layout: post
title: Google Drive 百宝箱
tags:
  - 技术分享
categories:
  - 技术分享
abbrlink: ae8d3e92
date: 2020-07-05
---

![img](http://jiangjiawei.epizy.com/wp-content/uploads/2020/06/u3207433114120194597fm26gp0.png)

原项目地址：[gd-utils](https://github.com/iwestlin/gd-utils)

转载:[ikarosone](https://www.ikarosone.top/archives/195.html)

### 功能简介(原文)

##### 本工具目前支持以下功能：

- 统计任意（您拥有相关权限的，下同，不再赘述）目录的文件信息，且支持以各种形式（html, table, json）导出。
  支持中断恢复，且统计过的目录（包括其所有子孙目录）信息会记录在本地数据库文件中（gdurl.sqlite） 请在本项目目录下命令行输入 *./count -h* 查看使用帮助
  
- 拷贝任意目录所有文件到您指定目录，同样支持中断恢复。 支持根据文件大小过滤，可输入 *./copy -h* 查看使用帮助

- 对任意目录进行去重，删除同一目录下的md5值相同的文件（只保留一个），删除空目录。 命令行输入 *./dedupe -h* 查看使用帮助

- 在 config.js 里完成相关配置后，可以将本项目部署在（可正常访问谷歌服务的）服务器上，提供 http api 文件统计接口

- 支持 telegram bot，配置完成后，上述功能均可通过 bot 进行操作

  <!--more-->

**搭建过程需要注意的地方:**

https://drive.google.com/drive/folders/1Lu7Cwh9lIJkfqYDIaJrFpzi8Lgdxr4zT

需要注意的地方：

- 视频中省略了一个比较重要的步骤就是**从本地上传service account授权文件到项目的 sa 目录下**，tg机器人的所有操作都是通过sa授权的。
- 视频中**nginx的配置里，server_name就是你的二级域名，需要和cloudflare的设置一样**的（bot.xxxxx.xxx），我分开录的视频所以没做到一致。
- 还有省略的步骤就是注册域名和把域名托管到cloudflare了，这一步网上太多资料了，甚至也有免费注册（一年）域名的地方（ https://www.freenom.com/ ），具体教程大家搜搜看吧。
- tg_whitelist: [‘your_tg_username’]为你自己的username，不是写自己机器人的名字，是写自己的username，在登录账号的设置中查找，这个白名单的目的是只允许机器人执行白名单内用户的指令。

# 原理/思路

TG创建bot，要起一个服务支持BOT的功能， 所以需要配置webhook 让tg 和服务器建立连接。webhook 需要有HTTPS的外网域名并且修改DNS指向你所配置的服务器IP，这样就能保证TG的请求可以顺利到达并且验证BOT。 在服务器内部如果如果是单BOT， 可以直接用nodje 配合 PM2 直接起服务,然后修改server.js端口号443。 如果服务器上有多个服务，那么就需要用反向代理，反代简单说就是一个服务+映射规则 (ngnix或者apache后者其他都可以) 侦听80或者443端口，如果有指定的映射请求， 就转发到内部映射的各个服务。

例如

```
aaa.domain.com <=> locahost:3001
bbb.domain.com <=> locahost:3002
domain.com/ccc <=> localhost:3003
```

# 步骤

1. 需要去tg 创建一个bot，会得到token 和bot的tgurl

2. BOT服务：

   1. 服务器上clone 项目，安装node, npm install

   2. 如果需要配置多个BOT, clone不同目录, server.js里修改配置port，和config.js

   3. 安装PM2，在每个bot目录下 PM2 start server.js

   4. ```
      pm2 status
      ```

       确认服务跑起来了

      1. 如果没起来， 查log文件（见底部）

   5. curl 检查本地连接, curl 检查远端连接， not found 就对了

3. 外部连接

   1. 修改DNS，我是用cloudflare 把添加A record， 直接把静态IP 绑定
   2. 绑定以后， 本地开个terminal, ping 刚添加域名，直到解析的IP是你绑定的，这步确保连接上是畅通的

4. apache2开启SSL和反代

   1. 复制证书到任意位置
   2. 运行底部命令
   3. /etc/apache2/sites-available 下找到默认的.conf，或者自己建个conf也行
   4. 修改底部配置信息
   5. 保存重启 `service apache2 restart`

5. 剩下的就是配置和检查webhook，这里面也有不少坑，在反代配置文件部分。。记不清了。。

6. 如果一切顺利 /help 会弹出目录

```
pm2 部分

tail -200 ~/.pm2/logs/server-error.log
tail -200 ~/.pm2/logs/server-out.log

curl "localhost:23333"
curl "domain:23333"

SSL+反代

sudo a2enmod ssl
sudo a2enmod proxy
sudo a2enmod proxy_balancer
sudo a2enmod proxy_http


/etc/apache2/sites-available/xxx.conf

<VirtualHost *:443>
   SSLEngine on
   SSLProtocol all
   SSLCertificateFile {{CERT_DIR}}/{{domain.cer}}
   SSLCertificateKeyFile {{CERT_DIR}}/{{domain.key}}
   SSLCACertificateFile {{CERT_DIR}}/{{domain.ca.cer}}
   
   ServerName {{domain}}
   
   ProxyRequests Off
   ProxyPreserveHost On
   ProxyVia Full

   <Proxy *>
       Require all granted
   </Proxy>
   # 这里我用的是子目录映射方式。懒得再申请一个证书。。domain.com/ccc <=> localhost:3003
   ProxyPass /{{bot1url}}/ http://127.0.0.1:23334/  # bot1
   ProxyPassReverse /{{bot1url}}/ http://127.0.0.1:23334/ # bot1
   ProxyPass /{{bot2url}}/ http://127.0.0.1:23333/ # bot2
   ProxyPassReverse /{{bot2url}}/ http://127.0.0.1:23333/ # bot2
</VirtualHost>


something for verify and DEBUG

Apache command:
service apache2 restart
service apache2 stop
service apache2 status
service apache2 reload
tail -100 /var/log/apache2/error.log


验证一下SSL:
https://www.ssllabs.com/ssltest/analyze.html 确保Trusted和In trust store是绿的（反正我这两个绿的就TG就能找到的到）

SET webhook

curl -F "url=https://{{domain}}/{{bot1url}}/api/gdurl/tgbot" 'https://api.telegram.org/bot{{BOT_TOKEN}}/setWebhook'

delete webhook
curl -F "url=" https://api.telegram.org/bot{{BOT_TOKEN}}/setWebhook


check webhook
curl "https://api.telegram.org/bot{{BOT_TOKEN}}/getWebhookInfo"
```

[![avatar](https://github.com/vitaminx/gd-utils/raw/master/doc/bot-worked.png)](https://github.com/vitaminx/gd-utils/blob/master/doc/bot-worked.png)

# Reference Link

https://core.telegram.org/bots

https://core.telegram.org/bots/api

https://www.jianshu.com/p/ca804497afa0

## 一键安装脚本

- 安装机器人需准备好以下四个条件：
  - 在Telegram上注册好机器人并取得并记录下该机器人TOKEN
  - 一个域名在cloudflare解析到该机器人所在VPS的IP
  - 向机器人@userinfobot获取个人TG账号ID并记录
  - 注册好一个Google team drive加入sa并记录下该盘ID
- 准备好以上四个条件后，复制以下全部内容粘贴到VPS命令行窗口回车即可
  - gdutils项目一键部署脚本（包括“查询转存”和“TG机器人”两部分）`bash -c "$(curl -fsSL https://raw.githubusercontent.com/vitaminx/gd-utils/master/gdutilsinstall.sh)"`
- gdutils项目一键部署脚本之“转存查询部分”`bash -c "$(curl -fsSL https://raw.githubusercontent.com/vitaminx/gd-utils/master/gdutilscsinstall.sh)"`
- gdutils项目一键部署脚本之“TG机器人部分”`bash -c "$(curl -fsSL https://raw.githubusercontent.com/vitaminx/gd-utils/master/gdutilsbotinstall.sh)"`
- 安装过程中需要输入一下四个参数：
  - 机器人TOKEN：这个在Telegram里面找“@BotFather”注册即可获得
  - Telegram用户ID：在Telegram里面向机器人@userinfobot发送消息即可获得
  - Google team drive ID：即为你转存文件的默认地址，脚本强制要求写谷歌团队盘ID
  - 域名：你在cloudflare上解析到VPS的域名（格式：abc.34513.com）
  - 脚本安装问题请信息发给TG：onekings 或 [vitaminor@gmail.com](mailto:vitaminor@gmail.com)
  - 系统使用问题（如无法转存、重启连不上机器人等等）请联系项目作者@vegg
- 测试可用完美安装系统：
  - Centos 7/8
  - debian 9/10
  - ubuntu 16.04/18.04/19.10/20.04

**检查没有权限的json文件！**

以下是解决办法：

- 在项目目录下，执行 `git pull` 拉取最新代码
- 执行 `./validate-sa.js -h` 查看使用说明
- 选择一个你的sa拥有阅读权限的目录ID，执行 `./validate-sa.js 你的目录ID`
- 修改配置文件的`pm2 reload server` 重启下进程

示例nginx配置：

```
server {
  listen 80;
  server_name your.server.name;

  location / {
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_pass http://127.0.0.1:23333/;
  }
}
```

安装过程中需要输入一下四个参数：

- 机器人TOKEN：这个在Telegram里面找“@BotFather”注册即可获得
- Telegram用户ID：在Telegram里面向机器人@userinfobot发送消息即可获得
- Google team drive ID：即为你转存文件的默认地址，脚本强制要求写谷歌团队盘ID
- 域名：你在cloudflare上解析到VPS的域名（格式：abc.34513.com）

#### 安装宝塔面板:

###### **Centos安装命令**

```
yum install -y wget && wget -O install.sh http://download.bt.cn/install/install_6.0.sh && sh install.sh
```

###### **Ubuntu/Deepin安装命令**

```
wget -O install.sh http://download.bt.cn/install/install-ubuntu_6.0.sh && sudo bash install.sh
```

###### **Debian安装命令：**

```
wget -O install.sh http://download.bt.cn/install/install-ubuntu_6.0.sh && bash install.sh
```

安装好宝塔面板后，根据提示安装Ngnix环境, 然后在宝塔面板软件管理安装PM2管理器，安装好会自带node.js。

![img](https://www.ikarosone.top/wp-content/uploads/2020/06/PM2.5-1024x403.jpg)![img](https://www.ikarosone.top/wp-content/uploads/2020/06/%E6%89%B9%E6%B3%A8-2020-06-28-130246.jpg)

在宝塔里新建一个网站，填写你的域名(需要提前解析好你的域名！)使用宝塔自带的一申请SSL证书。

- Telegram Bot API 提供了两种方式， webhook 和 long polling，目前项目只支持 webhook 方式。
- webhook 方式必须要用HTTPS 也就是需要准备**个人域名**和**一个有效证书**（选这cloudflare的ssl，解析到cloudflare）
- 证书一定要单独域名证书(泛域名证书不能用)

需要先将其解析到cloudflare

![img](http://jiangjiawei.epizy.com/wp-content/uploads/2020/07/image-1024x213.png)

![img](https://www.ikarosone.top/wp-content/uploads/2020/06/%E6%89%B9%E6%B3%A8-2020-06-28-130923.jpg)

SSH连接终端克隆项目到本地

```
git clone https://github.com/iwestlin/gd-utils && cd gd-utils
```

#### 安装依赖

```
npm i
```

如果报错信息里有`Error: not found: make`之类的消息，说明你的命令行环境缺少make命令，执行安装make

```
sudo apt-get install make//安装make
rm -rf /root/gd-utils/node_modules//删除node_modules
npm i//重新安装依赖
```

如果以上命令还是出错，可以再次删除/root/gd-utils目录下的node_modules，并执行以下命令

```
rm -rf /root/gd-utils/node_modules//删除node_modules
npm install --unsafe-perm=true --allow-root
```

**npm: command not found**
重新安装nodejs
sudo yum install nodejs

#### Service Account 配置

强烈建议使用service account（后称SA）, 获取方法请参见 [https://gsuitems.com/index.php/archives/13/](https://gsuitems.com/index.php/archives/13/#步骤2生成serviceaccounts) 获取到 SA 的 json 文件后，请将其拷贝到 `sa` 目录下(使用ftp或者命令)

****配置好 SA 以后，如果你不需要对个人盘下的文件进行操作，可跳过[个人帐号配置]这节，而且执行命令的时候，记得带上 `-S` 参数告诉程序使用SA授权进行操作。

#### 个人帐号配置

之前配置好rclone的，执行命令 cat /root/.config/rclone/rclone.conf 可以看到自己的client_id, client_secret 和 refresh_token 这三个变量，把这三个变量填入/root/gd-utils/config.js对应的项中 ，然后执行

***可使用https://goindex-quick-install.glitch.me/获取client_id, client_secret 和 refresh_token 这三个变量

```
node check.js
```

如果命令返回了你的谷歌硬盘根目录的数据，说明配置成功，主要是检查sa权限问题。

![img](https://www.ikarosone.top/wp-content/uploads/2020/06/%E6%89%B9%E6%B3%A8-2020-06-28-140950-1024x540.jpg)

#### Bot配置

首先在 https://core.telegram.org/bots#6-botfather 根据指示拿到 bot 的 token，然后填入 config.js 中的 `tg_token` 变量，还有不要忘记填入**自己的电报用户名(t.me/username)非创建的机器人的**,记得删除[]格式为tg_whitelist: ‘t.me/username’

**如果你修改了代码中的配置，需要 `pm2 reload server` 才能生效**。

![img](https://www.ikarosone.top/wp-content/uploads/2020/06/%E6%89%B9%E6%B3%A8-2020-06-28-141547.jpg)

回到宝塔面板，在安全选项中添加23333端口放行。

![img](https://www.ikarosone.top/wp-content/uploads/2020/06/%E6%89%B9%E6%B3%A8-2020-06-28-141923.jpg)

然后在PM2管理器中添加以下项目自动运行。

![img](https://www.ikarosone.top/wp-content/uploads/2020/06/%E6%89%B9%E6%B3%A8-2020-06-28-141846.jpg)

这时候回到安全选项可以看到23333端口正在使用中如果显示未使用则没有启动成功。

最后在网站配置里添加反向代理，站点就配置完成。

![img](http://jiangjiawei.epizy.com/wp-content/uploads/2020/07/image-1-1024x443.png)



回到终端执行以下命令（请将YOUR_WEBSITE_URL替换成你的网址）

```
curl 'YOUR_WEBSITE_URL/api/gdurl/count?fid=124pjM5LggSuwI1n40bcD5tQ13wS0M6wg'
```

如果返回了这样的文件统计，说明部署成功了

![img](https://www.ikarosone.top/wp-content/uploads/2020/06/%E6%89%B9%E6%B3%A8-2020-06-28-143247.jpg)

最后，在命令行执行（请将[YOUR_WEBSITE]和[YOUR_BOT_TOKEN]分别替换成你自己的网址和bot token）

```
curl -F "url=YOUR_WEBSITE/api/gdurl/tgbot" 'https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook'
```

这样，就将你的服务器连接上你的 telegram bot 了，试着给bot发送个 `/help`，如果它回复给你使用说明，那就配置成功了。

![img](https://www.ikarosone.top/wp-content/uploads/2020/06/%E6%89%B9%E6%B3%A8-2020-06-28-143841-1024x320.jpg)

教程地址：
https://www.ikarosone.top/archives/195.html
https://github.com/iwestlin/gd-utils
https://github.com/iwestlin/gd-utils/blob/master/doc/tgbot-appache2-note.md