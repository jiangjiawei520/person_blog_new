---
layout: post
title: 【CentOS7】原有磁盘扩容实战记录（LVM&非LVM）
tags:
  - 知识库
  - CentOS7
categories:
  - linux
abbrlink: 2575c79d
typora-root-url: ./..
date: 2024-03-13
---

### 一、逻辑卷（LVM）原磁盘扩容

> 说明：
>
> 原有磁盘扩容是指非新增磁盘情况下在原有磁盘进行了升级扩容（很多云主机做法推荐原磁盘扩容已成趋势！）

用到的命令:

```bash
 fdisk /dev/vdb
 p -> d -> 1 -> p -> n -> p -> 1 -> 回车 -> 回车 -> p -> w
 查看分区 > 删除分区 > 删除分区1 > 查看分区 > 创建分区 > 创建主分区 > 序号1 > 默认起始扇区 > 默认最终扇区 > 查看分区 > 保存
 partprobe /dev/vdb
 lsblk   //查看此时的/dev/vdb1已经变成了300G
 pvdisplay    /dev/vdb1    //查看物理卷大小只有50G
 pvresize /dev/vdb1        //扩展物理卷到新的大小为300G
 pvdisplay /dev/vdb1   //查看物理卷已经扩展为300G
 vgs        //看到卷组空出来250G
lvextend -r -l +100%FREE /dev/vg1/lv1   //扩展逻辑卷至300G
```

<!--more-->

以下为详解:

##### 1.查看磁盘使用状况

```bash
[root@VM_3_144_centos opt]# df -h
Filesystem           Size  Used Avail Use% Mounted on
devtmpfs             1.9G     0  1.9G   0% /dev
tmpfs                1.9G   24K  1.9G   1% /dev/shm
tmpfs                1.9G  1.3M  1.9G   1% /run
tmpfs                1.9G     0  1.9G   0% /sys/fs/cgroup
/dev/vda1             99G   77G   18G  81% /
tmpfs                378M     0  378M   0% /run/user/0
/dev/mapper/vg1-lv1   49G   33M   49G   1% /data
tmpfs                378M     0  378M   0% /run/user/1000
```

![在这里插入图片描述](/imgs/561d223d2e624cdab1cdec66d5e875fa-1710817893690-202-1711088610915-171.png)

> 如图可以看到/data目录已挂载一个大小为50G 的逻辑卷

##### 2.查看新增磁盘情况

```bash
[root@VM_3_144_centos opt]# lsblk
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sr0          11:0    1  140M  0 rom 
vda         253:0    0  100G  0 disk
└─vda1      253:1    0  100G  0 part /
vdb         253:16   0  300G  0 disk
└─vdb1      253:17   0   50G  0 part
  └─vg1-lv1 252:0    0   49G  0 lvm  /data
```

![在这里插入图片描述](/imgs/dc64ab02cfe747028a96a84d58394e79-1710817893690-205-1711088610915-173.png)

> 如图所示厂家在原有磁盘上新增之300G，那么我们就需要进行原磁盘扩容

##### 3.查看当前物理卷大小

```bash
[root@VM_3_144_centos opt]# pvs
  PV         VG  Fmt  Attr PSize   PFree  
  /dev/vdb1  vg1 lvm2 a--  <50.00g 1020.00m
```

![在这里插入图片描述](/imgs/6a078ba706bf4f3dbfff04ec1fb9f5a2-1710817893690-203-1711088610915-175.png)

> 物理卷只有50G

##### 4.分区（为了验证所有操作为热扩容所以我在磁盘里创建了一个文件）

```bash
[root@VM_3_144_centos opt]# cd /data/
[root@VM_3_144_centos data]# touch 1.txt
[root@VM_3_144_centos data]# ls
1.txt
[root@VM_3_144_centos ~]# fdisk /dev/vdb
p -> d -> 1 -> p -> n -> p -> 1 -> 回车 -> 回车 -> p -> w
查看分区 > 删除分区 > 删除分区1 > 查看分区 > 创建分区 > 创建主分区 > 序号1 > 默认起始扇区 > 默认最终扇区 > 查看分区 > 保存
注意：分区号例如vdb1分区号就是1、vdb2分区号就是2
[root@VM_3_144_centos ~]# partprobe /dev/vdb   //刷新磁盘
[root@VM_3_144_centos ~]# lsblk
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sr0          11:0    1  140M  0 rom 
vda         253:0    0  100G  0 disk
└─vda1      253:1    0  100G  0 part /
vdb         253:16   0  300G  0 disk
└─vdb1      253:17   0  300G  0 part
  └─vg1-lv1 252:0    0   49G  0 lvm  /data
```

![在这里插入图片描述](/imgs/9c61489c689a40d1bf7c2fdf6bed1cdd-1710817893690-204-1711088610915-177.png)  
![在这里插入图片描述](/imgs/973db30fa59d4107a9f51f0643174602-1710817893690-208-1711088610915-179.png)

> 可以看到vdb1已经300G

##### 5.扩展物理卷

```bash
[root@VM_3_144_centos ~]# pvdisplay         //查看物理卷只有50G
  --- Physical volume ---
  PV Name               /dev/vdb1
  VG Name               vg1
  PV Size               <50.00 GiB / not usable 3.00 MiB
  Allocatable           yes
  PE Size               4.00 MiB
  Total PE              12799
  Free PE               255
  Allocated PE          12544
  PV UUID               UjbZEv-bAc0-tnxd-Dicp-e4sU-lft5-WTtW90
[root@VM_3_144_centos ~]# pvresize /dev/vdb1            //扩展物理卷
  Physical volume "/dev/vdb1" changed
  1 physical volume(s) resized or updated / 0 physical volume(s) not resized
[root@VM_3_144_centos ~]# pvs               //看到物理卷300G
  PV         VG  Fmt  Attr PSize    PFree  
  /dev/vdb1  vg1 lvm2 a--  <300.00g <251.00g
[root@VM_3_144_centos ~]# pvdisplay /dev/vdb1   //验证
  --- Physical volume ---
  PV Name               /dev/vdb1
  VG Name               vg1
  PV Size               <300.00 GiB / not usable 2.00 MiB
  Allocatable           yes
  PE Size               4.00 MiB
  Total PE              76799
  Free PE               64255
  Allocated PE          12544
  PV UUID               UjbZEv-bAc0-tnxd-Dicp-e4sU-lft5-WTtW90

```

![在这里插入图片描述](/imgs/19857814d4804c2d9f147df2065087db-1710817893690-206-1711088610915-181.png)

##### 6.扩展逻辑卷

```bash
[root@VM_3_144_centos ~]#  lvextend -r -l +100%FREE /dev/vg1/lv1            //将剩余所有控件划分给lv1逻辑卷，且自动扩展文件
  Size of logical volume vg1/lv1 changed from 49.00 GiB (12544 extents) to <300.00 GiB (76799 extents).
  Logical volume vg1/lv1 successfully resized.
meta-data=/dev/mapper/vg1-lv1    isize=512    agcount=4, agsize=3211264 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=0 spinodes=0
data     =                       bsize=4096   blocks=12845056, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0 ftype=1
log      =internal               bsize=4096   blocks=6272, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
data blocks changed from 12845056 to 78642176
[root@VM_3_144_centos ~]# lvs
  LV   VG  Attr       LSize    Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  lv1  vg1 -wi-ao---- <300.00g                                                   
[root@VM_3_144_centos ~]# lsblk
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sr0          11:0    1  140M  0 rom 
vda         253:0    0  100G  0 disk
└─vda1      253:1    0  100G  0 part /
vdb         253:16   0  300G  0 disk
└─vdb1      253:17   0  300G  0 part
  └─vg1-lv1 252:0    0  300G  0 lvm  /data
```

![在这里插入图片描述](/imgs/144f497b43774163a0131c60f16d805c-1710817893690-207-1711088610915-183.png)

##### 7.验证

```bash
[root@VM_3_144_centos ~]# lvs
  LV   VG  Attr       LSize    Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  lv1  vg1 -wi-ao---- <300.00g                                                   
[root@VM_3_144_centos ~]# pvs
  PV         VG  Fmt  Attr PSize    PFree
  /dev/vdb1  vg1 lvm2 a--  <300.00g    0
[root@VM_3_144_centos ~]# lsblk
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sr0          11:0    1  140M  0 rom 
vda         253:0    0  100G  0 disk
└─vda1      253:1    0  100G  0 part /
vdb         253:16   0  300G  0 disk
└─vdb1      253:17   0  300G  0 part
  └─vg1-lv1 252:0    0  300G  0 lvm  /data
[root@VM_3_144_centos ~]# df -h
Filesystem           Size  Used Avail Use% Mounted on
devtmpfs             1.9G     0  1.9G   0% /dev
tmpfs                1.9G   24K  1.9G   1% /dev/shm
tmpfs                1.9G  1.3M  1.9G   1% /run
tmpfs                1.9G     0  1.9G   0% /sys/fs/cgroup
/dev/vda1             99G   77G   18G  82% /
tmpfs                378M     0  378M   0% /run/user/0
tmpfs                378M     0  378M   0% /run/user/1000
/dev/mapper/vg1-lv1  300G   34M  300G   1% /data
[root@VM_3_144_centos ~]# ls /data/
1.txt
```

![在这里插入图片描述](/imgs/73d3849799d14f3da52df7fe5d44f1f9-1710817893690-209-1711088610915-185.png)

> 看到/data磁盘目录大小以扩展到300G且数据文件1.txt并未丢失至此逻辑卷原盘扩容完毕

### 二、原磁盘(非LVM)扩容

由于过程重复所以不再演示直接给出命令：

```bash
#fdisk /dev/vdb
#p -> d -> 1 -> p -> n -> p -> 1 -> 回车 -> 回车 -> p -> w
#注释：查看分区 > 删除分区 > 删除分区1 > 查看分区 > 创建分区 > 创建主分区 > 序号1 > 默认起始扇区 > 默认最终扇区 > 查看分区 > 保存 
#注释：如没有分区（vdb1等），直接刷新即可,如下代码块
partprobe /dev/vdb         //刷新vdb盘
resize2fs /dev/vdb       //文件扩展，扩展ext4文件系统: resize2fs 、扩展xfs文件系统:  xfs_growfs
```

```
[root@host-172-16-32-114 ~]# df -h
文件系统             容量  已用  可用 已用% 挂载点
devtmpfs             7.7G     0  7.7G    0% /dev
tmpfs                7.8G     0  7.8G    0% /dev/shm
tmpfs                7.8G  9.0M  7.8G    1% /run
tmpfs                7.8G     0  7.8G    0% /sys/fs/cgroup
/dev/mapper/cs-root   70G  5.3G   65G    8% /
/dev/vdb              40G   28K   38G    1% /data
/dev/vda1           1014M  302M  713M   30% /boot
/dev/mapper/cs-home   42G  338M   41G    1% /home
tmpfs                1.6G     0  1.6G    0% /run/user/0
[root@host-172-16-32-114 ~]# lsblk 
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sr0          11:0    1 10.8G  0 rom  
vda         252:0    0  120G  0 disk 
├─vda1      252:1    0    1G  0 part /boot
└─vda2      252:2    0  119G  0 part 
  ├─cs-root 253:0    0   70G  0 lvm  /
  ├─cs-swap 253:1    0  7.9G  0 lvm  [SWAP]
  └─cs-home 253:2    0 41.1G  0 lvm  /home
vdb         252:16   0   60G  0 disk /data
```

