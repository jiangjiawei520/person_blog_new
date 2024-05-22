
    layout: post
    title: Linux安装Redis
    tags:
    - 语雀
    categories:
    - [语雀,我的知识库]
    abbrlink: 
    date: 2024-05-22 17:28:46
    
## 环境：
Linux CentOS 7.4

## 安装流程：

1. 安装 gccredis 是 c 语言编写的
```bash
yum install gcc-c++
```
<!--more-->

2. 下载 redis 安装包,在 root 目录下执行
```bash
wget http://download.redis.io/releases/redis-5.0.4.tar.gz
```

3. 解压 redis 安装包
```bash
tar -zxvf redis-5.0.4.tar.gz
```

4. 进入 redis 目录
```bash
cd redis-5.0.4
```

5. 编译
```bash
make
```

6. 安装
```bash
make PREFIX=/usr/local/redis install
```

7. 拷贝 redis.conf 到安装目录
```bash
cp redis.conf /usr/local/redis
```

8. 进入 /usr/local/redis 目录
```bash
cd /usr/local/redis/
```

9. 编辑 redis.conf
```
#后台启动，
daemonize yes
#绑定端口，默认是6379 需要安全组开放端口
port 6379
#绑定IP，
bind 192.168.2.128
#指定数据存放路径，存放的路径
dir /usr/local/redis/log rdb
#指定持久化方式
appendonly yes
#设置密码
requirepass redis129
```

10. 后端启动 redis：
```bash
./bin/redis-server ./redis.conf
```

11. 查看是否启动成功：
```bash
ps aux | grep redis
```
