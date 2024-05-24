---
layout: post
title: CentOS虚拟机centos-root扩容
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "Grbk@2024"
typora-root-url: ./..
date: 2024-05-24 10:45:56
---
本文介绍在虚拟机 vmware 的 CentOS 系统中实现无损扩容根分区的方法。

## 原由
手头上的虚拟机是由其它同事分享的，看上去已经有很多年头了，开发环境较齐全，于是就使用，至今已有2年了。如果按之前的做事方式，我肯定是重新安装一个系统，但现在已经无所谓了，连用户名我也没改。但渐渐磁盘空间不足，经查发现根分区只有区区26GB，我删除了很多临时文件，也是捉襟见肘，加上最近要继续研究 docker，帮其它同事构建镜像，因为扩展空间成当务之急。

## 技术小结
备份虚拟机，拍快照
<!--more-->
虚拟机创建硬盘
磁盘分区
扩容
## 实践
本节创建新磁盘，扩展将其所有容量至根目录/dev/mapper/centos-root。

## 备份虚拟机
在 vmware 创建快照，完成扩容后再删除，以防不测。

## 查看扩容前容量
```shell
$ df -h
文件系统                 容量  已用  可用 已用% 挂载点
/dev/mapper/centos-root   26G   20G  6.6G   75% /
devtmpfs                 1.9G     0  1.9G    0% /dev
tmpfs                    1.9G     0  1.9G    0% /dev/shm
tmpfs                    1.9G   21M  1.9G    2% /run
tmpfs                    1.9G     0  1.9G    0% /sys/fs/cgroup
/dev/sda1               1014M  232M  783M   23% /boot
tmpfs                    378M   16K  378M    1% /run/user/42
tmpfs                    378M   40K  378M    1% /run/user/1000
tmpfs                    378M     0  378M    0% /run/user/0
```

## vmware 添加磁盘
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1681780976694-b75654bd-f245-4862-881e-96528e248b3c.png#averageHue=%23f3f3f2&clientId=ueec5bf1c-3010-4&from=paste&id=u5b8b8614&originHeight=433&originWidth=735&originalType=url&ratio=1&rotation=0&showTitle=false&size=56975&status=done&style=none&taskId=u95751dba-9fcc-402c-968f-9e9cac27e9f&title=)

## 磁盘分区
```shell
# fdisk /dev/sdb // 输入n、p，几个回车，输入w。
```

最终得到/dev/sdb1分区。

```shell
ls /dev/sd*
/dev/sda  /dev/sda1  /dev/sda2  /dev/sda3  /dev/sda4  /dev/sdb  /dev/sdb1
```


具体信息如下：
```shell
# fdisk /dev/sdb   ## !!!
欢迎使用 fdisk (util-linux 2.23.2)。

更改将停留在内存中，直到您决定将更改写入磁盘。
使用写入命令前请三思。


命令(输入 m 获取帮助)：n    ## !!! 输出n创建分区
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p):     ## !!! 下面3个回车即可
分区号 (1-4，默认 1)：      ## !!!
起始 扇区 (2048-419430399，默认为 2048)： ## !!!
将使用默认值 2048
Last 扇区, +扇区 or +size{K,M,G} (2048-419430399，默认为 419430399)：
将使用默认值 419430399
分区 1 已设置为 Linux 类型，大小设为 200 GiB

命令(输入 m 获取帮助)：p   ## !!! 打印查看

磁盘 /dev/sdb：214.7 GB, 214748364800 字节，419430400 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x8a4e86e9

   设备 Boot      Start         End      Blocks   Id  System
/dev/sdb1            2048   419430399   209714176   83  Linux

命令(输入 m 获取帮助)：w   ## !!! 回写
The partition table has been altered!

Calling ioctl() to re-read partition table.
正在同步磁盘。


```
## 扩容
执行如下命令实现扩容。

```shell
partprobe
pvcreate /dev/sdb1
vgextend centos /dev/sdb1
lvextend -l +100%FREE /dev/centos/root

```
具体如下所列。

## 创建物理卷(pv)
```shell
# pvcreate /dev/sdb1
WARNING: xfs signature detected on /dev/sdb1 at offset 0. Wipe it? [y/n]: y
  Wiping xfs signature on /dev/sdb1.
  Physical volume "/dev/sdb1" successfully created.
```

## 扩展卷组(vg)
即将sdb1添加到卷组Volume group。
```shell
# vgextend centos /dev/sdb1
  Volume group "centos" successfully extended
```

## 扩展逻辑卷(lv)
此处使用所有的空间。
```shell
# lvextend -l +100%FREE /dev/centos/root
  Size of logical volume centos/root changed from <26.00 GiB (6655 extents) to <226.99 GiB (58109 extents).
  Logical volume centos/root successfully resized.
```

## 更新系统磁盘大小
```shell
# xfs_growfs /dev/mapper/centos-root
meta-data=/dev/mapper/centos-root isize=512    agcount=7, agsize=1113856 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=0 spinodes=0
data     =                       bsize=4096   blocks=6814720, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0 ftype=1
log      =internal               bsize=4096   blocks=2560, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
data blocks changed from 6814720 to 59503616

```
## 查看扩容后大小
```shell
# df -h
文件系统                 容量  已用  可用 已用% 挂载点
/dev/mapper/centos-root  227G   20G  208G    9% /
devtmpfs                 1.9G     0  1.9G    0% /dev
tmpfs                    1.9G     0  1.9G    0% /dev/shm
tmpfs                    1.9G   29M  1.9G    2% /run
tmpfs                    1.9G     0  1.9G    0% /sys/fs/cgroup
/dev/sda1               1014M  232M  783M   23% /boot
tmpfs                    378M   20K  378M    1% /run/user/42
tmpfs                    378M   40K  378M    1% /run/user/1000

```
/dev/mapper/centos-root占用大小为20GB不变，但使用率从75%下降到9%，实现了扩容。

小结
centos支持扩展/dev/mapper/centos-root，这是最快速的方式，无须挂载新磁盘目录。
