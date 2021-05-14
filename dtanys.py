# 字典键值 泛解析
def PanAnalysis(a,b,c=[]):
    if isinstance(a,dict):
        if b in a:
            c.append(a[b])
        for i,j in a.items():
            PanAnalysis(j,b,c)
    elif isinstance(a,list):
        for i in a:
           PanAnalysis(i,b,c)
    elif isinstance(a,tuple):
        for i in a:
           PanAnalysis(i,b,c)
    elif isinstance(a,set):
        for i in a:
           PanAnalysis(i,b,c)       
    elif isinstance(a, str):
        return 0
    elif isinstance(a, int):
        return 0
    else:
        return 0
    return a

# edict 命令解析
def XDictAnalysis(ps):
    arr = []
    ps = ps.split('/')[1:]
    for i,j in enumerate(ps):
        if j=='':
            ps[i+1] = '/' + ps[i+1]
        else:
            arr.append(j)
    ass = []
    for i in arr:
        lines = i.replace(']','').split('[')
        for z,j in enumerate(lines):
            if len(lines)>=2 and z>0:
                ass.append('[' + j + ']')
            else:
                ass.append(j)

    return [i for i in ass if i]

# edict
class XDict():
    '''
    "/xx" 即为选择对象键值['xx'];\n
    "/[any]" 前提为对象是iterable,any可以使用int与带引号的键值;\n
    "/xx['key1','key2]" 前提为对象是iterable[dict],即为选择iterable对象中所有键['key1','key2]的值;\n
    "/xx[int]" 前提为"/xx"是iterable,即为对象['xx']键值的第 int 个值;\n
    "/xx[int1,int2]" 前提为"/xx"是iterable,即为对象['xx']键值的 第int1和第int2 的值;\n
    "/xx[start:end:step]" 前提为"/xx"是iterable,即为切片操作;\n
    "//xx" 前提为对象是iterable[dict],即为选择iterable对象中所有键['xx']的值;\n
    "/*xx" 即为对象中所有键值为['xx']的值;\n
    PS : 键名中不要使用 ("/","//","*","[","]",":",",") 且 只能进行一次泛解析
    '''

    # 命令标识
    Identifier = ('/','//','*','[',']',':',',')

    # edict 命令解析
    def XDictAnalysis(ps):
        arr = []
        ps = ps.split('/')[1:]
        for i,j in enumerate(ps):
            if j=='':
                ps[i+1] = '/' + ps[i+1]
            else:
                arr.append(j)
        ass = []
        for i in arr:
            lines = i.replace(']','').split('[')
            for z,j in enumerate(lines):
                if len(lines)>=2 and z>0:
                    ass.append('[' + j + ']')
                else:
                    ass.append(j)
        return [i for i in ass if i]
            
    def __init__(self,dicts:dict,anys:str):
        self.dicts = dicts                      # 解析字典 
        self.anys = anys                        # 解析命令
        self.xcode = XDictAnalysis(self.anys)   # 解析码
        self.step = 0                           # 解析度
        self.steps = len(self.xcode)            # 解析位
    
    def edict(self)->list:
        if self.step>=self.steps:
            if not isinstance(self.dicts,list):
                self.dicts = [self.dicts]
            return self.dicts
        if self.xcode[self.step][0]=='/':
            if isinstance(self.dicts,list):
                self.dicts = [i[self.xcode[self.step][1:]] for i in self.dicts if self.xcode[self.step][1:] in i]
            else:
                self.xcode[self.step] = self.xcode[self.step][1:]
                return self.edict()
        elif self.xcode[self.step][0]=='*':
            self.dicts = PanAnalysis(self.dicts,self.xcode[self.step][1:])
        elif self.xcode[self.step][0]=='[':
            if ',' in self.xcode[self.step]:
                e = self.xcode[self.step].replace('[', '').replace(']', '').split(',')
                self.dicts = [eval(f"{self.dicts}[{z}]") for z in e if not ':' in z]
                for i in e:
                    if ':' in i:
                        for j in eval(f"{self.dicts}[{i}]"):
                            self.dicts.append(j)
            else:
                self.dicts = eval(f"{self.dicts}{self.xcode[self.step]}")
        else:
            if isinstance(self.dicts,list):
                self.xcode[self.step] = '/' + self.xcode[self.step]
                return self.edict()
            self.dicts = self.dicts[self.xcode[self.step]]
        self.step+=1
        return self.edict()
