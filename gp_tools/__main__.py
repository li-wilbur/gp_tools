from gp_tools.db_init import db_init
from gp_tools.agency_rating import get_gp, agency_rating, clear_table
from gp_tools import db_operation
from gp_tools.conf.mysql_conf import mysql_conf
from gp_tools.conf import collection_list
from time import sleep
from random import random

if __name__ == '__main__':
    db_init()
    clear = 1
    clear_sql = """delete  from gp_agency_rating;"""
    insert_sql = "INSERT INTO gp_agency_rating (gp_code,gp_name,gp_target_price,gp_latest_rating,gp_rating_agency,gp_analyst,gp_industry,gp_rating_date,gp_abstract) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    conn = db_operation.create_connection(**mysql_conf)
    operator = db_operation.execute_query
    if clear_table(clear):
        operator(conn, clear_sql)
    gp_list = collection_list.collection.values()
    for gp_code in gp_list:
        sleep(random())
        get_result = get_gp(gp_code)
        if get_result:
            for rating in agency_rating(get_result):
                print(rating)
                operator(conn, insert_sql, rating)
    db_operation.db_close_connection(conn)
