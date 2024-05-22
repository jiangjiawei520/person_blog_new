
    layout: post
    title: centos抓包 tcpdump
    tags:
    - 语雀
    categories:
    - [语雀,我的知识库]
    abbrlink: 
    date: 2024-05-22 17:28:46
    
准备工作：
1、安装flex
yum -y install flex
2、安装bison
yum -y install bison
安装tcpdump：
wget http://www.tcpdump.org/release/libpcap-1.5.3.tar.gz
wget http://www.tcpdump.org/release/tcpdump-4.5.1.tar.gz
tar -zxvf libpcap-1.5.3.tar.gz
<!--more-->
cd libpcap-1.5.3
./configure
sudo make install

cd ..
tar -zxvf tcpdump-4.5.1.tar.gz
cd tcpdump-4.5.1
./configure
sudo make install
使用：
tcpdump -i eth0（网卡） dst host 10.100.3.16（目标服务器） and src host DEV-mHRO64（源地址服务器） -X

-X：以十六进制与ASCII方式输出，用于抓取http等明文传输协议
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1639459397212-2721b33c-bc5e-4fdd-8ea1-e598f35980d3.png#averageHue=%232d2c24&clientId=u64540ab1-f6f5-4&from=paste&id=u5df3d162&originHeight=473&originWidth=1078&originalType=url&ratio=1&rotation=0&showTitle=false&size=62383&status=done&style=none&taskId=u83c467cc-4ec8-401c-9861-d47dcf0f7d4&title=)

例子
> 1、抓取包含10.10.10.122的数据包
> 
> tcpdump -i eth0 -vnn host 10.10.10.122
> 2、抓取包含10.10.10.0/24网段的数据包
> 
> tcpdump -i eth0 -vnn net 10.10.10.0/24
> 3、抓取包含端口22的数据包
> 
> tcpdump -i eth0 -vnn port 22
> 4、抓取udp协议的数据包
> 
> tcpdump -i eth0 -vnn udp
> 5、抓取icmp协议的数据包
> 
> tcpdump -i eth0 -vnn icmp
> 6、抓取arp协议的数据包
> 
> tcpdump -i eth0 -vnn arp
> 7、抓取ip协议的数据包
> 
> tcpdump -i eth0 -vnn ip
> 8、抓取源ip是10.10.10.122数据包。
> 
> tcpdump -i eth0 -vnn src host 10.10.10.122
> 9、抓取目的ip是10.10.10.122数据包
> 
> tcpdump -i eth0 -vnn dst host 10.10.10.122
> 10、抓取源端口是22的数据包
> 
> tcpdump -i eth0 -vnn src port 22
> 11、抓取源ip是10.10.10.253且目的ip是22的数据包
> 
> tcpdump -i eth0 -vnn src host 10.10.10.253 and dst port 22
> 12、抓取源ip是10.10.10.122或者包含端口是22的数据包
> 
> tcpdump -i eth0 -vnn src host 10.10.10.122 or port 22
> 13、抓取源ip是10.10.10.122且端口不是22的数据包
> 
> tcpdump -i eth0 -vnn src host 10.10.10.122 and not port 22
> 14、抓取源ip是10.10.10.2且目的端口是22，或源ip是10.10.10.65且目的端口是80的数据包。
> 
> tcpdump -i eth0 -vnn ( src host 10.10.10.2 and dst port 22 ) or ( src host 10.10.10.65 and dst port 80 )
> 15、抓取源ip是10.10.10.59且目的端口是22，或源ip是10.10.10.68且目的端口是80的数据包。
> 
> tcpdump -i eth0 -vnn ‘src host 10.10.10.59 and dst port 22’ or ’ src host 10.10.10.68 and dst port 80 ’
> 16、把抓取的数据包记录存到/tmp/fill文件中，当抓取100个数据包后就退出程序。
> 
> tcpdump –i eth0 -vnn -w /tmp/fil1 -c 100
> 17、从/tmp/fill记录中读取tcp协议的数据包
> 
> tcpdump –i eth0 -vnn -r /tmp/fil1 tcp
> 18、从/tmp/fill记录中读取包含10.10.10.58的数据包
> 
> tcpdump –i eth0 -vnn -r /tmp/fil1 host 10.10.10.58


获取到某目的主键的包
tcpdump dst host xxxx -A  
tcpdump -i eth0 -nntvvv -S dst host 19.16.240.43
tcpdump  host 173.16.33.90 and 19.16.240.43 -A -S -vv
eg:
tcpdump -i eth0 dst host 19.15.127.175 -A

抓取服务所有的包并写入文件
tcpdump -i any -A -nn -vvv -w login_https.pcap

tcpdump -S host <IP地址>：截获该IP的主机收到的和发出的所有的数据包
tcpdump -S host <IP地址> and <IP地址>：截获两个IP对应主机之间的通信
tcpdump -S port <端口号>：截获本机80端口的数据包
-S 参数的目的是获得ack的绝对值，不加该参数，第三次握手的ack为相对值1

[https://www.10qianwan.com/articledetail/253887.html](https://www.10qianwan.com/articledetail/253887.html)
