from bs4 import BeautifulSoup
import requests
import re

def get_info(hospital_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Cookie': "_webyyk_areaId=44; _webyyk_areaSpelling=guangdong; userLikesIdTemp=1527342610643; JSESSIONID=abcxEWkx755q2gzTFDFow; hisHos=24338"}

    wb_data = requests.get(hospital_url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    hospital_name = soup.select('body > div.jy_hspt_mid > div.wid1000 > div.jy_hspt_intro > div > div.l > h2')[0]
    hospital_address = soup.select('body > div.jy_hspt_mid > div.wid1000 > div.jy_hspt_main > div.jy_hspt_main_l > div.hspt_left_p1 > div.hspt_infor > div.r > table ')[0]
    hospital_outpatient = soup.select('body > div.jy_hspt_mid > div.wid1000 > div.jy_hspt_main > div.jy_hspt_main_l > div.hspt_left_p1 > div.xinxi.xinxi2 > ul > li.x3 > cite > font')[0].text

    name = re.compile(r'(<h2>)(.*)(<span>)').search(str(hospital_name)).group(2)
    address = re.compile(r'(<td>)(.*)(</td>)').search(str(hospital_address)).group(2)

    print("名：", name)
    print("地址：", address)
    print("门诊量：", hospital_outpatient)

URL = 'http://yyk.39.net/gz/zonghe/550b5.html'

get_info(URL)



'''

body > div.jy_hspt_mid > div.wid1000 > div.jy_hspt_main > div.jy_hspt_main_l > div.hspt_left_p1 > div.hspt_infor > div.r > table > tbody > tr:nth-child(2) > td:nth-child(2)
'''