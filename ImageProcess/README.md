# ImageProcess for new-yilia theme

## 使用七牛云

1. 首先安装 python 环境和所需依赖

```sh
pip install -r requirments.txt
```

2. 运行主程序，生成的 `data.json` 会自动存入 `source/photos/` 目录。

```sh
python main.py 
```

3. 可以将图片上传至 github 或者七牛云

```
# 先打开qiniu_upload.py，配置access_key、secret_key、url、bucket_name、upload_dic_path。
# 上传
python qiniu_upload.py 
```

4. 修改 `source/photos/static/ins.js`

- 找到 119 和 120 两行

```js
var minSrc = 'yor_photos_url/photos/min_photos/' + data.link[i];
var src = 'your_photos_url/photos/photos/' + data.link[i];
```



## 不使用七牛云



1. 首先安装 python 环境和所需依赖

```sh
pip install -r requirments.txt
```

2. 注释 main.py 中的


```
#from qiniu_upload import qiniu_upload_directory
```

2. 运行主程序，生成的 `data.json` 会自动存入 `source/photos/` 目录。

```sh
python main.py 
```

3. 再博客source中新建存储图片的目录，用于直接访问，也可以单独新建一个项目存放（放在一块比较方便0.0）

```
1、修改main.py中的压缩后图片路径
photos_src, min_photos = "photos\\", "min_photos\\"
-->
photos_src, min_photos = "photos\\", "..\\source\\photos\\min_photos\\"
2、\source\photos 新建min_photos

注：python main.py 运行后就会存储到新的位置，将资源发布到博客中，通过data.json相关配置文件去访问
```

3. 修改 `source/photos/static/ins.js`

- 找到 119 和 120 两行

```js
var minSrc = 'yor_photos_url/photos/min_photos/' + data.link[i];
var src = 'your_photos_url/photos/min_photos/' + data.link[i];

your_photos_url/photos/photos/
-->https://raw.githubusercontent.com/jiangjiawei520/person_blog_new/master/photos/min_photos/
```



整理：

```
1、图片传到photos
2、运行python main.py 
3、hexo d
```

