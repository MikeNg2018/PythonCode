#!python3
#功能：提取用ansible获得的各影院联系人信息
import os, json, re, openpyxl, json, pymysql

os.chdir('C:\\work\\工作\\零碎\\抽取影院联系人\\contact')

#新建工作簿存放数据
wbContacts = openpyxl.Workbook()
newsheet1 = wbContacts.get_active_sheet()
newsheet1.title = 'Contact'
contactsSheet = wbContacts.get_sheet_by_name('Contact')
contactsSheet['A1'] = "影院"
contactsSheet['B1'] = "IP"
contactsSheet['C1'] = "联系人"
contactsSheet['D1'] = "联系电话"
contactsSheet['G1'] = '没连通的影院'
contactsSheet['H1'] = 'IP'
contactsSheet['I1'] = '联系电话'
contactsSheet['J1'] = '是否在CSEP库'

#从第二行开始写数据
n = 2

#创建ansible数据库连接
db = pymysql.connect("192.168.100.59", "cpms", "cpmsuser", "ansible", charset='utf8')
cursor = db.cursor()

#创建CSEP数据库连接
db_2 = pymysql.connect("10.2.5.6", "cpms", "cpmsuser", "CSEP", charset='utf8')
cursor2 = db_2.cursor()

#创建正则匹配：分组查找联系人姓名，联系人电话
re_val = re.compile(r'(^\w{0,3})\s*(\d.*)')
#遍历目录下的ansible文件，转成JSON格式，用正则匹配，写入工作簿
for fn in os.listdir('.'):
    with open(fn, 'r', encoding='utf8') as files:
        jType = json.load(files)
    try:
        info_contact = jType['stdout_lines']
        findmatch = re.match(re_val, info_contact[1])

        #根据IP查找影院名称
        sql_ansible = "SELECT cinema FROM hosts WHERE ip = '%s';" % files.name
        cursor.execute(sql_ansible)
        results = cursor.fetchall()
        #影院名称
        contactsSheet.cell(column=1, row=n).value = results[0][0]
        #IP地址
        contactsSheet.cell(column=2, row=n).value = files.name
        #联系人姓名
        contactsSheet.cell(column=3, row=n).value = findmatch.group(1)
        #联系人电话
        contactsSheet.cell(column=4, row=n).value = findmatch.group(2)
        n = n + 1
    except:
        pass

#遍历目录下的ansible文件，找出连不通的影院
#从第二行开始写数据
m = 2
for fn in os.listdir('.'):
    with open(fn, 'r', encoding='utf8') as files:
        jType = json.load(files)
    try:
        #查找文件中含有unreachable的
        connect_fail = jType['unreachable']

        sql_ansible = "SELECT cinema FROM hosts WHERE ip = '%s';" % files.name
        cursor.execute(sql_ansible)
        results = cursor.fetchall()
        #查询CSEP上有IP的影院信息
        sql_CSEP = "SELECT PHONE FROM CMS_CINEMA_INFO WHERE IP = '%s';" % files.name
        cursor2.execute(sql_CSEP)
        results_CSEP = cursor2.fetchall()
        #IP地址
        contactsSheet.cell(column=8, row=m).value = files.name
        # 影院名称
        contactsSheet.cell(column=7, row=m).value = results[0][0]
        #影院联系人电话
        contactsSheet.cell(column=9, row=m).value = results_CSEP[0][0]
        #是否存在CSEP中
        contactsSheet.cell(column=10, row=m).value = '是'
        m = m + 1
    except:
        pass

wbContacts.save('C:\\work\\工作\\零碎\\抽取影院联系人\\Contact.xlsx')
wbContacts.close()
db.close()
db_2.close()