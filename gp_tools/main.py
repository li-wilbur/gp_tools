from tools.agency_rating import get_gp, agency_rating
from tools import db_operation
from conf.mysql_conf import mysql_conf
from conf import collection_list
from time import sleep
from random import random
import argparse


def init_args():
    """
    初始化命令行参数解析器并解析输入的参数。
    该函数会检查 'Clear' 参数是否合法，如果不合法则打印错误信息并返回 None。

    :return: 若参数合法，返回解析后的参数对象；若 'Clear' 参数不合法，返回 None
    """
    # 创建一个参数解析器对象，并添加程序的描述信息
    parser = argparse.ArgumentParser(description='这是一个机构对股票评级的数据查询工具')
    # 添加 -c 或 --code 命令行参数，该参数为字符串类型，可选输入，默认值为 0，用于指定股票代码
    parser.add_argument('-c', '--code', type=str, nargs='?', default=0, help='输入一个股票代码')
    # 添加 -C 或 --Clear 命令行参数，该参数为整数类型，可选输入，默认值为 0，用于指定是否先清理表数据
    parser.add_argument('-C', '--Clear', type=int, nargs='?', default=0, help='是否先清理表数据,0 OR 1')
    # 添加 -n 或 --no-db 命令行参数，该参数为整数类型，可选输入，默认值为 1，用于指定是否不依赖数据库
    parser.add_argument('-n', '--no-db', type=int, nargs='?', default=1, help='是否不依赖数据库,0 OR 1(不依赖数据库、无数据库,默认不依赖数据库)')
    # 解析命令行输入的参数
    args = parser.parse_args()
    # 检查 'Clear' 参数是否为 0 或 1
    if args.Clear not in [0, 1]:
        # 若 'Clear' 参数不合法，打印错误信息
        print('Clear 只能设置为0或者1！')
        return None
    # 若所有参数合法，返回解析后的参数对象
    return args


class RequestAndInsert:
    def __init__(self,mysql_conf,code,clear,no_db):
        """
        初始化数据库连接及相关参数

        :param mysql_conf: 数据库配置信息
        :param code: 股票代码
        :param clear: 是否清理表数据的标志，0 或 1
        :param no_db: 是否不依赖数据库的标志，0 或 1
        """
        # 如果依赖数据库，则创建数据库连接，并初始化操作方法
        if no_db != 1:
            self.conn = db_operation.create_connection(**mysql_conf)
            self.operator = db_operation.execute_query
            self.db_read = db_operation.read_query
        self.no_db = no_db
        self.code = code
        self.clear = clear

    def rai(self):
        """
        发起请求并插入数据到数据库，如果不依赖数据库则打印数据

        :return: 无
        """
        # 调用 get_gp 函数获取股票数据
        get_result = get_gp(self.code)
        # print(get_result)
        if get_result:
            # 如果不依赖数据库，打印前 3 条评级数据
            if self.no_db == 1:
                for rating in agency_rating(get_result)[0:3]:
                    print(rating)
            else:
                # 如果依赖数据库，将评级数据插入数据库
                for rating in agency_rating(get_result):
                    #print(rating)
                    self.operator(self.conn, insert_sql, rating)

    def gp_view(self):
        """
        查看 gp_agency_rating 表中指定股票代码的前 3 条最新评级数据

        :return: 无
        """
        if self.no_db != 1:
            # 构建查询 SQL 语句，查询指定股票代码的前 3 条最新评级数据
            view_sql = """SELECT * FROM	gp_agency_rating WHERE	gp_code = '{}' ORDER BY gp_rating_date DESC LIMIT 3;""".format(self.code)
            #print(view_sql)
            # 执行查询并获取结果
            result = self.db_read(self.conn, view_sql)
            # 遍历结果并打印每一行数据
            for row in result:
                print(row)

    def clear_table(self):
        """
        清空 gp_agency_rating 表中的数据

        :return: 无
        """
        if self.no_db != 1:
            # 构建删除 SQL 语句，删除 gp_agency_rating 表中的所有数据
            clear_sql = """delete  from gp_agency_rating;"""
            # 执行删除操作
            self.operator(self.conn, clear_sql)

    def close_conn(self):
        """
        关闭数据库连接

        :return: 无
            # 调用关闭连接的函数关闭数据库连接
        """
        if self.no_db != 1:
            db_operation.db_close_connection(self.conn)


if __name__ == '__main__':
    #db_init()

    insert_sql = "INSERT INTO gp_agency_rating (gp_code,gp_name,gp_target_price,gp_latest_rating,gp_rating_agency,gp_analyst,gp_industry,gp_rating_date,gp_abstract) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    args = init_args()
    if args:
        gp_rai = RequestAndInsert(mysql_conf,args.code,args.Clear,args.no_db)
        try:
            if args.Clear == 1:
                gp_rai.clear_table()
            if args.code == 0:
                gp_list = collection_list.collection.values()
                for gp_code in gp_list:
                    # 更新 RequestAndInsert 实例的股票代码为当前遍历到的股票代码
                    gp_rai.code = gp_code
                    # 调用 rai 方法，发起对当前股票代码的请求，若依赖数据库则将获取的评级数据插入数据库，否则打印数据
                    gp_rai.rai()
                    # 调用 gp_view 方法，查看 gp_agency_rating 表中当前股票代码的前 3 条最新评级数据
                    gp_rai.gp_view()
                    # 程序暂停一段随机时间，避免短时间内对服务器发起过多请求，减轻服务器压力
                    sleep(random())
            else:
                # 若用户指定了股票代码，调用 rai 方法，发起对指定股票代码的请求并处理数据
            # 无论程序执行过程中是否出现异常，都关闭数据库连接
            # 捕获程序执行过程中出现的异常，并打印异常信息
                # 调用 gp_view 方法，查看 gp_agency_rating 表中指定股票代码的前 3 条最新评级数据
                gp_rai.rai()
                gp_rai.gp_view()
        except Exception as e:
            print(e)
        finally:
            gp_rai.close_conn()