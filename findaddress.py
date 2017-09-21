# coding=utf-8
# python3!
# 抓取大众点评店铺名称、商圈和地址
import urllib.request
import re, os
import bs4

# 将该功能封装成类
class FindAddr:
    def __init__(self, url):
        self.url = url
        # 获取该网页的源代码并以UTF-8格式显示
        print('正在处理中……')
        webPage = urllib.request.urlopen(url)
        data = webPage.read()
        data = data.decode('UTF-8')
        # 将转换过格式的网页给BS4用
        soup = bs4.BeautifulSoup(data, "html.parser")
        # 结果保存文件路径
        fileDir = "D:\\tmp\\information.txt"

        # 判断文件是否存在，不存在就自动新建
        if os.path.exists(fileDir) is not True:
            with open(fileDir, 'w') as resultFile:
                pass

        # 查找这里面包含的信息
        findSomething = r'<h4>(.*?)</h4>|<span class="addr">(.*?)</span>|<span class="tag">(.*?)</span>'
        p = re.compile(findSomething)

        # 遍历源代码里面的所需信息，并用sub方法替换掉无用的信息，并写入TXT文本中
        # 遍历次数初始为0
        rollTime = 0
        try:
            for m in p.finditer(data):
                result = m.group()
                getit = re.sub(r'频道:|分类:|推荐:|地点:|商户没有被收录？|遇到什么问题？|<span class="addr">|</span>|<h4>|</h4>'
                               r'|<span class="tag">','',result)
                print(getit)
                with open(fileDir, 'a') as resultFile:
                    resultFile.write(getit + ',')
                rollTime = rollTime + 1
                if rollTime % 4 == 2:
                    with open(fileDir, 'a') as resultFile:
                        resultFile.write('\n')
            # 如果有多页，查找下一页
            # 正则匹配class="next"，如果有，就用BS得到下一页地址，返回给FindAddr类循环获得数据
            findNextPage = re.compile(r'class="next"')
            nP = findNextPage.findall(data)
            while nP == ['class="next"']:
                nextPage = soup.select('a[class="next"]')[0]
                newurl = 'http://www.dianping.com' + nextPage.get('href')
                return FindAddr(newurl)
        except: TypeError
        pass
        print('处理完毕，请到' + fileDir + '中找到结果')

print('请粘贴你要查找的大众点评网址：')
url = input()
FindAddr(url)