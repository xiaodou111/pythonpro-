import pandas as pd

from auto.utils.excelutil import rename_excel_ps
from auto.utils.gui import get_filename

desktop_path = r'D:\download\桌面'
# filename = input("请输入Excel文件名：")
filename = get_filename()
#
# save_path = desktop_path + '\\' + filename+'.xlsx'
# output_path = desktop_path + '\\'+ filename+'_modified.xlsx'
# 读取Excel文件
# 读取Excel文件
#只修改包含sheet页包含配送的excel
rename_excel_ps(save_path,output_path,{
            '过账日期': 'ZDATE',
            '业务机构名称': 'NAME1',
            '单据类型': 'DJLX',
            '商品编码': 'WAREID',
            '生产企业': 'SCQY',
            '相关单位名称': 'ORGNAME',
            '入库数量': 'RKSL',
            '出库数量': 'CKSL',
            '批号': 'PH'
        })



