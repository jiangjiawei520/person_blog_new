---
layout: post
title: nginx location 限制ip或ip段访问
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "Grbk@2024"
typora-root-url: ./..
date: 2024-05-23 18:36:32
---

## 配置
```
server {
    listen       80;
    server_name  localhost;
    location / {
<!--more-->
    	 allow all;
         deny 111.111.111.111;
         root /app/abc/html;
         index index.html index.htm;
    }
    # 转发配置
    include /apps/nginx/abc-proxy-pass.conf;
}   

```
```
deny 111.0.0.0/8;    // 禁止 111.0.0.1 ~ 111.255.255.254 网段的IP
deny 111.111.0.0/16;   // 禁止 111.111.0.1 ~ 111.111.254 网段的IP
deny 111.111.111.0/24;   // 禁止 111.111.111.1 ~ 111.111.111.254 网段的IP
deny all;  // 禁止所有IP
如果想禁止某个准确的IP，deny 后直接加IP（deny xxx.xxx.xxx.xxx;） 即可。
```
### 注意

1. 上面的配置中 allow 必须在 deny 的前面配置，不然 allow 不会生效。
2. 修改Nginx配置文件需要重启 Nginx 服务才能生效。
3. allow 允许 / deny 禁止 他们两用法相同。
## 重启Nginx
