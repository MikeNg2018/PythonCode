# code=utf-8
# python3
from bs4 import BeautifulSoup
import os, re, urllib

class GetSanti:
    def __init__(self, WebUrl):
        #print("输入网址：")
        #WebUrl = "http://www.luoxia.com/santi/26652.htm"
        self.WebUrl = WebUrl
        print('正在获取内容，请稍后')
        WebPage = urllib.request.urlopen(WebUrl)
        WebData = WebPage.read()
        WebData = WebData.decode("UTF-8")
        WebContent = BeautifulSoup(WebData, "html.parser")

        FileDir = "C:\\tmp\\Santi.txt"
        if os.path.exists(FileDir) is not True:
            with open(FileDir, "w", encoding='UTF-8') as File:
                pass

        os.chdir("C:\\tmp\\")
        try:
            # 找标题
            FindTitle = WebContent.title.text
            FinallTitle = re.sub('三体 | - 落霞小说网','',FindTitle)
            with open("Santi.txt", "a", encoding='UTF-8') as File:
                File.write(FinallTitle + '\n')

            # 找内容
            FindContents = WebContent.find('div', class_='ggad clearfix')
            for Parts in FindContents.next_siblings:
                if re.match(r'<div class="ggad clearfix">', str(Parts)):
                    break
                else:
                    GoodParts = re.sub(r'<p>|</p>', '', str(Parts))
                    with open("Santi.txt", "a", encoding='UTF-8') as File:
                        File.write(GoodParts.strip() + '\n')

            FindNextPage = WebContent.find('li', class_='next')
            NextPageUrl = FindNextPage.find('a').get('href')
            return GetSanti(NextPageUrl)
        except: TypeError
        pass
        print('获取完毕！')

print('请输入“落霞小说：三体”的地址：')
WebUrl = input()
GetSanti(WebUrl)