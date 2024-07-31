select hdr.sub_unit_num_id as 门店编码, unit.sub_unit_name as 门店名称, count(*) as 数量
from rrtprod_memorder.sd_bl_so_op_cf_hdr hdr
         left join rrtprod_memorder.fi_bl_cash_dtl dtl on hdr.cf_sale_no = dtl.reserved_no
         left join rrtprod_mdm.mdms_o_sub_unit unit on hdr.sub_unit_num_id = unit.sub_unit_num_id
where external_flag = 1
  and dtl.pay_type_id in ('531', '523', '521', '524', '525', '522')
  and unit.shop_category <> 4
  and date(hdr.create_dtme) = CURRENT_DATE
and unit.cort_num_id not in ('TX01','TZ01')
group by hdr.sub_unit_num_id, unit.sub_unit_name