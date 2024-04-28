---
title: python之__repr__
tag:
  - python
categories:
  - python
article_type: 0
no_word_count: false
no_toc: false
no_date: false
no_declare: false
no_reward: false
no_comments: false
no_share: false
no_footer: false
mathjax: false
typora-root-url: ./..
abbrlink: c113cf7f
date: 2024-04-28 15:19:01
top:
---

__repr__是Python中的一个特殊方法，用于返回对象的可打印字符串表示形式。它应该返回一个字符串，该字符串应该是一个有效的Python表达式，可以用来创建该对象的副本。通常情况下，__repr__方法的返回值应该是一个能够明确表示对象的字符串。

例如，假设我们有一个名为Person的类，它有两个属性：name和age。我们可以为Person类定义一个__repr__方法来返回该对象的字符串表示形式：

```
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"
```

当我们打印一个Person对象时，它将调用__repr__方法来获取其字符串表示形式： 

```cobol
person = Person("Alice", 25)
print(person)  # 输出: Person(name='Alice', age=25)
```