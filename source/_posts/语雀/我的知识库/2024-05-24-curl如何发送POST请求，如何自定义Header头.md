---
layout: post
title: curl如何发送POST请求，如何自定义Header头
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "bk@2024"
typora-root-url: ./..
date: 2024-05-24 10:50:14
---
# curl 使用
## 使用curl 发送POST请求
> HTTP 的POST请求通常用于提交数据，一般有四种常见的POST提交数据方式。做Web后端开发时，不可避免的要自己发送请求来调试接口，本篇是如何使用curl工具来进行各种方式的POST请求。


### 1. application/x-www-form-urlencoded
最常见的POST请求，form表单。 使用curl进行请求很简单，示例如下：
<!--more-->

> curl -X POST -d "name=zhangsan" 127.0.0.1:80/api/getInfo


### 2. Multipart/form-data
这种请求一般涉及文件上传。后端对这种类型的请求处理也更复杂一些。

> curl 127.0.0.1:80/api/multipart -F raw=@raw.data -F name=zhangsan


### 3. application/json
> curl 127.0.0.1:80/api/json -XPOST -d '{"name":"zhangsan"}' --header "Content-Type : application/json"


这种方式跟 application/x-www-form-urlencoded 类型的POST请求类似， -d 参数值是 JSON字符串，并且多了一个 Content-Type: application/json 指定发送内容的格式。 Web后端解析后，得到的结构都是 name=zhangsan 键值对。

### 4. text/xml 文件内容作为提交的数据
如果要提交的数据比较多，不方便写在命令行里，那么那么可以把数据内容写到文件中，通过 -d @filename 的方式来提交数据。 这是 -d 参数的一种使用方式。但是跟 multipart/form-data 中上传文件的POST不是一回事。 @ 符号表明后面跟的是文件名，要读取这个文件的内容作为 -d 的参数。

> // 创建数据文件 data.json 
> {
> 	"name" : "zhangsan",
> 	"age" : 18,
> 	"habit" : ["sing", "swimming"]
> }


请求示例如下：

> curl 127.0.0.1:80/api/json -XPOST -d @data.json --header "Content-Type : application/json"


如果要用 application/x-www-form-urlencoded 方式提交，后端解析出同样的数据，那么 -d 参数是这样的， 注意数组参数的写法 。

> // data.txt
> name=zhangsan&age=18&habit[]=sing&habit[]=swimming

请求示例如下：

> curl 127.0.0.1:80/api/test -XPOST -d @data.txt 
> 
> curl 127.0.0.1:80/api/test -XPOST -d 'name=zhangsan&age=18&habit[]=sing&habit[]=swimming'



## curl请求http结果保存到文件中
> curl --header "Content-type : application/json" "hostname:port/path" > ./result.json


## curl 设置自定义HEADER 头
Curl 是一个强大的命令行工具，它可以通过网络将信息传递给服务器或者从服务器获取数据。支持很多传输协议，尤其是 HTTP/HTTPS 以及其他诸如FTP/FTPS, RTSP, POP3/POP3S, SCP, IMAP/IMAPS 协议等。当你使用curl 向一个URL发送HTTP请求时，会使用一个默认的包含必要的头部字段(如： User-Agent，Host，Accept)的HTTP头。
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1677470662449-ffd98ebc-c259-4c22-ab86-3e0567fd87ce.png#averageHue=%23090808&clientId=u7294359b-e966-4&from=paste&id=ub8335f58&originHeight=341&originWidth=772&originalType=url&ratio=1&rotation=0&showTitle=false&size=99833&status=done&style=none&taskId=u400fec71-c1d0-4e25-9ba3-a56040fab2b&title=)


在一些HTTP请求中，需要覆盖默认的HTTP头或者添加自定义的头部字段。为了解决这些问题，curl提供一个简单的方法来完全控制传出HTTP请求的HTTP头。需要的参数是 -H 或者 --header。为了定义多个HTTP头部字段，-H 选项可以在curl命令中多次指定。示例如下：

> curl -H "host:220.181.38.149" -H "Accept-language:es" -H "Cookie:token=xxxx" www.baidu.com -v

![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1677470669399-71d73c4c-3c39-4192-93a7-e8de2fd73878.png#averageHue=%23090706&clientId=u7294359b-e966-4&from=paste&id=ua9717059&originHeight=339&originWidth=825&originalType=url&ratio=1&rotation=0&showTitle=false&size=106887&status=done&style=none&taskId=u47247263-3891-4354-9d28-ec5e450ff87&title=)


注意事项：
> header头、冒号和值质检不能有空格
> 自定义的Header头，需要加在标准头后面。


对于“User-Agent”,”Cookie”,”Host” 这类标准的HTTP头字段，通常会有另一种设置方法。curl命令提供了特定的选项来针对这些字段进行设置：
> -A (or ––user-anget)： 设置 User-Agent字段
> -b(or ––cookie) : 设置 Cookie字段
> -e(or ––referer)：设置 Referer 字段

示例如下，两种方式是等效的：
> curl -H "User-Agent: brower" hostname
> curl -A "brower" hostname

