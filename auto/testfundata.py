from auto.datalink.datalink import get_rrt_mysql, get_qy_mysql, get_oracle_prod, get_oracle_zjcs

try:
    connection = get_qy_mysql()
    print("连接成功qy_mysql！")
except Exception as e:
    print(f"数据库连接失败：{e}")


try:
    connection = get_rrt_mysql()
    print("连接成功rrt_mysql！")
except Exception as e:
    print(f"数据库连接失败：{e}")

try:
    connection = get_oracle_prod()
    print("连接成功rrt_oracle_正式库！")
except Exception as e:
    print(f"数据库连接失败：{e}")

try:
    connection = get_oracle_zjcs()
    print("连接成功rrt_oracle_直连库！")
except Exception as e:
    print(f"数据库连接失败：{e}")