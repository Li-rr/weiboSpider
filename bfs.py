import queue
'''
定义图
A -->B-->D
|        |
| -->c-->E
'''

graph = {}
graph['A'] = ['B', 'C']

graph['B'] = ['D']
graph['C'] = ['E']

graph['D'] = []
graph['E'] = ['D']
'''
算法描述：
1. 创建一个队列，用于存储要检查的节点
2. 从队列中取出一个元素，打印它，并将其未访问过的子结点放到队列中
3. 重复2，直至队列空
'''
depth = []

def bfs(adj,start):
    visited = set()
    q = queue.Queue()
    layer = 0
    last = start   # 第0层的元素
    tail = ""

    q.put(start)
    while not q.empty():
        u = q.get()
        print("当前层：{} 节点：{}".format(layer,u))
        get_u = adj.get(u,[])
        # if len(get_u) == 0:
        #     layer += 1
        for v in get_u:
            if v not in visited:
                visited.add(v)
                q.put(v)
                tail = v    # 当前层最后一个入队的元素

        # 如果当前层最后一个入队的元素出队，则进入下一层
        if u == last:
            layer += 1
            last =tail


bfs(graph,'A')