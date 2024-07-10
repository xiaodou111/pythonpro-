# WebPage是功能最全面的页面类，既可控制浏览器，也可收发数据包。
import time

from DrissionPage import WebPage
from DrissionPage import ChromiumPage
from DrissionPage.common import Actions
import re

from selenium.webdriver.support.wait import WebDriverWait

# 创建页面对象，并启动或接管浏览器
page = ChromiumPage(timeout=1)
# 跳转到登录页面
# page.get('https://portal-rrtuat.myquanyi.com/login.html')
page.get('https://portal-rrt.myquanyi.com/index.html')
try:
    # 定位到账号文本框，获取文本框元素
    ele = page.ele('#user')
    # # 输入对文本框输入账号
    ele.input('10013898')
    # # 定位到密码文本框并输入密码
    page.ele('#pwd').input('123321')
    # # 点击登录按钮
    page.ele('#btn').click()
except Exception as e:
    print('已登录,无需查找登陆元素')

page.ele('@text()=药店通').click()
page.ele('@text()=基础运维').click()
page.ele('@text()=D908客户端授权管理').click()

#
# #页面中待授权的按钮数,先不用这个
# # try:
# #      authorizeds=page.eles('xpath://button[contains(@class,"el-button--small")]/span[text()="授权"]')
# # except Exception as e:
# #     print("没有待授权的终端")
compchoice=page.ele('xpath://div[@label="公司编码"]//input[@class="el-input__inner"]')
comlist=['RT01','RD01','RX01','RZ41','TZ01','RP01','TX01','RZ31','RK01','RP51','RP41','RS01','RZ11','RP11','RF01','RB01','RP21','RJ01','RZ01','RZ21','RP31','RH01']
for everycomp in comlist:
    compchoice.click()
    time.sleep(1)
    compchoice.input(everycomp)
    ac = Actions(page)
    ac.move_to(compchoice)
    try:
        xpath_expression = f'xpath://div[@class="el-select-dropdown el-popper"]//li[contains(@class,"el-select-dropdown__item")]/span[contains(text(), "{everycomp}")]'
        page.ele(xpath_expression).click()
        # page.ele('xpath://div[@class="el-select-dropdown el-popper"]//li[contains(@class,"el-select-dropdown__item")]/span[contains(text(), "RT01")]').click()
        # page.ele('//div[@class="el-select-dropdown el-popper"]//li[@class="el-select-dropdown__item selected hover"]').click()
        # page.ele('//div[@class="el-select-dropdown el-popper"]//li[@class="el-select-dropdown__item hover"]').click()
    except Exception as e:
        print(f'{everycomp}:"找不到公司的下拉选项"')
    # page.ele('@@placeholder=el-range-input@@text()=开始日期').click()
    # page.ele('.el-range-input').click()
    page.ele('@@placeholder=开始日期@@class=el-range-input').click()
    page.ele('xpath://input[@class="el-range-input"]').click()
    # page.ele('xpath://div[@class="el-picker-panel__body"]//tr[@class="el-date-table__row"]//td[@class="available"]//span[text()=1]').click()
    # page.ele('xpath://div[@class="el-picker-panel__body"]//tr[@class="el-date-table__row"]//td[@class="available"]//span[text()=1]').click()
    #左边日期available的第一个和右边日期available的最后一个
    page.eles('xpath://div[@class="el-picker-panel__body"]/div[contains(@class,"is-left")]//tr[@class="el-date-table__row"]//td[contains(@class,"available")]//span')[0].click()
    page.eles('xpath://div[@class="el-picker-panel__body"]/div[contains(@class,"is-right")]//tr[@class="el-date-table__row"]//td[contains(@class,"available")]//span')[-1].click()
    page.ele('xpath://span[@class="el-radio__label"][contains(text(), "待授权")]').click()
    page.ele('xpath://button[contains(@class,"el-button")]/span[text()="查询"]').click()

    time.sleep(1)
    #一共多少条需要授权?
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
        print(f"{everycomp}:需要授权: {number}次")
    else:
        print("未能找到匹配的数字")
    if number==0:
        continue
    try:
        page.eles('xpath://button[contains(@class,"el-button--small")]/span[text()="授权"]')[0].click()
    except Exception as e:
        print(f'{everycomp}:"找不到授权元素"')
    for index in range(number):
        print(f"第{index+1}次授权")
        button_elements = page.eles('xpath://button[contains(@class,"el-button--small")]/span[text()="授权"]')
        if button_elements:
            print("正在进行授权")
            button_elements[0].click()
            page.ele('xpath://input[@class="el-input__inner" and @placeholder="请选择" and not(@readonly)]').click()
            page.ele('@@type=button@@aria-label=后一年').click()
            #查找日期为1号的获得了2个,只取第2个点击
            choose_date=page.eles('xpath://div[@class="el-picker-panel__body"]//tr[@class="el-date-table__row"]/td[@class="available"]//span[text()=1][1]')
            choose_date[0].click()
            page.ele('xpath://span[text()="提交"]').click()
        else:
            print("未找到可点击的按钮")
