
    layout: post
    title: “X-Content-Type-Options”头缺失或不安全
    tags:
    - 语雀
    categories:
    - [语雀,我的知识库]
    abbrlink: 
    date: 2024-05-22 17:28:46
    
在web安全测试中，今天我们说下扫描结果中包含X-Content-Type-Options请求头header的缺失或不安全的时候，我们该如何应对。
Web [服务器](https://cloud.tencent.com/act/pro/promotion-cvm?from_column=20065&from=20065)对于 HTTP 请求的响应头缺少 X-Content-Type-Options，这意味着此网站更易遭受跨站脚本攻击（XSS）。X-Content-Type-Options 响应头相当于一个提示标志，被服务器用来提示客户端一定要遵循在 Content-Type 首部中对 MIME 类型 的设定，而不能对其进行修改，这就禁用了客户端的 MIME 类型嗅探行为。浏览器通常会根据响应头 Content-Type 字段来分辨资源类型，有些资源的 Content-Type 是错的或者未定义，这时浏览器会启用 MIME-sniffing 来猜测该资源的类型并解析执行内容。利用这个特性，攻击者可以让原本应该解析为图片的请求被解析为 JavaScript 代码。
Nginx Web服务器
在服务器块下的nginx.conf中添加以下参数（add_header X-Content-Type-Options nosniff;）
```plsql
server {
listen 443;
server_name ds.v.com; # 驾驶安全
  location / {
<!--more-->
      client_body_timeout  7200;
      proxy_read_timeout 7200;
      proxy_send_timeout 7200;
      proxy_pass   http://127.0.0.1:9005/;
      proxy_cookie_path / "/; httponly; secure; SameSite=Lax";
      add_header X-Content-Type-Options nosniff;
  }

  ssl_certificate     "/etc/nginx/ssl/ds/ds.v.com.pem";
  ssl_certificate_key "/etc/nginx/ssl/ds/ds.v.com.key";
  # ssl_protocols      TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;
  ssl_protocols      TLSv1.3;

  ssl_session_cache shared:SSL:1m;
  ssl_session_timeout  10m;
  ssl_ciphers HIGH:!aNULL:!MD5;
  ssl_prefer_server_ciphers on;
}

```
保存nginx.conf文件, 然后重新启动Nginx以查看结果，漏洞验证：
可使用验证工具列举如下：

- 在线检测网站：[https://securityheaders.com/?q=http://www.luckysec.cn/](https://cloud.tencent.com/developer/tools/blog-entry?target=https%3A%2F%2Fsecurityheaders.com%2F%3Fq%3Dhttp%3A%2F%2Fwww.luckysec.cn%2F&source=article&objectId=2182642)
- curl 命令工具：curl -I "http://www.luckysec.cn/"
- 浏览器工具： F12 打开浏览器控制台网络查看网站响应头。
- 网络抓包工具：常用BurpSuite等工具。
