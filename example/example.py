import json
import requests
from dtanys import XDict

url = "http://music.163.com/api/playlist/detail?id=475934383"

headers = {
    'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    }

res = requests.get(url=url,headers=headers).json()

## 打印 json
# print(json.dumps(res, sort_keys=True, indent=4,ensure_ascii=False))

## 获取 歌单所有歌名
print(XDict(res,'/result/tracks//name').edict())
