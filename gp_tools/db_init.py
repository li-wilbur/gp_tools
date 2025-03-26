from gp_tools.conf.mysql_conf import mysql_conf
from gp_tools import db_operation

create_db_sql = """CREATE DATABASE IF NOT EXISTS `gp_tools` CHARACTER SET 'utf8mb4';"""

create_agency_rating_sql = """
CREATE TABLE  IF NOT EXISTS `gp_agency_rating` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gp_code` varchar(255) NOT NULL COMMENT '股票代码',
  `gp_name` varchar(255) NOT NULL COMMENT '股票名称',
  `gp_target_price` varchar(255) DEFAULT NULL COMMENT '目标价',
  `gp_latest_rating` varchar(255) DEFAULT NULL COMMENT '最新评级',
  `gp_rating_agency` varchar(255) DEFAULT NULL COMMENT '评级机构',
  `gp_analyst` varchar(255) DEFAULT NULL COMMENT '分析师',
  `gp_industry` varchar(255) DEFAULT NULL COMMENT '行业',
  `gp_rating_date` datetime DEFAULT NULL COMMENT '评级日期',
  `gp_abstract` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '摘要',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""

def db_init():
    conn = db_operation.create_connection(**mysql_conf)

    operator = db_operation.execute_query
    operator(conn, create_db_sql)
    operator(conn, create_agency_rating_sql)
    db_operation.db_close_connection(conn)

if __name__ == '__main__':
    db_init()