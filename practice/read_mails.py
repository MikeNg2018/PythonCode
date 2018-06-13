# -*- coding: utf-8 -*-
"""
通过email模块读取本地邮件文件并解码
mail_name：邮件文件名
mail_text: 邮件内容
"""
import os
import sys
import traceback
import email
from email.policy import default

if __name__ == "__main__":
    mails_path = "D:\\tmp\\"
    try:
        # 读取传入的文件夹名称
        if len(sys.argv) < 2:
            print("ERROR: Need a folder name!")
            exit()
        object_file_path_name = sys.argv[1] + "\\"
        # 找出该目录下的邮件文件名
        mail_name = os.listdir(mails_path + object_file_path_name)[0]
        # 获得邮件文件绝对路径
        path = mails_path + object_file_path_name + mail_name
        # mail模块读取eml格式邮件内容
        with open(path, 'rb') as read_mail:
            mail_msg = email.message_from_binary_file(
                read_mail, policy=default)

        for part in mail_msg.walk():
            mail_text = part.get_payload(decode=True)
        # 转换成UTF-8
        mail_text = str(mail_text, 'utf-8')
        print(mail_text)
    except Exception:
        traceback.print_exc()

    # with open(mails_path + object_file_path_name + 'test.html', 'wb') as f:
    #     f.write(mail_text)
