---
layout: post
title: JVM内存设置多大合适？Xmx和Xmn如何设置？
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "Grbk@2024"
typora-root-url: ./..
date: 2024-05-24 10:45:56
---
# 1、问题
Full GC为一次特殊GC行为的描述，这次GC会回收整个堆的内存，包含老年代，新生代，metaspace等
新上线一个java服务，或者是RPC或者是WEB站点， 内存的设置该怎么设置呢？设置成多大比较合适，既不浪费内存，又不影响性能呢？
分析：
依据的原则是根据Java Performance里面的推荐公式来进行设置。
 
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637811515231-8afac8c5-fe14-41dd-b1dc-3d1ec436ffb5.png#clientId=u5f4cbcf5-9031-4&from=paste&id=u33b480a8&originHeight=237&originWidth=640&originalType=url&ratio=1&size=105674&status=done&style=none&taskId=u77278c14-16ca-461a-b11b-9b64240e8b2)
<!--more-->
具体来讲：
	Java整个堆大小设置，Xmx 和 Xms设置为老年代存活对象的3-4倍，即FullGC之后的老年代内存占用的3-4倍
	永久代 PermSize和MaxPermSize设置为老年代存活对象的1.2-1.5倍。
	年轻代Xmn的设置为老年代存活对象的1-1.5倍。
	老年代的内存大小设置为老年代存活对象的2-3倍。
BTW：
	1、Sun官方建议年轻代的大小为整个堆的3/8左右， 所以按照上述设置的方式，基本符合Sun的建议。
	2、堆大小=年轻代大小+年老代大小， 即xmx=xmn+老年代大小 。 Permsize不影响堆大小。
	3、为什么要按照上面的来进行设置呢？ 没有具体的说明，但应该是根据多种调优之后得出的一个结论。
# 2、如何确认老年代存活对象大小？
### 方式1（推荐/比较稳妥）：
JVM参数中添加GC日志，GC日志中会记录每次FullGC之后各代的内存大小，观察老年代GC之后的空间大小。可观察一段时间内（比如2天）的FullGC之后的内存情况，根据多次的FullGC之后的老年代的空间大小数据来预估FullGC之后老年代的存活对象大小（可根据多次FullGC之后的内存大小取平均值）

### 方式2：（强制触发FullGC, 会影响线上服务，慎用）

	方式1的方式比较可行，但需要更改JVM参数，并分析日志。同时，在使用CMS回收器的时候，有可能不能触发FullGC（只发生CMS GC），所以日志中并没有记录FullGC的日志。在分析的时候就比较难处理。
	BTW：使用jstat -gcutil工具来看FullGC的时候， CMS GC是会造成2次的FullGC次数增加。 具体可参见之前写的一篇关于jstat使用的文章
所以，有时候需要强制触发一次FullGC，来观察FullGC之后的老年代存活对象大小。
	注：强制触发FullGC，会造成线上服务停顿（STW），要谨慎，建议的操作方式为，在强制FullGC前先把服务节点摘除，FullGC之后再将服务挂回可用节点，对外提供服务
在不同时间段触发FullGC，根据多次FullGC之后的老年代内存情况来预估FullGC之后的老年代存活对象大小
# 3、如何触发FullGC ？
## 使用jmap工具可触发FullGC

	jmap -dump:live,format=b,file=heap.bin <pid> 将当前的存活对象dump到文件，此时会触发FullGC
	jmap -histo:live <pid> 打印每个class的实例数目,内存占用,类全名信息.live子参数加上后,只统计活的对象数量. 此时会触发FullGC
具体操作实例：
	以我司的一个RPC服务为例。
	BTW：刚上线的新服务，不知道该设置多大的内存的时候，可以先多设置一点内存，然后根据GC之后的情况来进行分析。
	初始JVM内存参数设置为： Xmx=2G Xms=2G xmn=1G
使用jstat 查看当前的GC情况。如下图：
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637811515118-a4db2bc4-67fc-4dc7-90ee-7fa1abe09f1a.png#clientId=u5f4cbcf5-9031-4&from=paste&id=ube3d647e&originHeight=190&originWidth=540&originalType=url&ratio=1&size=36358&status=done&style=none&taskId=u25ae3e69-119d-410f-9392-d27dcb0849c)
YGC平均耗时： 173.825s/15799=11ms
FGC平均耗时：0.817s/41=19.9ms
平均大约10-20s会产生一次YGC
看起来似乎不错，YGC触发的频率不高，FGC的耗时也不高，但这样的内存设置是不是有些浪费呢？
为了快速看数据，我们使用了方式2，产生了几次FullGC，FullGC之后，使用的jmap -heap 来看的当前的堆内存情况（也可以根据GC日志来看）
heap情况如下图：（命令 ： jmap -heap <pid>）
 
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637811515241-3a6925f8-0be9-4beb-b895-bcd3209580cd.png#clientId=u5f4cbcf5-9031-4&from=paste&id=u29cbf2ec&originHeight=803&originWidth=423&originalType=url&ratio=1&size=99994&status=done&style=none&taskId=u9c0fd87e-82cc-41cf-ba83-78362a2e4c3)
上图中的concurrent mark-sweep generation即为老年代的内存描述。
老年代的内存占用为100M左右。 按照整个堆大小是老年代（FullGC）之后的3-4倍计算的话，设置各代的内存情况如下：
Xmx=512m Xms=512m Xmn=128m PermSize=128m 老年代的大小为 （512-128=384m）为老年代存活对象大小的3倍左右
调整之后的，heap情况
 
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637811515253-faf378ae-c345-403f-9eec-89620043ad24.png#clientId=u5f4cbcf5-9031-4&from=paste&id=u872d57a4&originHeight=794&originWidth=357&originalType=url&ratio=1&size=97002&status=done&style=none&taskId=u74c7a701-8b4b-48af-8d7b-a2c61b31ceb)
GC情况如下：
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637811515151-bbdf5e73-da64-4096-a7d6-3e7afdf62fca.png#clientId=u5f4cbcf5-9031-4&from=paste&id=u526b7051&originHeight=286&originWidth=559&originalType=url&ratio=1&size=53427&status=done&style=none&taskId=u6201a717-33e3-42e8-a4d4-97152f03095)
YGC 差不多在10s左右触发一次。每次YGC平均耗时大约9.41ms。可接受。
FGC平均耗时：0.016s/2=8ms
整体的GC耗时减少。但GC频率比之前的2G时的要多了一些。
注： 看上述GC的时候，发现YGC的次数突然会增多很多个，比如 从1359次到了1364次。具体原因是？
总结：
	在内存相对紧张的情况下，可以按照上述的方式来进行内存的调优， 找到一个在GC频率和GC耗时上都可接受的一个内存设置，可以用较小的内存满足当前的服务需要
但当内存相对宽裕的时候，可以相对给服务多增加一点内存，可以减少GC的频率，GC的耗时相应会增加一些。 一般要求低延时的可以考虑多设置一点内存， 对延时要求不高的，可以按照上述方式设置较小内存。
补充：
	永久代（方法区）并不在堆内，所以之前有看过一篇文章中描述的 整个堆大小=年轻代+年老代+永久代的描述是不正确的。
# 4、补充
-verbose:gc 现实垃圾收集信息
-Xloggc:gc.log 指定垃圾收集日志文件
-Xmn：young generation的heap大小，一般设置为Xmx的3、4分之一
-XX:SurvivorRatio=2 :生还者池的大小,默认是2，如果垃圾回收变成了瓶颈，您可以尝试定制生成池设置
-XX:NewSize: 新生成的池的初始大小。 缺省值为2M。
-XX:MaxNewSize: 新生成的池的最大大小。 缺省值为32M。
+XX:AggressiveHeap 会使得 Xms没有意义。这个参数让jvm忽略Xmx参数,疯狂地吃完一个G物理内存,再吃尽一个G的swap。
-Xss：每个线程的Stack大小，“-Xss 15120” 这使得JBoss每增加一个线程（thread)就会立即消耗15M内存，而最佳值应该是128K,默认值好像是512k.
# 5、术语和工具
JVM按照其存储数据的内容将所需内存分配为堆区与非堆区两个部分：所谓堆区即为通过new的方式创建的对象（类实例）所占用的内存空间；非堆区即为代码、常量、外部访问（如文件访问流所占资源）等。然而虽然java的垃圾回收机制虽然能够很好的解决内存浪费的问题，但是这种机制也仅仅的是回收堆区的资源，而对于非堆区的资源就束手无策了，针对这样的资源回收只能凭借开发人员自身的约束来解决。就算是这样（堆区有java回收机制、非堆区开发人员能够很好的解决），当运行时所需内存瞬间激增的时候JVM无奈的也要中止程序的运行。所以本文讲述的是如何解决后者的问题。
首先，常见参数种类配置内存：-Xms 、-Xmx、-XX:newSize、-XX:MaxnewSize、-Xmn，是用来配置堆区的，-XX:PermSize、-XX:MaxPermSize是用来配置非堆区的。
## 堆

1. -Xms ：表示java虚拟机堆区内存初始内存分配的大小，通常为操作系统可用内存的1/64大小即可，但仍需按照实际情况进行分配。有可能真的按照这样的一个规则分配时，设计出的软件还没有能够运行得起来就挂了。
2. -Xmx： 表示java虚拟机堆区内存可被分配的最大上限，通常为操作系统可用内存的1/4大小。但是开发过程中，通常会将 -Xms 与 -Xmx两个参数的配置相同的值，其目的是为了能够在java垃圾回收机制清理完堆区后不需要重新分隔计算堆区的大小而浪费资源。



如果想要进行更加精细的分配还可以对堆区内存进一步的细化，那就要用到下面的三个参数了-XX:newSize、-XX:MaxnewSize、-Xmn。当然这源于对堆区的进一步细化分：新生代、中生代、老生代。java中每新new一个对象所占用的内存空间就是新生代的空间，当java垃圾回收机制对堆区进行资源回收后，那些新生代中没有被回收的资源将被转移到中生代，中生代的被转移到老生代。而接下来要讲述的三个参数是用来控制新生代内存大小的。

1. -XX:newSize：表示新生代初始内存的大小，应该小于 -Xms的值；
2. -XX:MaxnewSize：表示新生代可被分配的内存的最大上限；当然这个值应该小于 -Xmx的值；
3. -Xmn：至于这个参数则是对 -XX:newSize、-XX:MaxnewSize两个参数的同时配置，也就是说如果通过-Xmn来配置新生代的内存大小，那么-XX:newSize = -XX:MaxnewSize = -Xmn，虽然会很方便，但需要注意的是这个参数是在JDK1.4版本以后才使用的。
## 非堆

1. -XX:PermSize：表示非堆区初始内存分配大小，其缩写为permanent size（持久化内存）
2. -XX:MaxPermSize：表示对非堆区分配的内存的最大上限。

这里面非常要注意的一点是：在配置之前一定要慎重的考虑一下自身软件所需要的非堆区内存大小，因为此处内存是不会被java垃圾回收机制进行处理的地方。并且更加要注意的是 最大堆内存与最大非堆内存的和绝对不能够超出操作系统的可用内存。


# 3 JVM性能调优监控工具详解
现实企业级Java开发中，会碰到如下问题：
1.OutOfMemoryError，内存不足
2.内存溢出
3.线程锁死
4.锁征用
5.Java进程消耗CPU过高
通过JVM一些常用的监控性能调优工具，可以很好的监控与发现问题所在。
在中银项目中出现了内存溢出的现象，通过使用各种工具配合使用来发现是那些对象没有成功释放，从而解决内存溢出的问题。
## jps
## jps（Java Virtual Machine Process Status Tool）主要用来输出JVM中运行的进程状态信息。语法格式如下：
> jps [options] [hostid] 

如果不指定hostid就默认为当前主机或服务器。
命令行参数如下：
> -q 不输出类名、Jar名和传入main方法的参数 
> -m 输出传入main方法的参数 
> -l 输出main类或Jar的全限名 
> -v 输出传入JVM的参数 

如下图：
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637813103007-8ccb35fa-a0d4-4e17-815b-ab63fc6bd7ac.png#clientId=u5f4cbcf5-9031-4&from=paste&id=u1dda8f8e&originHeight=331&originWidth=907&originalType=url&ratio=1&size=13724&status=done&style=none&taskId=u872a182e-be12-4ded-bd6a-9d07e710cf2)
## jstack
jstack主要用来查看某个Java进程内的线程堆栈信息。语法格式如下：
> jstack [option] pid
> jstack [option] executablecore
> jstack [option] [server-id@]remote-hostname-or-ip

命令行参数如下：
> -l long listings，会打印出额外的锁信息，在发生死锁时可以用jstack -l pid来观察锁持有情况
> -m mixed mode，不仅会输出Java堆栈信息，还会输出C/C++堆栈信息（比如Native方法）

jstack可以定位到线程堆栈，根据堆栈信息我们可以定位到具体代码，所以它在JVM性能调优中使用得非常多。找出某个Java进程中最耗费CPU的Java线程并定位堆栈信息，用到的命令有ps、top、printf、jstack、grep。操作如下：
1.查询Java进程ID，如下图：
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637813139878-11f079da-9659-4b53-bf0e-19915df4b607.png#clientId=u5f4cbcf5-9031-4&from=paste&id=uba4645f5&originHeight=250&originWidth=1253&originalType=url&ratio=1&size=24153&status=done&style=none&taskId=ue44e3775-5847-4fb4-bc7e-7f7ba13736b)
2.通过进程ID查询对CPU消耗最大的线程，可以使用ps -Lfp pid或者ps -mp pid -o THREAD，tid，time或者top -Hp pid，我这里用第三个，如下图：
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637813139857-c5392039-d03e-457f-a767-e350ff6a6c5f.png#clientId=u5f4cbcf5-9031-4&from=paste&id=u45318393&originHeight=392&originWidth=792&originalType=url&ratio=1&size=43548&status=done&style=none&taskId=ua4117adc-0ba9-46d9-81a0-87a70b154da)
将线程ID转成16进制用于查询，使用如下命令即可实现：
> printf "%x\n" pid 

3.使用jstack输出进程的堆栈信息，如下图：
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637813139859-71a9080b-f6d9-4808-bdcd-5eca9541fbfd.png#clientId=u5f4cbcf5-9031-4&from=paste&id=uca10b5c2&originHeight=263&originWidth=763&originalType=url&ratio=1&size=9980&status=done&style=none&taskId=uc5375df9-10be-4d7c-943a-27cd4daa2a0)
## jmap和jhat
jmap（Memory Map）用来查看堆内存使用状况，一般结合jhat（Java Heap Analysis Tool）使用。语法格式如下：
> jmap [option] pid
> jmap [option] executablecore
> jmap [option] [server-id@]remote-hostname-or-ip 

1.没有参数打印进程的类加载器和类加载器加载的持久代对象信息，输出：类加载器名称、对象是否存活（不可靠）、对象地址、父类加载器、已加载的类大小等信息，如下图：
> jmap pid 

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637813161675-525f50cd-51e1-461b-9f6c-b04900bd9ba8.png#clientId=u5f4cbcf5-9031-4&from=paste&id=u52b5b6be&originHeight=784&originWidth=1920&originalType=url&ratio=1&size=108520&status=done&style=none&taskId=uc1f99be8-b5d1-46b2-aec1-f59fe28f942)
2.查看进程堆内存使用情况，包括使用的GC算法、堆配置参数和各代中堆内存使用情况。比如下面的例子：
> jmap -heap pid 

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637813161705-abed0f70-8b85-49e5-bf48-1533463ee8b6.png#clientId=u5f4cbcf5-9031-4&from=paste&id=u89755e36&originHeight=784&originWidth=1920&originalType=url&ratio=1&size=99721&status=done&style=none&taskId=uda70167f-b587-401f-b828-50daa4e3499)
3.使用jmap -histo[:live] pid查看堆内存中的对象数目、大小统计直方图，如果带上live则只统计活对象并且会强制执行一次GC，如下：
> jmap -histo pid 
> jmap -histo:live pid 

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637813161731-41103103-85fb-433e-96bf-ed7052ddbdba.png#clientId=u5f4cbcf5-9031-4&from=paste&id=u9fc9d51f&originHeight=784&originWidth=1920&originalType=url&ratio=1&size=114414&status=done&style=none&taskId=uec587564-7f60-4147-a966-ab6eb879609)
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637813161869-3e7e6562-8d31-4c48-9f46-69abdf1fe14f.png#clientId=u5f4cbcf5-9031-4&from=paste&id=uccdb0a24&originHeight=784&originWidth=1920&originalType=url&ratio=1&size=113563&status=done&style=none&taskId=u8ae83391-60a8-41d2-b919-989887441fd)
class name是对象类型，说明如下：
> B  byte
> C  char
> D  double
> F  float
> I  int
> J  long
> Z  boolean
> [  数组，如[I表示int[]
> [L+类名 其他对象

还有一个很常用的情况是：用jmap把进程内存使用情况dump到文件中，再用jhat分析查看。jmap进行dump命令格式如下：
> jmap -dump:format=b,file=dumpFileName pid (文件的后缀建议采用".hprof") 

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637813161603-1e144742-d778-4b0d-8002-76326d33a719.png#clientId=u5f4cbcf5-9031-4&from=paste&id=u139d596c&originHeight=784&originWidth=1920&originalType=url&ratio=1&size=36796&status=done&style=none&taskId=u7c606118-6693-4bcf-94e8-37b075f726f)
dump出来的文件可以用MAT、VisualVM等工具查看，这里用jhat查看：
> jhat -port xxxx dumpFileName 

![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637813163735-dd61a3f7-4b56-4424-ba94-d6b8b9b97447.png#clientId=u5f4cbcf5-9031-4&from=paste&id=u4d4a4691&originHeight=784&originWidth=1920&originalType=url&ratio=1&size=46077&status=done&style=none&taskId=u3802b578-189e-4e88-9fe1-a4979baff52)
然后就可以在浏览器中输入主机地址:port查看了：
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637813163849-b1bdefbc-9b0c-4b79-a97a-f4f3ae2f8f79.png#clientId=u5f4cbcf5-9031-4&from=paste&id=u6fc46b91&originHeight=1030&originWidth=1920&originalType=url&ratio=1&size=194108&status=done&style=none&taskId=uf40a065a-6057-46d0-9352-f93c085881a)
## jstat
jstat（JVM统计监测工具），监控的内容有：类装载、内存、垃圾收集、jit编译的信息。语法格式如下：
> jstat [ generalOption | outputOptions vmid [interval[s|ms] [count]] ] 

vmid是虚拟机ID，在Linux/Unix系统上一般就是进程ID。interval是采样时间间隔。count是采样数目。比如下面输出的是GC信息，采样时间间隔为250ms，采样数为4：
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637813175752-2d779e8c-f9a0-4afb-9ad4-f21445109836.png#clientId=u5f4cbcf5-9031-4&from=paste&id=uc8d58f5c&originHeight=784&originWidth=1920&originalType=url&ratio=1&size=49741&status=done&style=none&taskId=u127583e7-bf0a-4b84-872b-b051d8d6c8e)
要明白上面各列的意义，先看JVM堆内存布局：
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1637813175754-f310dbca-7086-47f4-99c6-6d83b9e526b5.png#clientId=u5f4cbcf5-9031-4&from=paste&id=ue9ddbca8&originHeight=158&originWidth=300&originalType=url&ratio=1&size=41863&status=done&style=none&taskId=u75387c40-3a46-4c8a-b528-2282396a07e)
可以看出：
> 堆内存 = 年轻代 + 年老代 + 永久代 
> 年轻代 = Eden区 + 两个Survivor区（From和To） 

各列含义：
> S0C、S1C、S0U、S1U：Survivor 0/1区容量（Capacity）和使用量（Used）
> EC、EU：Eden区容量和使用量
> OC、OU：年老代容量和使用量
> PC、PU：永久代容量和使用量
> YGC、YGT：年轻代GC次数和GC耗时
> FGC、FGCT：Full GC次数和Full GC耗时
> GCT：GC总耗时

## jinfo
jinfo（实时查看与调整虚拟机的各项参数），语法格式如下：
> jinfo [option] <pid> jinfo [option] <executable <core> jinfo [option] [server_id@]<remote server IP or hostname>

## jconsole
jconsole，作用有：内存监控、线程监控、死锁。

# 测试
**具体操作实例：**
初始JVM内存参数设置为： Xmx=64M
使用jstat 查看当前的GC情况。如下图：
每6s显示一次  jstat -gcutil 100248 6000
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1638166089739-d059f9e8-4fbe-45dd-b43a-985f2e9c1fb5.png#clientId=ub1dc235f-1bc7-4&from=paste&height=195&id=ud7057d0d&originHeight=390&originWidth=783&originalType=binary&ratio=1&size=356342&status=done&style=none&taskId=u77a7106f-fc2a-4db2-8e04-fa9b1d93194&width=391.5)
YGC平均耗时： 0.290s/162=0.00179ms
FGC平均耗时：0.099s/3=0.033ms
平均大约0.001-0.002会产生一次YGC

[root@network nginxWebUI]# jmap -heap 100248

> New Generation (Eden + 1 Survivor Space):

>    capacity = 12976128 (12.375MB)

>    used     = 1808008 (1.7242507934570312MB)

>    free     = 11168120 (10.650749206542969MB)

>    13.933339745107324% used

> tenured generation:

>    capacity = 28602368 (27.27734375MB)

>    used     = 28432480 (27.115325927734375MB)

>    free     = 169888 (0.162017822265625MB)

>    99.40603519261063% used


**触发FullGC：**
**#**将当前的存活对象dump到文件，此时会触发FullGC
jmap -dump:live,format=b,file=heap.bin 100248
#打印每个class的实例数目,内存占用,类全名信息.live子参数加上后,只统计活的对象数量. 此时会触发FullGC
jmap -histo:live 100248

每6s显示一次  jstat -gcutil 100248 6000
![image.png](https://cdn.nlark.com/yuque/0/2021/png/12484160/1638166417397-99d1245b-7437-4b6b-9f08-5fc799f9c516.png#clientId=ub1dc235f-1bc7-4&from=paste&height=111&id=u118f7194&originHeight=222&originWidth=768&originalType=binary&ratio=1&size=195669&status=done&style=none&taskId=ucc86818e-d761-4d07-91df-127680135e3&width=384)
YGC平均耗时： 0.296s/164=0.0018ms
FGC平均耗时：0.248s/5=0.0496ms
平均大约0.0018会产生一次YGC

[root@network nginxWebUI]# jmap -heap 100248

> New Generation (Eden + 1 Survivor Space):

>    capacity = 15532032 (14.8125MB)

>    used     = 2673952 (2.550079345703125MB)

>    free     = 12858080 (12.262420654296875MB)

>    17.215725540611814% used

> tenured generation:

>    capacity = 34287616 (32.69921875MB)

>    used     = 20571944 (19.618934631347656MB)

>    free     = 13715672 (13.080284118652344MB)

>    59.998175434535895% used

tenured generation 即为老年代的内存描述。
老年代的内存占用为20M左右。年轻代的内存占用为3M左右。 按照整个堆大小是老年代（FullGC）之后的3-4倍计算的话，设置各代的内存情况如下：
     -Xmx72m  -Xms72m  -Xmn12m   老年代的大小为 （72-12=60m）为老年代存活对象大小的3倍左右
调整之后的，heap情况（jmap -heap pid）：
[root@network nginxWebUI]# jmap -heap 31905
> New Generation (Eden + 1 Survivor Space):

>    capacity = 11337728 (10.8125MB)

>    used     = 6419736 (6.122337341308594MB)

>    free     = 4917992 (4.690162658691406MB)

>    56.622773098807805% used
> tenured generation:

>    capacity = 62914560 (60.0MB)

>    used     = 29976016 (28.587356567382812MB)

>    free     = 32938544 (31.412643432617188MB)

>    47.64559427897135% used



GC情况如下(jstat -gcutil pid):
[root@network nginxWebUI]# jstat -gcutil 31905 6000

>   S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT     GCT   

>  75.97   0.00  86.60  49.03  92.96  90.43    106    0.344     2    0.084    0.428

>  75.97   0.00  86.60  49.03  92.96  90.43    106    0.344     2    0.084    0.428

>  75.97   0.00  86.60  49.03  92.96  90.43    106    0.344     2    0.084    0.428

>  75.97   0.00  90.93  49.03  92.96  90.43    106    0.344     2    0.084    0.428

>  75.97   0.00  90.93  49.03  92.96  90.43    106    0.344     2    0.084    0.428

>  75.97   0.00  90.93  49.03  92.96  90.43    106    0.344     2    0.084    0.428

>  75.97   0.00  90.93  49.03  92.96  90.43    106    0.344     2    0.084    0.428

> 

