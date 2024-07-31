SELECT hdr.sub_unit_num_id as 门店编码, unit.sub_unit_name as 门店名称,auth_user_name AS 工号, auth_login_name as 用户组编码,
        CASE
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) =1 then '店长'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) BETWEEN 10 AND 19 then '店长'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) BETWEEN 2 AND 3 THEN '收银'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) BETWEEN 20 AND 39 THEN '收银'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) BETWEEN 202 AND 203 THEN '收银'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) BETWEEN 220 AND 239 THEN '收银'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) =4 then '质量负责人'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) BETWEEN 40 AND 49 THEN '质量负责人'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) =5 then '采购员'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) BETWEEN 70 AND 79 THEN '采购员'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) =50 then '养护员'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) BETWEEN 51 AND 59 THEN '养护员'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) =60 then '验收员'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) BETWEEN 62 AND 69 THEN '验收员'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) =8 then '诊所信息员'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) BETWEEN 80 AND 89 THEN '诊所信息员'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) =9 then '驻店药师'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) BETWEEN 90 AND 99 THEN '驻店药师'
        WHEN CAST(RIGHT(auth_login_name, 3) AS SIGNED) BETWEEN 100 AND 130 then '医生'
    END AS 用户组,
       count(*) as 数量
FROM rrtprod_platform.sys_user_wechat_auth_log hdr
left join rrtprod_mdm.mdms_o_sub_unit unit on hdr.sub_unit_num_id = unit.sub_unit_num_id
WHERE auth_user_name IS NOT NULL
  AND length(auth_user_name) <= 8
  AND auth_user_name NOT REGEXP '[^0-9]' -- PostgreSQL 使用 ~ 而不是 REGEXP  !~ '[^0-9]'
  and date(hdr.create_dtme)=CURRENT_DATE
and unit.cort_num_id not in ('TX01','TZ01')
GROUP BY hdr.sub_unit_num_id,unit.sub_unit_name,auth_user_name,auth_login_name