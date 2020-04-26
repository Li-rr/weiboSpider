import re

test_str = '<div class=w"c">会员等级：110级 <a href="/member/present/comfirmTime?uid=1743951792">送Ta会员</a>'
test_str_2 =  '''<div class="c">昵称:美国驻华大使馆认证:美国驻华大使馆官方微博性别: \
男地区:北京 朝阳区生日:0001-00-00认证信息：美国驻华大使馆官方微博简介: \
本帐号的使用条款可在以下链接找到：http://t.cn/R6HRrV1 有时候，我 \
们的内容会将关注者定向到非美国政府网站，此处包含的链接仅供参考，不一定代表美国政府或美国国务院的观点或背书。 \
本微博由美国使馆新闻文化处维护。我们的主要目标是促进关于美国文化、社会以及使馆项目的对话。请访问我们的网站以了解更多签证、教育等方面的信息。 \
标签:<a href="/search/?keyword=%E6%96%87%E5%8C%96&amp;stag=1">文化</a> <a href="/search/?keyword=%E4%B8%AD%E7%BE%8E%E5%85%B3%E7%B3%BB&amp;stag=1"> \
中美关系</a> <a href="/search/?keyword=%E7%BE%8E%E5%9B%BD%E9%A9%BB%E5%8D%8E%E5%A4%A7%E4%BD%BF%E9%A6%86&amp;stag=1">美国驻华大使馆</a> <a href="/account/privacy/tags/?uid=1743951792&amp;st=a6939a">更多&gt;&gt;</a></div>'''
result_str = re.findall(r'会员等级：([0-9]+)级',test_str)

fuck_str = '''昵称:美国驻华大使馆认证:美国驻华大使馆官方微博性别:男地区 \
:北京 朝阳区生日:0001-00-00认证信息：美国驻华大使馆官方微博简介: \
本帐号的使用条款可在以下链接找到：http://t.cn/R6HRrV1 有时候， \
我们的内容会将关注者定向到非美国政府网站，此处包含的链接仅供参考， \
不一定代表美国政府或美国国务院的观点或背书。本微博由美国使馆新闻文化处维护。 \
我们的主要目标是促进关于美国文化、社会以及使馆项目的对话。请访问我们的网站以了解更多签证、教育等方面的信息。标签:文化 中美关系 美国驻华大使馆 更多>>
'''
fuck_str_2 = "互联网:http://weibo.com/usembassy手机版:https://weibo.cn/usembassy她的相册>>"

print(test_str_2)

nickname_str = re.findall(r'昵称.*?(?=认证)',fuck_str)
renzhi_str = re.findall(r'认证.*?(?=性别)',fuck_str)
sex_str = re.findall(r'性别.*?(?=地区)',fuck_str)
diqu_str = re.findall(r'地区.*?(?=生日)',test_str_2)
birthday_str = re.findall(r'生日.*?(?=认证信息)',fuck_str)
label_str = re.findall(r'标签.*',fuck_str)
person_url = re.findall(r'手机版.*?(?=[他|她|我]的相册)',fuck_str_2)
print(nickname_str)
print(renzhi_str)
print(sex_str)
print(diqu_str)

print(re.split(r"[: ]",diqu_str[0]))
print(birthday_str[0][3:])
label_list = re.split(r"[: \xa0]",label_str[0])
print(re.split(r"[: \xa0]",label_str[0]))
print(" ".join(label_list[1:-1]))
print(person_url)
