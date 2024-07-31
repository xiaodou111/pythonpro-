select hdr.sub_unit_num_id as 门店编码, unit.sub_unit_name as 门店名称, count(*) as 数量
from rrtprod_memorder.sd_bl_so_tml_hdr hdr
         left join rrtprod_mdm.mdms_o_sub_unit unit on hdr.sub_unit_num_id = unit.sub_unit_num_id
where unit.shop_category = 4
  and hdr.order_date = CURRENT_DATE
and unit.cort_num_id not in ('TX01','TZ01')
group by hdr.sub_unit_num_id, unit.sub_unit_name