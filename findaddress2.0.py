from bs4 import BeautifulSoup
import requests, os

def check_file(FilePath):
    '''
    判断文件是否存在，不存在就新建文件
    '''
    if os.path.exists(FilePath) is not True:
        with open(FilePath, 'w') as resultFile:
            pass

def get_shop(url, FilePath):
    '''
    爬虫主体函数
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Cookie': '_lxsdk_cuid=161dfc585986-0405e88a4d9746-a35346f-13c680-161dfc58599c8; _lxsdk=161dfc585986-0405e88a4d9746-a35346f-13c680-161dfc58599c8; _hc.v=60892413-50ed-aad7-7299-341b87e905ff.1519877719; s_ViewType=10; cy=4; cye=guangzhou; _lxsdk_s=16339c40583-cad-2d7-8bd%7C%7C16'
    }
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # 检测文件是否存在
    check_file(FilePath)

    shop_name = soup.select('div.tit > a > h4')
    shop_area = soup.select('div.txt > div.tag-addr > a > span')
    shop_addr = soup.select('div.txt > div.tag-addr > span')
    review_num = soup.select('a.review-num > b')
    shop_area_text = shop_area[1::2]

    for name, area, addr, number in zip(shop_name, shop_area_text, shop_addr,review_num):
        data = {
            'ShopName': name.get_text(),
            'Area': area.get_text(),
            'ShopAddr': addr.get_text(),
            'Review': number.get_text()
        }
        result = data['ShopName'] + ',' + data['Area'] + ',' + data['ShopAddr'] + ',' + data['Review'] + '\n'
        print(result)
        with open(FilePath, 'a') as resultFile:
            resultFile.write(result)

url = 'https://www.dianping.com/search/keyword/4/10_%E9%BA%A6%E5%BD%93%E5%8A%B3'
filepath = 'D:\\tmp\\information.txt'
get_shop(url, filepath)