---
layout: post
title: Linux源码安装postgis（包括SFCGAL，PGRouting）
tags:
  - Postgresql
  - PostGIS
categories:
  - [linux,Postgresql]
  - [linux,PostGIS]
abbrlink: 442a0405
date: 2024-03-15
---

系统版本[centos7](https://so.csdn.net/so/search?q=centos7&spm=1001.2101.3001.7020 "centos7").9

### 1、准备源码包

```diff
[root@localhost postgis]# ll
总用量 211764
drwxrwxr-x 140 root     root          8192  7月 13 18:04 cgal-releases-CGAL-4.13
-rw-r--r--   1 root     root     131376953  7月 13 13:27 cgal-releases-CGAL-4.13.tar.gz
drwxr-xr-x  15 root     root          4096  7月 13 18:00 CMake-3.21.1
-rw-r--r--   1 root     root      16794019  7月 13 13:27 CMake-3.21.1.zip
drwxrwxr-x  22 postgres postgres      4096  7月 13 16:11 gdal-3.3.1
-rw-r--r--   1 root     root      19582883  7月 13 13:27 gdal-3.3.1.tar.gz
drwxr-xr-x  11      501 games         4096  7月 13 13:28 geos-3.9.1
-rw-r--r--   1 root     root       4761372  7月 13 13:27 geos-3.9.1.tar.bz2
drwxrwxr-x   8 root     root          4096  7月 13 14:18 json-c-json-c-0.13.1-20180305
-rw-r--r--   1 root     root        625036  7月 13 13:27 json-c-json-c-0.13.1-20180305.tar.gz
drwxrwxr-x  21 root     root          8192  7月 13 14:23 libxml2-v2.9.12
-rw-r--r--   1 root     root       5233674  7月 13 13:27 libxml2-v2.9.12.tar.gz
drwxr-xr-x  16 root     root          4096  7月 14 09:26 pgrouting-2.6.3
-rw-r--r--   1 root     root       7458684  7月 13 13:27 pgrouting-2.6.3.zip
drwxr-xr-x  20      105      108      4096  7月 14 10:07 postgis-3.1.3
-rw-r--r--   1 root     root      17273487  7月 13 13:27 postgis-3.1.3.tar.gz
drwxr-xr-x  10      501 games         4096  7月 13 13:31 proj-6.3.2
-rw-r--r--   1 root     root       2827685  7月 13 13:27 proj-6.3.2.tar.gz
drwxrwxr-x  22 root     root          4096  7月 13 14:23 protobuf-3.10.1
-rw-r--r--   1 root     root       4905995  7月 13 13:27 protobuf-3.10.1.tar.gz
drwxr-xr-x   8 postgres postgres      4096  7月 13 15:35 protobuf-c-1.3.2
-rw-r--r--   1 root     root        500100  7月 13 13:27 protobuf-c-1.3.2.tar.gz
drwxrwxr-x  12 root     root           325  7月 14 08:58 SFCGAL-1.3.8
-rw-r--r--   1 root     root       2480730  7月 13 13:27 SFCGAL-1.3.8.tar.gz
drwxr-xr-x   5 postgres postgres      4096  7月 13 14:04 sqlite-autoconf-3340100
-rw-r--r--   1 root     root       2930089  7月 13 13:27 sqlite-autoconf-3340100.tar.gz
```

yum -y install gcc gcc-c++

<!--more-->

### 2、安装geos

下载路径：[http://download.osgeo.org/geos/geos-3.9.1.tar.bz2](http://download.osgeo.org/geos/geos-3.9.1.tar.bz2 "http://download.osgeo.org/geos/geos-3.9.1.tar.bz2")

```diff
[root@localhost src]# tar -jxvf geos-3.9.1.tar.bz2
[root@localhost src]# cd geos-3.9.1
[root@localhost geos-3.9.1]# ./configure --prefix=/usr/local/geos-3.9.1
//make编译
[root@localhost geos-3.9.1]# make -j 4
[root@localhost geos-3.9.1]# make install
```

### 3、安装sqlite

下载路径：[https://www.sqlite.org/2021/sqlite-autoconf-3340100.tar.gz](https://www.sqlite.org/2021/sqlite-autoconf-3340100.tar.gz "https://www.sqlite.org/2021/sqlite-autoconf-3340100.tar.gz")

```diff
[root@localhost src]# tar -zxvf sqlite-autoconf-3340100.tar.gz
[root@localhost src]# cd sqlite-autoconf-3340100
[root@localhost sqlite-autoconf-3340100]# ./configure --prefix=/usr/local/sqlite
//make编译
[root@localhost sqlite-autoconf-3340100]# make -j 4
[root@localhost sqlite-autoconf-3340100]# make install
//替换原有的sqlite
[root@localhost sqlite-autoconf-3340100]# mv /usr/bin/sqlite3 /usr/bin/sqlite3_old
[root@localhost sqlite-autoconf-3340100]# ln -s /usr/local/sqlite/bin/sqlite3 /usr/bin/sqlite3
[root@localhost sqlite-autoconf-3340100]# sqlite3 --version
3.34.1 2021-01-20 14:10:07 10e20c0b43500cfb9bbc0eaa061c57514f715d87238f4d835880cd846b9ebd1f
//暴露pkg_config，避免proj找不到sqlite
[root@localhost sqlite-autoconf-3340100]# export PKG_CONFIG_PATH=/usr/local/sqlite/lib/pkgconfig:$PKG_CONFIG_PATH
```

### 4、安装proj

下载路径：[http://download.osgeo.org/proj/proj-6.3.2.tar.gz](http://download.osgeo.org/proj/proj-6.3.2.tar.gz "http://download.osgeo.org/proj/proj-6.3.2.tar.gz")

```diff
[root@localhost src]# tar -zxvf proj-6.3.2.tar.gz
[root@localhost src]# cd proj-6.3.2
[root@localhost proj-6.3.2]# ./configure --prefix=/usr/local/proj-6.3.2
//make编译
[root@localhost proj-6.3.2]# make -j 4
[root@localhost proj-6.3.2]# make install
```

### 5、安装gdal

下载路径：[https://download.osgeo.org/gdal/3.3.1/gdal-3.3.1.tar.gz](https://download.osgeo.org/gdal/3.3.1/gdal-3.3.1.tar.gz "https://download.osgeo.org/gdal/3.3.1/gdal-3.3.1.tar.gz")

```diff
[root@localhost src]# tar -zxvf gdal-3.3.1.tar.gz
[root@localhost src]# cd gdal-3.3.1
//编译指定安装路径且绑定proj
[root@localhost gdal-3.3.1]# ./configure --prefix=/usr/local/gdal-3.3.1 --with-proj=/usr/local/proj-6.3.2
//make编译
[root@localhost gdal-3.3.1]# make -j 4
[root@localhost gdal-3.3.1]# make install
```

### 6、安装json

下载路径：[https://github.com/json-c/json-c/archive/json-c-0.13.1-20180305.tar.gz](https://github.com/json-c/json-c/archive/json-c-0.13.1-20180305.tar.gz "https://github.com/json-c/json-c/archive/json-c-0.13.1-20180305.tar.gz")

```diff
[root@localhost src]# tar -zxvf json-c-0.13.1.tar.gz
[root@localhost src]# cd json-c-0.13.1
[root@localhost json-c-0.13.1]# ./configure --prefix=/usr/local/json-c-0.13.1
//make编译
[root@localhost json-c-0.13.1]# make -j 4
[root@localhost json-c-0.13.1]# make install
```

### 7、安装libxml

下载路径：[https://gitlab.gnome.org/GNOME/libxml2/-/archive/v2.9.12/libxml2-v2.9.12.tar.gz](https://gitlab.gnome.org/GNOME/libxml2/-/archive/v2.9.12/libxml2-v2.9.12.tar.gz "https://gitlab.gnome.org/GNOME/libxml2/-/archive/v2.9.12/libxml2-v2.9.12.tar.gz")

```diff
//我这里用的是2.9.9版本
[root@localhost src]# tar -zxvf libxml2-2.9.12.tar.gz
[root@localhost src]# cd libxml2-2.9.12
[root@localhost libxml2-2.9.12]# ./configure --prefix=/usr/local/libxml2-2.9.12  //如果文件不存在，就使用./autogen.sh编译
[root@localhost libxml2-2.9.12]# ./autogen.sh --prefix=/usr/local/libxml2-2.9.12
//make编译
[root@localhost libxml2-2.9.12]# make -j 4
[root@localhost libxml2-2.9.12]# make install
```

### 8、安装protobuf

下载路径：[https://github.com/protocolbuffers/protobuf/archive/v3.10.1.tar.gz](https://github.com/protocolbuffers/protobuf/archive/v3.10.1.tar.gz "https://github.com/protocolbuffers/protobuf/archive/v3.10.1.tar.gz")

```diff
[root@localhost src]# tar -zxvf protobuf-3.10.1.tar.gz
[root@localhost src]# cd protobuf-3.10.1/
[root@localhost protobuf-3.10.1]# ./autogen.sh --prefix=/usr/local/protobuf-3.10.1
[root@localhost protobuf-3.10.1]# ./configure --prefix=/usr/local/protobuf-3.10.1
//make编译
[root@localhost protobuf-3.10.1]# make -j 4
[root@localhost protobuf-3.10.1]# make install
//配置环境变量
[root@localhost protobuf-3.10.1]# vim /etc/profile
export PROTOBUF_HOME=/usr/local/protobuf-3.10.1
export PATH=$GCC_HOME/bin:$PROTOBUF_HOME/bin:$PATH
export PKG_CONFIG_PATH=/usr/local/protobuf-3.10.1/lib/pkgconfig:/usr/local/sqlite/lib/pkgconfig:$PKG_CONFIG_PATH
//保存退出，生效文件
[root@localhost protobuf-3.10.1]# source /etc/profile
//验证protobuf是否安装成功
[root@localhost protobuf-3.10.1]# protoc --version
libprotoc 3.10.1
//成功
```

### 9、安装protobuf-c

下载路径：[https://github.com/protobuf-c/protobuf-c/releases/download/v1.3.2/protobuf-c-1.3.2.tar.gz](https://github.com/protobuf-c/protobuf-c/releases/download/v1.3.2/protobuf-c-1.3.2.tar.gz "https://github.com/protobuf-c/protobuf-c/releases/download/v1.3.2/protobuf-c-1.3.2.tar.gz")

```diff
[root@localhost src]# tar -zxvf protobuf-c-1.3.2.tar.gz
[root@localhost src]# cd protobuf-c-1.3.2
//导入protobuf的pkgconfig
[root@localhost protobuf-c-1.3.2]# export PKG_CONFIG_PATH=/usr/local/protobuf-3.10.1/lib/pkgconfig
[root@localhost protobuf-c-1.3.2]# ./configure --prefix=/usr/local/protobuf-c-1.3.2
//make编译
[root@localhost protobuf-c-1.3.2]# make -j 4
[root@localhost protobuf-c-1.3.2]# make install
//配置环境变量
[root@localhost protobuf-c-1.3.2]# vim /etc/profile
export PROTOBUF_HOME=/usr/local/protobuf-3.10.1
export PROTOBUFC_HOME=/usr/local/protobuf-c-1.3.2
export PATH=$GCC_HOME/bin:$PROTOBUF_HOME/bin:$PROTOBUFC_HOME/bin:$PATH
export PKG_CONFIG_PATH=/usr/local/protobuf-3.10.1/lib/pkgconfig:/usr/local/sqlite/lib/pkgconfig:$PKG_CONFIG_PATH
//保存退出，生效文件
[root@localhost protobuf-c-1.3.2]# source /etc/profile
```

### 10、安装sfcgal

10.1、cmake  
下载路径：[https://codeload.github.com/Kitware/CMake/zip/refs/tags/v3.21.1](https://codeload.github.com/Kitware/CMake/zip/refs/tags/v3.21.1 "https://codeload.github.com/Kitware/CMake/zip/refs/tags/v3.21.1")

```diff
[root@localhost src]# unzip CMake-3.21.1.zip
[root@localhost src]# cd CMake-3.21.1/
[root@localhost CMake-3.21.1]# ./configure --prefix=/usr/local/cmake-3.21.1
//make编译
[root@localhost CMake-3.21.1]# make -j 4
[root@localhost CMake-3.21.1]# make install
//配置环境变量
[root@localhost CMake-3.21.1]# vim /etc/profile
export PROTOBUF_HOME=/usr/local/protobuf-3.10.1
export PROTOBUFC_HOME=/usr/local/protobuf-c-1.3.2
export CMAKE_HOME=/usr/local/cmake-3.21.1
export PATH=$GCC_HOME/bin:$CMAKE_HOME/bin:$PROTOBUF_HOME/bin:$PROTOBUFC_HOME/bin:$PATH
export PKG_CONFIG_PATH=/usr/local/protobuf-3.10.1/lib/pkgconfig:/usr/local/sqlite/lib/pkgconfig:$PKG_CONFIG_PATH
//保存退出，生效文件
[root@localhost CMake-3.21.1]# source /etc/profile
```

10.2、cgal  
sfcgal依赖boost,cgal，避免编译sfcgal时各种找不到库的问题。  
yum -y install boost-devel

下载路径：[https://github.com/CGAL/cgal/archive/releases/CGAL-4.13.tar.gz](https://github.com/CGAL/cgal/archive/releases/CGAL-4.13.tar.gz "https://github.com/CGAL/cgal/archive/releases/CGAL-4.13.tar.gz")

```diff
[root@localhost src]# tar -zxvf cgal-releases-CGAL-4.13.tar.gz
[root@localhost src]# cd cgal-releases-CGAL-4.13
[root@localhost cgal-releases-CGAL-4.13]# mkdir build && cd build
//cmake不指定安装目录
[root@localhost build]# cmake ..
//make编译
[root@localhost build]# make -j 4
[root@localhost build]# make install
```

10.3、sfcgal  
下载路径：[https://github.com/Oslandia/SFCGAL/archive/v1.3.8.tar.gz](https://github.com/Oslandia/SFCGAL/archive/v1.3.8.tar.gz "https://github.com/Oslandia/SFCGAL/archive/v1.3.8.tar.gz")

```diff
[root@localhost src]# tar -zxvf v1.3.8.tar.gz
[root@localhost src]# cd SFCGAL-1.3.8/
[root@localhost SFCGAL-1.3.8]# mkdir build && cd build
[root@localhost build]# cmake -DCMAKE_INSTALL_PREFIX=/usr/local/sfcgal-1.3.8 ..
[root@localhost build]# make -j 4
[root@localhost build]# make install
```

### 11、安装PgRouting

pgrouting依赖boost,cgal，如果没有安装，需要安装下  
下载路径：[https://codeload.github.com/pgRouting/pgrouting/zip/refs/tags/v2.6.3](https://codeload.github.com/pgRouting/pgrouting/zip/refs/tags/v2.6.3 "https://codeload.github.com/pgRouting/pgrouting/zip/refs/tags/v2.6.3")

```diff
[root@localhost src]# unzip pgrouting-2.6.3.zip
[root@localhost src]# cd pgrouting-2.6.3/
[root@localhost pgrouting-2.6.3]# mkdir build && cd build
//引入pg的环境变量
[root@localhost build]# source /root/.bash_profile
//cmake不指定安装路径
[root@localhost build]# cmake ..
//make编译
[root@localhost build]# make -j 4
[root@localhost build]# make install
```

### 12、安装postgis

```diff
配置ld.so.conf
[root@localhost src]# vim /etc/ld.so.conf
include ld.so.conf.d/*.conf
/pg/pgsql/lib
/usr/local/proj-6.3.2/lib
/usr/local/gdal-3.3.1/lib
/usr/local/geos-3.9.1/lib
/usr/local/sfcgal-1.3.8/lib64
/usr/local/json-c-0.13.1/lib
/usr/local/libxml2-2.9.12/lib
/usr/local/protobuf-3.10.1/lib
/usr/local/protobuf-c-1.3.2/lib

//保存退出，生效文件
[root@localhost src]# ldconfig -v
```

下载路径：[https://download.osgeo.org/postgis/source/postgis-3.1.3.tar.gz](https://download.osgeo.org/postgis/source/postgis-3.1.3.tar.gz "https://download.osgeo.org/postgis/source/postgis-3.1.3.tar.gz")

```diff
[root@localhost src]# tar -zxvf postgis-3.1.3.tar.gz
[root@localhost src]# cd postgis-3.1.3
//三种安装方式
//基本安装
[root@localhost postgis-3.1.3]# ./configure --prefix=/pg/pgsql --with-gdalconfig=/usr/local/gdal-3.3.1/bin/gdal-config --with-pgconfig=/pg/pgsql/bin/pg_config --with-geosconfig=/usr/local/geos-3.9.1/bin/geos-config --with-projdir=/usr/local/proj-6.3.2 --with-xml2config=/usr/local/libxml2-2.9.12/bin/xml2-config --with-jsondir=/usr/local/json-c-0.13.1
//带protobuf安装，支持mvt
[root@localhost postgis-3.1.3]# ./configure --prefix=/pg/pgsql --with-gdalconfig=/usr/local/gdal-3.3.1/bin/gdal-config --with-pgconfig=/pg/pgsql/bin/pg_config --with-geosconfig=/usr/local/geos-3.9.1/bin/geos-config --with-projdir=/usr/local/proj-6.3.2 --with-xml2config=/usr/local/libxml2-2.9.12/bin/xml2-config --with-jsondir=/usr/local/json-c-0.13.1 --with-protobufdir=/usr/local/protobuf-c-1.3.2 
//带protobuf，sfcgal安装
[root@localhost postgis-3.1.3]# ./configure --prefix=/pg/pgsql --with-gdalconfig=/usr/local/gdal-3.3.1/bin/gdal-config --with-pgconfig=/pg/pgsql/bin/pg_config --with-geosconfig=/usr/local/geos-3.9.1/bin/geos-config --with-projdir=/usr/local/proj-6.3.2 --with-xml2config=/usr/local/libxml2-2.9.12/bin/xml2-config --with-jsondir=/usr/local/json-c-0.13.1 --with-protobufdir=/usr/local/protobuf-c-1.3.2 --with-sfcgal=/usr/local/sfcgal-1.3.8/bin/sfcgal-config
//make编译
[root@localhost postgis-3.1.3]# make -j 4
[root@localhost postgis-3.1.3]# make install
```

### 13、验证安装

```diff
[root@localhost postgis-3.1.3]# su - postgres
Last login: Fri Sep 17 11:16:51 CST 2021 on pts/0
-bash-4.2$ psql
psql (12.6)
Type "help" for help.

postgres=# create datebase mytest;
CREATE DATABASE
postgres=# \c mytest
You are now connected to database "mytest" as user "postgres".
//验证postgis扩展
mytest=# create extension postgis;
CREATE EXTENSION
//验证栅格类数据需要的raster扩展
mytest=# create extension postgis_raster;
CREATE EXTENSION
//如果安装带有sfcgal，验证下三维sfcgal扩展
mytest=# create extension postgis_sfcgal;
CREATE EXTENSION
mytest=# create extension pgrouting;
CREATE EXTENSION
mytest=# \dx
                                List of installed extensions
  Name      | Version |   Schema   |                        Description
----------------+---------+------------+------------------------------------------------------------
pgrouting      | 2.6.3   | public     | pgRouting Extension
plpgsql        | 1.0     | pg_catalog | PL/pgSQL procedural	language
postgis        | 3.1.3   | public     | PostGIS geometry and geography spatial types and functions
postgis_raster | 3.1.3   | public     | PostGIS raster types and functions
postgis_sfcgal | 3.1.3   | public     | PostGIS SFCGAL functions
(5 rows)

mytest=#select name from pg_available_extensions;
         name
------------------------------
plpgsql
pgrouting
postgis
postgis_tiger_geocoder
postgis_raster
postgis_topology
postgis_sfcgal
address_standardizer
address_standardizer_data_us
(9 rows)
```

### 14、环境变量参考

postgis环境变量

```diff
export PG_HOME=/pg/pgsql
export PROTOBUF_HOME=/usr/local/protobuf-3.10.1
export PROTOBUFC_HOME=/usr/local/protobuf-c-1.3.2
export CMAKE_HOME=/usr/local/cmake-3.21.1
export PATH=$GCC_HOME/bin:$CMAKE_HOME/bin:$PROTOBUF_HOME/bin:$PROTOBUFC_HOME/bin:$PATH
export PKG_CONFIG_PATH=/usr/local/protobuf-3.10.1/lib/pkgconfig:/usr/local/sqlite/lib/pkgconfig:$PKG_CONFIG_PATH
```

postgresql环境变量

```diff
[root@localhost build]# cat /root/.bash_profile
# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

# User specific environment and startup programs

PATH=$PATH:$HOME/.local/bin:$HOME/bin

export PATH

PGHOME=/pg/pgsql

export PGHOME

PGDATA=$PGHOME/data

export PGDATA

PATH=$PATH:$HOME/.local/bin:$HOME/bin:$PGHOME/bin

export PATH
```

### 15、文中报错

报错1：安装libxml

```diff
libxml.c:15:20: fatal error: Python.h: No such file or directory

 #include <Python.h>
           	^  
compilation terminated.

libxml2-py.c:4:20: fatal error: Python.h: No such file or directory

 #include <Python.h>
            ^
compilation terminated.

In file included from types.c:9:0:

libxml_wrap.h:1:20: fatal error: Python.h: No such file or directory

 #include <Python.h>
            ^
compilation terminated.
make[4]: *** [libxml.lo] Error 1
make[4]: *** Waiting for unfinished jobs....
make[4]: *** [types.lo] Error 1
make[4]: *** [libxml2-py.lo] Error 1
make[4]: Leaving directory `/root/libxml2-v2.9.12/python'
make[3]: *** [all-recursive] Error 1
make[3]: Leaving directory `/root/libxml2-v2.9.12/python'
make[2]: *** [all] Error 2
make[2]: Leaving directory `/root/libxml2-v2.9.12/python'
make[1]: *** [all-recursive] Error 1
make[1]: Leaving directory `/root/libxml2-v2.9.12'
make: *** [all] Error 2
```

解决方式：yum install python-dev\*

报错2：安装cgal

```diff
-- Could NOT find GMP (missing: GMP_LIBRARIES GMP_INCLUDE_DIR)

CMake Error at Installation/cmake/modules/CGAL_SetupDependencies.cmake:66 (message):

CGAL requires GMP to be found

Call Stack (most recent call first):

 Installation/CMakeLists.txt:673 (include)

-- Configuring incomplete, errors occurred!

See also "/root/cgal-releases-CGAL-4.13/build/CMakeFiles/CMakeOutput.log". E_DIR)
```

解决方式：yum -y install gmp\* mpfr\*