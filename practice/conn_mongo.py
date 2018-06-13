from pymongo import MongoClient

# 连接数据库
client = MongoClient('mongodb://user:pwd@ip:port')
db = client.testdb  # testdb数据库名

# 查询
cursor = db.inventory.find() # 注意返回的是查询结果的游标，这是产生文档的迭代对象
for doc in cursor:
    print(doc)
