# -*- coding: utf-8 -*-
import sys
import traceback


def exc_demo():
    try:
        # 可能会出现异常的代码
        a = 1 / 0
    except Exception as e:
        # 获取异常信息
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_info = traceback.extract_tb(exc_traceback)
        filename, line, func, text = tb_info[-1]
        b = filename.split('gatherone_crm/')[-1]
        print(b)
        # 输出异常信息
        print(f"Exception type: {exc_type}")
        print(f"Exception message: {exc_value}")
        print(f"File name: {filename}")
        print(f"Line number: {line}")


if __name__ == '__main__':
    exc_demo()
