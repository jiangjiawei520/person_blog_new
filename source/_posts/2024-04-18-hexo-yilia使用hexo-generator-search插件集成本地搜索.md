---
title: hexo+yilia(new-yilia)使用hexo-generator-search插件集成本地搜索
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
abbrlink: 613d6936
date: 2024-04-18 17:43:32
top:
---

yilia主题也有集成搜索功能，不过它使用的搜索是基于标题和标签的，有一定的局限性，没有提供全文检索功能。这篇文章介绍的就是集成全文检索和今日诗词。

### 效果图

![](/imgs/20200411232312.png)

动图  
![](/imgs/hexo-yilia-local-search2.gif)

## 1.集成本地搜索

参考：为 Hexo 博客增加一个站内搜索：[https://www.barretlee.com/blog/2017/06/04/hexo-search-insite/](https://www.barretlee.com/blog/2017/06/04/hexo-search-insite/)

![](/imgs/20200411214252.png)

### 原理说明

使用`hexo-generator-search`插件为文章生成一个全局的`search.xml`，里面包含所有文章的内容（可配置）。然后再去这个文件中搜索关键字，以此来找到需要的文章。



<!--more-->

### 1.1安装插件

[https://github.com/wzpan/hexo-generator-search](https://github.com/wzpan/hexo-generator-search)

安装分为两步，首先通过 npm 将插件安装到本地：

```
npm install hexo-generator-search --save
```

然后在主题new-yilia的（`_config.yml`）配置：

```
search:
  path: search.xml
  field: all
```

+   `path`，生成的路径，上述配置后可以通过 `/search.xml` 访问到文。
+   `field`，用来配置全局检索的区间，可以是 `post/page/all`。

重新clean、测试，就可以访问：[http://localhost:4000/search.xml](http://localhost:4000/search.xml) 了。

### 1.2为网页添加搜索栏

参考了博主的代码：[https://github.com/barretlee/hexo-search-plugin-snippets](https://github.com/barretlee/hexo-search-plugin-snippets)

#### 1.2.1添加搜索框

在`E:\OneDrive - shjd\github\person_blog_new\themes\new-yilia\layout\layout.ejs`的`<div id="wrapper" class="body-wrap">`上面添加如下代码（同时添加了‘今日诗词’）

```
<% if(theme.search) { %>
<div class="page-header" style="">
    <%# 今日诗词网址： https://www.jinrishici.com/ %>
    <span>🍻  
        <span id="jinrishici-sentence" title="今日诗词">正在加载今日诗词....</span>
    </span>
    <script src="https://sdk.jinrishici.com/v2/browser/jinrishici.js" charset="utf-8"></script>

    <%# 《集成本地搜索 %>
    <script type="text/javascript" src="/js/search.js"></script>
    <span id="local-search" class="local-search local-search-plugin" style="">
      <input type="search" placeholder="站内搜索" id="local-search-input" class="local-search-input-cls" style="">
      <i id="local-search-icon-search" class="icon" aria-hidden="true" title="站内搜索">🔍</i>
      <div id="local-search-result" class="local-search-result-cls"></div>
    </span>

    <script type="text/javascript" src="https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
    <script>
        if ($('.local-search').size()) {
          $.getScript('/js/search.js', function() {
            searchFunc("/search.xml", 'local-search-input', 'local-search-result');
          });
        }
    </script>
    <%# 集成本地搜索》 %>
</div>
<% } %>

...上面添加，这段和注释去掉
  <div id="wrapper" class="body-wrap">
```



#### 1.2.2添加js脚本

新建文件：`E:\OneDrive - shjd\github\person_blog_new\themes\new-yilia\source\js\search.js`

```
// A local search script with the help of hexo-generator-search
// Copyright (C) 2015 
// Joseph Pan <http://github.com/wzpan>
// Shuhao Mao <http://github.com/maoshuhao>
// This library is free software; you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as
// published by the Free Software Foundation; either version 2.1 of the
// License, or (at your option) any later version.
// 
// This library is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, write to the Free Software
// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
// 02110-1301 USA
// 

var searchFunc = function (path, search_id, content_id) {
    'use strict';
    var BTN = "<i id='local-search-close'>x</i>";
    $.ajax({
        url: path,
        dataType: "xml",
        success: function (xmlResponse) {
            // get the contents from search data
            var datas = $("entry", xmlResponse).map(function () {
                return {
                    title: $("title", this).text(),
                    content: $("content", this).text(),
                    url: $("url", this).text()
                };
            }).get();

            var $input = document.getElementById(search_id);
            var $resultContent = document.getElementById(content_id);

            $input.addEventListener('input', function () {
                var str = '<ul class=\"search-result-list\">';
                var keywords = this.value.trim().toLowerCase().split(/[\s\-]+/);
                $resultContent.innerHTML = "";
                if (this.value.trim().length <= 0) {
                    return;
                }
                // perform local searching
                datas.forEach(function (data) {
                    var isMatch = true;
                    var content_index = [];
                    if (!data.title || data.title.trim() === '') {
                        data.title = "Untitled";
                    }
                    var data_title = data.title.trim().toLowerCase();
                    var data_content = data.content.trim().replace(/<[^>]+>/g, "").toLowerCase();
                    var data_url = data.url;
                    var index_title = -1;
                    var index_content = -1;
                    var first_occur = -1;
                    // only match artiles with not empty contents
                    if (data_content !== '') {
                        keywords.forEach(function (keyword, i) {
                            index_title = data_title.indexOf(keyword);
                            index_content = data_content.indexOf(keyword);

                            if (index_title < 0 && index_content < 0) {
                                isMatch = false;
                            } else {
                                if (index_content < 0) {
                                    index_content = 0;
                                }
                                if (i == 0) {
                                    first_occur = index_content;
                                }
                                // content_index.push({index_content:index_content, keyword_len:keyword_len});
                            }
                        });
                    } else {
                        isMatch = false;
                    }
                    // show search results
                    if (isMatch) {
                        str += "<li><a href='" + data_url +
                            "' class='search-result-title'>" + data_title + "</a>";
                        var content = data.content.trim().replace(/<[^>]+>/g, "");
                        if (first_occur >= 0) {
                            // cut out 100 characters
                            var start = first_occur - 20;
                            var end = first_occur + 80;

                            if (start < 0) {
                                start = 0;
                            }

                            if (start == 0) {
                                end = 100;
                            }

                            if (end > content.length) {
                                end = content.length;
                            }

                            var match_content = content.substr(start, end);

                            // highlight all keywords
                            keywords.forEach(function (keyword) {
                                var regS = new RegExp(keyword, "gi");
                                match_content = match_content.replace(regS,
                                    "<em class=\"search-keyword\">" +
                                    keyword + "</em>");
                            });

                            str += "<p class=\"search-result\">" + match_content +
                                "...</p>"
                        }
                        str += "</li>";
                    }
                });
                str += "</ul>";
                if (str.indexOf('<li>') === -1) {
                    return $resultContent.innerHTML = BTN +
                        "<ul><span class='local-search-empty'>没有找到内容，更换下搜索词试试吧~<span></ul>";
                }
                $resultContent.innerHTML = BTN + str;
            });
        }
    });
    $(document).on('click', '#local-search-close', function () {
        $('#local-search-input').val('');
        $('#local-search-result').html('');
    });
    $(document).on('focus', '#local-search', function () {
        $('#local-search-icon-search').html('❌');
        $('#local-search-icon-search').attr('id', 'local-search-icon-close');
        //console.log("66666");
    });
    $(document).on('click', '#local-search-icon-close', function () {
        $('#local-search-input').val('');
        $('#local-search-result').html('');
        $('#local-search-icon-close').html('🔍');
        $('#local-search-icon-close').attr('id', 'local-search-icon-search');
        //console.log("1111");
    });
}
```



#### 1.2.3添加样式文件

1.新建：`E:\OneDrive - shjd\github\person_blog_new\themes\new-yilia\source\css\search.css`

```
.local-search {
    position: absolute;
    text-align: left;
    display:inline-block;
    margin-bottom: 0px;
    right:10%;
}
.local-search-input-cls {
    width: 200px;
    /* margin: 10px 0; */
    padding: 8px 12px;
    border-radius: 4px;
    border: 2px solid #5ad1ed;
    color: #666;
    font-size: 14px
}
.local-search-input-cls::-webkit-input-placeholder {
    color: #2d2626;
}
.local-search-input-cls::-moz-input-placeholder {
    color: #2d2626;
}
.local-search-input-cls::-ms-input-placeholder {
    color: #2d2626;
}
#local-search-close {
    content:'x';
    position: absolute;
    right: 10px;
    top: 10px;
    background: #fff;
    color: #888;
    border-radius: 100%;
    line-height: 16px;
    text-align: center;
    font-size: 16px;
    font-family: consolas;
    border: 1px solid #ccc;
    display: block;
    width: 20px;
    height: 20px;
    cursor: pointer;
    font-style: normal;
    font-weight: 400;
    transform: rotateZ(0);
    transition: all .3s
}
#local-search-close:hover {
    border-color: #666;
    color: #222;
    transform: rotateZ(180deg);
    transition: all .3s
}
.local-search-result-cls {
    position: absolute;
    z-index: 99;
    width: 400px;
    /* top: 50px; */
    right: -16px;
}
.local-search-result-cls .local-search-empty {
    color: #888;
    line-height: 44px;
    text-align: center;
    display: block;
    font-size: 16px;
    font-weight: 400
}
.local-search-result-cls ul {
    width: 360px;
    max-height: 450px;
    min-height: 0;
    height: auto;
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 10px 20px;
    background: rgba(255, 255, 255, 0.9);
    box-shadow: 3px 4px 10px #7dc3d8;
    margin-top: 20px;
}
.local-search-result-cls ul li {
    text-align: left;
    border-bottom: 1px solid #bdb7b7;
    padding-bottom: 20px;
    margin-bottom: 20px;
    line-height: 30px;
    font-weight: 400
}
.local-search-result-cls ul li:last-child {
    border-bottom: none;
    margin-bottom: 0
}
.local-search-result-cls ul li a {
    margin-top: 20px;
    font-size: 16px;
    text-decoration:none;
    transition: all .3s
}
.local-search-result-cls ul li a:hover {
    text-decoration:underline;
}
.local-search-result-cls ul li p {
    margin-top: 10px;
    font-size: 14px;
    max-height: 124px;
    overflow: hidden
}
.local-search-result-cls ul li em.search-keyword {
    color: #e58c7c;
    font-weight:bold;
}
.local-search-plugin .local-search-input-cls {
    opacity: .6;
    width: 160px;
    transition: all .3s
}
.local-search-plugin .local-search-input-cls:hover {
    opacity: 1;
    width: 200px;
    transition: all .3s
}
.local-search-plugin .icon {
    position: relative;
    left: -30px;
    color: #999;
    cursor: pointer
}
```

2.将上面的样式引入页面中，修改`E:\OneDrive - shjd\github\person_blog_new\themes\new-yilia\layout\_partial\css.ejs`，再后面添加：

```
<link rel="stylesheet" type="text/css" href="<%=config.root%>css/search.css">
```

3.修改`E:\OneDrive - shjd\github\person_blog_new\themes\new-yilia\source\css\main.0cf68a.css`最后面添加：

```
/* 页面头部：包含‘今日诗词’，站内搜索 */
.page-header {
    position: relative;
    border: 1px solid #fff;
    margin: 5px 30px 4px 30px;
    background: #fff;
    -webkit-transition: all 0.2s ease-in;
    height:45px;
    font-family: '微软雅黑';
    border-radius:5px;
    padding-left:10px;
}

/* 今日诗词 */
#jinrishici-sentence{
  color:#27d7a1;
  padding-left: 10px;
  line-height: 45px;
  font-size: 15px;
}
```



### 效果图2

详见文章[开头](#)

### 参考

+   hexo+yilia集成本地搜索：https://yansheng836.github.io/article/915f21c1.html
+   今日诗词安装：[https://www.jinrishici.com/doc/#json-fast-easy](https://www.jinrishici.com/doc/#json-fast-easy)
+   为 Hexo 博客增加一个站内搜索：[https://www.barretlee.com/blog/2017/06/04/hexo-search-insite/](https://www.barretlee.com/blog/2017/06/04/hexo-search-insite/)
+   搜索栏样式参考：[http://liangtao.site/](http://liangtao.site/)
+   search.js部分参考：[https://github.com/Kiritor/hexo-theme-yilia-l/blob/8f42e032e14a9746682dc91a0382a0576687a1f0/layout/\_partial/post/search.ejs](https://github.com/Kiritor/hexo-theme-yilia-l/blob/8f42e032e14a9746682dc91a0382a0576687a1f0/layout/_partial/post/search.ejs)
+   另一种配置方式：[https://github.com/Kiritor/hexo-theme-yilia-l/search?q=wrapStyle&unscoped\_q=wrapStyle](https://github.com/Kiritor/hexo-theme-yilia-l/search?q=wrapStyle&unscoped_q=wrapStyle)
+   可复制的表情包：[http://www.fhdq.net/emoji/emojifuhao.html](http://www.fhdq.net/emoji/emojifuhao.html)

## 2.更近一步

### 适配手机端

`E:\OneDrive - shjd\github\person_blog_new\themes\new-yilia\source\css\main.0cf68a.css`，新增下面内容

```
@media screen and (max-width:800px) {
.page-header {
    position: relative;
    border: 1px solid #fff;
    /* margin: 5px 30px 4px 30px; */
    background: #fff;
    -webkit-transition: all 0.2s ease-in;
    height: 45px;
    font-family: '微软雅黑';
    border-radius: 5px;
    padding-left: 2px;
}
}
```

`E:\OneDrive - shjd\github\person_blog_new\themes\new-yilia\source\css\search.css`，新增

```
/* 手机端 */
@media screen and (max-width:800px) {
.local-search {
    position: absolute;
    text-align: left;
    display:inline-block;
    margin-bottom: 0px;
    right: -5%;
}
.local-search-plugin .local-search-input-cls {
    opacity: .6;
    width: 100px;
    transition: all .3s;
}
.local-search-result-cls {
    right: 2px;
}
.local-search-result-cls ul {
    width: 360px;
    max-height: 400px;
    min-height: 0;
    height: auto;
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 10px 20px;
    background: rgba(255, 255, 255, 0.9);
    box-shadow: 3px 4px 10px #7dc3d8;
    margin-top: 20px;
}
}
```



### 手机端取消本地搜索功能

因为考虑到手机端界面比较小，这里取消搜索功能。

`E:\OneDrive - shjd\github\person_blog_new\themes\new-yilia\layout\layout.ejs`，在layout.ejs的最后的body前新增

```
<script>
    // 移动设备侦测
    var isMobile = {
      Android: function () {
        return navigator.userAgent.match(/Android/i);
      },
      BlackBerry: function () {
        return navigator.userAgent.match(/BlackBerry/i);
      },
      iOS: function () {
        return navigator.userAgent.match(/iPhone|iPad|iPod/i);
      },
      Opera: function () {
        return navigator.userAgent.match(/Opera Mini/i);
      },
      Windows: function () {
        return navigator.userAgent.match(/IEMobile/i);
      },
      any: function () {
        return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
      }
    };

    if(isMobile.any()){
        //手机端取消搜索功能
        $('.local-search').css("display","none");
    }

    if ($('.local-search').size() && !isMobile.any()) {
      $.getScript('/js/search.js', function() {
        searchFunc("/search.xml", 'local-search-input', 'local-search-result');
      });
    }
</script>
```

或者直接用css隐藏搜索框`E:\OneDrive - shjd\github\person_blog_new\themes\new-yilia\source\css\search.css`

```
/* 手机端 */
@media screen and (max-width:800px) {
    .local-search {
        display:none;
        /* right: -5%; */
    }
}
```



## bug

测试时，修改文件名后，可能不能立即将文章加入索引，即不能进行搜索。

停止测试，重新hexo s即可。