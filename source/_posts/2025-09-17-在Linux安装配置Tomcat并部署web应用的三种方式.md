---
title: 在Linux安装配置Tomcat并部署web应用的三种方式
tag:
  - centos
categories:
  - tomcat
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
abbrlink: eed9a1f6
date: 2025-09-17 09:43:40
top:
---

系统版本：centos7.3版本 java版本：1.8



## 准备工作

1、java -version 检查是否有java环境，没有则需要去安装并配置到环境变量中。

2、下载tomcat包，下载地址：http://tomcat.apache.org/download-90.cgi

可以本地下载后上传到[服务器](https://cloud.tencent.com/product/cvm?from_column=20065&from=20065)上，也可以直接在服务器上使用wget命令下载，本案例直接使用wget命令下载 ：

>  [root@localhost~]# wget http://mirrors.tuna.tsinghua.edu.cn/apache/tomcat/tomcat-9/v9.0.11/bin/apache-tomcat-9.0.11.tar.gz

<!--more-->

## 安装Tomcat

1、新建tomcat存放的目录

```javascript
[root@localhost ~]# mkdir /usr/local/tomcat
```

2、拷贝下载好的 apache-tomcat-9.0.11.tar.gz 到 tomcat目录下

```javascript
[root@localhost ~]# cp apache-tomcat-9.0.11.tar.gz /usr/local/tomcat/
```

3、进入tomcat目录，并解压apache-tomcat-9.0.11.tar.gz

```javascript
[root@localhost ~]# cd /usr/local/tomcat/

[root@localhost tomcat]# tar -zxvf apache-tomcat-9.0.11.tar.gz
```

4、进入解压的tomcat包的bin目录，并启动tomcat

```javascript
[root@localhost tomcat]# cd /usr/local/tomcat/apache-tomcat-9.0.11/bin/

[root@localhost bin]# ./catalina.sh start

或：[root@localhost bin]# ./startup.sh
```

​    注: ./catalina.sh start 和 ./startup.sh 都能启动tomcat。使用 ./catalina.sh stop 或 ./shutdown.sh 停止tomcat。

5、浏览器访问并解决防火墙问题。

在浏览器使用ip进行访问（端口默认：8080），http://192.168.0.8:8080，可以看到tomcat的管理界面。

192.168.0.8 为服务器的ip地址，如果访问不了，有可能是服务器防火墙问题，8080端口被拦截了，于是需要打开8080端口，并保存重启防火墙：

```javascript
[root@localhost bin]# iptables  -I  INPUT  -p  tcp  --dport  8080  -j  ACCEPT  

[root@localhost bin]# /etc/init.d/iptables  save

[root@localhost bin]# /etc/init.d/iptables  restart
```

在server.xml配置中可以修改访问端口，<Connector port="8080" 修改成80端口，浏览器上就可以直接通过http://192.168.0.111 进行访问。

6、配置 tomcat 帐号密码权限（登陆使用Web管理界面）

修改tomcat下的配置文件 tomcat-users.xml

```javascript
[root@localhost ~]# vim /usr/local/tomcat/apache-tomcat-9.0.11/conf/tomcat-users.xml
```

在前添加以下代码：

```javascript
<role rolename="tomcat"/>
<role rolename="manager-gui"/>
<role rolename="admin-gui"/>
<role rolename="manager-script"/>
<role rolename="admin-script"/>
<user username="tomcat" password="tomcat" roles="tomcat,manager-gui,admin-gui,admin-script,manager-script"/>
```

注：username 和 password 则是登陆tomcat管理界面需要的账号密码。

:wq 保存退出，重启tomcat

浏览器访问：http://192.168.0.8:8080

可以通过 Manager App 管理已部署的项目。

点击进入 Manager App 需要账号密码，上面有设置。

## 三、Tomcat配置服务和自启动

1、Tomcat配置服务

新建服务脚本：

```javascript
[root@localhost ~]# vim /etc/init.d/tomcat
```

添加脚本内容：

```javascript
#!/bin/bash
# description: Tomcat7 Start Stop Restart
# processname: tomcat7
# chkconfig: 234 20 80

CATALINA_HOME=/usr/local/tomcat/apache-tomcat-9.0.11

case $1 in
        start)
                sh $CATALINA_HOME/bin/startup.sh
                ;;
        stop)
                sh $CATALINA_HOME/bin/shutdown.sh
                ;;
        restart)
                sh $CATALINA_HOME/bin/shutdown.sh
                sh $CATALINA_HOME/bin/startup.sh
                ;;
        *)
                echo 'please use : tomcat {start | stop | restart}'
        ;;
esac
exit 0
```

:wq 保存脚本。

执行脚本，启动、停止 和 重启服务。

启动：service tomcat start

停止：service tomcat stop

重启：service tomcat restart

2、Tomcat配置开机自启动

向chkconfig添加 tomcat 服务的管理

```javascript
[root@localhost ~]# chkconfig --add tomcat
```

设置tomcat服务自启动

```javascript
[root@localhost ~]# chkconfig tomcat on
```

查看tomcat的启动状态

```javascript
[root@localhost ~]# chkconfig --list | grep tomcat
```

状态如下：

[root@localhost ~]# chkconfig --list | grep tomcat

tomcat      0:off 1:off 2:on 3:on 4:on 5:on 6:off

关闭tomcat服务自启动：chkconfig tomcat off

删除tomcat服务在chkconfig上的管理：chkconfig --del tomcat

## 四、部署web项目（三种方式）

1、第一种方式 : 部署项目到webapps（不推荐）

进入tomcat下的webapps目录，并新建一个目录为web项目的主目录。

代码语言：javascript

```javascript
[root@localhost ~]# cd /usr/local/tomcat/apache-tomcat-9.0.11/webapps

[root@localhost webapps]# mkdir sam

[root@localhost webapps]# ls
docs  examples  host-manager  manager  ROOT  sam
```

sam 目录为项目的目录，现在把web项目打包出来的war拷贝并解压到sam目录下。

这里我直接用最简答的 index.html 来代替web项目war包作测试。

```javascript
[root@localhost sam]# ls
index.html
```

浏览器访问：http://192.168.0.8:8080/sam/index.html 既可访问到sam目录下的index.html

这种方式不被推荐，项目不好管理，而且需要链接加上项目名才能正常访问。

2、第二种方式：修改server.xml文件，配置[虚拟主机](https://cloud.tencent.com/product/lighthouse?from_column=20065&from=20065)

修改tomcat conf下的server.xml配置

```javascript
[root@localhost conf]# vim server.xml 
```

在Engine节点内添加 Host节点

```javascript
<Host name="www.sam.com">
      <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
             prefix="www.sam.com_access_log." suffix=".txt"
             pattern="%h %l %u %t "%r" %s %b" />
      <Context path="" docBase="/home/sam/site/com.sam.www" />
</Host>
```

name="www.sam.com"：指访问的[域名](https://cloud.tencent.com/product/domain?from_column=20065&from=20065)，所以需要你先拥有 sam.com 这个域名，并把 www.sam.com 映射到当前服务器上才能正常访问，本地测试可以通过修改本机host文件来做映射测试。

浏览器访问：http://www.sam.com:8080 能访问到 /home/sam/site/com.sam.www 下的项目。

注：www.sam.com为我个人域名，你需要自行注册域名，并做相应的ip映射。如果仅是本地测试，可以修改本机的host文件，添加记录：192.168.0.8 www.sam.com ，将web.sam.com的访问映射到192.168.0.8这台服务器中。

3、第三种方式：修改server.xml和Catalina，配置虚拟主机。

这种方式，我用 web.sam.com 这个项目为例。

修改tomcat conf下的server.xml配置

```javascript
 [root@localhost conf]# vim server.xml 
```

在Engine节点内添加 简单的Host节点，:wq 保存退出

```javascript
<Host name="web.sam.com"></Host>
```

进入tomcat conf下的Catalina目录

```javascript
[root@localhost conf]# cd /usr/local/tomcat/apache-tomcat-9.0.11/conf/Catalina
```

新建目录 web.sam.com （与server.xml中配置的host名称一样）

```javascript
[root@localhost Catalina]# mkdir web.sam.com
```

进入web.sam.com目录并新建ROOT.xml文件，添加相应的配置内容。

```javascript
[root@localhost Catalina]# cd web.sam.com/
[root@localhost web.sam.com]# vim ROOT.xml
```

ROOT.xml 文件添加以下内容:

```javascript
<?xml version="1.0" encoding="UTF-8"?>
<Context path="" docBase="/home/sam/site/com.sam.web" >

        <Valve className="org.apache.catalina.valves.AccessLogValve"
                directory="logs/com.sam.web"
                prefix="web.sam.com_localhost_access_log." suffix=".txt"
                resolveHosts="true"    
                pattern="%h %l %u %t "%r" %s %b" />
         
</Context>
```

 :wq保存退出。

同样，新建项目目录 /home/sam/site/com.sam.web ，并把war包解压到该目录下，重启tomcat。

浏览器访问：http://web.sam.com:8080，此时就会访问到web.sam.com这个项目的内容，而不是 www.sam.com的内容。

当然，需要在sam.com域名管理中添加 web.sam.com域名映射，或者本地测试需要修改本机host文件，添加记录 ：192.168.0.8 web.sam.com ，将web.sam.com的访问映射到192.168.0.8这台服务器中。

## 五、配置静态资源访问，配置目录位置的网络映射

配置后，可以直接访问到本地资源文件，而不需要访问到具体项目。

1、针对第二种部署方式的配置（以 www.sam.com 项目为例）

修改tomcat conf下的server.xml配置

```javascript
 [root@localhost conf]# vim server.xml 
```

在

```javascript
<Host name="www.sam.com">
      <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
                       prefix="www.sam.com_access_log." suffix=".txt"
                       pattern="%h %l %u %t "%r" %s %b" />
      <Context path="" docBase="/home/sam/site/com.sam.www" />
      <Context path="/upload" docBase="/home/sam/share/upload" />
</Host>
```

在 /home/sam/share/upload 存放共享资源 a.jpg

浏览器访问：http://www.sam.com:8080/upload/a.jpg ，即可获取到该资源。

说明：

以上配置后，会把www.sam.com域名下的所有 http://www.sam.com:8080/upload 请求拦截，并直接从/home/sam/share/upload 共享目录下寻求对应的资源文件。

如访问：http://www.sam.com:8080/upload/a/b.txt , 该请求直接从/home/sam/share/upload目录下寻找a目录，并寻找a目录下的b.txt，然后直接把该资源返回。

于是我们只要把共享资源存放在配置的共享目录中，就能通过域名直接访问相应的资源。

2、针对第三种部署方式的配置（以 web.sam.com 项目为例）

修改Catalina目录下对应的项目目录里面的内容。

进入Catalina 下的 web.sam.com 目录

```javascript
[root@localhost conf]# cd /usr/local/tomcat/apache-tomcat-9.0.11/conf/Catalina/web.sam.com
```

新建文件 upload.xml

```javascript
[root@localhost web.sam.com]# vim upload.xml
```

添加内容：

```javascript
<?xml version="1.0" encoding="UTF-8"?>
<Context path="/upload" docBase="/home/sam/share/upload" >
        <Valve className="org.apache.catalina.valves.AccessLogValve"
        directory="logs/com.sam.web_upload"
        prefix="web.sam.com_upload_localhost_access_log." suffix=".txt"
        resolveHosts="true"
        pattern="%h %l %u %t "%r" %s %b" />
</Context>
```

:wq 保存推出，重启tomcat。

在 /home/sam/share/upload 存放共享资源 a.jpg

