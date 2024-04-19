# hexo-theme-new-yilia

此项目是根据[hexo-theme--yilia](https://github.com/litten/hexo-theme-yilia)主题做了扩展改造。

<div align="center"><img src="https://github.com/jackhanyuan/hexo-theme-new-yilia/blob/5c8b3f4708820a45898ca3deff26597d74fa3825/new-yilia-demo.png?raw=true)" alt="new yalia demo" width=100%></div>

## 开始使用

### 全新安装

在 B 电脑上同样先安装好 node、git、ssh、hexo，然后建好 hexo 文件夹，安装好插件，（然后选做：将备份到远程仓库的文件及文件夹删除），然后执行以下命令：

```sh
git init
git remote add github https://github.com/yourname/yourname.github.io.git 
git pull github backup:backup

npm install #第一次下拉需要安装一下依赖项，后面如果更改仍然需要刷新
```

### **发布博客后同步**

```
方式一（git默认方式）：
git add #可以用git master 查看更改内容  
git commit -m "更新信息"  
git push -u origin hexo:hexo #以后每次提交可以直接git push

方式二（hexo默认方式）：
hexo d

方式三（hexo-git-backup结合GitHub Actions方式）：
hexo b
自动触发GitHub Actions，部署到静态页面分支（正常是master）
```

### **平时同步管理**

每次想写博客时，先执行：

<div align="center"><img src="https://raw.githubusercontent.com/jiangjiawei520/person_blog_new/master/imgs/image-20240417093815731.png" alt="new yalia demo" width=100%></div>

```auto
git pull github backup:backup #github为远程主机名
#git pull gitee backup:backup  
```

进行同步更新。

## 目录结构梳理

```
person_blog_new                  #博客目录
|   |--.gitignore                #配置git应该忽略和不跟踪这些文件和文件夹
|   |--README.md                 #用于向项目的访问者提供项目的相关信息和说明。
|   |--_config.yml               #配置GitHub Pages 网站，配置网站的各种属性，包括主题、导航、元数据等。
|   |--_admin-config.yml         #hexo-admin 配置各种属性信息。
|   |--new-yilia-demo.png        #博客示例图片
|   |--package-lock.json         #确保在不同环境下安装相同的依赖版本，以及在执行 npm install 时保持依赖的版本一致性
|   |--package.json              #确保在不同环境下安装相同的依赖版本，以及在执行 npm install 时保持依赖的版本一致性
|   |--upload.conf               #七牛云上传配置，需求修改为自己的src_dir
|   |--upload_tsj.conf           #七牛云上传配置，需求修改为自己的src_dir(台式机)
|   |--.github                   #
|   |   |--workflows             #
|   |   |   |--autodeploy.yml    #github action配置，在 GitHub 仓库中设置和运行自定义的自动化任务，以响应各种事件，如提交代码、拉取请求、发布版本等
|   |--ImageProcess              #略缩图生成，辅助生产图片用于博客相册功能
|   |   |--ImageProcess.py       #
|   |   |--README.md             #
|   |   |--main.py               #略缩图生成主程序
|   |   |--qiniu_upload.py       #
|   |   |--requirments.txt       #
|   |   |--__pycache__           #
|   |   |--min_photos            #
|   |   |--photos                #
|   |--node_modules              #依赖
|   |--public                    #静态资源
|   |--scaffolds                 #hexo模版
|   |--scripts                   #脚本资源
|   |   |--auto_open.js          #hexo new自动打开typora脚本
|   |--tools					 #工具文件夹
|   |   |--backup.bat            #hexo b快捷脚本
|   |   |--clean.bat             #hexo clean快捷脚本
|   |   |--create_post_bjb.bat   #hexo new快捷脚本
|   |   |--dir_tree.py           #文件夹目录树生成脚本
|   |   |--dir_tree.txt          #文件夹目录树结构
|   |   |--generate_deploy.bat   #hexo g && hexo d快捷脚本
|   |   |--hexo-deploy.bat   	 #hexo-admin windows deploy脚本
|   |   |--hexo-deploy.sh   	 #hexo-admin linux deploy脚本
|   |   |--imageCleaning.py      #md使用图片去重功能，清除博客未使用的无用图片
|   |   |--open_page_bjb.bat     #hexo新建文件快速使用typor打开脚本
|   |--source                    #资源文件夹
|   |   |--404.html              #404页面
|   |   |--CNAME                 #域名填写文件
|   |   |--robots.txt            #
|   |   |--404                   #404资源目录
|   |   |--_drafts               #暂时md资源目录
|   |   |--_posts                #发布md资源目录
|   |   |--about                 #关于我资源目录
|   |   |--archives              #归档资源目录
|   |   |--categories            #分类资源目录
|   |   |--imgs                  #图片目录
|   |   |--music                 #音乐目录
|   |   |--photos                #略缩图目录
|   |--themes                    #主题
```



## Hexo常用命令

根据需求，修改hexo根目录下的 `_config.yml` 文件及`themes/new-yilia`目录下的`_config.yml`文件。

```sh
# Hexo常用命令
hexo -v # 查看hexo版本
hexo cl # 清理
hexo g # 构建
hexo s # 启动本地sever服务
hexo d # 部署
```

## git常用命令

```
//首次时
git config --global user.name "你的名字或昵称"
git config --global user.email "你的邮箱"
//当天第一次时（初始化）
git init
//每次更新代码时add 和commit
git status //查看仓库状态
git add . //用于更新所有代码
git commit -m "first commit"  （first commit 本次提交的内容）
git remote add origin https://github.com/852172891/test3.git //重新添加远程仓库地址，地址换成你建的项目的地址
git pull origin master --allow-unrelated-histories //正常需要把远程仓库和本地同步，消除差异
git push -u origin master  //将本地仓库的代码提交到github的仓库远程仓库的master主干，这一句执行的时候 可能需要输入你的 github 账号 和密码

其他
git clone https://github.com/852172891/test3.git //fork他人模板
git remote -v                                  //查看远程仓库详细信息，可以看到仓库名称
git remote remove orign                      //删除orign仓库（如果把origin拼写成orign，删除错误名称仓库）


git branch new_branch    //新建分支
git push -u origin new_branch       // 推送本地分支到远程仓库，并设置跟踪关系
git checkout 分支名 // 切换分支
git branch -a   //查询所有分支
git branch -d branch_name //删除本地分支
git push origin --delete branch_name  //删除远程分支
```

​	
