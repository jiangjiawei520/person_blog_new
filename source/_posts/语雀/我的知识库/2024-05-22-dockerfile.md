
    layout: post
    title: dockerfile
    tags:
    - 语雀
    categories:
    - [语雀,我的知识库]
    abbrlink: 
    date: 2024-05-22 17:28:46
    
# nginx
## 模版
```dockerfile
[root@localhost local]# tree
.
├── conf
│   ├── default.conf
│   └── nginx.repo
├── Dockerfile
<!--more-->
```

- default.conf nginx转发配置文件
- Dockerfile docker的配置文件
- nginx.repo 容器安装nginx的yum镜像

```dockerfile
server {
    listen 80;
    server_name localhost;
    location / {
				#测试地址，我采用宿主机的ip端口，开的web服务
        proxy_pass http://192.168.1.110:8080/;
        proxy_set_header Host $host:80;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Via "nginx";
    }
} 
```

```dockerfile
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/centos/7/$basearch/
gpgcheck=0
enabled=1   
```

```dockerfile
#Dockerfile，采用centos7作为标准镜像，不用nginx标准镜像原因是因为那样启动的容器是mina版的linux，太简单
FROM centos:centos7

#MAINTAINER 维护者信息
MAINTAINER fendo kai.yang@yeepay.com
ADD default.conf /etc/nginx/conf.d/
ADD nginx.repo /etc/yum.repos.d/
#RUN 执行以下命令
RUN yum install -y nginx

#EXPOSE 映射端口
EXPOSE 80

#CMD 运行以下命令，daemon off后台运行，否则启动完就自动关闭
CMD ["/usr/sbin/nginx", "-g","daemon off;"]          
```

## 构建镜像
切记最后有个点，否则会报错( requires exactly 1 argument)
```dockerfile
docker build -t nginx-1.1 .
```
## 查看镜像
```dockerfile
[root@localhost local]# docker images
REPOSITORY                        TAG                 IMAGE ID            CREATED             SIZE
nginx-1.1                         latest              dd7d54fef2f3        12 minutes ago      283MB

```
## 运行镜像
```dockerfile
[root@localhost local]# docker run -d -p 8888:80 -p 90:80 nginx-1.1
```
