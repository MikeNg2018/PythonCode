from bs4 import BeautifulSoup
import requests
from urllib.parse import quote
import re

import os
import time
import random


def find_total_pages(url):
    '''
    查总页数
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Cookie': "_webyyk_areaId=44; _webyyk_areaSpelling=guangdong; userLikesIdTemp=1527342610643; JSESSIONID=abcxEWkx755q2gzTFDFow; hisHos=24338"}

    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    total_pages = soup.select(
        'body > div.serach-wrap > div > div.serach-left > div.serach-left-list > div > div.pages > cite')[0]
    total_pages_number = int(re.compile(r'\d+').findall(str(total_pages))[0])
    print(total_pages_number)
    return total_pages_number


def auto_next_page(url, total_pages_number):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Cookie': "_webyyk_areaId=44; _webyyk_areaSpelling=guangdong; userLikesIdTemp=1527342610643; JSESSIONID=abcxEWkx755q2gzTFDFow; hisHos=24338"}

    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    try:
        next_page = soup.select(
            'body > div.serach-wrap > div > div.serach-left > div.serach-left-list > div > div.next > a')[0]

        print("============IN NORMAL==================")
        print("======", next_page)
        while next_page:
            find_one = next_page.get('href')
            # 将找出的URL以等号分隔，找出下一页的搜索条件，并转换成GBK编码
            url_part_one = find_one.split('=')[0]
            url_part_two_find_city = find_one.split('=')[1]

            city_to_gbk = quote(url_part_two_find_city, encoding='gbk')
            real_next_page_url = "{}{}{}{}".format(
                "http://yyk.39.net", url_part_one, "=", city_to_gbk)
            print("real_next_page_url", real_next_page_url)

            cut_http_string = real_next_page_url.lstrip('http://')
            # print(cut_http_string)
            next_page_number = str(cut_http_string.split('/')[3])
            print("next_page_number", next_page_number)
            c_p_string = re.search(
                '(\w_\w)(\d(\d)?(\d)?)',
                next_page_number).group(1)
            print("c_p_string", c_p_string)
            page_plus = int(
                re.match(
                    '(\w_\w)(\d(\d)?(\d)?)',
                    next_page_number).group(2))
            page_plus_one = page_plus
            print("page_plus_one:", page_plus_one)
            print("TTTTTTTTTTTTTTTT:", total_pages_number)
            new_next_page_url = "{}{}{}{}{}{}{}".format("http://", '/'.join(cut_http_string.split(
                '/')[0:3]), "/", c_p_string, page_plus_one, "/", cut_http_string.split('/')[4])
            print("$$$$$$$$$$$$$$$$$$$",new_next_page_url)
            get_link(new_next_page_url, total_pages_number, page_plus_one)


    except IndexError:
        '''
        处理找不到下页的情况
        '''
        print("================IN EXCEPT ======================")
        cut_http_string = url.lstrip('http://')
        # print(cut_http_string)
        next_page_number = cut_http_string.split('/')[3]
        # print(next_page_number)
        c_p_string = re.search(
            '(\w_\w)(\d(\d)?(\d)?)',
            next_page_number).group(1)
        # print(c_p_string)
        page_plus = re.match(
            '(\w_\w)(\d(\d)?(\d)?)',
            next_page_number).group(2)
        page_plus_one = int(page_plus) + 1
        # print(page_plus_one)

        new_next_page_url = "{}{}{}{}{}{}{}".format("http://", '/'.join(cut_http_string.split(
            '/')[0:3]), "/", c_p_string, page_plus_one, "/", cut_http_string.split('/')[4])
        # print(new_next_page_url)
        print("total_pages_number:", total_pages_number)
        get_link(new_next_page_url, total_pages_number)


def get_link(url, total_pages_number, *args):
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

    for arg in args:
        print("++++++++ARG++++++++++", arg)
        if arg == 4:
            print("END")
            break
    auto_next_page(url, total_pages_number)


url = "http://yyk.39.net/guangdong/hospitals/?name=%C8%FD%CB%AE"

total_pages_number = find_total_pages(url)

get_link(url, total_pages_number)


'''
body > div.serach-wrap > div > div.serach-left > div.serach-left-list > div > div.pages > cite
http://yyk.39.net/guangdong/hospitals/c_p2/?name=%B9%E3%D6%DD
http://yyk.39.net/guangdong/hospitals/c_p2/?name=%B9%E3%D6%DD
http://yyk.39.net/guangdong/hospitals/c_p3/?name=%B9%E3%D6%DD
%B9%E3%D6%DD
'''
