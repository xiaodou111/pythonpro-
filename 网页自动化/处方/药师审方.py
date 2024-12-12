from datetime import datetime
import time
from threading import Thread

from DrissionPage import ChromiumPage
import re
import itertools

from DrissionPage._base import browser
from DrissionPage._configs.chromium_options import ChromiumOptions
from selenium.webdriver import ActionChains, Keys
from DrissionPage.common import Actions


def yaoshi(page,username,password,env):
    while True:
          try:
              if page.ele('#user'):

              # 定位到账号文本框，获取文本框元素
                   ele = page.ele('#user')
                   # # 输入对文本框输入账号
                   ele.input(username)
                   # # 定位到密码文本框并输入密码
                   page.ele('#pwd').input(password)
                   # # 点击登录按钮
                   page.ele('#btn').click()

          # time.sleep(5)
              page.ele('@text()=药店通',timeout=10).click()
              page.ele('@text()=处方中心').click()
              page.ele('@text()=D504处方总览').click()
              timechoice = page.ele('xpath://div//input[@class="el-input__inner" and @placeholder="请输入登记日期"]',timeout=10).click()
              page.ele(
                  'xpath://tr[@class="el-date-table__row"]/td[@class="available today"]').click()
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
                      print(f"环境:{env},:需要审核: {number}次")
              else:
                  print("未能找到匹配的数字")

              shyss=page.eles('xpath://span[text()=" 审核 "]')
              element_count=len(shyss)
              print(f"本页共{element_count}个需要审核")
              page.ele('xpath://button[@title="查询"]').click()

              j = 0

              while True:
                  page.ele('xpath://button[@title="查询"]').click()
              # buttonlist=[button1]
              # infinite_comlist = itertools.cycle(buttonlist)
                  i=0

                  while i<10:
                      time.sleep(1)
                      page.eles('xpath://span[text()=" 审核 "]',timeout=10)[i].click()
                      # print(f"检查第{i}行是否有001")
                      if page.ele('xpath://block/span[text()="001"]'):
                          # print(f"第{i}行存在001")
                          # picture=page.ele('xpath://block/span[text()="001"]')
                          # print(picture.text)
                          page.ele('xpath://span[text()="通过"]').click()
                          page.ele('xpath://div[@class="dialog__body"]')
                          ac.scroll(delta_y=2000)
                          time.sleep(2)

                          page.ele('xpath://span[text()="签 名"]',timeout=10).click()
                          time.sleep(1)
                          page.ele('xpath://span[text()="通 过"]',timeout=10).click()
                          j+=1
                          print(f"线程{env}已通过{j}张处方")
                          # print("已点击")
                      else:
                          page.eles('xpath://div[@class="el-dialog__header"]//button[@aria-label="Close"]/i[@class="el-dialog__close el-icon el-icon-close"]')[1].click()
                          time.sleep(1)
                          i+=1
          except Exception as e:
              time.sleep(5)
              ac.key_up('F5')
              continue




# li[@class="el-select-dropdown__item"]


co = ChromiumOptions().auto_port()

# 禁用保存密码提示气泡
co.set_pref('credentials_enable_service', False)
pages_data = [
    {'url': 'https://portal-rrt.myquanyi.com/index.html', 'username': '10004932', 'password': '123321','env':'Thread1'},
    {'url': 'https://portal-rrt.myquanyi.com/index.html', 'username': '10020395', 'password': '123321','env':'Thread2'},
    # {'url': 'https://portal-rrt.myquanyi.com/index.html', 'username': '10004932', 'password': '123321','env':'Thread3'},
]

threads = []
for data in pages_data:
    page = ChromiumPage(co, timeout=4)
    ac = Actions(page)
    page.get(data['url'])
    thread = Thread(target=yaoshi, args=(page, data['username'], data['password'],data['env']))
    threads.append(thread)
    thread.start()
# 等待所有线程完成
for thread in threads:
    thread.join()