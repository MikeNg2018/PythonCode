# codeing-utf8

import xlrd
import cx_Oracle
import time
import traceback
import sys
import os
from datetime import datetime
from xlrd import xldate_as_tuple

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

if __name__ == "__main__":
    start_time = time.time()
    try:
        if len(sys.argv) < 2:
            exit()
        pcyclepc = sys.argv[1]
        fromid = '6E1C39062A64EA40E0530802A8C098BA'

        # 数据库操作
        # db = cx_Oracle.connect('hr', 'hrpwd', 'localhost:1521/XE')
        # dsn_tns = cx_Oracle.makedsn('127.0.0.1', 1521, 'test')
        # db = cx_Oracle.connect('system', '123456', dsn_tns)
        db = cx_Oracle.connect('system', '123456', 'localhost/xe')
        cursor = db.cursor()


        project_dir = "D:\\Mike\\PythonCode\\练习\\untitled\\" + pcyclepc + "\\"
        # project_dir = "/var/www/html/hwwce1/performance/_file" + pcyclepc + "/"

        excel_files = os.listdir(project_dir)

        # print(excel_files)
        # 查找目录内的所有Excel文件的文件名，并根据文件夹名
        for each_excel in excel_files:
            # print(each_excel)
            # find_fid = cursor.execute(
            #     "SELECT fid FROM HWWCE1_PERFORMANCE_FILE WHERE PCYCLEPC='" +
            #     pcyclepc +
            #     "' AND PFILEENGNAME='" +
            #     each_excel +
            #     "'")
            # fid_num = find_fid.fetchone()[0]
            wb = xlrd.open_workbook(project_dir + each_excel)

            # 创建存放结果的列表
            result_list = []

            # result = open("result.txt", "a", encoding='utf8')

            # sheets_len = len(wb.sheet_names())
            # for sheet_index in range(0, sheets_len):
            #     table = wb.sheet_by_index(sheet_index)

            table = wb.sheet_by_name('NTM1')
            # 列数
            col_number = table.ncols

            # 行数
            row_number = table.nrows

            '''
            pcycle:     01考核周期（显示）
            staffno:    03员工工号（显示）
            staffname:  04姓名（显示）         
            '''
            xianshi = '（显示）'
            include_xianshi = []

            for each_cell in range(0, col_number):
                if table.cell(0, each_cell).value == '01考核周期（显示）':
                    real_01_col = each_cell
                elif table.cell(0, each_cell).value == '03员工工号（显示）':
                    real_03_col = each_cell
                elif table.cell(0, each_cell).value == '04姓名（显示）':
                    real_04_col = each_cell
                # if xianshi in table.cell(0, each_cell).value:
                #     include_xianshi.append(each_cell)
                #     print('（显示）', each_cell)

            # print('01:', real_01_col)
            # print('03:', real_03_col)
            # print('04:', real_04_col)
            # print('显示：', need_display)
            #

            # # 循环读取工作表内容
            for row in range(3, row_number):
                for col in range(0, col_number):
                    if xianshi in table.cell(0, col).value:
                        pkey = table.cell(0, col).value
                        pvalue = table.cell(row, col).value
                    else:
                        pkey = ''
                        pvalue = ''
                    staffname = table.cell(row, real_04_col).value
                    staffno = table.cell(row, real_03_col).value
                    pcycle = table.cell(row, real_01_col).value

                    # ctype：0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
                    # 如果pcycle为date，转换成年/月/日 格式
                    # print(table.cell(row, 0).ctype)
                    if table.cell(row, 0).ctype == 3:
                        date = datetime(*xldate_as_tuple(pcycle, 0))
                        pcycle = date.strftime('%Y/%d/%m')

                    # # 如果staffname为number，打印Sheet名，并退出程序
                    # if table.cell(row, 7).ctype == 2:
                    #     print("不能为数值", table.cell(row, 7).value)
                    #     print(table.name)
                        # sys.exit(0)
                    # sended 列序
                    sended = col
                    filesheetrow = "{}/{}/{}".format(fromid, row, row_number)
                    # result_list.append((str(pkey), str(pvalue), str(staffname), str(staffno), str(pcycle)))
                    result_list.append((str(pcycle),
                                        str(pcyclepc),
                                        str(staffno),
                                        str(staffname),
                                        str(pkey),
                                        str(pvalue),
                                        sended,
                                        fromid,
                                        filesheetrow))
            #批量插入
            cursor.prepare("""INSERT INTO "SYSTEM"."test"
                                               (PCYCLE, PCYCLEPC, STAFFNO, STAFFNAME, PKEY, PVALUE, SENDED, FROMID, FILESHEETROW)
                                                   VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)""")
            cursor.executemany(None, result_list)
            db.commit()
            # # 测试打印
            for a in result_list:
            # #     result.write(str(a))
                print(a)
    except Exception:
        traceback.print_exc()
    end_time = time.time()
    print(end_time - start_time)
