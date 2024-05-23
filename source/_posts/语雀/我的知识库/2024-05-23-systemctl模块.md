---
ayout: post
title: systemctl模块
tags:
  - 语雀
categories:
  - - 语雀
    - 我的知识库
abbrlink: d0f15685
password: Grbk@2024
date: 2024-05-23 16:24:16
---
systemctl在enable、disable、mask子命令里面增加了--now选项，可以激活同时启动服务，激活同时停止服务等。
立刻启动单元： systemctl start
立刻停止单元： systemctl stop
重启单元：systemctl restart
重新加载配置：systemctl reload
输出单元运行的状态：systemctl status
检测单元是否为自动启动：systemctl is-enabled
设置为开机自动激活单元：systemctl enable
<!--more-->
设置为开机自动激活单元并现在立刻启动：systemctl enable --now
取消开机自动激活单元：systemctl disable
禁用一个单元：systemctl mask
取消禁用一个单元：systemctl unmask
显示单元的手册页（前提是由unit提供）：systemctl help
重新载入整个systemd的系统配置并扫描unit文件的变动：systemctl daemon-reload
