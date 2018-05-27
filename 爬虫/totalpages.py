from bs4 import BeautifulSoup
import requests
import re


real_next_page_url = 'http://yyk.39.net/guangdong/hospitals/c_p2/?name=%B9%E3%D6%DD'

cut_http_string = real_next_page_url.lstrip('http://')
# print(cut_http_string)
next_page_number = str(cut_http_string.split('/')[3])
print("next_page_number", next_page_number)
comp = re.compile(r'(\w_\w)(\d(\d)?(\d)?)')
c_p_string = re.search('(.*)(-?[1-9]\d*$)', next_page_number).group(1)
print("c_p_string", c_p_string)
page_plus = comp.match(next_page_number).group(2)

print("page_plus_one:", page_plus)
