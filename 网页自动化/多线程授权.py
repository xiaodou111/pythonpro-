from datetime import datetime
import time
from threading import Thread

from DrissionPage import ChromiumPage
import re
import itertools

from DrissionPage._configs.chromium_options import ChromiumOptions


def qyautochick(page,username,password,env):
    try:
        # 定位到账号文本框，获取文本框元素
        ele = page.ele('#user')
        # # 输入对文本框输入账号
        ele.input(username)
        # # 定位到密码文本框并输入密码
        page.ele('#pwd').input(password)
        # # 点击登录按钮
        page.ele('#btn').click()
    except Exception as e:
        print('已登录,无需查找登陆元素')
    time.sleep(1)
    page.ele('@text()=药店通').click()
    page.ele('@text()=基础运维').click()
    page.ele('@text()=D908客户端授权管理').click()

    #
    # #页面中待授权的按钮数,先不用这个
    # # try:
    # #      authorizeds=page.eles('xpath://button[contains(@class,"el-button--small")]/span[text()="授权"]')
    # # except Exception as e:
    # #     print("没有待授权的终端")
    time.sleep(2)
    compchoice = page.ele('xpath://div[@label="公司编码"]//input[@class="el-input__inner"]',timeout=10)
    comlist = ['RT01', 'RD01', 'RX01', 'RZ41', 'TZ01', 'RP01', 'TX01', 'RZ31', 'RK01', 'RP51', 'RP41', 'RS01', 'RZ11',
               'RP11', 'RF01', 'RB01', 'RP21', 'RJ01', 'RZ01', 'RZ21', 'RP31', 'RH01']
    k = 1
    infinite_comlist = itertools.cycle(comlist)
    # for everycomp in comlist:
    #     compchoice.click()
    #     time.sleep(1)
    #     compchoice.input(everycomp)
    #     ac = Actions(page)
    #     ac.move_to(compchoice)

    try:
        while True:
            everycomp = next(infinite_comlist)
            time.sleep(1)
            compchoice.input(everycomp)
            try:
                xpath_expression = f'xpath://div[@class="el-select-dropdown el-popper"]//li[contains(@class,"el-select-dropdown__item")]/span[contains(text(), "{everycomp}")]'
                page.ele(xpath_expression).click()
                # page.ele('xpath://div[@class="el-select-dropdown el-popper"]//li[contains(@class,"el-select-dropdown__item")]/span[contains(text(), "RT01")]').click()
                # page.ele('//div[@class="el-select-dropdown el-popper"]//li[@class="el-select-dropdown__item selected hover"]').click()
                # page.ele('//div[@class="el-select-dropdown el-popper"]//li[@class="el-select-dropdown__item hover"]').click()
            except Exception as e:
                # print(f'{everycomp}:"找不到公司的下拉选项"')
                pass
            # page.ele('@@placeholder=el-range-input@@text()=开始日期').click()
            # page.ele('.el-range-input').click()
            page.ele('@@placeholder=开始日期@@class=el-range-input').click()
            page.ele('xpath://input[@class="el-range-input"]').click()
            # page.ele('xpath://div[@class="el-picker-panel__body"]//tr[@class="el-date-table__row"]//td[@class="available"]//span[text()=1]').click()
            # page.ele('xpath://div[@class="el-picker-panel__body"]//tr[@class="el-date-table__row"]//td[@class="available"]//span[text()=1]').click()
            # 左边日期available的第一个和右边日期available的最后一个
            page.eles(
                'xpath://div[@class="el-picker-panel__body"]/div[contains(@class,"is-left")]//tr[@class="el-date-table__row"]//td[contains(@class,"available")]//span')[
                0].click()
            page.eles(
                'xpath://div[@class="el-picker-panel__body"]/div[contains(@class,"is-right")]//tr[@class="el-date-table__row"]//td[contains(@class,"available")]//span')[
                -1].click()
            page.ele('xpath://span[@class="el-radio__label"][contains(text(), "待授权")]').click()
            page.ele('xpath://button[contains(@class,"el-button")]/span[text()="查询"]').click()

            time.sleep(1)
            # 一共多少条需要授权?
            span_element = page.ele('.el-pagination__total')

            # 获取元素的文本
            span_text = span_element.text
            # print(span_text)
            # 使用正则表达式提取数字
            number_pattern = r'共 (\d+) 条'
            match = re.search(number_pattern, span_text)
            # 确保找到了匹配项
            if match:
                number = int(match.group(1))
                if number>0:
                    print(f"环境:{env},公司:{everycomp}:需要授权: {number}次")

            else:
                print("未能找到匹配的数字")
            if number == 0:
                continue
            try:
                page.eles('xpath://button[contains(@class,"el-button--small")]/span[text()="授权"]')[0].click()
            except Exception as e:
                print(f'{everycomp}:"找不到授权元素"')
            for index in range(number):
                # print(f"第{index + 1}次授权")
                #只显示了第一行的设备名
                equipname=page.ele('xpath://tr[@class="el-table__row"]/td[contains(@class,"el-table_1_column_5")]').text
                now = datetime.now()
                print(f"{now}-正在给环境:{env},公司:{everycomp},设备:{equipname}进行授权")
                time.sleep(1)
                button_elements = page.eles('xpath://button[contains(@class,"el-button--small")]/span[text()="授权"]')
                if button_elements:
                    # print("正在进行授权")
                    button_elements[0].click()

                    # print("正在点击日期授权")
                    page.ele(
                        'xpath://input[@class="el-input__inner" and @placeholder="请选择" and not(@readonly)]').click()
                    # print("点击日期授权按钮完成")

                    try:
                         page.ele('@@type=button@@aria-label=后一年').click()
                    except Exception as e:
                        print("找不到下一年按钮")
                    # 查找日期为1号的获得了2个,只取第2个点击
                    time.sleep(1)
                    choose_date = page.eles(
                        'xpath://div[@class="el-picker-panel__body"]//tr[@class="el-date-table__row"]/td[@class="available"]//span[text()=1]')
                    # 点击报错“该元素没有位置及大小”怎么办？
                    # 没有位置及大小是正常的，很多元素都没有位置和大小。
                    # 这个时候你要检查是否页面中有同名元素，定位符没写准确拿到了另一个。
                    # 如果要点击的元素就是没有位置的，可以强制使用
                    # 点击，用法是.click(by_js=True)，可以简写为.click('js')。
                    try:
                        choose_date[0].click()
                    except Exception as e:
                        try:
                            choose_date[1].click()
                        except Exception as e:
                            try:
                                choose_date[2].click()
                            except Exception as e:
                                print("找不到元素")
                    page.ele('xpath://span[text()="提交"]').click()
                    k += 1
                    # print(f"本次共完成授权{k + 1}次")
                else:
                    print("未找到可点击的按钮")
    except KeyboardInterrupt:
        print("循环被用户中断")

# page = ChromiumPage(timeout=1)
# page1=page.get('https://portal-rrt.myquanyi.com/index.html')
# qyautochick(page)
co = ChromiumOptions().auto_port()
# 禁用保存密码提示气泡
co.set_pref('credentials_enable_service', False)
pages_data = [
    # {'url': 'https://portal-rrtuat.myquanyi.com/login.html', 'username': '10013898', 'password': '123321','env':'uat'},
    {'url': 'https://portal-rrt.myquanyi.com/index.html', 'username': '10013898', 'password': '123321','env':'prod'},
    # {'url': 'https://portal-rrtbeta.myquanyi.com/index.html', 'username': '9010', 'password': '123321','env':'beta'}
]
# 为每个页面启动一个新线程
threads = []
for data in pages_data:
    page = ChromiumPage(co, timeout=5)
    page.get(data['url'])
    thread = Thread(target=qyautochick, args=(page, data['username'], data['password'],data['env']))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()


