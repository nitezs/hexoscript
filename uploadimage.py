import os
import re
import time
import urllib.parse

import requests

posts = 'source\\_posts'
img = 'source\\img'
files = os.listdir(posts)
content = ''
filename = ''
for filename in files:
    file = open(posts + '\\' + filename, 'r+', encoding='utf8')
    content = file.read()
    file.close()
    r = re.compile('(/img/(.*?)/(.*?)\.(jpg|png|jpeg|gif))')
    l = r.findall(content)
    for i in l:
        s = [urllib.parse.unquote(i[0]), urllib.parse.unquote(i[1]), urllib.parse.unquote(i[2]),
             urllib.parse.unquote(i[3])]
        print('正在处理:' + s[0])
        ex = i[0].split('.')
        imgpath = img + '/' + s[1] + '/' + s[2] + '.' + s[3]
        header = {
            'Authorization': ''

        }
        file = {
            'smfile': open(imgpath, 'rb')
        }
        print('开始上传:' + s[0])
        data = object
        success = False
        url = ''
        while not success:
            try:
                res = requests.request('post', 'https://sm.ms/api/v2/upload', files=file, headers=header)
                data = res.json()
                res.close()
                code = data['code']
                if code == 'flood':
                    print('上传限制: ' + data['message'])
                    time.sleep(5)
                    file = {
                        'smfile': open(imgpath, 'rb')
                    }
                    continue
                if code == 'image_repeated':
                    url = data['images']
                else:
                    url = data['data']['url']
                if url == '':
                    print('url 获取失败')
                    success = False
                else:
                    success = True
            except:
                print('错误: 请求失败, 正在重试 ' + s[0])
                success = False

        print(s[0] + ':' + url)
        content = content.replace(i[0], url)
        file = open(posts + '\\' + filename, 'w', encoding='utf8')
        file.write(content)
        file.close()
        print(' ')
