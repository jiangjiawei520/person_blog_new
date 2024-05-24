---
layout: post
title: MySQL将主键默认值设为UUID()
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "bk@2024"
typora-root-url: ./..
date: 2024-05-24 10:50:14
---

```shell
DELIMITER $$
CREATE
    /*[DEFINER = { user | CURRENT_USER }]*/
    TRIGGER `tysb_gdbs`.`dcsj_tdjc_shxx` -- 触发器名称
    BEFORE INSERT             -- 触发器被触发的时机
<!--more-->
    ON `tysb_gdbs`.`dcsj_tdjc_shxx`       -- 触发器所作用的表名称
    FOR EACH ROW BEGIN
		SET new.GUID=REPLACE(UUID(),'-',''); -- 触发器执行的逻辑
    END$$

DELIMITER ;
```
