
    layout: post
    title: SQL Select语句完整的执行顺序
    tags:
    - 语雀
    categories:
    - [语雀,我的知识库]
    abbrlink: 
    date: 2024-05-22 17:28:46
    
## 一、SQL Select语句完整的执行顺序
> SELECT语句的处理过程
> 1. FROM阶段

> 2. WHERE阶段

> 3. GROUP BY阶段

> 4. HAVING阶段
<!--more-->

> 5. SELECT阶段

> 6. ORDER BY阶段

> 1、from子句组装来自不同数据源的数据；  

> 2、where子句基于指定的条件对记录行进行筛选；  

> 3、group by子句将数据划分为多个分组；  

> 4、使用组函数进行计算；  

> 5、使用having子句筛选分组；  

> 6、计算所有的表达式；  

> 7、使用order by对结果集进行排序。


