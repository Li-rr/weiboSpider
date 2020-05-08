from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time
import re
import os,sys
sys.path.append('.\\')
from model import UserInfo,UserRealion
from mondbSql import *

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
        self.id_url = 'https://weibo.cn/'   # 用于访问用户首页
        self.follow_page_url = 'https://weibo.cn/{}/follow?page={}'  # 分别由uid和page填充
        self.fans_page_url = 'https://weibo.cn/{}/fans?page={}'  # 分别由uid和page填充
        self.uid = ""
        self.header = {
            # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
            # 'Cookie':"SUB=_2A25zsFjHDeRhGeFO7VcV9SfIzzuIHXVRW3iPrDV6PUJbkdANLUPwkW1NQU28Nmzjj5-mK3hYtRJbUBBOUJJ3vT12; SUHB=0oUYxaQY9Gtt95; SCF=AqTb-Z3_3pyUQpGZL6NHjz1tBCZnZ8jkAFXN8ZHOTbRLsAvL-4xnuH-E6UY9sOKfp7RnMpWgds_q-lkI9_FTvVc.; SSOLoginState=1588865175; _T_WM=35081461371; XSRF-TOKEN=0ef517; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode%3D20000174"
        }
        self.db_weibo, self.conn = connDB()  # 获取数据库连接与weibo数据库

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
        try:
            response = requests.get(url=url,headers=headers)
            if response.status_code == 200:
                return response.text
            else:
                print("错误状态码：{}".format(response.status_code))
                return ""
        except Exception as e:
            print(e)
            print("访问 {} 出错".format(url))
            return ""

    # 获取用户信息
    '''
    info = {'user_url_token': urltoken, 这里替换为user_id
    'user_data_json': infojson, 这里不需要替换
    'user_following_list': followinglist，获取关注列表
    }
    '''
    def getUserInfo(self,user_id):
        url_index_url = self.id_url + user_id
        print(url_index_url)
        headers = self.header

        # headers['Host'] = 'weibo.cn'
        print(headers)
        user_index_html = self.getHtmlText(url=url_index_url,headers=headers)
        if user_index_html != "":

            user_info = UserInfo()

            user_index_soup = BeautifulSoup(user_index_html,'lxml')
            # 获取uid
            uid = user_index_soup.find("td",attrs={'valign': 'top'}).a['href']
            uid = uid.split('/')[1]

            # 获取微博数量
            divMessage = user_index_soup.find('div', attrs={'class': 'tip2'})
            weiBoCount = divMessage.find('span').getText()
            weiBoCount = (weiBoCount.split('[')[1]).replace(']', '')

            # 获取关注数和粉丝数
            a = divMessage.find_all('a')[:2]
            followCount = (a[0].getText().split('[')[1]).replace(']', '')
            fansCount = (a[1].getText().split('[')[1]).replace(']', '')
            user_info.user_id = user_id
            user_info.user_uid = uid
            user_info.tweets_num = weiBoCount
            user_info.followers_num = followCount
            user_info.fans_num = fansCount
            self.uid = uid

            print("uid: {} 微博数量：{} 关注数：{} 粉丝数：{}".format(uid,weiBoCount,followCount,fansCount))
            # 获取完成后进入资料页面
            detailInfo_url = "/{}/info".format(uid)

            user_info_html = self.getHtmlText(url=self.id_url+detailInfo_url,headers=self.header)
            if user_info_html != "":
                print(user_info_html)
                user_info_html = user_info_html.replace("<br>","").replace("<br/>","")
                user_info_soup = BeautifulSoup(user_info_html,'lxml')

                body = user_info_soup.find('body')
                tip_element = body.find_all_next(name='div', attrs={"class": "c"})

                result = re.findall(r'会员等级：([0-9]+)级', str(tip_element))
                user_info.vip_level = result[0] if len(result) > 0 else 0
                nickname = re.findall(r'昵称.*?(?=[认证|性别])', str(tip_element))
                sex_str = re.findall(r'性别.*?(?=地区)', str(tip_element))

                user_info.nick_name = nickname[0][3:] if len(nickname) > 0 else ""  # 加判断
                #print(sex_str)
                user_info.gender = sex_str[0][3:]
                area = re.findall(r'地区.*?(?=[生日|简介]|$)', str(tip_element))
                area_split = re.split(r"[: ]", area[0])
                if len(area_split) == 3:
                    user_info.province = area_split[1]
                    user_info.city = area_split[2]
                elif len(area_split) == 2:
                    user_info.province = area_split[1]
                label = re.findall(r'标签.*', str(tip_element))
                if len(label) > 1:
                    label_list = re.split(r"[: \xa0]", label[0])
                    if len(label_list) == 5:
                        user_info.label = " ".join(label_list[1:-1])
                    elif len(label_list) > 1 and len(label_list) < 5:
                        user_info.label = " ".join(label_list[1:])
                # print(label) # 获取标签有点问题
                personal_url = re.findall(r'手机版.*?(?=[他|她|我]的相册|<a)', str(tip_element))
                user_info.person_url = personal_url[0][4:]
                user_info.userPrint()
                insertDataToUserInfo(self.db_weibo,user_info.getDict())
            else:
                print("访问 {} 页面失败，返回为空".format(  ))

            # 开始获取用户关注或粉丝。。。。。。。。。。。
            divMessage = user_index_soup.find('div',attrs={'class':'tip2'})
            aa = divMessage.find_all('a')
            followUrl = self.id_url + aa[0].get('href')
            fansUrl = self.id_url + aa[1].get('href')

            user_id_list = self.getUserFollowAndFans(fans_or_follow_url=fansUrl,flag="关注",cur_id=user_info.user_id,cur_name=user_info.nick_name)
            print("粉丝或关注数量：{}".format(len(user_id_list)))
            info = {
                'user_id': user_id,
                'user_following_list': user_id_list
            }
        else:
            print("访问 {} 页面失败，返回为空".format(url_index_url))
            info = {
                'user_id':user_id,
                'user_following_list':[]
            }
        return info


    def getUserFollowAndFans(self,fans_or_follow_url=None,flag=None,cur_id=None,cur_name=None):
        '''
        获取关注或者粉丝的链接
        :param fans_or_follow_url:
        :param flag: 用于标识现在爬取的是粉丝还是关注
        :return:
        '''
        fans_or_follow_html = self.getHtmlText(url=fans_or_follow_url,
                                               headers=self.header)

        soup = BeautifulSoup(fans_or_follow_html,'lxml')

        # 获取页码
        try:
            pageSize = soup.find('div', attrs={"id": "pagelist"})
            pageSize = pageSize.find('div').getText()
            pageSize = pageSize.split("/")[1].split('页')[0]
        except Exception as e:
            print(e)
            pageSize = 1
        print('页码数 {}'.format(pageSize))

        user_id_list = [] # 存储爬取到的关注或粉丝的ID
        # 遍历 fans or follow 页面
        for page_index in range(1,int(pageSize) + 1):
            if flag == "关注":
                page_url = self.follow_page_url.format(self.uid, page_index)
            elif flag == "粉丝":
                page_url = self.fans_page_url.format(self.uid, page_index)

            # print("page url", page_url)

            header = self.header
            header['Host'] = 'weibo.cn'
            fans_or_follow_page = self.getHtmlText(url=page_url,headers=self.header)
            # 使用BeautifulSoup解析网页的HTML
            if fans_or_follow_page != "":
                fans_or_follow_page = fans_or_follow_page.replace('<br>', '')
                soup = BeautifulSoup(fans_or_follow_page,'lxml')
                body = soup.find('body')
                table_all = body.find_all_next('table')
                for t_num, table in enumerate(table_all):
                    need_content = table.find_all("td", attrs={"valign": "top"})
                    need_content = need_content[1]
                    user_realtion = UserRealion()
                    # print("len(need_content)", len(need_content))
                    # print(need_content)
                    userName = need_content.contents[0].getText()
                    id_url = need_content.contents[0].get("href")
                    cur_follow_id = id_url.split("/")[-1]
                    # print("用户名 {} id {}".format(userName,cur_follow_id))
                    user_realtion.reation = flag
                    user_id_list.append(cur_follow_id)
                    if flag == "关注":
                        user_realtion.son_name = cur_name
                        user_realtion.son_id = cur_id
                        user_realtion.father_name = userName
                        user_realtion.father_id = cur_follow_id
                        # 插入数据
                        insertDataToUserRealtion(self.db_weibo,user_realtion.getDict())

            else:
                print("访问 {} 页面失败，返回为空".format(page_url))


        return user_id_list




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
    close(crawl_obj.conn)