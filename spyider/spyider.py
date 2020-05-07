from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time


class Crawl:
    def __init__(self, username="13885842844", password="5762nnxc"):
        self.option = Options()
        self.option.add_argument("--headless")
        self.option.add_argument("--disable-gpu")
        self.browser = webdriver.Firefox()
        # self.browser.set_window_size(1050, 840)
        self.timeout = 30  # 设置超时时间
        self.wait = WebDriverWait(self.browser, self.timeout)

        self.username = username
        self.password = password
        self.index_url = 'https://passport.weibo.cn/signin/login'  # 登录页面
        self.id_url = 'https://weibo.cn/'
        self.header = {
            # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
            # 'Cookie':"SUB=_2A25zsFjHDeRhGeFO7VcV9SfIzzuIHXVRW3iPrDV6PUJbkdANLUPwkW1NQU28Nmzjj5-mK3hYtRJbUBBOUJJ3vT12; SUHB=0oUYxaQY9Gtt95; SCF=AqTb-Z3_3pyUQpGZL6NHjz1tBCZnZ8jkAFXN8ZHOTbRLsAvL-4xnuH-E6UY9sOKfp7RnMpWgds_q-lkI9_FTvVc.; SSOLoginState=1588865175; _T_WM=35081461371; XSRF-TOKEN=0ef517; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode%3D20000174"
        }

    def setCookies(self,cookie):

        self.header['Cookie'] = cookie
        print(cookie)
        print("设置cookie成功")

    def open(self):
        '''
        登录首页
        :return:
        '''
        self.browser.get(self.index_url)

        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

    def getCookies(self):
        '''
        获取cookie
        :return:
        '''
        self.open()
        try:
            WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "geetest_radar_tip"))
            )
            check_input = self.browser.find_element_by_class_name('geetest_radar_tip')
            check_input.click()  # 点击
        except:
            print("验证失败")

        try:
            WebDriverWait(self.browser, self.timeout).until(
                EC.title_is("微博")
            )

            self.browser.get(url='https://weibo.cn/')
            WebDriverWait(self.browser, self.timeout).until(
                EC.title_is("我的首页")
            )
            cookies = self.browser.get_cookies()
            print(cookies)
            cookie = [item["name"] + "=" + item["value"] for item in cookies]
            cookie_str = '; '.join(item for item in cookie)
        except:
            print("cookie获取失败")

        return cookie_str

    def visitUserIndex(self, cookieStr):
        '''
        访问用户首页
        :return:
        '''
        print(cookieStr)

    def getHtmlText(self,url=None,headers=None):
        #try:
        response = requests.get(url=url,headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print("错误状态码：{}".format(response.status_code))
            return ""
        # except Exception as e:
        #     print(e)
        #     return ""
    def getUserInfo(self,user_id):
        url = self.id_url + user_id
        print(url)
        headers = self.header

        # headers['Host'] = 'weibo.cn'
        print(headers)
        html_text = self.getHtmlText(url=url,headers=headers)
        if html_text != None:
            print(html_text)

if __name__ == '__main__':
    crawl_obj = Crawl()
    cook_str = crawl_obj.getCookies()
    # cook_str = "SUB=_2A25zsEF-DeRhGeFO7VcV9SfIzzuIHXVRW282rDV6PUJbkdANLUb1kW1NQU28Nmu8nu8lNILCoEDXqEDPwr8M0dEY; " \
    #            "SUHB=0JvQYbmuFHgJl1; " \
    #            "SCF=AhP8IVmn0ig_4nWChRDHge9SR6TO8Wgb23bs-cRykJXU8hbXnhUpjFygPsA3dXI3gZDdYIDDsOD6ZkFv5bUNYno.; " \
    #            "SSOLoginState=1588867374; " \
    #            "_T_WM=66472165284; " \
    #            "MLOGIN=1; " \
    #            "WEIBOCN_FROM=1110106030; " \
    #            "M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174"
    crawl_obj.setCookies(cook_str)
    crawl_obj.getUserInfo('usembassy')

'''
SCF=AhP8IVmn0ig_4nWChRDHge9SR6TO8Wgb23bs-cRykJXU8hbXnhUpjFygPsA3dXI3gZDdYIDDsOD6ZkFv5bUNYno.; 
_T_WM=66472165284; 
MLOGIN=1; 
SUB=_2A25zsEWCDeRhGeFO7VcV9SfIzzuIHXVRW2vKrDV6PUJbkdAKLUr8kW1NQU28NilO4FGNBZ2gCKbCQD0MKKL3jkHN; 
SUHB=0h15m3yEboA8ye; 
SSOLoginState=1588868562; 
WEIBOCN_FROM=1110006030; 
M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174
'''