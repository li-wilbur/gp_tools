from gp_tools.db_init import db_init
from gp_tools.agency_rating import get_gp, agency_rating
from gp_tools import db_operation
from gp_tools.conf.mysql_conf import mysql_conf
from gp_tools.conf import collection_list
from time import sleep
from random import random
import argparse


def init_args():
    """init argos"""
    parser = argparse.ArgumentParser(description='这是一个机构对股票评级的数据查询工具')
    parser.add_argument('-c', '--code', type=str, nargs='?', default=0, help='输入一个股票代码')
    parser.add_argument('-C', '--Clear', type=int, nargs='?', default=0, help='是否先清理表数据,0 OR 1')
    parser.add_argument('-n', '--no-db', type=int, nargs='?', default=0, help='是否不依赖数据库,0 OR 1(不依赖数据库、无数据库)')
    args = parser.parse_args()
    if args.Clear not in [0, 1]:
        print('Clear 只能设置为0或者1！')
        return None
    return args


class RequestAndInsert:
    def __init__(self,mysql_conf,code,clear,no_db):
        """init DB """
        if no_db != 1:
            self.conn = db_operation.create_connection(**mysql_conf)
            self.operator = db_operation.execute_query
            self.db_read = db_operation.read_query
        self.no_db = no_db
        self.code = code
        self.clear = clear


    def rai(self):
        """
        requests and insert
        :return:
        """
        get_result = get_gp(self.code)
        # print(get_result)
        if get_result:
            if self.no_db == 1:
                for rating in agency_rating(get_result)[0:3]:
                    print(rating)
            else:
                for rating in agency_rating(get_result):
                    #print(rating)
                    self.operator(self.conn, insert_sql, rating)

    def gp_view(self):
        """ view gp_agency_rating TOP3"""
        if self.no_db != 1:
            view_sql = """SELECT * FROM	gp_agency_rating WHERE	gp_code = '{}' ORDER BY gp_rating_date DESC LIMIT 3;""".format(self.code)
            #print(view_sql)
            result = self.db_read(self.conn, view_sql)
            for row in result:
                print(row)

    def clear_table(self):
        """clear table"""
        if self.no_db != 1:
            clear_sql = """delete  from gp_agency_rating;"""
            self.operator(self.conn, clear_sql)

    def close_conn(self):
        """ close connection """
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
                i = 0
                for gp_code in gp_list:
                    #print(gp_code)
                    gp_rai.code = gp_code
                    sleep(random())
                    gp_rai.rai()
                    gp_rai.gp_view()
            else:
                gp_rai.rai()
                gp_rai.gp_view()
        except Exception as e:
            print(e)
        finally:
            gp_rai.close_conn()