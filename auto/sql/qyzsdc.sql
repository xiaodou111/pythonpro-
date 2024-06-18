select hdr.series,ys.empe_name,hdr.logical_storageid,
 hdr.tenant_num_id,hdr.data_sign,hdr.order_date,hdr.cort_num_id,hdr.sub_unit_num_id,hdr.tml_num_id, sub.MANAGER_CODE
from rrtprod_memorder.sd_bl_so_tml_hdr hdr
left join rrtprod_memorder.sd_bl_so_op_reg_hdr ys on ys.tml_num_id=hdr.tml_num_id and ys.cort_num_id=hdr.cort_num_id
                                                         and hdr.sub_unit_num_id=ys.sub_unit_num_id
left join rrtprod_mdm.mdms_o_sub_unit sub
on hdr.sub_unit_num_id = sub.sub_unit_num_id
         where logical_storageid in (1,2,3,4) and hdr.tenant_num_id = 18
  and hdr.data_sign = 0
  and hdr.status_num_id = 6
and hdr.order_date=DATE_SUB(CURDATE(), INTERVAL 1 DAY)