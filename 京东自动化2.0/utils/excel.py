import os
import xlrd
import xlwt
from xlutils.copy import copy


class MakeExcel():
    def __init__(self, sheet_name, xls_name):
        """
        实例化接收两个参数
        :param sheet_name: 字符串，sheet表格的名称
        :param xls_name: 字符串，文件名
        """
        self.sheet_name = sheet_name
        self.xls_name = xls_name + ".xls"

    def make_base_excel(self, title):
        """
        创建一个空表格模板并保存到excel文件中
        :param title: 只接收列表嵌套列表，表格字段名称
        :return: None
        """
        index = len(title)
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(self.sheet_name)
        for i in range(0, index):
            for j in range(0, len(title[i])):
                sheet.write(i, j, title[i][j])
        workbook.save(self.xls_name)
        print("%s表格模板创建成功！" % self.xls_name)
        return self.xls_name

    def add_base_sheet(self, sheet_name, title):
        """
        在已有的excel文件上新增一个sheet表格
        :param sheet_name: 字符串，sheet表格名称
        :param title: 列表嵌套列表，表格字段名称
        :return:
        """
        index = len(title)
        rb = xlrd.open_workbook(self.xls_name, formatting_info=True)
        wb = copy(rb)
        sheet = wb.add_sheet(sheet_name)
        for i in range(0, index):
            for j in range(0, len(title[i])):
                sheet.write(i, j, title[i][j])
        wb.save(self.xls_name)
        print("新增表格模板成功！")

    def white_excel_content(self, value, P1=0):
        """
        向已有的表格模板中添加数据内容
        :param value: 列表嵌套列表，数据内容
        :param P1: 整形，代表sheet表格标识，默认0开始代表第一个表格
        :return: None
        """
        index = len(value)
        workbook = xlrd.open_workbook(self.xls_name)
        sheets = workbook.sheet_names()
        worksheet = workbook.sheet_by_name(sheets[P1])
        rows_old = worksheet.nrows
        new_workbook = copy(workbook)
        new_worksheet = new_workbook.get_sheet(P1)
        for i in range(0, index):
            for j in range(0, len(value[i])):
                new_worksheet.write(i + rows_old, j, value[i][j])
        new_workbook.save(self.xls_name)
        print("数据内容追加完成！")

    def read_sheet(self, fail_list, P1=0):
        """
        读取excel表格中的数据
        :param P1: 整形，代表sheet表格标识，默认0开始代表第一个表格
        :return: None
        """
        temp_list = []
        workbook = xlrd.open_workbook(self.xls_name)
        sheets = workbook.sheet_names()
        worksheet = workbook.sheet_by_name(sheets[P1])
        for i in range(0, worksheet.nrows):
            if i == 0:
                pass
            else:
                for f in fail_list:
                    if int(worksheet.cell_value(i, 5)) == int(f):
                        pass
                    else:
                        temp_list.append(str(int(worksheet.cell_value(i, 5))))
        return list(set(temp_list))