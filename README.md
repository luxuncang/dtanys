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
  'd':{'html':{'content':['css','js']}}
}
```

1. 使用路径方式快速定位字典值

* `/d/html/content[0]` 等价于 `test['d']['html']['content'][0]`

2. 使用 `,` 选择多个列表值

* `/b[0,3]` 等价于 `test['b'][0]` 和 `test['b'][3]`

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
from pprint import pprint
from dtanys import jsonpath
data = { 
    "store": {
    "book": [
      { "category": "reference",
        "author": "Nigel Rees",
        "title": "Sayings of the Century",
        "price": 8.95
      },
      { "category": "fiction",
        "author": "Evelyn Waugh",
        "title": "Sword of Honour",
        "price": 2.99
      },
      { "category": "reference",
        "author": "Herman Melville",
        "title": "Moby Dick",
        "isbn": "0-553-21311-3",
        "price": 18.99
      },
      { "category": "fiction",
        "author": "J. R. R. Tolkien",
        "title": "The Lord of the Rings",
        "isbn": "0-395-19395-8",
        "price": 22.99
      }
    ],
    "bicycle": {
      "color": "red",
      "price": 19.95
    },
    "test" : {
        'dir': dir
    }
    },
    "test" : 'dsajk'
}

# /a /*a //*a /*['a', 'b'] //*['a', 'b'] /a[1] /a[1:5:2] /a[1,2,3] //a[@b="s"] //[1] //['a', 'b']

# pprint(jsonpath.xpath(data, '/test'))
# pprint(jsonpath.xpath(data, '/store/book[@price>10 | @category="fiction"]'))
# pprint(jsonpath.xpath(data, '/store["test", "bicycle",]/*color'))
# pprint(jsonpath.xpath(data, '/*[@price>10 and @category="fiction"]//price'))
# pprint(jsonpath.xpath(data, '/store/book[@price>10 | @category="fiction"]//price'))
# pprint(jsonpath.xpath(data, '//*["price","title"]'))
# pprint(jsonpath.xpath(data, '/store/book[1,2]/*price'))


```
更多案例请参考[example](https://github.com/luxuncang/dtanys/tree/dtanys-1.0.5/example)文件

## 文档


#### dtanys语法

| 表达式 | 描述 |
| :----: | :----- |
| / | 从根节点选取 |
| // | 从匹配选择的当前节点选择字典中的节点，而不考虑它们的位置 |
| [ any ] | 当any为带引号的键时，选取当前对象的键值；否则即为切片或索引 |
| [ ,... ] | 要选择多个无规律的索引时，即可使用此方法，可重复选择 |
| [@x=="Y" and @Z>=10] | 当需要筛选时可调用@表达式，支持多级逻辑表达式 and or || && |
| * | 匹配任何元素节点 |
| XX | 从当前节点的键值选取键值为"XX"的值 |
| *XX | 从当前节点的键值选取所有键值为"XX"的值 |

---
