---
layout: post
title: oracle转mysql函数
tags:
- 语雀
categories:
- [语雀,我的知识库]
abbrlink: 
password: "bk@2024"
typora-root-url: ./..
date: 2024-05-24 10:50:14
---
```
create or replace procedure P_GET_TABLE_MYSQL_DDL(
    vTableName in varchar,
    vTableDdl out varchar
)
AS
begin
<!--more-->
with v_base as (
    select TABLE_NAME T_NAME, COMMENTS
    from USER_TAB_COMMENTS
    where TABLE_NAME = vTableName
),
     v_columns as (
         select chr(10) || chr(9) || LOWER(utc.COLUMN_NAME) || ' '
                    || CASE
                           WHEN DATA_TYPE = 'DATE' then LOWER(NVL(tm.NEW_TYPE, utc.DATA_TYPE))
                           WHEN DATA_TYPE = 'NUMBER' and DATA_PRECISION > 1
                               then LOWER(NVL(tm.NEW_TYPE, utc.DATA_TYPE))  ||
                                    '(' || DATA_PRECISION || decode(DATA_SCALE, 0, '', ',' || DATA_SCALE) || ')'
                           WHEN DATA_TYPE = 'NUMBER' and DATA_PRECISION = 1
                               then 'tinyint(1)'
                           else LOWER(NVL(tm.NEW_TYPE, utc.DATA_TYPE)) || '(' || DATA_LENGTH || ')' end
                    || DECODE(utc.COLUMN_NAME, 'ID', ' primary key', '')
                    || ' comment ''' || comm.COMMENTS || '''' as ddl_column
         from (
                  select *
                  from v_base
                           left join USER_TAB_COLS on TABLE_NAME = v_base.T_NAME
              ) utc
                  left join (
             select 'NUMBER' OLD_TYPE, 'numeric' NEW_TYPE
             from dual
             union all
             select 'VARCHAR2' OLD_TYPE, 'varchar'
             from dual
             union all
             select 'NVARCHAR2' OLD_TYPE, 'nvarchar'
             from dual
         ) tm on tm.OLD_TYPE = utc.DATA_TYPE
                  left join USER_COL_COMMENTS comm
                            on comm.TABLE_NAME = utc.TABLE_NAME and comm.COLUMN_NAME = utc.COLUMN_NAME
         order by COLUMN_ID
     ),
     b_columns as (
         select wm_concat(ddl_column) as ddl_columns
         from v_columns
     )
select '## 创建表' || LOWER(T_NAME) || chr(10) || 'create table ' || LOWER(T_NAME) || ' ('
           || ddl_columns || chr(10) || ') comment ''' || COMMENTS || '''' AS ddlSql into vTableDdl
from b_columns, v_base;
end;
```
