select sub_unit_num_id as 门店编码, max(sub_unit_name) as 门店名称, count(*) as 数量
from (select hdr.sub_unit_num_id, unit.sub_unit_name, hdr.tml_num_id, hdr.order_date
      from rrtprod_memorder.sd_bl_so_tml_hdr hdr
               left join rrtprod_mdm.mdms_o_sub_unit unit on hdr.sub_unit_num_id = unit.sub_unit_num_id
      WHERE type_num_id = 2
        and date(hdr.create_dtme) = CURRENT_DATE
      and hdr.status_num_id = 6
      and unit.cort_num_id not in ('TX01','TZ01')
-- and not exists(select 1 from sd_bl_so_op_cf_hdr cf where hdr.sub_unit_num_id=cf.sub_unit_num_id)
     ) a
group by sub_unit_num_id