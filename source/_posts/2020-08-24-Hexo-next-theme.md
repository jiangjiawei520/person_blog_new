---
title: Hexo 的文档
tags:
  - 技术分享
categories:
  - 技术分享
  - [博客,hexo]
abbrlink: 398792d6
typora-root-url: ./..
date: 2020-08-24
---
​	[Hexo](https://hexo.io/zh-cn/) 是高效的静态站点生成框架，她基于 [Node.js](https://nodejs.org/)。 通过 Hexo 你可以轻松地使用 Markdown 编写文章，除了 Markdown 本身的语法之外，还可以使用 Hexo 提供的 [标签插件](https://hexo.io/zh-cn/docs/tag-plugins.html) 来快速的插入特定形式的内容。在这篇文章中，假定你已经成功安装了 Hexo，并使用 Hexo 提供的命令创建了一个站点。

你可以访问 [Hexo 的文档](https://hexo.io/zh-cn/docs/) 了解如何安装 Hexo

在 Hexo 中有两份主要的配置文件，其名称都是 `_config.yml`。 其中，一份位于站点根目录下，主要包含 Hexo 本身的配置；另一份位于主题目录下，这份配置由主题作者提供，主要用于配置主题相关的选项。

为了描述方便，在以下说明中，将前者称为 **站点配置文件**， 后者称为 **主题配置文件**。

<!--more-->

## 安装 NexT

Hexo 安装主题的方式非常简单，只需要将主题文件拷贝至站点目录的 `themes` 目录下， 然后修改下配置文件即可。具体到 NexT 来说，安装步骤如下。



### 下载主题

如果你熟悉 [Git](http://git-scm.com/)， 建议你使用 克隆最新版本 的方式，之后的更新可以通过 `git pull` 来快速更新， 而不用再次下载压缩包替换。

- [克隆最新版本](http://theme-next.iissnan.com/getting-started.html#clone)
- [下载稳定版本](http://theme-next.iissnan.com/getting-started.html#stable)

在终端窗口下，定位到 Hexo 站点目录下。使用 `Git` checkout 代码：

```
$ cd your-hexo-site
$ git clone https://github.com/iissnan/hexo-theme-next themes/next
```

如果你对 Git 感兴趣，可以通过《Pro Git》这本书来学习。你可以访问我制作的一个 [在线版本（第一版）](http://iissnan.com/progit)。

### 启用主题

与所有 Hexo 主题启用的模式一样。 当 克隆/下载 完成后，打开 **站点配置文件**， 找到 `theme` 字段，并将其值更改为 `next`。

启用 NexT 主题

```
theme: next
```

到此，NexT 主题安装完成。下一步我们将验证主题是否正确启用。在切换主题之后、验证之前， 我们最好使用 `hexo clean` 来清除 Hexo 的缓存。

### 验证主题

首先启动 Hexo 本地站点，并开启调试模式（即加上 `--debug`），整个命令是 `hexo s --debug`。 在服务启动的过程，注意观察命令行输出是否有任何异常信息，如果你碰到问题，这些信息将帮助他人更好的定位错误。 当命令行输出中提示出：

```
INFO  Hexo is running at http://0.0.0.0:4000/. Press Ctrl+C to stop.
```

此时即可使用浏览器访问 `http://localhost:4000`，检查站点是否正确运行。

当你看到站点的外观与下图所示类似时即说明你已成功安装 NexT 主题。这是 NexT 默认的 Scheme —— Muse

![img](/imgs/validation-default-scheme-mac.png)

现在，你已经成功安装并启用了 NexT 主题。下一步我们将要更改一些主题的设定，包括个性化以及集成第三方服务。

## 主题设定

### 选择 Scheme

Scheme 是 NexT 提供的一种特性，借助于 Scheme，NexT 为你提供多种不同的外观。同时，几乎所有的配置都可以 在 Scheme 之间共用。目前 NexT 支持三种 Scheme，他们是：

- Muse - 默认 Scheme，这是 NexT 最初的版本，黑白主调，大量留白
- Mist - Muse 的紧凑版本，整洁有序的单栏外观
- Pisces - 双栏 Scheme，小家碧玉似的清新

Scheme 的切换通过更改 **主题配置文件**，搜索 scheme 关键字。 你会看到有三行 scheme 的配置，将你需用启用的 scheme 前面注释 `#` 去除即可。

选择 Pisces Scheme

```
#scheme: Muse
#scheme: Mist
scheme: Pisces
```

### 设置 语言

编辑 **站点配置文件**， 将 `language` 设置成你所需要的语言。建议明确设置你所需要的语言，例如选用简体中文，配置如下：

```
language: zh-Hans
```

目前 NexT 支持的语言如以下表格所示：

| 语言         | 代码                 | 设定示例                            |
| :----------- | :------------------- | :---------------------------------- |
| English      | `en`                 | `language: en`                      |
| 简体中文     | `zh-Hans`            | `language: zh-Hans`                 |
| Français     | `fr-FR`              | `language: fr-FR`                   |
| Português    | `pt`                 | `language: pt` or `language: pt-BR` |
| 繁體中文     | `zh-hk` 或者 `zh-tw` | `language: zh-hk`                   |
| Русский язык | `ru`                 | `language: ru`                      |
| Deutsch      | `de`                 | `language: de`                      |
| 日本語       | `ja`                 | `language: ja`                      |
| Indonesian   | `id`                 | `language: id`                      |
| Korean       | `ko`                 | `language: ko`                      |

### 设置 菜单

菜单配置包括三个部分，第一是菜单项（名称和链接），第二是菜单项的显示文本，第三是菜单项对应的图标。 NexT 使用的是 [Font Awesome](http://fontawesome.io/) 提供的图标， Font Awesome 提供了 600+ 的图标，可以满足绝大的多数的场景，同时无须担心在 Retina 屏幕下 图标模糊的问题。

编辑 **主题配置文件**，修改以下内容：

1. 设定菜单内容，对应的字段是 `menu`。 菜单内容的设置格式是：`item name: link`。其中 `item name `是一个名称，这个名称并不直接显示在页面上，她将用于匹配图标以及翻译。

   菜单示例配置

   ```
   menu:
     home: /
     archives: /archives
     #about: /about
     #categories: /categories
     tags: /tags
     #commonweal: /404.html
   ```

   若你的站点运行在子目录中，请将链接前缀的 `/` 去掉

   NexT 默认的菜单项有（标注  的项表示需要手动创建这个页面）：

   | 键值       | 设定值                    | 显示文本（简体中文） |
   | :--------- | :------------------------ | :------------------- |
   | home       | `home: /`                 | 主页                 |
   | archives   | `archives: /archives`     | 归档页               |
   | categories | `categories: /categories` | 分类页               |
   | tags       | `tags: /tags`             | 标签页               |
   | about      | `about: /about`           | 关于页面             |
   | commonweal | `commonweal: /404.html`   | 公益 404             |

2. 设置菜单项的显示文本。在第一步中设置的菜单的名称并不直接用于界面上的展示。Hexo 在生成的时候将使用 这个名称查找对应的语言翻译，并提取显示文本。这些翻译文本放置在 NexT 主题目录下的 `languages/{language}.yml` （`{language}` 为你所使用的语言）。

   以简体中文为例，若你需要添加一个菜单项，比如 `something`。那么就需要修改简体中文对应的翻译文件 `languages/zh-Hans.yml`，在 `menu` 字段下添加一项：

   ```
   menu:
     home: 首页
     archives: 归档
     categories: 分类
     tags: 标签
     about: 关于
     search: 搜索
     commonweal: 公益404
     something: 有料
   ```

3. 设定菜单项的图标，对应的字段是 `menu_icons`。 此设定格式是 `item name: icon name`，其中 `item name` 与上一步所配置的菜单名字对应，`icon name` 是 Font Awesome 图标的 名字。而 `enable` 可用于控制是否显示图标，你可以设置成 `false` 来去掉图标。

   菜单图标配置示例

   ```
   menu_icons:
     enable: true
     # Icon Mapping.
     home: home
     about: user
     categories: th
     tags: tags
     archives: archive
     commonweal: heartbeat
   ```

   在菜单图标开启的情况下，如果菜单项与菜单未匹配（没有设置或者无效的 Font Awesome 图标名字） 的情况下，NexT 将会使用  作为图标。

   请注意键值（如 `home`）的大小写要严格匹配

### 设置 侧栏

默认情况下，侧栏仅在文章页面（拥有目录列表）时才显示，并放置于右侧位置。 可以通过修改 **主题配置文件** 中的 `sidebar` 字段来控制侧栏的行为。侧栏的设置包括两个部分，其一是侧栏的位置， 其二是侧栏显示的时机。

1. 设置侧栏的位置，修改 `sidebar.position` 的值，支持的选项有：

   - left - 靠左放置
   - right - 靠右放置

   目前仅 Pisces Scheme 支持 `position` 配置。影响版本**5.0.0**及更低版本。

   ```
   sidebar:
     position: left
   ```

2. 设置侧栏显示的时机，修改 `sidebar.display` 的值，支持的选项有：

   - `post` - 默认行为，在文章页面（拥有目录列表）时显示
   - `always` - 在所有页面中都显示
   - `hide` - 在所有页面中都隐藏（可以手动展开）
   - `remove` - 完全移除

   ```
   sidebar:
     display: post
   ```

   已知侧栏在 `use motion: false` 的情况下不会展示。 影响版本**5.0.0**及更低版本。

### 设置 头像

编辑 **主题配置文件**， 修改字段 `avatar`， 值设置成头像的链接地址。其中，头像的链接地址可以是：

| 地址             | 值                                                           |
| :--------------- | :----------------------------------------------------------- |
| 完整的互联网 URI | `http://example.com/avatar.png`                              |
| 站点内的地址     | 将头像放置主题目录下的 `source/uploads/` （新建 uploads 目录若不存在） 配置为：`avatar: /uploads/avatar.png`或者 放置在 `source/images/` 目录下 配置为：`avatar: /images/avatar.png` |

头像设置示例

```
avatar: http://example.com/avatar.png
```

### 设置 作者昵称

编辑 **站点配置文件**， 设置 `author` 为你的昵称。

### 站点描述

编辑 **站点配置文件**， 设置 `description` 字段为你的站点描述。站点描述可以是你喜欢的一句签名:)

## 集成常用的第三方服务

### 百度统计

注意： baidu_analytics 不是你的百度 id 或者 百度统计 id

1. 登录 [百度统计](http://tongji.baidu.com/)， 定位到站点的代码获取页面
2. 复制 `hm.js?` 后面那串统计脚本 id，如： ![img](/imgs/analytics-baidu-id.png)
3. 编辑 **主题配置文件**， 修改字段 `baidu_analytics` 字段，值设置成你的百度统计脚本 id。

### 阅读次数统计（LeanCloud） 由 [Doublemine](https://github.com/iissnan/hexo-theme-next/pull/439) 贡献

请查看 [为NexT主题添加文章阅读量统计功能](https://notes.wanghao.work/2015-10-21-为NexT主题添加文章阅读量统计功能.html#配置LeanCloud)

### Algolia 搜索

详细的配置请参考： [第三方服务 - Algolia](http://theme-next.iissnan.com/third-party-services.html#algolia-search)