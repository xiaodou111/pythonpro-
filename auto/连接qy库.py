import pymysql
import pandas as pd
from datetime import datetime, timedelta

# 获取昨天的日期
yesterday = datetime.now() - timedelta(days=1)
# 格式化日期为字符串
formatted_date = yesterday.strftime('%Y%m%d')
filename = f'{formatted_date}_销售.xlsx'
desktop_path = r'D:\download\桌面'
save_path = desktop_path + '\\' + filename
# 创建连接
try:
    # connection = pymysql.connect(host='172.20.139.17',
    #                              user='rrtselect',
    #                              password='3U5AWzwrrkS^=aSdc',
    #                              # database='your_database',
    #                              charset='utf8mb4',
    #                              cursorclass=pymysql.cursors.DictCursor)

    connection = pymysql.connect(host='172.20.139.17',
                                 user='rrtselect',
                                 port=5066,
                                 password='3U5AWzwrrkS^=aSdc',
                                 database='',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    print("连接成功！")
#
    with connection.cursor() as cursor:

#
#         # 查询数据
        sql = """
           select HDR.ORDER_DATE,
       DTL.CREATE_DTME,
       HDR.TML_NUM_ID,
       HDR.TYPE_NUM_ID,
       HDR.SOURCE_TML_NUM_ID,
       HDR.SO_FROM_TYPE,
       DTL.ITEM_NUM_ID,
       UNIT.PRO_CODE_OLD,
       DTL.ITEM_NAME,
       DTL.BATCH_ID,
       DTL.DEDUCT_AMOUNT,
       DTL.RETAIL_PRICE,
       DTL.RETAIL_AMOUNT,
       DTL.TRADE_PRICE,
       DTL.QTY,
       DTL.TAX_RATE,
       DTL.F_AMOUNT,
       DTL.EXPIRY_DATE,
       DTL.SERIES,
       HDR.CORT_NUM_ID,
       HDR.SUB_UNIT_NUM_ID,
       SUB.OLD_SUB_UNIT_ID,
       HDR.VIP_NO,
       hdr.CREATE_USER_ID,
       sub.MANAGER_CODE
from rrtprod_memorder.sd_bl_so_tml_hdr hdr
         inner join rrtprod_memorder.sd_bl_so_tml_lock_dtl dtl  -- sd_bl_so_tml_lock_dtl销售明细表
                    on hdr.tenant_num_id = dtl.tenant_num_id
                        and hdr.data_sign = dtl.data_sign
                        and hdr.order_date = dtl.order_date
                        and hdr.cort_num_id = dtl.cort_num_id
                        and hdr.sub_unit_num_id = dtl.sub_unit_num_id
                        and hdr.tml_num_id = dtl.tml_num_id
         inner join rrtprod_mdm.mdms_p_product_unit unit
                    on dtl.cort_num_id = unit.cort_num_id and dtl.tenant_num_id = unit.tenant_num_id
   and dtl.data_sign = unit.data_sign
   and dtl.item_num_id = unit.item_num_id
	 	  inner join rrtprod_mdm.mdms_o_sub_unit sub
on dtl.sub_unit_num_id = sub.sub_unit_num_id
    and dtl.tenant_num_id = unit.tenant_num_id
    and dtl.data_sign = unit.data_sign
    and dtl.item_num_id = unit.item_num_id
where hdr.tenant_num_id = 18
  and hdr.data_sign = 0
  and hdr.status_num_id = 6
and hdr.order_date=DATE_SUB(CURDATE(), INTERVAL 1 DAY)
             """
        # cursor.execute(sql, ('value1',))
        cursor.execute(sql)

        rows = cursor.fetchall()

       # 将查询结果转换为DataFrame
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

       # 导出DataFrame到Excel文件
        df.to_excel(save_path, index=False)
        # result = cursor.fetchone()
        # result = cursor.fetchall()
        print(f"文件已保存到 {save_path}")
#
finally:
    connection.close()