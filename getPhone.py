#!python3
#功能：查询CSEP上的联系电话写入表
import os, json, re, openpyxl, json, pymysql

os.chdir('C:\\work\\工作\\零碎\\抽取影院信息')

wbData = openpyxl.load_workbook('data.xlsx')
newsheet = wbData.get_sheet_by_name('Sheet0')

#创建CSEP数据库连接
db_2 = pymysql.connect("10.2.5.6", "cpms", "cpmsuser", "CSEP", charset='utf8')
cursor2 = db_2.cursor()

#写入表头
newsheet.cell(column=1,row=1).value = '影院名称'
newsheet.cell(column=2,row=1).value = '影院编码'
newsheet.cell(column=3,row=1).value = '影院名称'
newsheet.cell(column=4,row=1).value = '电话1'
newsheet.cell(column=5,row=1).value = '电话2'
#有数据的行只到218行
for n in range(2,218):
    try:
        #影院ID在第三列
        cinemaID = newsheet.cell(column=3, row=n).value
        #print(cinemaID)
        #查询影院ID对应的联系人电话号码
        sql_CSEP = "SELECT PHONE FROM CMS_CINEMA_INFO WHERE CINEMA_CODE = '%s';" % cinemaID
        cursor2.execute(sql_CSEP)
        results_CSEP = cursor2.fetchall()
        #print(results_CSEP[0][0])
        #不能直接用results_CSEP，而是要用results_CSEP[0][0]
        newsheet.cell(column=10,row=n).value = results_CSEP[0][0]
    except:ValueError

wbData.save('C:\\work\\工作\\零碎\\抽取影院联系人电话\\data.xlsx')
wbData.close()
db_2.close()