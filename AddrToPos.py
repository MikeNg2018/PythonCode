#!python3
# 需要安装第三方Requests库
import requests,os

def code(address):
    # address为传入要查询的地址，KEY为我自己在高德申请的开发者KEY
    parameters = {'address': address, 'key': '###'}
    # 地理/逆地理编码的接口地址
    base = 'http://restapi.amap.com/v3/geocode/geo'
    # 用requests.get方法获得接口返回结果
    response = requests.get(base, parameters)
    # response.json方法返回JSON格式的数据
    answer = response.json()
    # 查询结果
    result = address + "的经纬度：" + answer['geocodes'][0]['location']
    print(result)
    # 写入文件
    with open('C:\\work\\Mike\\pythoncode\\result.txt', 'a', encoding='utf8') as ResultFile:
        ResultFile.write(result+'\n')

if __name__ == '__main__':
    # 切换工作目录，读取放有地址或地名的文本
    os.chdir("C:\\work\\Mike\\pythoncode")
    # 只读方式打开文本（以UTF8格式打开）
    with open('addr.txt', 'r', encoding='utf8') as AddrFile:
        # 循环读取文件的每一行到变量line
        for line in AddrFile.readlines():
            # 删除每一行后面的换行符
            address = line.strip()
            # 调用code函数
            code(address)
