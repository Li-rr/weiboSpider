import pymongo as pmg

def connDB():
    conn = pmg.MongoClient("localhost",27017)
    db_weibo = conn.weibo # 连接weibo数据库，没有则自动创建

    return db_weibo,conn

def insertDataToFollowFansGraph(db,data):
    '''
    插入微博关注/分数关系图
    :param db:
    :return:
    '''
    follow_fans_graph = db.weibo_graph_set  # 使用weibo_graph_set集合，没有则自动创建
    # follow_fans_graph.insert(data)
    follow_fans_graph.update(data,{'$set':data},upsert=True)

def insertDataToUserInfo(db,data):
    userInfo_table = db.user_info_set
    userInfo_table.insert(data)

def insertDataToUserRealtion(db,data):
    userRealtion_table = db.user_realtion_set
    userRealtion_table.insert(data)

def close(conn):
    conn.close()
