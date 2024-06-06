from auto.datalink.datalink import get_rrt_mysql

try:
    connection = get_rrt_mysql()
    print("连接成功！")
except Exception as e:
    print(f"数据库连接失败：{e}")