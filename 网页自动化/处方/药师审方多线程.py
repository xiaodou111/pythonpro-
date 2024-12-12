import datetime
import threading
import time
from threading import Thread

from DrissionPage import ChromiumPage
import re
import itertools

from DrissionPage._configs.chromium_options import ChromiumOptions


def yssf(username,password,port,env):
    co = ChromiumOptions().set_local_port(port)
    co.set_pref('credentials_enable_service', False)
    page = ChromiumPage(co, timeout=4)
    page.get("https://portal-rrt.myquanyi.com/index.html")
    if page.ele('#user'):
        ele = page.ele('#user')
        # # 输入对文本框输入账号
        ele.input(username)
        # # 定位到密码文本框并输入密码
        page.ele('#pwd').input(password)
        # # 点击登录按钮
        page.ele('#btn').click()
        time.sleep(8)
    page.ele('@text()=药店通', timeout=10).click()
    # time.sleep(3)
    page.ele('@text()=处方中心').click()
    # time.sleep(3)
    page.ele('@text()=D504处方总览').click()
    timechoice = page.ele('xpath://div//input[@class="el-input__inner" and @placeholder="请输入登记日期"]',
                          timeout=10).click()
    page.ele('xpath://tr[@class="el-date-table__row"]/td[@class="available today"]').click()
    # page.eles('x://tr[@class="el-date-table__row"]/td[contains(@class,"available")]')[0].click()
    # page.eles('xpath://div//input[@class="el-input__inner" and @placeholder="请输入登记日期"]', timeout=10)[1].click()
    # page.eles(
    #     'xpath://tr[@class="el-date-table__row"]/td[@class="available today"]')[1].click()
    statuschoice = page.ele('xpath://div//input[@placeholder="请输入当前状态"]').click()
    page.ele('xpath://span[text()="未审核"]').click()
    page.ele('xpath://button[@title="查询"]').click()
    time.sleep(2)
    # 一共多少条需要授权?
    span_element = page.ele('.el-pagination__total')
    # 获取元素的文本
    span_text = span_element.text
    print(span_text)
    # 使用正则表达式提取数字
    number_pattern = r'共 (\d+) 条'
    match = re.search(number_pattern, span_text)
    # 确保找到了匹配项
    if match:
        number = int(match.group(1))
        if number > 0:
            # print(f"环境:{env},:需要审核: {number}次")
            pass
    else:
        print("未能找到匹配的数字")
    shyss = page.eles('xpath://span[text()=" 审核 "]')
    element_count = len(shyss)
    print(f"本页共{element_count}个需要审核")
    page.ele('xpath://button[@title="查询"]').click()
    j = 0
    while True:
        page.ele('xpath://button[@title="查询"]').click()
        # buttonlist=[button1]
        # infinite_comlist = itertools.cycle(buttonlist)
        i = 0
        while i < 10:
            time.sleep(1)
            page.eles('xpath://span[text()=" 审核 "]', timeout=10)[i].click()
            # print(f"检查第{i}行是否有001")
            if page.ele('xpath://block/span[text()="001"]'):
                # print(f"第{i}行存在001")
                # picture=page.ele('xpath://block/span[text()="001"]')
                # print(picture.text)
                page.ele('xpath://span[text()="通过"]').click()
                page.ele('xpath://div[@class="dialog__body"]')
                # ac.scroll(delta_y=2000)
                time.sleep(4)
                page.ele('xpath://span[text()="签 名"]', timeout=10).click()
                time.sleep(1)
                page.ele('xpath://span[text()="通 过"]', timeout=10).click()
                time.sleep(2)
                #following-sibling获取下一个兄弟节点
                # if page.ele('xpath://div[@class="el-dialog__header"]/span[text()="处方签名"]/following-sibling::button[1]'):
                #     page.ele('xpath://div[@class="el-dialog__header"]/span[text()="处方签名"]/following-sibling::button[1]').click()

                j += 1
                print(f"{env}已通过{j}张处方")
                # print("已点击")
            else:
                page.eles(
                    'xpath://div[@class="el-dialog__header"]//button[@aria-label="Close"]/i[@class="el-dialog__close el-icon el-icon-close"]')[
                    1].click()
                time.sleep(1)
                i += 1

pages_data = [
    {'url': 'https://portal-rrt.myquanyi.com/index.html', 'username': '10004932', 'password': 'rrt1212#','env':'瑞人堂','port':'7836'},
    {'url': 'https://portal-rrt.myquanyi.com/index.html', 'username': '10020395', 'password': 'rrt1212#','env':'康康','port':'7837'},
    {'url': 'https://portal-rrt.myquanyi.com/index.html', 'username': '10001631', 'password': 'rrt1212#','env':'瑞人堂','port':'7838'},
]
# 为每个页面启动一个新线程
threads = []
for data in pages_data:
    thread = Thread(target=yssf, args=(data['username'], data['password'],data['port'],data['env']))
    threads.append(thread)
    thread.start()
# now = datetime.datetime.now()
# while now.hour >= 7 and now.hour <= 22:
#        try:
#            thread.start()
#        except Exception as e:
#           # page.quit()
#           print("出错了,正在重试")
#           time.sleep(2)
#           continue

# 主循环开始
# now = datetime.datetime.now()
# while now.hour >= 7 and now.hour <= 22:
while True:
    # 检查是否有线程尚未完成
    for index, thread in enumerate(threads):
        if not thread.is_alive():  # 如果线程已经完成
            try:
                # 尝试重新启动线程
                new_thread = threading.Thread(target=yssf, args=(
                pages_data[index]['username'], pages_data[index]['password'], pages_data[index]['port'],
                pages_data[index]['env']))
                threads[index] = new_thread
                new_thread.start()
            except Exception as e:
                print("出错了, 正在重试:", e)
                # 等待一段时间后再次尝试启动线程
                time.sleep(2)
                continue

    # 每次循环等待一段时间
    time.sleep(2)
    now = datetime.datetime.now()

# 等待所有线程完成
for thread in threads:
    thread.join()


# 等待所有线程完成
for thread in threads:
    thread.join()