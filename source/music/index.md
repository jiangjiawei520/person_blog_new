---
title: 音乐
no_word_count: true
no_date: true
no_declare: true
no_toc: true
no_reward: true
no_comments: false
---


<center>
<img src="https://qiniu.findn.cn/blog/photos/article/music-2.jpg" />
</center>
<!-- 用meting-js 添加APlayer音乐播放器, 可以实现添加导入音乐列表, 详见: https://github.com/metowolf/MetingJS -->
<!-- 支持server：netease, tencent, kugou, xiami, baidu -->
<!-- 网易云音乐 “我喜欢的音乐”不支持 其它收藏歌单均支持 -->
<!-- require APlayer -->
<link rel="stylesheet" href="https://fastly.jsdelivr.net/npm/aplayer/dist/APlayer.min.css">

<script src="https://fastly.jsdelivr.net/npm/aplayer/dist/APlayer.min.js"></script>
<!-- require MetingJS -->

<script src="https://fastly.jsdelivr.net/npm/meting@2/dist/Meting.min.js"></script>

<!-- 歌单 替换id即可 -->
<meting-js style="margin-top: 1.5rem;width: auto;height: auto"
	server="netease"
	type="playlist"
	id="9698528188"
	fixed="false"
	mini="false"
	theme="#0088cc"
	autoplay="false"
	loop="all"
	preload="auto"
	volume="0.7"
	order="list"
	mutex="true"
	list-folded="false"
	list-max-height="700px"
	storage-name="metingjs">
</meting-js>







