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

def close(conn):
    conn.close()
