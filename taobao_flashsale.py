import datetime
import pyttsx3
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

'''
购物车标识（ID）：J_CartSwitch
结算按钮（ID）：J_SmallSubmit
六位支付密码框（CLASS_NAME）：sixDigitPassword
确认付款按钮（ID）：J_authSubmit
'''

# 初始化语音播报
speak = pyttsx3.init()


# 登录检测函数
def detect_login():
    flag = False
    try:
        shopping_cart = driver.find_element(By.ID, "J_CartSwitch").text == "购物车（全部）"
        flag = True
        return flag
    except exceptions.NoSuchElementException:
        return flag


# 下单and付款函数
def buy(buy_time):
    # 秒杀开始时间
    end_time = datetime.datetime.strptime(buy_time, '%Y-%m-%d %H:%M:%S.%f')
    # 监听当前北京时间与秒杀开始时间的区间
    while True:
        if (end_time - datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                                                  '%Y-%m-%d %H:%M:%S.%f')).seconds <= 0.5:
            # 开始秒杀
            try:
                driver.find_element(By.ID, "J_SmallSubmit").click()
                # 检测下单页面
                while True:
                    try:
                        # 预付款
                        driver.find_element(By.CLASS_NAME, "go-btn").click()
                        print("下单成功！")
                        break
                    except exceptions.NoSuchElementException:
                        print("下单页面未加载完成？")

                # 检测交易页面
                while True:
                    try:
                        # 输入交易密码，更改最后一位数字即可
                        driver.find_element(By.CLASS_NAME, "sixDigitPassword").send_keys(Keys.NUMPAD6)
                        driver.find_element(By.CLASS_NAME, "sixDigitPassword").send_keys(Keys.NUMPAD5)
                        driver.find_element(By.CLASS_NAME, "sixDigitPassword").send_keys(Keys.NUMPAD4)
                        driver.find_element(By.CLASS_NAME, "sixDigitPassword").send_keys(Keys.NUMPAD3)
                        driver.find_element(By.CLASS_NAME, "sixDigitPassword").send_keys(Keys.NUMPAD2)
                        driver.find_element(By.CLASS_NAME, "sixDigitPassword").send_keys(Keys.NUMPAD1)
                        print("密码输入成功！")
                        # 确认付款
                        driver.find_element(By.ID, "J_authSubmit").click()
                        print("付款中...")
                        break
                    except exceptions.NoSuchElementException:
                        print("交易页面未加载完成？")

                time2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                print("付款成功，付款成功的时间为" + time2)
                speak.say("付款成功，付款成功的时间为" + time2)
                speak.runAndWait()
                break
            except exceptions:
                speak.say("结算时发生错误，请检查！")
                speak.runAndWait()
                raise
        # 显示距离秒杀开始时间还有多少秒
        else:
            current_time = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                                                      '%Y-%m-%d %H:%M:%S.%f')
            date = str((end_time - current_time).seconds)
            print("距离结算还有 " + date + " 秒！")


# 主方法
if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("https://cart.taobao.com/cart.htm")  # 会自动阻塞程序
    # 判断是否登录
    login_flag = True
    while True:
        if login_flag:
            if detect_login():
                print("检测到已经登录！")
                speak.say("检测到已经登录")
                speak.runAndWait()
                break
            else:
                print("您还没有登录，请先扫码登录！")
                driver.find_element(By.CLASS_NAME, "icon-qrcode").click()
                speak.say("您还没有登录，请先扫码登录")
                speak.runAndWait()
                login_flag = False
        else:
            if detect_login():
                print("登录成功，请选择需要秒杀的商品！")
                speak.say("登录成功，请选择需要秒杀的商品")
                speak.runAndWait()
                break
    time1 = datetime.datetime.now().strftime('%H:%M:%S')
    print("当前时间：" + time1)
    speak.say("当前时间：" + time1)
    speak.runAndWait()
    buy("2022-08-20 14:06:30.00")





