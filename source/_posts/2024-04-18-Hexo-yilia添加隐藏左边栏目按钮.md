---
title: Hexo+yilia添加隐藏左边栏目按钮
tag:
  - hexo
categories:
  - [博客,hexo]
article_type: 0
no_word_count: false
no_toc: false
no_date: false
no_declare: false
no_reward: false
no_comments: false
no_share: false
no_footer: false
mathjax: false
typora-root-url: ./..
abbrlink: 2af8072d
date: 2024-04-18 18:16:26
top:
---

效果图：  
![file](/imgs/image-1573145229532.png)

点击按钮时，缩进左侧边栏，再次点击再弹出来。

## 添加隐藏左边栏目按钮

参考：[添加隐藏左边栏目按钮](https://cqh-i.github.io/2019/08/07/hexo-yilia%E4%B8%BB%E9%A2%98%E6%B7%BB%E5%8A%A0%E9%9A%90%E8%97%8F%E5%B7%A6%E8%BE%B9%E6%A0%8F%E7%9B%AE%E6%8C%89%E9%92%AE/)

折腾了一个下午,终于把隐藏左边侧边栏目的效果实现了. 实现了点击按钮隐藏侧边栏, 查找和修改源码实在是太麻烦了.

### 制作按钮样式

先找一款你喜欢的CSS菜单按钮切换,或者自己实现一个,我在网上找到一款比较[简单的样式](https://c.runoob.com/codedemo/3156),稍微做了下修改.

<!--more-->

```
.mymenucontainer {
	display:block;
	cursor:pointer;
	left:0;
	top:0;
	width:35px;
	height:35px;
	z-index:9999;
	position:fixed;
}
.bar1 {
	width:35px;
	height:3px;
	background-color:#333;
	margin:6px 0;
	transition:0.4s;
	-webkit-transform:rotate(-45deg) translate(-8px,8px);
	transform:rotate(-45deg) translate(-8px,8px);
}
.bar2 {
	width:35px;
	height:3px;
	background-color:#333;
	margin:6px 0;
	transition:0.4s;
	opacity:0;
}
.bar3 {
	width:35px;
	height:3px;
	background-color:#333;
	margin:6px 0;
	transition:0.4s;
	-webkit-transform:rotate(45deg) translate(-4px,-6px);
	transform:rotate(45deg) translate(-4px,-6px);
}
.change .bar1 {
	-webkit-transform:rotate(0deg) translate(0px,0px);
	transform:rotate(0deg) translate(0px,0px);
}
.change .bar2 {
	opacity:1;
}
.change .bar3 {
	-webkit-transform:rotate(0deg) translate(0px,0px);
	transform:rotate(0deg) translate(0px,0px);
}
```

样式制作完成后,压缩,然后添加进`themes\new-yilia\source\css\main.0cf68a.css`文件中,添加在最上面即可（否则下面兼容移动端会取不到mymenucontainer）

### 添加按钮到相应的位置

打开`themes\new-yilia\layout\layout.ejs`文件, 找到`<div class="left-col"`,在其上面添加如下代码:

```
<div class="mymenucontainer" onclick="myFunction(this)">
  <div class="bar1"></div>
  <div class="bar2"></div>
  <div class="bar3"></div>
</div>
```

在`</body>`之后, `</html>`前添加如下Js代码:

```
<script>
    var hide = false;
    function myFunction(x) {
        x.classList.toggle("change");
        if(hide == false){
            $(".left-col").css('display', 'none');
            $(".mid-col").css("left", 6);
            $(".tools-col").css('display', 'none');
            $(".tools-col.hide").css('display', 'none');
            hide = true;
        }else{
            $(".left-col").css('display', '');
            $(".mid-col").css("left", 300);
            $(".tools-col").css('display', '');
            $(".tools-col.hide").css('display', '');
            hide = false;
        }
    }
</script>
```

重新生成文件,部署即可看到效果, 可以看看[我的博客](https://cqh-i.github.io/)效果

效果图：  
![file](/imgs/image-1573143726040.png)

> 引用结束

### 响应式：手机端隐藏按钮

手机端(当页面变小时)隐藏按钮：修改文件：`themes\new-yilia\source\css\main.0cf68a.css`，找到`@media screen and (max-width:800px)`下面的内容：

```
@media screen and (max-width:800px) {
    #container, body, html {
        height:auto;
        overflow-x:hidden;
        overflow-y:auto
    }
    #mobile-nav {
        display:block
    }
    .body-wrap {
        margin-bottom:0
    }
    .left-col{
        display:none
    }
}
```

在`.left-col`中添加一个按钮的标签（需要确保上面pc端添加的mymenucontainer样式在本样式下面）：

```
.left-col,.mymenucontainer {
    display:none
}
```



## 🐛bug

有个小问题：在PC端进行测试时，如果先尝试缩放，然后返回再展开，直接测试手机端，就会出现问题：按钮仍然撑开界面；但是如果进到页面直接测试手机端就不会这种问题（或者是在缩放后进行测试也不会影响）。

因为这个问题好像影响不是很大，就不深入了。



**本文链接：** https://yansheng836.bitbucket.io/article/31bbdc67.html
**版权声明：** 本作品采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可协议进行许可。转载请注明出处！