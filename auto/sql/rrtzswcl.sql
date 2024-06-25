with new as (select order_date, SUB_UNIT_NUM_ID, tml_num_id
             from d_qy_zsdj
             where
--                  sub_unit_num_id in
--                    (select NBUSNO
--                     from D_RRT_QY_COMPID_BUSNO
--                     where OBUSNO in (select BUSNO from D_BP_BUSNO))
             order_date = trunc(sysdate)-1 and LOGICAL_STORAGEID=1 and EMPE_NAME is not null
             group by order_date, SUB_UNIT_NUM_ID, tml_num_id),

     old as (select trunc(REG_DATE) as REG_DATE,BUSNO,REGISTER_NO from t_med_register_h where trunc(REG_DATE)=trunc(sysdate)-1
             group by trunc(REG_DATE), BUSNO,REGISTER_NO),
     new_hz as (select order_date, SUB_UNIT_NUM_ID, count(tml_num_id) sumsl
                from new
                group by order_date, SUB_UNIT_NUM_ID),
     old_hz as (select BUSNO, REG_DATE, count(REGISTER_NO) sumsl from old group by BUSNO, REG_DATE),
     re as (select a.BUSNO, REG_DATE, nvl(a.sumsl, 0) as 老系统销售单数, order_date,
                   nvl(b.sumsl, 0) as 新系统数量,
                   case
                       when nvl(a.sumsl, 0) = 0 then 0
                       else
                           case
                               when nvl(b.sumsl, 0) >= 50 then 1
                               else
                            case when  b.sumsl>a.sumsl then 1 else
                                   round(nvl(b.sumsl, 0) / a.sumsl, 3) end end end as bl
            from old_hz a
                     left join new_hz b on substr(a.BUSNO, 2, 4) = b.SUB_UNIT_NUM_ID
                and a.REG_DATE = b.order_date
            order by a.BUSNO, a.REG_DATE)
select q.REG_DATE as 日期, q.BUSNO as 门店编码, s.ORGNAME as 门店名称, q.老系统销售单数,
       q.新系统数量, q.bl as 录单比率
--        ,b.RN as 门店批次
from re q
         left join s_busi s on q.BUSNO = s.BUSNO
--          left join D_BP_BUSNO b on q.BUSNO=b.BUSNO