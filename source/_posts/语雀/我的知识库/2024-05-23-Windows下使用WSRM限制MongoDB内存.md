---
ayout: post
title: Windows下使用WSRM限制MongoDB内存
tags:
  - 语雀
categories:
  - - 语雀
    - 我的知识库
abbrlink: e1e4f2ac
password: Grbk@2024
date: 2024-05-23 16:24:16
---
 MongoDB，在WINDOWS 2008 64位环境下部署的，Mongodb吃内存太厉害了，如果不重启服务，内存一直蹭蹭地往上涨，定时重启MongoDB服务是能暂时的收回内存，但这也不是长久之计。如果不去限制MongoDB的内存那么系统有多少内存都能被它消耗掉，我们的服务器上还有IIS, SQL SERVER, Redis等其他服务，不能将内存全部分配给Mongodb使用，怎样限制MongoDB的内存呢？
为了解决这个问题，Windows 2008自带的“Windows 系统资源管理器”，可以完美的解决这个问题。配置的方法如下：
## 1、安装 Windows 系统资源管理器
打开：开始  -- 管理工具  -- 服务器管理器
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845984501-de88d3a0-3b6d-48dd-ad11-88c56a0114aa.png#averageHue=%23a9b29c&clientId=u8c01eb78-6d75-4&from=paste&id=u1b8d4b9d&originHeight=317&originWidth=494&originalType=url&ratio=1&rotation=0&showTitle=false&size=18009&status=done&style=none&taskId=u8f39b7c2-249c-41d4-b136-b169f760298&title=)
选择“功能”  -- 添加功能  -- 勾选  Windows 系统资管理器
在弹出的窗口点击“添加必须的功能”
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845984591-eefe7264-0d70-4fb1-b5a6-535fbcf98189.png#averageHue=%23e9e8e7&clientId=u8c01eb78-6d75-4&from=paste&id=u15322a13&originHeight=532&originWidth=872&originalType=url&ratio=1&rotation=0&showTitle=false&size=36479&status=done&style=none&taskId=u2f7acb83-31e3-420a-ba1c-95a283968cf&title=)
<!--more-->
下一步   ---  安装
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845984605-0c649567-8570-4391-8d0f-464dc0b28b8b.png#averageHue=%23e8e6e4&clientId=u8c01eb78-6d75-4&from=paste&id=u67656a9d&originHeight=563&originWidth=765&originalType=url&ratio=1&rotation=0&showTitle=false&size=26498&status=done&style=none&taskId=ub63b1645-6a83-42bf-8004-44d08fa2754&title=)
稍微等待1分钟左右 Windows 系统资管理器就安装好了
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845984597-f1e23b92-d9eb-402d-a6f5-50c4c1bc64e2.png#averageHue=%23eae8e6&clientId=u8c01eb78-6d75-4&from=paste&id=ua2d1ed1c&originHeight=301&originWidth=612&originalType=url&ratio=1&rotation=0&showTitle=false&size=15820&status=done&style=none&taskId=u0fb5d2c4-659b-4e48-a1e3-0cd5ce58990&title=)
## 2、新建资源分配策略
打开  Windows 系统资管理器
选择 管理此计算机  --- 连接
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845984561-c8699518-2c17-4cb0-989d-51b4a831f6fb.png#averageHue=%23ecebe9&clientId=u8c01eb78-6d75-4&from=paste&id=uf9ceefc5&originHeight=411&originWidth=701&originalType=url&ratio=1&rotation=0&showTitle=false&size=26169&status=done&style=none&taskId=u062b5431-3e3a-4205-ae69-cf391ac67ba&title=)
在资源分配策略上右键  -- 新建资源分配策略
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845985485-474bad6a-ef53-497d-9aea-1f2728626d30.png#averageHue=%23e5e4e2&clientId=u8c01eb78-6d75-4&from=paste&id=u98c7c8b0&originHeight=283&originWidth=353&originalType=url&ratio=1&rotation=0&showTitle=false&size=17550&status=done&style=none&taskId=u2ff5bd57-dc7b-44db-8615-0aab153ac2e&title=)
随便填写个名字，例如 Mongodb Limit ,然后点击下面那个添加按钮
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845985556-407ba314-1a61-4a5c-99b8-1c2834e6dfb8.png#averageHue=%23e3e1de&clientId=u8c01eb78-6d75-4&from=paste&id=u17fe7cf0&originHeight=389&originWidth=448&originalType=url&ratio=1&rotation=0&showTitle=false&size=14796&status=done&style=none&taskId=ucd35893c-ab37-48ca-9160-95c513c25c1&title=)
在常规窗口下拉 进程匹配条件 --  新建
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845985656-137c6c9c-dd53-465a-b775-e512f7ea16c9.png#averageHue=%23d5d3cf&clientId=u8c01eb78-6d75-4&from=paste&id=u137ba759&originHeight=398&originWidth=495&originalType=url&ratio=1&rotation=0&showTitle=false&size=16026&status=done&style=none&taskId=ud3450798-ff63-4ccf-b075-f6ee2672a5b&title=)
在弹出的窗口中继续点击添加
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845985706-9998d1b0-6ad9-4246-a0bd-d4cb0c66b45a.png#averageHue=%23d6d3ce&clientId=u8c01eb78-6d75-4&from=paste&id=ucc6a5348&originHeight=327&originWidth=432&originalType=url&ratio=1&rotation=0&showTitle=false&size=10108&status=done&style=none&taskId=u6792c757-51eb-4386-bc70-8ec9b677379&title=)
## 3、Mongodb注册成服务
## 4、配置Mongodb分配策略
因为我服务器上的Mongodb注册成了服务，所以在这里选择： 已注册的服务 ，再点击右边的“选择“按钮
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845985817-45d3074f-5daa-4f26-b233-418b897b7baf.png#averageHue=%23d6d3ce&clientId=u8c01eb78-6d75-4&from=paste&id=u18592f1b&originHeight=472&originWidth=656&originalType=url&ratio=1&rotation=0&showTitle=false&size=25060&status=done&style=none&taskId=ufdc0ad01-d25e-4cb4-9bbb-e4e289165e7&title=)
在众多服务中找到mongodb服务
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845986664-498a0b78-98e5-4342-bb25-ef18739257a0.png#averageHue=%23d6d3cd&clientId=u8c01eb78-6d75-4&from=paste&id=ufd77a286&originHeight=326&originWidth=578&originalType=url&ratio=1&rotation=0&showTitle=false&size=19403&status=done&style=none&taskId=ud02b3de6-f277-43f8-8d27-7369be652db&title=)
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845986694-342c475b-e43e-460b-bfa8-9cb50aaeba71.png#averageHue=%23d6d3ce&clientId=u8c01eb78-6d75-4&from=paste&id=u800260e9&originHeight=427&originWidth=477&originalType=url&ratio=1&rotation=0&showTitle=false&size=14927&status=done&style=none&taskId=ufaf3edd8-6eeb-4beb-87a9-301926bf0b6&title=)
一路”确定“
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845986766-67f65955-8463-424f-a949-07f1a50bc443.png#averageHue=%23e1dfdc&clientId=u8c01eb78-6d75-4&from=paste&id=u55ff2cd2&originHeight=419&originWidth=491&originalType=url&ratio=1&rotation=0&showTitle=false&size=13786&status=done&style=none&taskId=u090d0338-5ead-4bb1-ad71-b5f9c47f202&title=)
回到资源分配的常规页面，这里我们将CPU限制为40%
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845986794-b7093b3f-a8af-44dc-a9ca-9b50b7dfa3c2.png#averageHue=%23d7d5d1&clientId=u8c01eb78-6d75-4&from=paste&id=u54e73e21&originHeight=419&originWidth=442&originalType=url&ratio=1&rotation=0&showTitle=false&size=14258&status=done&style=none&taskId=u1a2da85c-ab16-4923-8f28-e14daef3bb7&title=)
切换到”内存“ 页
为了测试，我们将内存限制为1000M
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845987090-dddc9a10-9d33-4d56-a446-2ff4979cdb46.png#averageHue=%23d7d5d1&clientId=u8c01eb78-6d75-4&from=paste&id=u65f444b6&originHeight=439&originWidth=459&originalType=url&ratio=1&rotation=0&showTitle=false&size=16456&status=done&style=none&taskId=u78eb9288-7028-498a-8b2d-6e9ff070d6c&title=)
设置好了就可以在这里看到我们的新策略
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845987670-33bed2e2-a079-4d5f-9824-04eb25dd5d83.png#averageHue=%23f3f3f3&clientId=u8c01eb78-6d75-4&from=paste&id=ua416ebd3&originHeight=315&originWidth=579&originalType=url&ratio=1&rotation=0&showTitle=false&size=20423&status=done&style=none&taskId=u76141072-2f47-4cbe-8e85-be18a009cea&title=)
## 5、让新策略起效
在 资源管理器上点击右键展开菜单，选择”属性“
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845987736-dbe17efc-e1a9-4869-86b2-93dbb61e8814.png#averageHue=%23e2e1df&clientId=u8c01eb78-6d75-4&from=paste&id=ua947f25a&originHeight=295&originWidth=408&originalType=url&ratio=1&rotation=0&showTitle=false&size=19692&status=done&style=none&taskId=u733b61c1-f64b-4573-b17b-812503a7778&title=)
将日历修改为禁用，然后选择当前资源分配策略为我们新建的 MongodbLimit
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845987844-594b846e-7f82-4b6a-af83-18eb913819c3.png#averageHue=%23dddbd8&clientId=u8c01eb78-6d75-4&from=paste&id=ufdd2d301&originHeight=418&originWidth=478&originalType=url&ratio=1&rotation=0&showTitle=false&size=17611&status=done&style=none&taskId=u4879bbbd-965f-4484-8f96-428811a733b&title=)
确定后发现在MongodbLimit 后面多了个 {管理} 字样，说明我们的设置其效果了。
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845988614-5e55ea98-aaae-423f-9ed6-de42405b9206.png#averageHue=%23ececeb&clientId=u8c01eb78-6d75-4&from=paste&id=ue7e010c0&originHeight=140&originWidth=262&originalType=url&ratio=1&rotation=0&showTitle=false&size=6380&status=done&style=none&taskId=ue5ab1907-faef-465d-8fa0-34bdede120d&title=)
我们重启mongodb服务，发现最大内存限制在了1000MB附近
![image.png](https://cdn.nlark.com/yuque/0/2023/png/12484160/1678845987976-f30b28eb-a9f1-475f-9cb9-5fe5fcae0827.png#averageHue=%23d6d3cd&clientId=u8c01eb78-6d75-4&from=paste&id=u79f56deb&originHeight=128&originWidth=533&originalType=url&ratio=1&rotation=0&showTitle=false&size=7204&status=done&style=none&taskId=uf6ef71a3-3ca6-48db-a9c6-8a8ea19b70a&title=)
