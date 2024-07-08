# WebPage是功能最全面的页面类，既可控制浏览器，也可收发数据包。
from DrissionPage import WebPage
from DrissionPage import ChromiumPage
import re
# 创建页面对象，并启动或接管浏览器
page = ChromiumPage()
# 跳转到登录页面
page.get('https://portal-rrtuat.myquanyi.com/login.html')
page.get('https://portal-rrt.myquanyi.com/index.html')


# 定位到账号文本框，获取文本框元素
ele = page.ele('#user')
# 输入对文本框输入账号
ele.input('10013898')
# 定位到密码文本框并输入密码
page.ele('#pwd').input('123321')
# 点击登录按钮
page.ele('#btn').click()
page.ele('@text()=药店通').click()
page.ele('@text()=基础运维').click()
page.ele('@text()=D908客户端授权管理').click()
# page.ele('@@placeholder=el-range-input@@text()=开始日期').click()
# page.ele('.el-range-input').click()
page.ele('@@placeholder=开始日期@@class=el-range-input').click()
page.ele('xpath://input[@class="el-range-input"]').click()
page.ele('xpath://div[@class="el-picker-panel__body"]//tr[@class="el-date-table__row"]//td[@class="available"]//span[1]').click()
page.ele('xpath://div[@class="el-picker-panel__body"]//tr[@class="el-date-table__row"]//td[@class="available"]//span[text()=31]').click()
# 获取文本带空格的元素 两种方式
# page.ele('xpath://span[@class="el-radio__label"][text()=" 待授权 "]').click()
page.ele('xpath://span[@class="el-radio__label"][contains(text(), "待授权")]').click()
#----
page.ele('xpath://button[contains(@class,"el-button")]/span[text()="查询"]').click()

page.ele('@@type=text@@placeholder=请选择@@class=el-input__inner').click()

#页面中待授权的按钮数,先不用这个
# try:
#      authorizeds=page.eles('xpath://button[contains(@class,"el-button--small")]/span[text()="授权"]')
# except Exception as e:
#     print("没有待授权的终端")
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
    print(f"需要授权: {number}次")
else:
    print("未能找到匹配的数字")
# print(f"总条数: {number}")
for index in range(number):
    print(f"第{index+1}次授权")
    button_elements = page.eles('xpath://button[contains(@class,"el-button--small")]/span[text()="授权"]')
    if button_elements:
        button_elements[0].click()
        page.ele('xpath://input[@class="el-input__inner" and @placeholder="请选择" and not(@readonly)]').click()
        page.ele('@@type=button@@aria-label=后一年').click()
        #查找日期为1号的获得了2个,只取第2个点击
        choose_date=page.eles('xpath://div[@class="el-picker-panel__body"]//tr[@class="el-date-table__row"]/td[@class="available"]//span[text()=1][1]')
        choose_date[1].click()
        page.ele('xpath://span[text()="提交"]').click()
    else:
        print("未找到可点击的按钮")

# page.eles('xpath://button[contains(@class,"el-button--small")]/span[text()="授权"]')[0].click()

# page.ele('xpath://input[@class="el-input__inner" and @placeholder="请选择" and not(@readonly)]').click()
# page.ele('@@type=button@@aria-label=后一年').click()
# #查找日期为1号的获得了三个,只取第三个点击
# choose_date=page.eles('xpath://div[@class="el-picker-panel__body"]//tr[@class="el-date-table__row"]/td[@class="available"]//span[text()=1][1]')
# choose_date[2].click()
# for  span in choose_date:
#     print(f"Processing span element #{span }")
    # 在这里进行你需要的操作，例如点击
#     span.click()
# print(len(choose_date))
# //input[@class='el-input__inner' and @placeholder='请选择' and not(@readonly)]
# <button type="button" aria-label="后一年" class="el-picker-panel__icon-btn el-date-picker__next-btn el-icon-d-arrow-right"></button>
# <input type="text" autocomplete="off" name="" placeholder="请选择" class="el-input__inner">
# page.ele('@@class=el-radio__label@@text()=待授权').click()
# class="el-radio__label
# //span[@class="el-radio__label" and text()=" 待申请 "

#XPath
# ('//tr[@class="el-date-table__row"]/td[@class="available"]/span')
# page.ele('@@placeholder=开始日期@@class=el-range-input').click()
# //li/p[@class="name"]
# page.ele('@class=el-date-table__row').click()
# element = page.ele('tr.el-date-table__row td.available span').click()
# element = page.ele('div.el-date-table__row td span:contains("1")')

# <td class="available in-range start-date" uia-uid="535|2"><div><span>
#           1
#         </span></div></td>
# placeholder="开始日期"
# 取 <tr class="el-date-table__row">下的<td class="available"> 下的<span>1</span>元素