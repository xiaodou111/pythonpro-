SELECT hdr.sub_unit_num_id as 门店编码, unit.sub_unit_name as 门店名称,auth_user_name AS 工号, count(*) as 数量
FROM rrtprod_platform.sys_user_wechat_auth_log hdr
left join rrtprod_mdm.mdms_o_sub_unit unit on hdr.sub_unit_num_id = unit.sub_unit_num_id
WHERE auth_user_name IS NOT NULL
  AND length(auth_user_name) <= 8
  AND auth_user_name NOT REGEXP '[^0-9]' -- PostgreSQL 使用 ~ 而不是 REGEXP  !~ '[^0-9]'
  and date(hdr.create_dtme)=CURRENT_DATE
and unit.cort_num_id not in ('TX01','TZ01')
GROUP BY hdr.sub_unit_num_id,unit.sub_unit_name,auth_user_name