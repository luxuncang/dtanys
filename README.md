# Dtanys

<b>dtanys是一个python字典解析器，让人专注于非数据处理的代码构造中，dtanys使用xpath式语法</b>


## 安装 `Dtanys`

### 使用 [PyPi](https://pypi.org/) 安装 `Dtanys`

* `pip` Find, install and publish Python packages with the Python Package Index 

* `pip install dtanys`

## 开始使用

1. 导入 `from dtanys import XDict`

### 使用场景

```python
test = {
  'a':"这是一个测试的字典！",
  'b':['python','java','C','C++','go'],
  'c':[{'normal':1},{'abnormal':0},{'normal':1}],
  'd':{'html':{'content'['css','js']}}
}
```

1. 使用路径方式快速定位字典值

* `/d/html/content[0]` 等价于 `test['d']['html']['content'][0]`

2. 使用 `,` 选择多个列表值

* `/b[0,3]` 等价于 `test['d']['b'][0]` 和 `test['d']['b'][3]`

3. 使用 `[start:end:step]` 选择多个列表值,完全支持切片操作

* `/b[0:2:1]` 等价于 `test['d'][0:2:1]`

4. 使用 `,` 选择多个键值

* `/['a','b']` 等价于 `test['a']` 和 `test['b']`
  
5. 使用 `//` 选择所有键值

* `/c//normal` 等价于 `test['c'][0]['normal']` 和 `test['c'][2]['normal']`

6. 使用 `*` 进行泛解析

* `/*normal` 等价于 `test['c'][0]['normal']` 和 `test['c'][2]['normal']`


#### example.py 模板

``` python
## 获取一个网易云歌单json数据
import json
import requests
from dtanys import XDict

url = "http://music.163.com/api/playlist/detail?id=475934383"

headers = {
    'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    }

res = requests.get(url=url,headers=headers).json()

## 打印 json
print(json.dumps(res, sort_keys=True, indent=4,ensure_ascii=False))

## 获取 歌单所有歌名
print(XDict(res,'/result/tracks//name').edict())

```


## 文档

#### XDict语法

| 表达式 | 描述 |
| :----: | :----- |
| / | 从根节点选取 |
| // | 从匹配选择的当前节点选择字典中的节点，而不考虑它们的位置 |
| [ any ] | 当any为带引号的键时，选取当前对象的键值；否则即为切片或索引 |
| [ ,... ] | 要选择多个无规律的索引时，即可使用此方法，可重复选择 |
| * | 匹配任何元素节点 |
| XX | 从当前节点的键值选取键值为"XX"的值 |
| *XX | 从当前节点的键值选取所有键值为"XX"的值 |

---

ps : 第一次写 github 项目，如有问题或建议请提Issues或Insight