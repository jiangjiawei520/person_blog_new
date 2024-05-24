---
layout: post
title: nginx 之 https 证书配置
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "Grbk@2024"
typora-root-url: ./..
date: 2024-05-24 10:45:56
---
## HTTPS原理和作用
**为什么需要HTTPS**
原因：HTTP不安全

- 传输数据被中间人盗用、信息泄露
- 数据内容劫持、篡改

<!--more-->
**HTTPS协议的实现**
对传输内容进行加密以及身份验证
对称加密：加密秘钥和解密秘钥是对等的，一样的
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734441479-cc82011e-141a-4109-be46-265e910bb599.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u2d561b60&originHeight=430&originWidth=1363&originalType=url&ratio=1&size=119895&status=done&style=none&taskId=u538ef2f0-e757-4caa-9501-3dc325e5e28)


非对称加密：
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734441997-b2e81fc2-54f0-4fc0-89f4-bcb1cbe2a245.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u84818e82&originHeight=508&originWidth=1378&originalType=url&ratio=1&size=154059&status=done&style=none&taskId=u865636ee-bdeb-4fa1-a293-29d03de57b3)

HTTPS加密协议原理：
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734441313-2f6110e4-06ae-42b6-b1b2-7821d68b4bf1.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u037b4920&originHeight=379&originWidth=1369&originalType=url&ratio=1&size=110409&status=done&style=none&taskId=u8ba4fb9b-0453-45e8-8fb3-5288f69370c)

中间人伪造客户端和服务端：（中间人可以伪装成客户端和服务端，中间人可以对数据进行劫持，不安全）
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734441930-f2465198-82a7-428d-b380-bd724548959b.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u5bfdbc6c&originHeight=425&originWidth=1519&originalType=url&ratio=1&size=148699&status=done&style=none&taskId=u3d3292c7-f526-48a3-b173-906c6e981b5)


HTTPS的CA签名证书：（服务端和客户端通过实现约定好的证书进行认证，都会对证书进行校验，所以中间人没法劫持数据，故安全）
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734442113-9a8abb83-50db-4ef9-8501-8bf79a3cf628.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u4a5f5f3d&originHeight=338&originWidth=1564&originalType=url&ratio=1&size=222881&status=done&style=none&taskId=u175ca3ea-7b89-47bb-ab23-51fad3bd1b2)

## HTTPS 配置使用
**证书签名生成CA证书**
先确认环境：已经安装openssl和nginx已经编译ssl的模块
> openssl version

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734442202-089befbc-2246-4465-95aa-0d8cf42e5c26.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u00a4d0db&originHeight=69&originWidth=299&originalType=url&ratio=1&size=3902&status=done&style=none&taskId=uc5f9fd74-58d9-44e8-9402-91281a7cfad)

> /usr/local/nginx/sbin/nginx -V

无ssl模块时，需要新增[https://www.cnblogs.com/zoulixiang/p/10196671.html](https://www.cnblogs.com/zoulixiang/p/10196671.html)
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734442190-cb75e850-c989-499c-89cb-7974b7542192.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u0ee320c0&originHeight=92&originWidth=374&originalType=url&ratio=1&size=7853&status=done&style=none&taskId=u25e07f04-c79e-400c-83af-6a18f43bee1)

> rpm -qa | grep open

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734442655-55e6675c-c3c5-45e2-9650-3b4e2d2d98e1.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=ueb959291&originHeight=272&originWidth=491&originalType=url&ratio=1&size=19351&status=done&style=none&taskId=ue44a67dc-49d7-4394-91ad-9eb6544a610)
生成秘钥和CA证书步骤：
步骤1、生成key秘钥
步骤2、生成证书签名请求文件（csr文件）
步骤3、生成证书签名文件（CA文件）

**证书签名生成和Nginx的HTTPS服务场景演示**
先创建一个用来放秘钥的文件夹 ssl_key
> cd /etc/nginx/
> mkdir ssl_key

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734442744-ed396286-52d1-4072-bfbb-44b83764c6bd.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u25d8e4fc&originHeight=50&originWidth=492&originalType=url&ratio=1&size=5235&status=done&style=none&taskId=ua10e0d21-1495-4171-b0db-fda1a7390b5)
输入加密算法
> openssl genrsa -idea -out SSL.key 1024

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734442920-86d8a8b1-d89e-40c5-bbe8-6d6f37895642.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u31bba290&originHeight=147&originWidth=628&originalType=url&ratio=1&size=12190&status=done&style=none&taskId=u1367a9f5-de05-4da3-b81c-0f0c023fac1)
回车，会让输入密码，这里设置为123456，完成后会生成一个.key的文件
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734443053-bb092372-d6d3-45a7-baa6-c4ccde1b063b.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u00ce7db6&originHeight=72&originWidth=253&originalType=url&ratio=1&size=2335&status=done&style=none&taskId=uab9b4f53-346d-4135-865d-b815acaa512)

生成证书签名请求文件（csr文件）
> openssl req -new -key SSL.key -out SSL.csr

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734443115-4b491182-b140-4a40-bfaf-563ea121df46.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u455706ec&originHeight=348&originWidth=641&originalType=url&ratio=1&size=35744&status=done&style=none&taskId=u0584b3f2-5ce1-44ac-8bdc-21d21a90d16)

查看生成的请求文件
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734443434-b30ca058-8b5b-4b5d-8181-8f8890cc6f97.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u0d622666&originHeight=90&originWidth=294&originalType=url&ratio=1&size=4103&status=done&style=none&taskId=uf8874530-3245-4b89-afb3-fc2b9c0bc2e)

生成证书签名文件（CA文件） 打包 有效期设置了 10 年
> openssl x509 -req -days 3650 -in SSL.csr -signkey SSL.key -out SSL.crt

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734443638-09f7a1e9-4f54-4937-ac5c-8369e9419549.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u5992af16&originHeight=178&originWidth=712&originalType=url&ratio=1&size=16095&status=done&style=none&taskId=uad2b6fb2-fbf5-4bd7-8d63-84e26011756)

Nginx的HTTPS语法配置
>  ssl开关
> 配置语法：ssl on|off;
> 默认状态：ssl off;
> 配置方法：http、server
>  
> ssl证书文件
> 配置语法：ssl_certificate file;
> 默认状态：-
> 配置方法：http、server
>  
> ssl密码文件
> 配置语法：ssl_certificate_key file;
> 默认状态：ssl off;
> 配置方法：http、server
> 进入/etc/nginx/conf.d/
> test_https.conf

> server
>  {
>    listen       443;# https 监听的是 443端口
>    server_name  192.168.1.112 www.zhangbiao.com;
>  
>    keepalive_timeout 100;
>  
>    ssl on;
>    ssl_session_cache   shared:SSL:10m;
>    ssl_session_timeout 10m;
>  
>    ssl_certificate /usr/local/nginx/ssl_key/SSL.crt; # 证书路径
>    ssl_certificate_key /usr/local/nginx/ssl_key/SSL.key; # 请求认证 key 的路径
>  
>    index index.html index.htm;
>    location / {
>        root  /opt/app/code;
>    }
> }

配置好之后，关闭和启动，都需要数之前设置的密码
关闭
> nginx -s stop -c /etc/nginx/nginx.conf


启动 
> nginx -c /etc/nginx/nginx.conf

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734443824-f9bd563f-aa77-450b-8c1a-ab23bb6cef8f.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u286197ae&originHeight=126&originWidth=1054&originalType=url&ratio=1&size=15545&status=done&style=none&taskId=u9ee8571f-d918-426e-be0c-629c624c53d)

访问

| 1 | https://www.zhangbiao.com/index.html |
| --- | --- |

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734443781-d820853e-dea9-4be8-ba83-bf195e009f77.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u50d23119&originHeight=441&originWidth=892&originalType=url&ratio=1&size=32562&status=done&style=none&taskId=ua04350b8-519b-49d9-a1be-8f159f7b638)
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734444069-69a9993d-a0bb-4956-ae9e-cd2e77186e12.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u9869d17b&originHeight=95&originWidth=505&originalType=url&ratio=1&size=9641&status=done&style=none&taskId=uc49f56aa-3d96-4384-8fce-61038068521)


## 基于Nginx的HTTPS服务_实战场景配置苹果要求的openssl后台HTTPS服务
配置苹果要求的证书： 

- 1、服务器所有的连接使用TLS1.2以上的版本（openssl 1.0.2）
- 2、HTTPS证书必须使用SHA256以上哈希算法签名
- 3、HTTPS证书必须使用RSA2048位或ECC256位以上公钥算法
- 4、使用前向加密技术

首先看openssl版本：，为1.0.1，需要升级 
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734444428-94079a5b-245e-44ee-981d-663c341b79ab.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u6c5f6879&originHeight=57&originWidth=591&originalType=url&ratio=1&size=5338&status=done&style=none&taskId=ua8ff7e88-dc4d-48d9-8138-aa7e0508ee5)

查看当前使用的自签算法类型：openssl x509 -noout -text -in ./jesonc.crt，使用的是sha256，位数是1024位，都不符合规定 

| 1 | openssl x509 -noout -text -in ./jesonc.crt |
| --- | --- |

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734444700-3be7328a-9b8a-4cde-9753-f0fb4814f977.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u7f0dc57f&originHeight=583&originWidth=788&originalType=url&ratio=1&size=58461&status=done&style=none&taskId=uff139f17-1362-4b3f-b32c-0d263bd8519)
升级openssl，使用shell脚本升级
update_openssl.sh

| 1
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
15 | #!/bin/sh |
| --- | --- |

#jeson@imoocc.com
cd /opt/download
wget https://www.openssl.org/source/openssl-1.0.2k.tar.gz
tar -zxvf openssl-1.0.2k.tar.gz
cd openssl-1.0.2k
./config --prefix=/usr/local/openssl
make && make install
mv /usr/bin/openssl /usr/bin/openssl.OFF
mv /usr/include/openssl /usr/include/openssl.OFF
ln -s /usr/local/openssl/bin/openssl /usr/bin/openssl
ln -s /usr/local/openssl/include/openssl /usr/include/openssl
echo "/usr/local/openssl/lib" >>/etc/ld.so.conf
ldconfig -v
openssl version -a

执行脚本 

| 1 | sh ./update_openssl.sh |
| --- | --- |


版本升级成功，查看版本

| 1 | openssl version |
| --- | --- |

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734444745-c60e4776-d850-4179-b2f6-ae63d7656953.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=ue75a12fc&originHeight=46&originWidth=328&originalType=url&ratio=1&size=3592&status=done&style=none&taskId=ub80bf9cf-a683-4461-8fce-4c791b3e0b5)

**制作复合苹果的证书**
修改算法

| 1 | openssl req -days 36500 -x509 -sha256 -nodes -new^Cy rsa:2048 -keyout jesonc_apple.crt |
| --- | --- |


![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734444929-da727afc-a551-4451-b988-6c657b74f17b.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=ubb210baf&originHeight=71&originWidth=616&originalType=url&ratio=1&size=5401&status=done&style=none&taskId=u68353192-de67-46f9-a8e3-89099fa0544)

修改配置文件 
test_https.conf 

| 1
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
19 | server |
| --- | --- |

 {
   listen       443;
   server_name  192.168.1.112 www.zhangbiao.com;
 
   keepalive_timeout 100;
 
   ssl on;
   ssl_session_cache   shared:SSL:10m;
   ssl_session_timeout 10m;
 
   ssl_certificate /etc/nginx/ssl_key/jesonc_apple.crt;
   ssl_certificate_key /etc/nginx/ssl_key/jesonc.key;
 
   index index.html index.htm;
   location / {
       root  /opt/app/code;
   }
}

检查配置语法，并重载

| 1
2 | nginx -tc /etc/nginx/nginx.conf |
| --- | --- |

nginx -s reload -c /etc/nginx/nginx.conf
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734444969-f5769a8b-a744-4846-9a60-b6539ccd5da4.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=ud094a4cb&originHeight=138&originWidth=1063&originalType=url&ratio=1&size=18706&status=done&style=none&taskId=u9c319759-e93f-431c-b209-164cc91dda8) 

查看443端口是否启动

| 1 | netstat -luntp &#124; grep 443 |
| --- | --- |

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734445142-1052142a-03bb-4615-914f-73eab7da04d3.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=uce5ccc96&originHeight=70&originWidth=859&originalType=url&ratio=1&size=6053&status=done&style=none&taskId=u072aec2a-d7a9-49e1-a7f6-91a8758ecba)

访问

| 1 | https://www.zhangbiao.com/index.html |
| --- | --- |

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734445559-00eb3e81-1cdd-448c-9e41-e2b169854b20.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u569fc1c5&originHeight=657&originWidth=1070&originalType=url&ratio=1&size=56340&status=done&style=none&taskId=u8f9c1fda-eb80-420d-a7b1-a9e783d2d12)

成功返回地页面
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639734445743-5bdbf69e-ca72-4806-969f-04ba8d4211e3.png#clientId=ubc5cfd8b-06e5-4&from=paste&id=u971fa098&originHeight=180&originWidth=640&originalType=url&ratio=1&size=13012&status=done&style=none&taskId=udbf297d0-8663-4d7c-a5a9-e04b5fa5c6d)

## HTTPS 服务优化
方法一：
激活keepalive 长连接
方法二：
设置 session 缓存

**test_https.conf**

| 1
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
19 | server |
| --- | --- |

 {
   listen       443;
   server_name  116.62.103.228 jeson.t.imooc.io;
 
   keepalive_timeout 100; # 长连接 100s
 
   ssl on;
   ssl_session_cache   shared:SSL:10m; # 设置 10M 的缓存
   ssl_session_timeout 10m; # session 过期时间 10 分钟
 
   ssl_certificate /etc/nginx/ssl_key/jesonc_apple.crt;
   ssl_certificate_key /etc/nginx/ssl_key/jesonc.key;
 
   index index.html index.htm;
   location / {
       root  /opt/app/code;
   }
}
