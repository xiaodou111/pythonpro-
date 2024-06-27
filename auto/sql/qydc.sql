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
from rrtuat_memorder.sd_bl_so_tml_hdr hdr
         inner join rrtuat_memorder.sd_bl_so_tml_lock_dtl dtl  -- sd_bl_so_tml_lock_dtl销售明细表
                    on hdr.tenant_num_id = dtl.tenant_num_id
                        and hdr.data_sign = dtl.data_sign
                        and hdr.order_date = dtl.order_date
                        and hdr.cort_num_id = dtl.cort_num_id
                        and hdr.sub_unit_num_id = dtl.sub_unit_num_id
                        and hdr.tml_num_id = dtl.tml_num_id
         inner join rrtuat_mdm.mdms_p_product_unit unit
                    on dtl.cort_num_id = unit.cort_num_id and dtl.tenant_num_id = unit.tenant_num_id
   and dtl.data_sign = unit.data_sign
   and dtl.item_num_id = unit.item_num_id
	 	  inner join rrtuat_mdm.mdms_o_sub_unit sub
on dtl.sub_unit_num_id = sub.sub_unit_num_id
    and dtl.tenant_num_id = unit.tenant_num_id
    and dtl.data_sign = unit.data_sign
    and dtl.item_num_id = unit.item_num_id
where hdr.tenant_num_id = 18
  and hdr.data_sign = 0
  and hdr.status_num_id = 6
and hdr.order_date=DATE_SUB(CURDATE(), INTERVAL 1 DAY)
-- and not exists(select 1 from rrtprod_memorder.sd_bl_so_tml_hdr ex1 WHERE ex1.order_date >= '2024-06-13' and ex1.create_user_id <= 1 and ex1.series=hdr.series )
-- and hdr.order_date=CURDATE()
-- and hdr.order_date=date'2024-06-07'