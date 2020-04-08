from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class WeiboLogin():
    def __init__(self, username="0331_ee6ebc@163.com", password="cua633476"):
        self.url = "https://passport.weibo.cn/signin/login"
        # self.browser = webdriver.PhantomJS(executable_path=r"D:\迅雷下载\phantomjs-2.1.1-windows\bin\phantomjs.exe")    # 可编程的无头浏览器
        self.option = Options()
        self.option.add_argument("--headless")
        self.option.add_argument("--disable-gpu")
        self.browser = webdriver.Firefox(options=self.option)
        self.browser.set_window_size(1050,840)
        self.wait = WebDriverWait(self.browser,20)
        self.username = username
        self.password = password
        print("初始化完成")

    def open(self):
        '''
        打开网页输入用户名密码并点击
        :return:
        '''
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID,'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID,'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID,'loginAction')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()
    def run(self):
        '''
        破解入口
        :return:
        '''
        self.open()
        print("开始等待10秒")
        time.sleep(10)  # 等待10秒
        print('页面标题',self.browser.title)
        if "验证" in self.browser.title:
            # print(self.browser)
            print('当前页面的url',self.browser.current_url)
            f_test = self.browser.find_element_by_id('message-p')
            print("f_test",f_test.text)
            check_input = self.browser.find_element_by_class_name('geetest_radar_btn')
            print(check_input)
            check_input.click() # 点击
        WebDriverWait(self.browser,30).until(
            EC.title_is("微博")
        )
        cookies = self.browser.get_cookies()
        cookie = [item["name"] + "=" + item["value"] for item in cookies]
        cookie_str = '; '.join(item for item in cookie)
        self.browser.quit()
        return cookie_str

if __name__ == '__main__':
    # try:
    loginer = WeiboLogin()
    cookie_str = loginer.run()
    print('获取cookie成功')
    print('Cookie:', cookie_str)
    # except Exception as e:
    #     print(e)
