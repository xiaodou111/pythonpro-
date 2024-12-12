import os
import schedule
import time

def run_script(script_name):
    script_path = f"./{script_name}"
    try:
        os.system(f"python {script_path}")
    except Exception as e:
        print(f"{script_name}运行失败")
# 每秒执行一次
schedule.every(20).seconds.do(run_script,'testtask.py')
# schedule.every().second.do(run_script,'testtask2.py')
#每天某个时间执行一次
# schedule.every().day.at("11:15").do(run_script,'postgre导入oracle.py')
# schedule.every().day.at("11:15").do(run_script,'testtask2.py')

while True:
    schedule.run_pending()
    time.sleep(1)



# schedule.every(10).minutes.do(job, name)
# schedule.every().hour.do(job, name)
# schedule.every().day.at("10:30").do(job, name)
# schedule.every(5).to(10).days.do(job, name)
# schedule.every().monday.do(job, name)
# schedule.every().wednesday.at("13:15").do(job, name)

# 每隔十分钟执行一次任务
# 每隔一小时执行一次任务
# 每天的10:30执行一次任务
# 每隔5到10天执行一次任务
# 每周一的这个时候执行一次任务
# 每周三13:15执行一次任务
# run_pending：运行所有可以运行的任务