#!python3
#功能：查询CSEP上的联系电话写入表
import os, openpyxl, pymysql, time

os.chdir('C:\\work\\工作\\零碎\\抽取影院信息')

wbData = openpyxl.Workbook()
newsheet = wbData.get_active_sheet()

#创建CSEP数据库连接
db_2 = pymysql.connect("10.2.5.6", "cpms", "cpmsuser", "CSEP", charset='utf8')
cursor2 = db_2.cursor()

#写入表头
newsheet.cell(column=1,row=1).value = '影院名称'
newsheet.cell(column=2,row=1).value = '影院编码'
newsheet.cell(column=3,row=1).value = '影院地址'
newsheet.cell(column=4,row=1).value = '电话1'
newsheet.cell(column=5,row=1).value = '电话2'

# 查询数据
print("查询数据",time.strftime('%Y-%m-%d %X', time.localtime()))
sql_CSEP = "SELECT CINEMA_NAME,CINEMA_CODE,ADDRESS,PHONE,TELEPHONE FROM CMS_CINEMA_INFO WHERE ADDRESS LIKE '%浙江%';"
cursor2.execute(sql_CSEP)
results_CSEP = cursor2.fetchall()

# 循环嵌套写入excel
print("写入数据中",time.strftime('%Y-%m-%d %X', time.localtime()))
resultsLen = len(results_CSEP)
columnNumber = 1
rowNumber = 1
for x in range(0, resultsLen):
    rowNumber = rowNumber + 1
    for y in range(0, 5):
        newsheet.cell(column=columnNumber, row=rowNumber).value = results_CSEP[x][y]
        columnNumber = columnNumber + 1
        if columnNumber > 5:
            columnNumber = 1

wbData.save('C:\\work\\工作\\零碎\\抽取影院信息\\data.xlsx')
wbData.close()
print("写入完毕",time.strftime('%Y-%m-%d %X', time.localtime()))
db_2.close()