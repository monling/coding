
# https://www.zhihu.com/question/58498720

# 找到之后，打开浏览器的 network 查看请求的链接。

# 经过一番筛选，找到了需要的请求链接，返回的是json格式数据。答主们的回答内容全在一个 'content'里面，
# 这里就需要将json字符串转换成python的字典，然后就能直接获取'content'里面的 'html' 内容啦。

# 获取到html后，稍微看下就能找到很多图片链接，但是有些是没用的。我经过仔细对比后，
# 发现有用的图片基本上都在 data-original 这个属性里面，好 那么就用正则提取出来
# （我正则只是入门阶段，根据网上的匹配规则，自己照葫芦画瓢写了一个 'data-original="(.+?)"'，使用 findall 匹配出来是一个列表）

# 再循环下载到本地即可。

# 不过，在这过程中还是遇到一些问题。通过python模拟浏览器请求链接，
# 通常要加 headers 才行，不过我只加了一个 user-agent ，当图片下载完成之后，
# 却发现好多图片根本没法打开，我就奇怪了。调试了一会儿，发现请求的某些图片，状态码返回 504 ，
# 也就是说请求失败咯。解决方法也简单，通过浏览器打开这张图片，查看发送的header头，将 python 中的 headers 照着浏览器补全即可。
# 然后删了所有图片，再次运行即可完美下载~
import re
import json
import requests
import os
import time

class Pics:
    def __init__(self):
        self.header = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3551.3 Safari/537.36',
            'Upgrade-Insecure-Requests':'1',
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }
        # 获取问题的json链接
        self.url = 'https://www.zhihu.com/api/v4/questions/58498720/answers?include=content&limit=20&offset=0&sort_by=default'
        # 存放根目录路径
        self.base_dir = 'D:/pics/'
        #问题链接
        self.index_url = 'https://www.zhihu.com/question/58498720'
        self.page = ''
        self.makeNewSession()

    def makeNewSession(self):
        requests.get(self.index_url, headers=self.header)
        self.session = requests.session()

    def getContent(self):
        print('正在扒%s'%self.url)
        json_str = self.session.get(self.url, headers=self.header)
        json_obj = json.loads(json_str.content.decode())

        data = json_obj.get('data')
        if data:
            self.url = json_obj.get('paging').get('next')
        else:
            self.url = ''

        for i in data:
            self.formatPic(i.get('content'))

    def formatPic(self,content):
        result = list(set(re.findall(r'data-original="(.+?)"', content))) #正则获取图片 然后去重
        for i in result:
            path,authority = self.makePicName(i)

            pic = self.session.get(i,headers=self.header)
            if pic.status_code != 200:
                print('图片：'+i+'获取失败')
                print('状态码：'+pic.status_code)
                time.sleep(3)
            self.savePic(pic,path)

    def savePic(self,pic,name):
        with open(self.page+name,'wb') as f:
            f.write(pic.content)
            print('保存图片'+self.page+name)

    def makePicName(self,link):
        rindex = link.rfind('/')
        index = link.find('pic')
        return link[rindex:],link[index:rindex]

    def mkdir(self,path):
        print('创建'+path)
        path = self.base_dir + path
        is_exists = os.path.exists(path)
        if not is_exists:
            os.mkdir(path)
        self.page = path

    def run(self):
        index = 1
        is_exists = os.path.exists(self.base_dir)
        if not is_exists:
            os.mkdir(self.base_dir)
        while True:
            if self.url == '':
                break

            page = '第{}页'.format(index)
            self.mkdir(page)
            self.getContent()
            index += 1

        print('图片扒取完毕')

if __name__ == '__main__':
    pic = Pics()
    pic.run()

#ll