from bs4 import BeautifulSoup
import requests
from urllib.parse import quote
import re
import time
import os

# 用作存放医院页URL
hospital_page_list = []


# 新建文件存放结果，如果存在，文件名加_new


def check_file(path):
    """
    检查输入路径的文件夹和文件是否存在，不存在自动创建
    :param path:
    :return:
    """
    path = path.strip()
    path_dirname = os.path.dirname(path)
    is_exists = os.path.exists(path_dirname)

    if not is_exists:
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


def get_info(hospital_url, file_path):
    """
    功能：查找每个医院名称，地址和门诊量
    :param hospital_url:传入每家医院的URL
    :return:将需要的信息打印到屏幕
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Cookie': "_webyyk_areaId=44; _webyyk_areaSpelling=guangdong; userLikesIdTemp=1527342610643; JSESSIONID=abcxEWkx755q2gzTFDFow; hisHos=24338"}

    wb_data = requests.get(hospital_url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    hospital_name = soup.select(
        'body > div.jy_hspt_mid > div.wid1000 > div.jy_hspt_intro > div > div.l > h2')[0]

    name = re.compile(
        r'(<h2>)(.*)(<span>)').search(str(hospital_name)).group(2)

    hospital_address = soup.select(
        'body > div.jy_hspt_mid > div.wid1000 > div.jy_hspt_main > div.jy_hspt_main_l > div.hspt_left_p1 > div.hspt_infor > div.r > table ')[0]
    address = re.compile(
        r'(<td>)(.*)(</td>)').search(str(hospital_address)).group(2)

    try:
        hospital_outpatient = soup.select(
            'body > div.jy_hspt_mid > div.wid1000 > div.jy_hspt_main > div.jy_hspt_main_l > div.hspt_left_p1 > div.xinxi.xinxi2 > ul > li.x3 > cite > font')[0].text

    except IndexError:
        hospital_outpatient = 'None'

    try:
        bed_number = soup.select(
            'body > div.jy_hspt_mid > div.wid1000 > div.jy_hspt_main > div.jy_hspt_main_l > div.hspt_left_p1 > div.xinxi.xinxi2 > ul > li.x1 > cite > font')[0].text
    except IndexError:
        bed_number = 'None'

    # 生成结果
    result = name + ',' + address + ',' + hospital_outpatient + ',' + bed_number + '\n'

    # 检查文件是否存在，然后写入数据
    check_file(file_path)
    with open(file_path, 'a') as resultFile:
        resultFile.write(result)


    print("名：", name)
    print("地址：", address)
    print("门诊量：", hospital_outpatient)
    print("床位数：", bed_number)


def find_total_pages(url):
    """
    查找总页数
    :param url: 传入URL
    :return: 返回总页数
    """
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
    """
    查找每页医院的URL
    :param url:
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Cookie': "_webyyk_areaId=44; _webyyk_areaSpelling=guangdong; userLikesIdTemp=1527342610643; JSESSIONID=abcxEWkx755q2gzTFDFow; hisHos=24338"}

    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    # 找出该页医院的URL
    hospital_url = soup.select(
        'body > div.serach-wrap > div > div.serach-left > div.serach-left-list > ul > li > a')

    for i in hospital_url:
        hospital_info_page_url = 'http://yyk.39.net' + i.get('href')
        hospital_page_list.append(hospital_info_page_url)

    time.sleep(1)


def find_each_page(url, total_pages_number):
    """
    找出每一分页的URL
    :param url:
    :param total_pages_number:
    :return:
    """
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


# url = "http://yyk.39.net/guangdong/hospitals/?name=%C8%FD%CB%AE"
print('使用说明：')
print('输入网址：例如：http://yyk.39.net/guangdong/hospitals/?name=%C8%FD%CB%AE')
print('输入路径和文件，双反斜杠（例如：D:\\\\tmp\\\\info.txt）')
print('停止程序：Ctrl+C')

try:
    while True:
        print("===================")
        url = input("输入网址（必填）>>>>")
        file_path = input("输入路径和文件（必填）>>>>")
        print("===================")
        if url and file_path:
            # 找出总页数
            print("正在获取数据，请稍后……")
            total_pages_number = find_total_pages(url)
            # 找每页医院的URL
            find_each_page(url, total_pages_number)
            # 将每家医院的URL传给get_info提取数据
            for eachUrl in range(0, len(hospital_page_list)):
                get_info(hospital_page_list[eachUrl], file_path)
                time.sleep(1)
            break
        else:
            print("=====网址和路径不能为空，请重新输入=====")
            continue

except KeyboardInterrupt:
    print('\n')
    print("=============已手动停止，Bye!!!=============")
    print('\n')
else:
    print('\n\n')
    print("=============Finish==============")
    print('请到:%s查看结果' %file_path)
    print('\n\n')



'''

24页
http://yyk.39.net/guangdong/hospitals/?name=%B9%E3%D6%DD

4页
http://yyk.39.net/guangdong/hospitals/?name=%C8%FD%CB%AE

1页
http://yyk.39.net/guangdong/hospitals/?name=%B8%DF%C3%F7

'''
