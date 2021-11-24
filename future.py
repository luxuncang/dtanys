'''1.0.6解析器'''

from collections.abc import Iterable
import re
import functools
import operator

# 字典键值 泛解析 
def DictAnalysis(data, key):
    def RecursionAnalysis(data, key, area = {'value' : [],'area' : []}):
        if isinstance(data, Iterable):
            if isinstance(data, dict):
                if key in data:
                    area['value'].append(data[key])
                    area['area'].append(data)
                for j in data.values():
                    RecursionAnalysis(j, key, area)
            elif isinstance(data, str):
                pass
            else:
                for i in data:
                    RecursionAnalysis(i, key, area)
        return area
    res = RecursionAnalysis(data, key)
    return res

# 列表降维
def functools_reduce_iconcat(a):
    return functools.reduce(operator.iconcat, a, [])

# 命令标识
class jsonpath():

    Identifier = ('/', '//', '*', '[', ']', ':', ',', '@', '=', '>', '<', '>=', '<=', '!=', 'or', 'and', '|', '&')

    @staticmethod
    def xpath(data, expr):
        xcode = jsonpath.exprparse(expr)
        step = 0
        steps = len(xcode)
        return jsonpath.node(data, step, steps, xcode)

    @staticmethod
    def node(data, step, steps, xcode):
        if step >= steps:
            if not isinstance(data, Iterable):
                data = [data]
            return data
        if xcode[step] == '/':
            return jsonpath.node(data, step + 1, steps, xcode)
        elif xcode[step] == '//':
            if isinstance(data, list):
                data = [list(i) for i in zip(*[jsonpath.node(i, 0, 1, [xcode[step + 1]]) for i in data])]
                if len(data)==1:
                    data = functools_reduce_iconcat(data)
                # data = functools_reduce_iconcat([jsonpath.node(i, 0, 1, [xcode[step + 1]]) for i in data])
                step += 1
            return jsonpath.node(data, step + 1, steps, xcode)
        elif xcode[step][0] == '*':
            if xcode[step][0] == '*' and (step + 1)<len(xcode) and '@' in xcode[step + 1]:
                zcode = jsonpath.ifparse(xcode[step + 1])
                zdata = []
                ifdata = []
                for i,j in enumerate(zcode):
                    if (i + 1)%2:
                        zdata.append(jsonpath.nodeput(DictAnalysis(data, j[0])['area'], 0, 1, [f"[@{''.join(j)}]"]))
                    else:
                        ifdata.append(j)
                data = jsonpath.ifsetput(zdata , zdata, ifdata)
                return jsonpath.node(data, step + 2, steps, xcode)
            elif xcode[step] == "*":
                zcode = jsonpath.manypares(xcode[step + 1])
                data = [DictAnalysis(data, i)['value'] for i in zcode]
                return jsonpath.node(data, step + 2, steps, xcode)
            else:
                data = DictAnalysis(data, xcode[step][1:])['value']
                return jsonpath.node(data, step + 1, steps, xcode)
        elif xcode[step][0] == '[':
            if xcode[step][0:2] == '[@':
                zcode = jsonpath.ifparse(xcode[step])
                zdata = []                   # 条件data容器
                ifdata = []                  # and or
                for i,j in enumerate(zcode):
                    if isinstance(j, list):
                        zdata.append([])
                        for z,k in enumerate(data):
                            if jsonpath.boolput(k, j):
                                zdata[-1].append(z)
                    else:
                        ifdata.append(j)
                data = jsonpath.setput(data , zdata, ifdata)
                return jsonpath.node(data, step + 1, steps, xcode)
            elif ',' in xcode[step]:
                zcode = jsonpath.manypares(xcode[step])
                data = [jsonpath.node(data, 0, 1, [str([i])]) for i in zcode]
                # data = functools_reduce_iconcat([jsonpath.node(data, 0, 1, [str([i])]) for i in zcode])
                return jsonpath.node(data, step + 1, steps, xcode)
            else:
                return jsonpath.node(eval(f"data{xcode[step]}"), step + 1, steps, xcode)
        else:
            if xcode[step] in data:
                return jsonpath.node(data[xcode[step]], step + 1, steps, xcode)
            else:
                return jsonpath.node([], step + 1, steps, xcode)
        
    # 节点码解析
    @staticmethod
    def exprparse(expr):
        res = []
        xcode = re.split('(/{1,2})', expr)[1:]
        for i in xcode:
            iparse = jsonpath.indexparse(i)
            if isinstance(iparse, tuple):
                res += list(iparse)
            else:
                res.append(iparse)
        return res
    
    # *泛解析
    @staticmethod
    def panparse(expr):
        res = re.split('(\*{1})', expr)[1:]
        if res:
            return res
        return expr

    # ,解析
    @staticmethod
    def manypares(expr):
        pattern = re.compile('\[(.+)\]')
        try:
            res = eval(pattern.search(expr).group(0))
            return res
        except SyntaxError:
            raise SyntaxError("Can't use the sample with ','")

    # [] 解析
    @staticmethod
    def indexparse(expr):
        pattern = re.compile('(.+)(\[.+\])')
        res = pattern.search(expr)
        if res:
            return res.groups()
        return expr

    # @ 解析
    @staticmethod
    def ifparse(expr):
        expr = jsonpath.indexparse(expr)[1:-1]
        zexpr = re.split('( and | or | \| | & )', expr)
        res = []
        for i in zexpr:
            l = re.split('(<=|>=|=|>|<)(.+)', i)
            if len(l) != 1:
                res.append([l[0][1:].strip()] + [j.strip() for j in l[1:-1]])
            else:
                res += l[0].split()
        return res
    
    # 交并补处理
    @staticmethod
    def setput(datas ,zdata, ifdata):
        if ifdata:
            for i,j in enumerate(zdata):
                if i >= 1:
                    if ifdata[i-1] == 'and':
                        data = set(j) & data
                    elif ifdata[i-1] == '&':
                        data = set(j) & data
                    elif ifdata[i-1] == 'or':
                        data = set(j) | data
                    elif ifdata[i-1] == '|':
                        data = set(j) | data
                else:
                    data = set(j)
            return [datas[i] for i in data]
        else:
            return [datas[i] for i in zdata[0]]

    # *[@ ]
    @staticmethod
    def ifsetput(datas ,zdata, ifdata):
        if ifdata:
            for i,j in enumerate(zdata):
                if i >=1:
                    if ifdata[i-1] == 'and':
                        data = [k for k in j if k in data]
                    elif ifdata[i-1] == '&':
                        data = [k for k in j if k in data]
                    elif ifdata[i-1] == 'or':
                        data += [k for k in j if not k in data]
                    elif ifdata[i-1] == '|':
                        data += [k for k in j if not k in data]
                else:
                    data = j
            return data
        else:
            return functools_reduce_iconcat(datas)

    # 逻辑处理
    @staticmethod
    def boolput(k, j):
        if j[1] == '=':
            return eval(f"k['{j[0]}'] == {j[2]}")
        elif j[1] == '>':
            return eval(f"k['{j[0]}'] > {j[2]}")
        elif j[1] == '<':
            return eval(f"k['{j[0]}'] < {j[2]}")
        elif j[1] == '>=':
            return eval(f"k['{j[0]}'] >= {j[2]}")
        elif j[1] == '<=':
            return eval(f"k['{j[0]}'] <= {j[2]}")
        else:
            raise SyntaxError(f"{j[1]} not a legal operator!")

    # 容错
    @staticmethod
    def nodeput(data, step, steps, xcode):
        zcode = jsonpath.ifparse(xcode[step])
        zdata = []                   # 条件data容器
        ifdata = []                  # and or
        for i,j in enumerate(zcode):
            if isinstance(j, list):
                zdata.append([])
                for z,k in enumerate(data):
                    if jsonpath.boolput(k, j):
                        zdata[-1].append(z)
        else:
            ifdata.append(j)
        data = jsonpath.setput(data , zdata, ifdata)
        return data

