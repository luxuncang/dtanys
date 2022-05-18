"""
dtanys是一个python字典解析器
~~~~~~~~~~~~~~~~~~~~~

让人专注于非数据处理的代码构造中，dtanys使用xpath式语法
usage:

   >>> from dtanys import jsonpath
   >>> r = {} or json
   >>> jsonpath.xpath(r,'/result/tracks//["name","id"]')
   [[],...]

其他使用说明请前往https://github.com/luxuncang/dtanys

:copyright: (c) 2021 by ShengXin Lu.
"""

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__
from .dtanys import XDict
from .future import jsonpath


# 版本说明
# 1.0.3 开始正式发布
# 1.0.4 修复了"//xx"中xx只能是iterable[dict]的问题,并且添加了直接使用/[any]的功能

'''
v1.0.5
* 较大改动，继续兼容XDict 
* 新增[@x="x" and @y>10]条件筛选 (>,<,=,>=,<=) (and, or, |, &)
* 新增*[a,b] 多项泛解析解析，同时可使用@条件
* 删除原切片与索引同时使用的功能
'''
