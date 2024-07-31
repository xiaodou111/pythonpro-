select hdr.sub_unit_num_id as 门店编码, unit.sub_unit_name as 门店名称, hdr.tml_num_id as 订单号, hdr.create_dtme as 创建时间
      from rrtprod_memorder.sd_bl_so_tml_hdr hdr
               left join rrtprod_mdm.mdms_o_sub_unit unit on hdr.sub_unit_num_id = unit.sub_unit_num_id
      where date(hdr.create_dtme) = CURRENT_DATE
        and unit.cort_num_id not in ('TX01','TZ01')
      and hdr.status_num_id = 6