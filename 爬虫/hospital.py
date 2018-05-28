from bs4 import BeautifulSoup
import requests
from urllib.parse import quote
import re
import time


def find_total_pages(url):
    '''
    查总页数
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Cookie': "_webyyk_areaId=44; _webyyk_areaSpelling=guangdong; userLikesIdTemp=1527342610643; JSESSIONID=abcxEWkx755q2gzTFDFow; hisHos=24338"}

    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    try:
        total_pages = soup.select(
            'body > div.serach-wrap > div > div.serach-left > div.serach-left-list > div > div.pages > cite')[0]
    except IndexError:
        total_pages_number = 0
        return total_pages_number
    else:
        total_pages_number = int(re.compile(
            r'\d+').findall(str(total_pages))[0])
    # print(total_pages_number)
        return total_pages_number


def get_link(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Cookie': "_webyyk_areaId=44; _webyyk_areaSpelling=guangdong; userLikesIdTemp=1527342610643; JSESSIONID=abcxEWkx755q2gzTFDFow; hisHos=24338"}

    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    # 找出该页医院的URL
    hospital_url = soup.select(
        'body > div.serach-wrap > div > div.serach-left > div.serach-left-list > ul > li > a')

    for i in hospital_url:
        print('http://yyk.39.net' + i.get('href'))

    time.sleep(1)


def find_each_page(url, total_pages_number):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Cookie': "_webyyk_areaId=44; _webyyk_areaSpelling=guangdong; userLikesIdTemp=1527342610643; JSESSIONID=abcxEWkx755q2gzTFDFow; hisHos=24338"}

    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    # 找下一页URL，转成GBK编码，再合并成完整的URL
    # 多页时找出每页的地址，然后逐条URL传给get_link()
    # 单页时直接传URL给get_link()
    # ================
    # 多页
    if total_pages_number > 0:
        next_page = soup.select(
            'body > div.serach-wrap > div > div.serach-left > div.serach-left-list > div > div.next > a')[0]

        find_one = next_page.get('href')
        # 将找出的URL以等号分隔，找出下一页的搜索条件，并转换成GBK编码
        url_part_one = find_one.split('=')[0]
        url_part_two_find_city = find_one.split('=')[1]

        city_to_gbk = quote(url_part_two_find_city, encoding='gbk')
        real_next_page_url = "{}{}{}{}".format(
            "http://yyk.39.net", url_part_one, "=", city_to_gbk)
        # print("real_next_page_url:", real_next_page_url)

        # 接收转码后的URL进行拆分
        sp = real_next_page_url.split('c_p')
        u_link_part1 = sp[0]
        u_link_part2 = sp[1]

        # 第二部分以/分隔，提取第二部分
        page_split = u_link_part2.split('/')
        url_end_part = page_split[1]

        # 创建空列表存放处理后的URL，并存入第一页的URL

        all_url = []
        all_url.append(url)

        # 总页数从外部传入，生成以第二页开始，总页数为止的URL，存入列表
        for pages in range(2, total_pages_number + 1):
            finall_url = "{}{}{}{}{}".format(
                u_link_part1, "c_p", pages, "/", url_end_part)
            all_url.append(finall_url)
            # print(finall_url)
        # 打印数据所有元素
        for eachUrl in range(0, len(all_url)):
            print(all_url[eachUrl])
            get_link(all_url[eachUrl])
    # ==========================
    # 单页
    elif total_pages_number == 0:
        get_link(url)


url = "http://yyk.39.net/guangdong/hospitals/?name=%B8%DF%C3%F7"

total_pages_number = find_total_pages(url)

find_each_page(url, total_pages_number)

# get_link(url, total_pages_number)


'''
body > div.serach-wrap > div > div.serach-left > div.serach-left-list > div > div.pages > cite
http://yyk.39.net/guangdong/hospitals/c_p2/?name=%B9%E3%D6%DD
http://yyk.39.net/guangdong/hospitals/c_p2/?name=%B9%E3%D6%DD
http://yyk.39.net/guangdong/hospitals/c_p3/?name=%B9%E3%D6%DD
%B9%E3%D6%DD

4页
http://yyk.39.net/guangdong/hospitals/?name=%C8%FD%CB%AE

1页
http://yyk.39.net/guangdong/hospitals/?name=%B8%DF%C3%F7

'''
