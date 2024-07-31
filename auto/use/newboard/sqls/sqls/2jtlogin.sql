select hdr.sub_unit_num_id as 门店编码, unit.sub_unit_name as 门店名称,computer_name as 计算机名 ,count(*) as 数量
from rrtprod_platform.sys_user_wechat_auth_log hdr
left join rrtprod_mdm.mdms_o_sub_unit unit on hdr.sub_unit_num_id = unit.sub_unit_num_id
where LENGTH(computer_name) = 7
and date(hdr.create_dtme)=CURRENT_DATE
and unit.cort_num_id not in ('TX01','TZ01')
group by hdr.sub_unit_num_id, unit.sub_unit_name,computer_name