
    layout: post
    title: Shell文本处理grep、sed、awk
    tags:
    - 语雀
    categories:
    - [语雀,我的知识库]
    abbrlink: 
    date: 2024-05-22 17:28:46
    
## grep
grep是一款强大的文本搜索工具，支持正则表达式。
常用参数:
```bash
 -v        取反
 -i        忽略大小写
 -c        符合条件的行数
 -n        输出的同时打印行号
 ^*        以*开头         
<!--more-->
 *$        以*结尾 
 ^$        空行 
```
```bash
# 示例文本
[root@iz2ze76ybn73dvwmdij06zz ~]# cat monkey
One day,a little monkey is playing by the well.一天,有只小猴子在井边玩儿.
He looks in the well and shouts :它往井里一瞧,高喊道：
“Oh!My god!The moon has fallen into the well!” “噢!我的天!月亮掉到井里头啦!”
An older monkeys runs over,takes a look,and says,一只大猴子跑来一看,说,
“Goodness me!The moon is really in the water!” “糟啦!月亮掉在井里头啦!”
And olderly monkey comes over.老猴子也跑过来.
He is very surprised as well and cries out:他也非常惊奇,喊道：
“The moon is in the well.” “糟了,月亮掉在井里头了!”
A group of monkeys run over to the well .一群猴子跑到井边来,
They look at the moon in the well and shout:他们看到井里的月亮,喊道：
“The moon did fall into the well!Come on!Let’get it out!”
“月亮掉在井里头啦!快来!让我们把它捞起来!”
Then,the oldest monkey hangs on the tree up side down ,with his feet on the branch .
然后,老猴子倒挂在大树上,
And he pulls the next monkey’s feet with his hands.拉住大猴子的脚,
All the other monkeys follow his suit,其他的猴子一个个跟着,
And they join each other one by one down to the moon in the well.
它们一只连着一只直到井里.
Just before they reach the moon,the oldest monkey raises his head and happens to see the moon in the sky,正好他们摸到月亮的时候,老猴子抬头发现月亮挂在天上呢
He yells excitedly “Don’t be so foolish!The moon is still in the sky!”
它兴奋地大叫：“别蠢了!月亮还好好地挂在天上呢!


# 直接查找符合条件的行
➜ cat monkey | grep moon

# 查找反向符合条件的行
➜ cat monkey | grep -v moon

# 直接查找符合条件的行数
➜ cat monkey | grep -c  moon

# 忽略大小写查找符合条件的行数
➜ cat monkey | grep -i my

# 查找符合条件的行并输出行号
➜ cat monkey | grep -n moon

# 查找开头是J的行
➜ cat monkey | grep '^J'

# 查找结尾是呢的行
➜ cat monkey | grep "呢$"
```
## sed
sed是一种流编辑器，是一款处理文本比较优秀的工具，可以结合正则表达式一起使用。

### sed执行过程
![](https://cdn.nlark.com/yuque/0/2022/webp/12484160/1653873455635-c9b46f88-46e2-4f62-b812-bf196456b318.webp#averageHue=%23e8f1b8&clientId=u41f0373c-e280-4&from=paste&id=ua778ea8e&originHeight=872&originWidth=794&originalType=url&ratio=1&rotation=0&showTitle=false&status=done&style=none&taskId=u3dfde6a8-4bcb-4e8c-b787-73bc6420acc&title=)
常用命令:
```bash
   d  删除选择的行    
   s   查找    
   y  替换
   i   当前行前面插入一行
   a  当前行后面插入一行
   p  打印行       
   q  退出     

 替换符:

   数字 ：替换第几处    
   g :  全局替换    
   \1:  子串匹配标记，前面搜索可以用元字符集\(..\)
   &:  保留搜索刀的字符用来替换其他字符
```
示例：
```bash
# 示例文本
➜ cat word
Twinkle, twinkle, little star
How I wonder what you are
Up above the world so high
Like a diamond in the sky
When the blazing sun is gone
little

➜ cat word1
Oh if there's one thing to be taught
it's dreams are made to be caught
and friends can never be bought
Doesn't matter how long it's been
I know you'll always jump in
'Cause we don't know how to quit

# 替换
# 全局替换
➜ sed  's/little/big/g' word
Twinkle, twinkle, big star
How I wonder what you are
Up above the world so high
Like a diamond in the sky
When the blazing sun is gone
big

# 全局替换并修改(去掉 -i 表示打印当前替换后的文本，但实际上未对文件做修改)
➜ sed -i 's/little/big/g' word
Twinkle, twinkle, big star
How I wonder what you are
Up above the world so high
Like a diamond in the sky
When the blazing sun is gone
big

# 按行替换（替换2到最后一行)
➜ sed '2,$s/to/can/' word1
Oh if there's one thing to be taught
it's dreams are made can be caught
and friends can never be bought
Doesn't matter how long it's been
I know you'll always jump in
'Cause we don't know how can quit

# 删除
➜  sed '2d' word
Twinkle, twinkle, little star
Up above the world so high
Like a diamond in the sky
When the blazing sun is gone

# 显示行号
➜  sed '=;2d' word
1
Twinkle, twinkle, little star
2
3
Up above the world so high
4
Like a diamond in the sky
5
When the blazing sun is gone
6
little

# 删除第2行到第四行
➜  happy sed '=;2,4d' word
1
Twinkle, twinkle, little star
2
3
4
5
When the blazing sun is gone
6
little

# 添加行
# 向前插入
➜  echo "hello" | sed 'i\kitty'
kitty
hello
# 向后插入
➜  echo "kitty" | sed 'i\hello'
hello
kitty

# 修改行
# 替换第二行为hello kitty
➜  sed '2c\hello kitty' word
Twinkle, twinkle, little star
hello kitty
Up above the world so high
Like a diamond in the sky
When the blazing sun is gone

# 替换第二行到最后一行为hello kitty
➜  sed '2,$c\hello kitty' word
Twinkle, twinkle, little star
hello kitty

# 写入行
# 把带star的行写入c文件中,c提前创建
➜  sed -n '/star/w c' word
➜  cat c
Twinkle, twinkle, little star

# 退出
# 打印3行后，退出sed
➜  sed '3q' word
Twinkle, twinkle, little star
How I wonder what you are
Up above the world so high
```
## awk
比起sed和grep，awk不仅仅是一个小工具，也可以算得上一种小型的编程语言了，支持if判断分支和while循环语句还有它的内置函数等，是一个要比grep和sed更强大的文本处理工具。

