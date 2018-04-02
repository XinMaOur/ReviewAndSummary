
<https://docs.mongodb.com/manual/tutorial/manage-mongodb-processes/>
## 查找发现官网直接下载速度贼慢
    yum list | grep 'mongod'
发现yum源中有包含不过版本有点老，v2.6.12.
新版3.2.4
## 安装
    yum install mongodb.x86_64 mongodb-server.x86_64
### python
    yum install pymongo
    
## 开启mongodb
mongod --config mongodb.conf


## Error(可能会碰到的问题)
    ERROR: child process failed, exited with error number 1


    ERROR: child process failed, exited with error number 100
很可能是没有正常关闭导致的，那么可以删除 mongod.lock 文件
## 使用
    #encoding:utf=8  
    import pymongo  
    
    connection=pymongo.Connection('10.32.38.50',27017)  
    
    #选择myblog库  
    db=connection.myblog  
    
    # 使用users集合  
    collection=db.users  
## 绑定mongod.conf和mongod命令
    mongod --port 8000 --dbpath /var/lib/mongodb/data
## 开启mongo shell
    mongo --host 127.0.0.1 --port 8000

    