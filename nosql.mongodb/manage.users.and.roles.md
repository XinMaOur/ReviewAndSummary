### Reference
<https://docs.mongodb.com/manual/tutorial/manage-users-and-roles/>

## Manage Users and Roles

### 创建一个自定义用户角色
#### 1.通用连接方式
    mongo --port 8000 --host 127.0.0.1 -u hixxx -p 'xxx' --authenticationDatabase 'admin' 

    MongoDB shell version: 2.6.12
    connecting to: 127.0.0.1:8000/test
    Server has startup warnings: 
    2018-04-01T14:46:42.811+0800 [initandlisten] 
    2018-04-01T14:46:42.811+0800 [initandlisten] ** WARNING: Readahead for /var/lib/mongodb/data is set to 4096KB
    2018-04-01T14:46:42.811+0800 [initandlisten] **          We suggest setting it to 256KB (512 sectors) or less
    2018-04-01T14:46:42.811+0800 [initandlisten] **          http://dochub.mongodb.org/core/readahead

#### 2.创建角色
    > db.createRole(
    ...    {
    ...      role: "mongostatRole",
    ...      privileges: [
    ...        { resource: { cluster: true }, actions: [ "serverStatus" ] }
    ...      ],
    ...      roles: []
    ...    }
    ... )
    {
        "role" : "mongostatRole",
        "privileges" : [
            {
                "resource" : {
                    "cluster" : true
                },
                "actions" : [
                    "serverStatus"
                ]
            }
        ],
        "roles" : [ ]
    }

### 修改一个已经存在的用户角色 
    db.changeUserPassword("hixxx", "yidiantong")

#### 1.赋权
    > use admin
    > db.grantRolesToUser(
        "hixxx",
        [
        { role: "read", db: "wangda" }
        ]
    )
#### 2.撤销权限
    > use admin
    switched to db admin
    > db.getUser('hixxx')
    {
        "_id" : "admin.hixxx",
        "user" : "hixxx",
        "db" : "admin",
        "roles" : [
            {
                "role" : "read",
                "db" : "wangda"
            },
            {
                "role" : "root",
                "db" : "admin"
            }
        ]
    }
    > db.revokeRolesFromUser(
    ...     "hixxx",
    ...     [
    ...       { role: "read", db: "wangda" }
    ...     ]
    ... )
    > db.getUser('hixxx')
    {
        "_id" : "admin.hixxx",
        "user" : "hixxx",
        "db" : "admin",
        "roles" : [
            {
                "role" : "root",
                "db" : "admin"
            }
        ]
    }

### 修改已经存在用户的密码

### 查看用户所扮演的所有角色
#### 1.查看用户库中，hixxx所属数据库,扮演角色
    > use admin
    > db.getUser('hixxx')
    {
        "_id" : "admin.hixxx",
        "user" : "hixxx",
        "db" : "admin",
        "roles" : [
            {
                "role" : "read",
                "db" : "wangda"
            },
            {
                "role" : "root",
                "db" : "admin"
            }
        ]
    }

#### 2.查看当前角色的所有权限

    > use admin
    > db.getRole( "mongostatRole", { showPrivileges: true } )
    {
        "role" : "mongostatRole",
        "db" : "admin",
        "isBuiltin" : false,
        "roles" : [ ],
        "inheritedRoles" : [ ],
        "privileges" : [
            {
                "resource" : {
                    "cluster" : true
                },
                "actions" : [
                    "serverStatus"
                ]
            }
        ],
        "inheritedPrivileges" : [
            {
                "resource" : {
                    "cluster" : true
                },
                "actions" : [
                    "serverStatus"
                ]
            }
        ]
    }
    > 

### 查看角色所拥有的所有权限

    > use wangda
    switched to db wangda
    > db.getRole( "read", { showPrivileges: true } )
    {
	"role" : "read",
	"db" : "wangda",
	"isBuiltin" : true,
	"roles" : [ ],
	"inheritedRoles" : [ ],
	"privileges" : [
		{
			"resource" : {
				"db" : "wangda",
				"collection" : ""
			},
			"actions" : [
				"collStats",
				"dbHash",
				"dbStats",
				"find",
				"killCursors",
				"planCacheRead"
			]
		},
    ......
	],
	"inheritedPrivileges" : [
		{
			"resource" : {
				"db" : "wangda",
				"collection" : ""
			},
			"actions" : [
				"collStats",
				"dbHash",
				"dbStats",
				"find",
				"killCursors",
				"planCacheRead"
			]
		},
		{
			"resource" : {
				"db" : "wangda",
				"collection" : "system.indexes"
			},
			"actions" : [
				"collStats",
				"dbHash",
				"dbStats",
				"find",
				"killCursors",
				"planCacheRead"
			]
		},
		......
	]
}


#### 附 
<table>
<tr>
    <td>角色类型</td>
    <td>权限级别</td>
</tr>
<tr>
    <td>普通用户角色</td>
    <td>read、readWrite</td>
</tr>
<tr>
    <td>数据库管理员角色</td>
    <td>dbAdmin、dbOwner、userAdmin</td>
</tr>
<tr>
    <td>集群管理员角色</td>
    <td>clusterAdmin、clusterManager、clusterMonitor、hostManager</td>
</tr>
<tr>
    <td>数据库备份与恢复角色</td>
    <td>backup、restore</td>
</tr>
<tr>
    <td>所有数据库角色</td>
    <td>readAnyDatabase、readWriteAnyDatabase、userAdminAnyDatabase、dbAdminAnyDatabase</td>
</tr>
<tr>
    <td>超级用户角色</td>
    <td>root</td>
</tr>
<tr>
    <td>核心角色</td>
    <td>__system</td>
</tr>
</table>