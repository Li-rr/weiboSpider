## 基于selenium的微博爬虫
### 环境
- python 3.7
- selenium3
- mongoDB
### 实现功能
- 爬取用户发的微博内容
- 爬取用户关注与粉丝（最大只能爬取20页）
- 使用图方法遍历用户的的粉丝，最大遍历三层（超时问题）
- 爬取微博用户简介
### 未实现功能
- 挖掘微博用户关系
- 爬取用户微博
- 改造为多线程
- 改造为selenium + requests

### **数据字段**

#### 用户数据

| 字段            | 说明                            |
| --------------- | ------------------------------- |
| user_id         | 用户的id，唯一标识符            |
| user_uid        | 用户的uid，可用于follow或者fans |
| nick_name       | 昵称                            |
| gender          | 性别                            |
| province        | 省                              |
| city            | 市                              |
| tweets_num      | 微博发表数                      |
| fans_num        | 粉丝数                          |
| followers_num   | 关注数                          |
| sex_orientation | 性取向（未使用）                |
| sentiment       | 感情状况（未使用）                      |
| vip_level       | 会员等级                        |
| label           | 标签                            |
| person_url      | 用户首页链接                    |
| crawl_time      | 抓取时间（未使用）                        |

#### 微博数据

| 字段         | 说明                     |
| ------------ | ------------------------ |
| weibo_id     | 微博id                   |
| user_id      | 微博作者的id             |
| content      | 内容                     |
| created_at   | 发表时间                 |
| repost_num   | 转发数                   |
| comment_num  | 评论数                   |
| like_num     | 点赞数                   |
| tool         | 发布微博的工具           |
| origin_weibo | 原始微博，转发的微博才有 |
| crawl_time   | 抓取时间戳 （未使用）              |

#### 用户关系数据

| 字段        | 说明             |
| ----------- | ---------------- |
| _id         | 用户关系id       |
| fan_id      | 关注者的用户id   |
| follower_id | 被关注者的用户id |
| crawl_time  | 抓取时间（未使用）         |



### 参考链接

1. [爬取新浪微博用户信息及微博内容](https://blog.csdn.net/Asher117/article/details/82793091)
2. [数据字段的参考](https://github.com/nghuyong/WeiboSpider/blob/master/.github/data_stracture.md)