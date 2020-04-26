
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

    def getDict(self):
        userinfo_dict = {}
        userinfo_dict['_id'] = self.user_id
        userinfo_dict['user_uid'] = self.user_uid
        userinfo_dict['nick_name'] = self.nick_name
        userinfo_dict['gender'] = self.gender
        userinfo_dict['province'] = self.province
        userinfo_dict['city'] = self.city
        userinfo_dict['tweets_num'] = self.tweets_num
        userinfo_dict['fans_num'] = self.fans_num
        userinfo_dict['followers_num'] = self.followers_num
        userinfo_dict['sex_orientation'] = self.sex_orientation
        userinfo_dict['sentiment'] = self.sentiment
        userinfo_dict['vip_level'] = self.vip_level
        userinfo_dict['label'] = self.label
        userinfo_dict['person_url'] = self.person_url
        return userinfo_dict

    def userPrint(self):
        user_info = self.getDict()
        for key in user_info.keys():
            print(key,user_info[key])
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