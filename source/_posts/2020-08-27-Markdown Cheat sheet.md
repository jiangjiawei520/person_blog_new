---
layout: post
title: markdown备忘表
tags:
  - 技术分享
categories:
  - 技术分享
abbrlink: a904f437
date: 2020-08-27
---

## 总览

该Markdown备忘单提供了所有Markdown语法元素的快速概述。它无法涵盖所有的极端情况，因此，如果您需要有关这些元素中任何一个的更多信息，请参阅我们的参考指南以获取[基本语法](http://markdown.p2hp.com/basic-syntax)和[扩展语法](http://markdown.p2hp.com/extended-syntax)。

<!--more-->

## 基本语法 

这些是John Gruber原始设计文档中概述的元素。所有Markdown应用程序都支持这些元素。 .

| 元素                                                         | Markdown 语法                              |
| ------------------------------------------------------------ | ------------------------------------------ |
| [标题](http://markdown.p2hp.com/basic-syntax/index.html#headings) | `# H1## H2### H3`                          |
| [粗体](http://markdown.p2hp.com/basic-syntax/index.html#bold) | `**bold text**`                            |
| [斜体](http://markdown.p2hp.com/basic-syntax/index.html#italic) | `*italicized text*`                        |
| [块引用](http://markdown.p2hp.com/basic-syntax/index.html#blockquotes-1) | `> blockquote`                             |
| [有序列表](http://markdown.p2hp.com/basic-syntax/index.html#ordered-lists) | `1. First item2. Second item3. Third item` |
| [无序列表](http://markdown.p2hp.com/basic-syntax/index.html#unordered-lists) | `- First item- Second item- Third item`    |
| [代码](http://markdown.p2hp.com/basic-syntax/index.html#code) | ``code``                                   |
| [水平线](http://markdown.p2hp.com/basic-syntax/index.html#horizontal-rules) | `---`                                      |
| [超链接](http://markdown.p2hp.com/basic-syntax/index.html#links) | `[title](https://www.example.com)`         |
| [图片](http://markdown.p2hp.com/basic-syntax/index.html#images-1) | `![alt text](image.jpg)`                   |

## 扩展语法 

这些元素通过添加其他功能来扩展基本语法。并非所有Markdown应用程序都支持这些元素。 .

| 元素                                                         | Markdown 语法                                                |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [表格](http://markdown.p2hp.com/extended-syntax/index.html#tables) | `| Syntax | Description || ----------- | ----------- || Header | Title || Paragraph | Text |` |
| [围栏代码块](http://markdown.p2hp.com/extended-syntax/index.html#fenced-code-blocks) | ````{  "firstName": "John",  "lastName": "Smith",  "age": 25}```` |
| [脚注](http://markdown.p2hp.com/extended-syntax/index.html#footnotes) | `Here's a sentence with a footnote. [^1][^1]: This is the footnote.` |
| [标题ID](http://markdown.p2hp.com/extended-syntax/index.html#heading-ids) | `### My Great Heading {#custom-id}`                          |
| [自定义列表](http://markdown.p2hp.com/extended-syntax/index.html#definition-lists) | `term: definition`                                           |
| [删除线](http://markdown.p2hp.com/extended-syntax/index.html#strikethrough) | `~~The world is flat.~~`                                     |
| [任务列表](http://markdown.p2hp.com/extended-syntax/index.html#task-lists) | `- [x] Write the press release- [ ] Update the website- [ ] Contact the media` |