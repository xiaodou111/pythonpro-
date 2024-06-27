with new as (select order_date, SUB_UNIT_NUM_ID, tml_num_id
             from d_rrtprod_memorder
             where SUB_UNIT_NUM_ID in
                   (select NBUSNO
                    from D_RRT_QY_COMPID_BUSNO
                    where OBUSNO in (select BUSNO from D_BP_BUSNO))
               and order_date = trunc(sysdate)-1
               and not exists(select 1 from d_rrtprod_memorder ex1 WHERE ex1.order_date >= date'2024-06-13' and ex1.create_user_id <= 1 and ex1.series=d_rrtprod_memorder.series)
--              group by order_date, SUB_UNIT_NUM_ID, tml_num_id
             ),

     old as (select h.BUSNO, h.ACCDATE, h.SALENO
             from t_sale_h h
                      join t_sale_d d on h.SALENO = d.SALENO
                      join t_ware_base w on d.WAREID = w.WAREID
                      left join s_busi s on h.BUSNO = s.BUSNO
             where s.busno in (select BUSNO from D_BP_BUSNO)
               and h.ACCDATE = trunc(sysdate)-1
               and not exists(select 1
                              from t_sale_pay p
                              where p.saleno = h.saleno and p.paytype in
                                                            ('Z022', 'Z025', 'Z027', 'Z030', 'Z032', 'Z034', 'Z077',
                                                             'Z081', 'Z098', 'Z100', 'Z101', 'Z084', 'Z102', 'Z107')
                                and p.netsum <> 0)
               and not exists(select 1 from T_SALE_RETURN_H th where th.SALENO=h.SALENO)
               and not exists(select 1 from T_SALE_RETURN_H th2 where th2.RETSALENO=h.SALENO)
               and not exists(select 1 from t_internal_sale_h ngd where SHIFTDATE>=date'2024-05-20' and ngd.NEWSALENO=h.SALENO)
               and not exists(select 1 from d_bp_exclude_sale exc where exc.SALENO=h.SALENO)
--              group by h.BUSNO, h.ACCDATE, h.SALENO
             ),
     new_hz as (select order_date, SUB_UNIT_NUM_ID, count(tml_num_id) sumsl
                from new
                group by order_date, SUB_UNIT_NUM_ID),
     old_hz as (select BUSNO, ACCDATE, count(SALENO) sumsl from old group by BUSNO, ACCDATE),
     re as (select bs.BUSNO,trunc(sysdate)-1 as ACCDATE, nvl(a.sumsl, 0) as 老系统销售单数, order_date, SUB_UNIT_NUM_ID,
                   nvl(b.sumsl, 0) as 新系统数量,
                   case
                       when nvl(a.sumsl, 0) = 0 then 0
                       else
                           case
                               when nvl(b.sumsl, 0) >= 50 then 1
                               else
                            case when  b.sumsl>a.sumsl then 1 else
                                   round(nvl(b.sumsl, 0) / a.sumsl, 3) end end end as bl
            from  D_BP_BUSNO bs
                     left join old_hz a on bs.BUSNO=a.BUSNO
                     left join new_hz b on substr(a.BUSNO, 2, 4) = b.SUB_UNIT_NUM_ID
                and a.ACCDATE = b.order_date),
--             order by a.BUSNO, a.ACCDATE)
hz as (
select q.ACCDATE as 日期,
       case when q.新系统数量<10 then 1 else 0 end as 低于10笔记录,
       case when q.新系统数量<50 then 1 else 0 end as 低于50笔记录,
       1 as 计入,
       tb2.CLASSNAME as 店型 , q.BUSNO as 业务机构编码, s.ORGNAME as 门店名称,tb.CLASSNAME as 事业部,tb1.CLASSNAME as 片区, q.老系统销售单数,
       q.新系统数量, q.bl as 录单比率
from re q
         left join s_busi s on q.BUSNO = s.BUSNO
         left join D_BP_BUSNO b on q.BUSNO=b.BUSNO
         join t_busno_class_set ts on q.busno=ts.busno and ts.classgroupno ='303'
         join t_busno_class_base tb on ts.classgroupno=tb.classgroupno and ts.classcode=tb.classcode
         join t_busno_class_set ts1 on q.busno=ts1.busno and ts1.classgroupno ='304'
         join t_busno_class_base tb1 on ts1.classgroupno=tb1.classgroupno and ts1.classcode=tb1.classcode
         join t_busno_class_set ts2 on q.busno=ts2.busno and ts2.classgroupno ='305'
         join t_busno_class_base tb2 on ts2.classgroupno=tb2.classgroupno and ts2.classcode=tb2.classcode)

select 日期,事业部,片区,sum(计入) as 机构数,
       sum(低于50笔记录) as 录单低于50笔机构数,sum(低于50笔记录)/sum(计入) as 录单低于50笔机构数占比,
       sum(低于10笔记录) as 录单低于10笔机构数,sum(低于10笔记录)/sum(计入) as 录单低于10笔机构数占比
from hz
group by 事业部,片区,日期
union all
select 日期,事业部,null,sum(计入) as 机构数,
       sum(低于50笔记录) as 录单低于50笔机构数,sum(低于50笔记录)/sum(计入) as 录单低于50笔机构数占比,
       sum(低于10笔记录) as 录单低于10笔机构数,sum(低于10笔记录)/sum(计入) as 录单低于10笔机构数占比
from hz
group by 事业部,日期