
    layout: post
    title: 日期类型存储范围错误Incorrect datetime value
    tags:
    - 语雀
    categories:
    - [语雀,我的知识库]
    abbrlink: 
    date: 2024-05-22 17:28:47
    
**问题原因：不同的数据库日期类型存储范围不同导致的错误。**
> mysql中对日期类型的存储范围是不同的。
> DATE 范围从'1000-01-01' to '9999-12-31'.
> DATETIME 范围从'1000-01-01 00:00:00' to '9999-12-31 23:59:59'.
> TIMESTAMP 范围从'1970-01-01 00:00:01' UTC to '2038-01-19 03:14:07' UTC.

