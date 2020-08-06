import pymysql
from mysql_pool.sql_setting import mysqlInfo
from DBUtils.PooledDB import PooledDB


class ConnMysql(object):
    __pool = None

    def __init__(self):
        # 构造函数，创建数据库连接、游标
        self.coon = ConnMysql.getmysqlconn()
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库连接池连接
    @staticmethod
    def getmysqlconn():
        global __pool
        if ConnMysql.__pool is None:
            __pool = PooledDB(
                creator=pymysql,
                mincached=1,
                maxcached=5,
                maxconnections=6,
                maxshared=3,
                blocking=True,
                maxusage=None,
                setsession=[],
                ping=2,
                host=mysqlInfo['host'],
                user=mysqlInfo['user'],
                passwd=mysqlInfo['passwd'],
                db=mysqlInfo['db'],
                port=mysqlInfo['port'],
                charset=mysqlInfo['charset'])
        return __pool.connection()

    # 插入、修改、删除一条
    def sql_change_msg(self, sql):
        change_sql = self.cur.execute(sql)
        self.coon.commit()
        return change_sql

    # 查询一条
    def sql_select_one(self, sql):
        self.cur.execute(sql)
        select_res = self.cur.fetchone()
        return select_res

    # 查询多条
    def sql_select_many(self, sql, count=None):
        self.cur.execute(sql)
        if count is None:
            select_res = self.cur.fetchall()
        else:
            select_res = self.cur.fetchmany(count)
        return select_res

    # 释放资源
    def release(self):
        self.coon.close()
        self.cur.close()
