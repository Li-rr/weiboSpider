from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from mondbSql import *
import time
import re
import queue
import sys


class WeiboUser:
    def __init__(self, parent="", son=""):
        self.userName = ""  # 用户名
        self.id = ""  # 用于访问用户微博首页的id
        self.uid = ""  # uid可以用于关注列表，评论列表等
        self.fansNum = ""  # 粉丝数
        self.parentUser = parent
        self.sonUser = son

    def print(self):
        print("用户名：{} id: {} uid: {} 粉丝数：{} 父微博：{} 子微博：{}"
              .format(self.userName, self.id, self.uid, self.fansNum, self.parentUser, self.sonUser))

    # 转换为数据库存储格式的数据
    def to_db_data(self):
        follow_fans_dict = {}
        follow_fans_dict['userName'] = self.userName
        follow_fans_dict['id'] = self.id
        follow_fans_dict['fansNum'] = self.fansNum
        follow_fans_dict['parentUser'] = self.parentUser
        follow_fans_dict['sonUser'] = self.sonUser
        return follow_fans_dict


class WeiboLogin():
    def __init__(self, username="0331_ee6ebc@163.com", password="cua633476"):
        self.url = "https://passport.weibo.cn/signin/login"
        # self.browser = webdriver.PhantomJS(executable_path=r"D:\迅雷下载\phantomjs-2.1.1-windows\bin\phantomjs.exe")    # 可编程的无头浏览器
        self.option = Options()
        self.option.add_argument("--headless")
        self.option.add_argument("--disable-gpu")
        self.browser = webdriver.Firefox()
        self.browser.set_window_size(1050, 840)
        self.wait = WebDriverWait(self.browser, 20)
        self.username = username
        self.password = password
        self.uids = ['1743951792']  # 美国大使馆的uid
        self.uid = ""
        self.ids = ['usembassy']  # 美国驻华大使馆的id
        self.seeds = ['usembassy']  # 用于bfs遍历的种子
        self.follow_url = ""  # 关注的人
        self.fans_url = ""  # 关注他的人

        self.id_url = 'http://weibo.cn/'
        self.page_url = 'http://weibo.cn/{}?page={}'
        self.follow_page_url = 'http://weibo.cn/{}/follow?page={}'  # 分别由uid和page填充
        self.fans_page_url = 'http://weibo.cn/{}/fans?page={}'  # 分别由uid和page填充

        self.db_weibo, self.conn = connDB()  # 获取数据库连接与weibo数据库
        print("初始化完成")

    def open(self):
        '''
        打开网页输入用户名密码并点击
        :return:
        '''
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

    def getCookies(self):
        '''
        破解入口
        :return:
        '''
        self.open()

        try:
            WebDriverWait(self.browser, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "geetest_radar_tip"))
            )
            print('当前页面的url', self.browser.current_url)
            f_test = self.browser.find_element_by_id('message-p')
            print("f_test", f_test.text)
            check_input = self.browser.find_element_by_class_name('geetest_radar_tip')
            check_input.click()  # 点击
            print("按钮点击验证完成")
        except Exception as e:
            print("验证失败")
            print(e)

        try:
            WebDriverWait(self.browser, 30).until(
                EC.title_is("微博")
            )

            cookies = self.browser.get_cookies()
            print(cookies)
            cookie = [item["name"] + "=" + item["value"] for item in cookies]
            cookie_str = '; '.join(item for item in cookie)
            # self.browser.quit()
        except Exception as e:
            print("获取cooie失败")
            print(e)
        return cookie_str

    def getUserInfoAndWeibo(self):
        for id in self.ids:
            id_url = self.id_url + id
            print(id_url)
            self.browser.get(id_url)
            # try:
            WebDriverWait(self.browser, 3).until(
                EC.title_is("美国驻华大使馆的微博")
            )
            # 使用BeautifulSoup解析网页的HTML
            soup = BeautifulSoup(self.browser.page_source, 'lxml')

            # 获取uid
            uid = soup.find('td', attrs={'valign': 'top'})
            uid = uid.a['href']
            uid = uid.split('/')[1]
            self.uid = uid

            # 爬取最大页码数目
            pageSize = soup.find('div', attrs={'id': 'pagelist'})
            pageSize = pageSize.find('div').getText()
            pageSize = (pageSize.split('/')[1]).split('页')[0]

            # 爬取微博数量
            divMessage = soup.find('div', attrs={'class': 'tip2'})
            weiBoCount = divMessage.find('span').getText()
            weiBoCount = (weiBoCount.split('[')[1]).replace(']', '')

            aa = divMessage.find_all('a')
            for a in aa:
                a_text = a.getText()
                print(a_text, type(a_text))
                if "关注" in a_text:
                    self.follow_url = self.id_url + a.get("href")
                    print(self.follow_url)
                    # 爬取关注
                    self.getFollowAndFans(cur_weibo_user=id, flag="关注")
                elif "粉丝" in a_text:
                    self.fans_url = self.id_url + a.get("href")
                    # 爬取粉丝
                    self.getFollowAndFans(cur_weibo_user=id, flag="粉丝")
                    print(self.fans_url)

            print("开始爬取全文内容")
            # 爬取微博数量
            divMessage = soup.find('div', attrs={'class': 'tip2'})
            weiBoCount = divMessage.find('span').getText()
            weiBoCount = (weiBoCount.split('[')[1]).replace(']', '')
            # 爬取关注数量和粉丝数量
            a = divMessage.find_all('a')[:2]
            guanZhuCount = (a[0].getText().split('[')[1]).replace(']', '')
            fenSiCount = (a[1].getText().split('[')[1]).replace(']', '')
            print("最大页码 {} 微博数量 {} 粉丝数量 {} 关注数量 {}".format(pageSize, weiBoCount, fenSiCount, guanZhuCount))
            count = 0
            for page_index in range(1, int(pageSize)):
                break
                page_url = self.page_url.format(id, page_index)
                print('page_url', page_url)
                self.browser.get(page_url)
                time.sleep(1)
                # 使用BeautifulSoup解析网页的HTML
                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                body = soup.find('body')
                # 具体的数值可通过页面查看
                div_all = body.find_all_next('div', attrs={'class': 'c'})[1:-2]
                for divs in div_all:  # 当前微博的divs包含了很多div
                    # yuanChuang : 0表示转发，1表示原创
                    yuanChuang = '1'  # 初始值为原创，当非原创时，更改此值
                    div = divs.find_all("div")
                    content = dianZhan = zhuanFa = pinLun = laiYuan = faBuTime = ""

                    # 优化代码逻辑
                    div_num = len(div)  # 0为原创无图，1为原创有图，2为转载
                    print("该条微博ID", div[0].parent.get("id"))  # 通过获取父元素来获取id
                    content_elem = div[0].find('span', attrs={'class': 'ctt'})  # 获取内容元素
                    full_url = None  # 如果有全文链接，则用来保存全文链接
                    for full_url in content_elem: pass
                    if len(full_url.string) == 2:
                        try:
                            f_url = full_url.get("href")
                            content = self.getFullContent(f_url)
                        except Exception as e:
                            print("获取全文微博失败")
                    else:
                        content = div[0].find('span', attrs={'class': 'ctt'}).getText()

                    aa = div[div_num - 1].find_all("a")  # 用来获取点赞，转发，评论数
                    for a in aa:
                        text = a.getText()
                        if "赞" in text:
                            dianZhan = (text.split('[')[1]).replace(']', '')
                        elif "转发" in text:
                            zhuanFa = (text.split('[')[1]).replace(']', '')
                        elif "评论" in text:
                            pinLun = (text.split('[')[1]).replace(']', '')
                    # 获取来源和时间
                    span = divs.find("span", attrs={'class': "ct"}).getText()
                    span_split = span.split("来自")
                    faBuTime = str(span_split[0])
                    laiYuan = span_split[1] if len(span_split) == 2 else "无"
                    weibo_id = div[0].parent.get("id")

                    print("微博ID {} 微博内容 {} \n 赞 {} 转发 {} 评论 {} 来源 {} 时间 {}".
                          format(weibo_id, content, dianZhan, zhuanFa, pinLun, laiYuan, faBuTime, ))
                    print()

                break

    def getFullContent(self, spec_url):
        '''
        获取微博全文
        :param spec_url: 指定微博的url
        :return:
        '''
        print("进入获取全文函数")
        f_url = self.id_url + spec_url
        print('拼接后的url', f_url)
        self.browser.get(f_url)
        try:
            WebDriverWait(self.browser, 3).until(
                EC.title_is("评论列表")
            )
            c_soup = BeautifulSoup(self.browser.page_source, 'lxml')
            c_content_divs = c_soup.find('div', attrs={'id': 'M_'})
            c_content_elem = c_content_divs.find('span', attrs={"class": "ctt"})  # 获取内容元素
            # print("全文内容", c_content_elem.getText())
            # print('div lens', len(c_content_divs))
            # print(c_content_divs[0])
            print("离开获取全文函数")
            return c_content_elem.getText()
        except Exception as e:
            print("在getfull函数中失败", e)

        # sys.exit(0)

    def getFollowAndFans(self, cur_weibo_user, flag):
        print("进入获取follow函数")

        if flag == "关注":
            self.browser.get(self.follow_url)  # 打开follow页面
            WebDriverWait(self.browser, 3).until(
                EC.title_is("美国驻华大使馆关注的人")
            )
        elif flag == "粉丝":
            self.browser.get(self.fans_url)  # 打开fans页面
            WebDriverWait(self.browser, 3).until(
                EC.title_is("美国驻华大使馆的粉丝")
            )

        soup = BeautifulSoup(self.browser.page_source, 'lxml')

        # 获取follow or fans 页码
        pageSize = soup.find('div', attrs={"id": "pagelist"})
        pageSize = pageSize.find('div').getText()
        pageSize = pageSize.split("/")[1].split('页')[0]
        print(pageSize)

        # 遍历 fans or follow 页面
        for page_index in range(1, int(pageSize) + 1):
            if flag == "关注":
                page_url = self.follow_page_url.format(self.uid, page_index)
            elif flag == "粉丝":
                page_url = self.fans_page_url.format(self.uid, page_index)
            print("page url", page_url)
            self.browser.get(page_url)
            time.sleep(1)

            # 使用BeautifulSoup解析网页的HTML
            html_doc = self.browser.page_source
            print("--")
            print(html_doc)
            new_html = (html_doc.replace('<br>', ''))
            soup = BeautifulSoup(new_html, 'lxml')
            body = soup.find('body')
            table_all = body.find_all_next('table')
            for t_num, table in enumerate(table_all):
                print(type(table))
                print("=====================")

                need_content = table.find_all("td", attrs={"valign": "top"})
                print("need_content的数量 {}".format(len(need_content)))
                need_content = need_content[1]
                # 创建用户保存数据
                if flag == "关注":
                    user = WeiboUser(parent="", son=cur_weibo_user)  # 当前微博用户作为儿子
                elif flag == "粉丝":
                    user = WeiboUser(parent=cur_weibo_user, son="")
                print("len(need_content)", len(need_content))
                for i, temp_element in enumerate(need_content):
                    if "Tag" in str(type(temp_element)):
                        if i == 0:
                            user.userName = temp_element.getText()
                            id_url = temp_element.get("href")
                            temp_element = str(temp_element)

                            user.id = id_url.split("/")[-1]
                            # print("url",id_url.split("/"))
                        if flag == "关注":
                            if i == 3:
                                temp_element = str(temp_element)
                                user.uid = re.split(r'[? = &]', temp_element)[4]
                                print("===>", re.split(r'[? = &]', temp_element))
                        elif flag == "粉丝":
                            if i == 2:
                                temp_element = str(temp_element)
                                user.uid = re.split(r'[? = &]', temp_element)[4]
                                print("--->", re.split(r'[? = &]', temp_element))
                    else:
                        user.fansNum = temp_element.string
                        # print(user.fansNum)
                    # print("->",temp_element)
                    # print("==>",type(temp_element))
                user.print()
                # 向数据库中插入数据
                insertDataToFollowFansGraph(self.db_weibo, user.to_db_data())
            #     if t_num == 1:
            #         break
            # break
        print("离开获取follow函数")

    def bfs(self, choice=1):
        '''
        基于深度优先遍历，层序遍历粉丝
        :param choice: 用于选择遍历粉丝还是关注，1：为粉丝；2：为关注
        :return:
        '''

        # 从开始节点开始遍历
        for seed in self.seeds:

            crawl_queue = queue.Queue()  # 待访问队列
            crawl_visited = set()  # 已访问列表

            # 用于判断层数
            last = seed
            tail = ""
            layer = 0

            # 种子入队
            crawl_queue.put(seed)

            while not crawl_queue.empty():

                cur_node = crawl_queue.get()    # 获取节点
                id_url = self.id_url + cur_node  # 用于访问用户首页
                print("cur_node {}".format(cur_node))

                self.browser.get(id_url)  # 访问用户首页
                WebDriverWait(self.browser, 3).until(
                    EC.title_is("美国驻华大使馆的微博")  # 这里可以修改成列表存储的形式
                )
                # 使用BeautifulSoup解析网页的HTML
                soup = BeautifulSoup(self.browser.page_source, 'lxml')

                # 获取uid
                uid = soup.find('td', attrs={'valign': 'top'})
                uid = uid.a['href']
                uid = uid.split('/')[1]
                self.uid = uid

                # 获取个人信息
                divMessage = soup.find('div', attrs={'class': 'tip2'})
                weiBoCount = divMessage.find('span').getText()
                weiBoCount = (weiBoCount.split('[')[1]).replace(']', '')  # 微博数量

                # 获取粉丝/关注列表
                aa = divMessage.find_all('a')

                user_id_list = []   # 存储关注或粉丝的列表
                for a in aa:
                    a_text = a.getText()
                    print(a_text, type(a_text))
                    if "关注" in a_text:
                        self.follow_url = self.id_url + a.get("href")
                        print(self.follow_url)
                        # # 爬取关注
                        # self.getFollowAndFans(cur_weibo_user=id, flag="关注")
                    elif "粉丝" in a_text:
                        self.fans_url = self.id_url + a.get("href")
                        # 爬取粉丝
                        user_id_list = self.getFollowAndFansUrl(cur_weibo_user=cur_node, flag="粉丝")

                print("粉丝的数量：{}".format(len(user_id_list)))

                # 节点入队：
                for cur_user in user_id_list:
                    if cur_user not in crawl_visited:
                        crawl_visited.add(cur_user)
                        crawl_queue.put(cur_user)   # 入队
                        tail = cur_user # 当前层最后一个入队的元素

                # 如果当前层最后一个入队的元素出队，则进入下一层
                if cur_node == last:
                    layer += 1
                    last = tail
                # 爬到第三层时停止
                if layer == 3:
                    break

    def getFollowAndFansUrl(self, cur_weibo_user,flag):
        '''
        获取关注或者粉丝的链接
        :param cur_weibo_user:
        :param flag: 用于标识现在爬取的是粉丝还是关注
        :return: 返回由用户id获取的列表
        '''
        if flag == "关注":
            self.browser.get(self.follow_url)  # 打开follow页面
            WebDriverWait(self.browser, 3).until(
                EC.title_is("美国驻华大使馆关注的人")
            )
        elif flag == "粉丝":
            self.browser.get(self.fans_url)  # 打开fans页面
            WebDriverWait(self.browser, 3).until(
                EC.title_is("美国驻华大使馆的粉丝")
            )
        soup = BeautifulSoup(self.browser.page_source, 'lxml')

        # 获取页码
        pageSize = soup.find('div', attrs={"id": "pagelist"})
        pageSize = pageSize.find('div').getText()
        pageSize = pageSize.split("/")[1].split('页')[0]
        print("{} 页码：{}".format(flag, pageSize))
        user_id_list = []  # 存储爬取到的关注或粉丝的id
        # 遍历 fans or follow页面
        for page_index in range(1, int(pageSize) + 1):
            if flag == "关注":
                page_url = self.follow_page_url.format(self.uid, page_index)
            elif flag == "粉丝":
                page_url = self.fans_page_url.format(self.uid, page_index)

            # print(" {} page url {}".format(flag,page_url))
            # 访问页面
            self.browser.get(page_url)
            time.sleep(1)

            html_doc = self.browser.page_source
            # print("--")
            # print(html_doc)
            new_html = (html_doc.replace('<br>', ''))
            soup = BeautifulSoup(new_html, 'lxml')
            body = soup.find('body')
            table_all = body.find_all_next('table')
            count =0
            # 遍历每个粉丝或者关注者
            for t_num, table in enumerate(table_all):
                need_content = table.find_all("td", attrs={"valign": "top"})
                # print("need_content的数量 {}".format(len(need_content)))
                need_content = need_content[1]

                # 获取id，注：不是uid
                for i , temp_element in enumerate(need_content):
                    if "Tag" in str(type(temp_element)):
                        if i == 0:
                            userName = temp_element.getText()
                            id_url = temp_element.get("href")
                            user_id = id_url.split("/")[-1]
                            # print("姓名：{} id：{}".format(userName,user_id))
                            user_id_list.append(user_id)
                            count += 1
            # print("页码：{} 的粉丝数量：{}".format(page_index,count))

        print("============")
        print("粉丝或关注者的数量：{}".format(len(user_id_list)))
        return user_id_list
            # break


if __name__ == '__main__':
    # try:
    loginer = WeiboLogin()
    cookie_str = loginer.getCookies()
    # print('获取cookie成功')
    # print('Cookie:', cookie_str)
    # loginer.getUserInfoAndWeibo()
    loginer.bfs()
    close(loginer.conn)  # 关闭数据库连接
