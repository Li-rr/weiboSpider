
class UserInfo:
    def __init__(self):
       self.user_id = ""
       self.user_uid = ""
       self.nick_name = ""
       self.gender = ""
       self.province = ""
       self.city = ""
       self.tweets_num = 0
       self.fans_num = 0
       self.followers_num = 0
       self.sex_orientation = ""
       self.sentiment = ""
       self.vip_level = ""
       self.label = ""
       self.person_url = "" # 用户首页链接
       self.crwal_time = ""

class WeiboData:
    def __init__(self):
        self.weibo_id = ""
        self.user_id = ""
        self.content = ""
        self.created_at = ""
        self.repost_num = 0
        self.comment_num = 0
        self.like_num = 0
        self.tool = ""
        self.origin_weibo = ""
        self.crawl_time = ""

class UserRealion:
    def __init__(self):
        self.reation_id = "" # 用户关系id
        self.son_id = ""
        self.father_id = ""
        self.crwal_time = ""