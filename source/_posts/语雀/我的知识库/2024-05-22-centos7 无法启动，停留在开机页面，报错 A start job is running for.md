
    layout: post
    title: centos7 无法启动，停留在开机页面，报错 A start job is running for
    tags:
    - 语雀
    categories:
    - [语雀,我的知识库]
    abbrlink: 
    date: 2024-05-22 17:28:46
    
## 问题描述
[centos7](https://so.csdn.net/so/search?q=centos7&spm=1001.2101.3001.7020) 部署的服务因服务器IP更换，出现报错"A start job is running for /etc/rc.d/rc.local compatibility "，因IP地址更换，在fastdfs服务中设置开机自启动，故storage与tracker间无法通信，导致无法开机。
## 解决步骤
1.开机后按"e"进入单用户模式
 
![](https://cdn.nlark.com/yuque/0/2023/png/12484160/1702108606801-727a2957-6113-4689-8eeb-08cd5c6c2841.png#averageHue=%23272727&clientId=u3eb9fbdc-2231-4&from=paste&id=u40117dd9&originHeight=335&originWidth=631&originalType=url&ratio=1&rotation=0&showTitle=false&status=done&style=none&taskId=ub9705176-2d28-4472-87c9-714bfe8738b&title=)
2. 将红框中的ro改成rw rd.break，(不是rw init=/bin/bash)然后按ctrl+x，稍等一会就会进入单用户模式。
![](https://cdn.nlark.com/yuque/0/2023/png/12484160/1702108571359-eb2175ea-bda4-48bd-a538-58a9ca1328ca.png#averageHue=%23100e0e&clientId=u710a28e1-bd75-4&from=paste&id=u4a8ab6c3&originHeight=328&originWidth=894&originalType=url&ratio=1&rotation=0&showTitle=false&status=done&style=none&taskId=u10a60692-b4c6-498d-b3e8-530a9cba2c6&title=)
  然后修改根路径，在sh-4.2#后面逐步执行
<!--more-->
  chroot /sysroot
  cp /etc/passwd- /etc/passwd
  cp /etc/shadow- /etc/passwd
3.按住"Ctrl+x"，进入单用户模式，修改自启动文件内容
![](https://cdn.nlark.com/yuque/0/2023/png/12484160/1702108606783-4d0d1f81-6e49-4b5c-b554-120a776535b8.png#averageHue=%230f0f0f&clientId=u3eb9fbdc-2231-4&from=paste&id=u0ad864e0&originHeight=278&originWidth=610&originalType=url&ratio=1&rotation=0&showTitle=false&status=done&style=none&taskId=u54f4ee38-6fa0-47a3-b614-dca336a53b3&title=)
4.赋予文件写权限
```plsql
chmod +w /etc/rc.d/rc.local

mount -rw -o remount /
```
5.修改"/etc/rc.d/rc.local"
```
vi /etc/rc.d/rc.local
```
![](https://cdn.nlark.com/yuque/0/2023/png/12484160/1702108626114-04d39287-9189-4166-8559-35f4f306ec90.png#averageHue=%23131212&clientId=u3eb9fbdc-2231-4&from=paste&id=u2927b2e9&originHeight=462&originWidth=613&originalType=url&ratio=1&rotation=0&showTitle=false&status=done&style=none&taskId=ua47956bf-9f8a-4c04-bf25-6a47cf744bc&title=)
6.修改完成后，exit后执行"exec /sbin/init"退出单用户模式
 若等待一段时间，仍无法进入，则关闭客户机后，重新启动客户机进入即可。

 
