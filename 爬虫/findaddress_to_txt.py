from bs4 import BeautifulSoup
import requests
import os
import time
import random


def check_file(path):
    '''
    检查输入路径的文件夹和文件是否存在，不存在自动创建
    '''
    path = path.strip()
    path_dirname = os.path.dirname(path)
    isExists = os.path.exists(path_dirname)

    if not isExists:
        # 目录不存在时，创建目录和文件
        os.makedirs(path_dirname)
        if os.path.exists(path) is not True:
            with open(path, 'w') as resultFile:
                pass
    else:
        # 目录存在时，创建文件
        if os.path.exists(path) is not True:
            with open(path, 'w') as resultFile:
                pass


def get_shop(url, FilePath):
    '''
    爬虫主体函数
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Cookie': '_lxsdk_cuid=161dfc585986-0405e88a4d9746-a35346f-13c680-161dfc58599c8; _lxsdk=161dfc585986-0405e88a4d9746-a35346f-13c680-161dfc58599c8; _hc.v=60892413-50ed-aad7-7299-341b87e905ff.1519877719; s_ViewType=10; cy=4; cye=guangzhou; _lxsdk_s=16339c40583-cad-2d7-8bd%7C%7C16'}

    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    # 随机停止时间
    sleepTime = random.randint(2, 4)
    time.sleep(sleepTime)

    # 检测文件是否存在
    check_file(FilePath)

    # 找需要的内容
    shop_name = soup.select('div.tit > a > h4')
    shop_area = soup.select('div.txt > div.tag-addr > a > span')
    shop_addr = soup.select('div.txt > div.tag-addr > span')
    review_num = soup.select('a.review-num > b')
    shop_area_text = shop_area[1::2]

    # 将结果保存在字典，在逐行写入文件
    for name, area, addr, number in zip(
            shop_name, shop_area_text, shop_addr, review_num):
        data = {
            'ShopName': name.get_text(),
            'Area': area.get_text(),
            'ShopAddr': addr.get_text(),
            'Review': number.get_text()
        }
        result = data['ShopName'] + ',' + data['Area'] + ',' + \
            data['ShopAddr'] + ',' + data['Review'] + '\n'
        print(result)
        with open(FilePath, 'a') as resultFile:
            resultFile.write(result)

    # 找出下一页Url，返回给get_shop函数
    try:
        while True:
            findNextPage = str(soup.select('div.page > a.next'))
            changeToList = findNextPage.split('"')
            newUrl = str(changeToList[5])
            print(newUrl)
            return get_shop(newUrl, FilePath)
    except BaseException:
        IndexError

    print('\n\n处理完毕，请到' + FilePath + '中找到结果\n\n')


print('使用说明：')
print('输入网址（例如这类网址：https://www.dianping.com/search/keyword/4/10_%E9%BA%A6%E5%BD%93%E5%8A%B3）')
print('输入路径和文件（例如：D:\\tmp\info.txt）')

url = input('请输入网址：\n')
filepath = input('请输入路径：\n')

get_shop(url, filepath)
