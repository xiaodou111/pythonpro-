with new as (select order_date, SUB_UNIT_NUM_ID, tml_num_id
             from d_rrtprod_memorder
             where sub_unit_num_id in
                   (select NBUSNO
                    from D_RRT_QY_COMPID_BUSNO
                    where OBUSNO in (select BUSNO from D_BP_BUSNO))
               and order_date = trunc(sysdate) -1
               and so_from_type = 17
             group by order_date, SUB_UNIT_NUM_ID, tml_num_id),

     old as (select s.BUSNO, h.ACCDATE, h.SALENO
             from t_sale_h h
                      join t_sale_d d on h.SALENO = d.SALENO
                      join t_ware_base w on d.WAREID = w.WAREID
                      left join s_busi s on h.BUSNO = s.BUSNO
             where s.busno in (select BUSNO from D_BP_BUSNO)
               and h.ACCDATE = trunc(sysdate)-1
               and exists(select 1
                              from t_sale_pay p
                              where p.saleno = h.saleno and p.paytype in
                                                            ('Z022', 'Z025', 'Z027', 'Z030', 'Z032', 'Z034', 'Z077',
                                                             'Z081', 'Z098', 'Z100', 'Z101', 'Z084', 'Z102', 'Z107')
                                and p.netsum <> 0)
               and not exists(select 1 from T_SALE_RETURN_H th where th.SALENO=h.SALENO)
               and not exists(select 1 from T_SALE_RETURN_H th2 where th2.RETSALENO=h.SALENO)
               and not exists(select 1 from t_internal_sale_h ngd where SHIFTDATE>=date'2024-05-20' and ngd.NEWSALENO=h.SALENO)
               and not exists(select 1 from d_bp_exclude_sale exc where exc.SALENO=h.SALENO)
             group by s.BUSNO, h.ACCDATE, h.SALENO),
     new_hz as (select order_date, SUB_UNIT_NUM_ID, count(tml_num_id) sumsl
                from new
                group by order_date, SUB_UNIT_NUM_ID),
     old_hz as (select BUSNO, ACCDATE, count(SALENO) sumsl from old group by BUSNO, ACCDATE),
     re as (select a.BUSNO, ACCDATE, nvl(a.sumsl, 0) as 老系统销售单数, order_date,
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
                and a.ACCDATE = b.order_date
            order by a.BUSNO, a.ACCDATE)
select q.ACCDATE as 日期, q.BUSNO as 门店编码, s.ORGNAME as 门店名称, q.老系统销售单数,
       q.新系统数量, q.bl as 录单比率
from re q
         left join s_busi s on q.BUSNO = s.BUSNO
         left join D_BP_BUSNO b on q.BUSNO=b.BUSNO