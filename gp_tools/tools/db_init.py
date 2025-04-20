# 从上级目录的 conf 文件夹中的 mysql_conf 文件导入数据库配置信息
from ..conf.mysql_conf import mysql_conf
# 导入自定义的数据库操作模块
import db_operation

# 定义创建数据库的 SQL 语句，若数据库 gp_tools 不存在则创建，并指定字符集为 utf8mb4
create_db_sql = """CREATE DATABASE IF NOT EXISTS `gp_tools` CHARACTER SET 'utf8mb4';"""

# 定义创建 gp_agency_rating 表的 SQL 语句，若表不存在则创建
create_agency_rating_sql = """
CREATE TABLE  IF NOT EXISTS `gp_agency_rating` (
  `id` int NOT NULL AUTO_INCREMENT,  -- 自增主键
  `gp_code` varchar(255) NOT NULL COMMENT '股票代码',  -- 存储股票代码
  `gp_name` varchar(255) NOT NULL COMMENT '股票名称',  -- 存储股票名称
  `gp_target_price` varchar(255) DEFAULT NULL COMMENT '目标价',  -- 存储目标价
  `gp_latest_rating` varchar(255) DEFAULT NULL COMMENT '最新评级',  -- 存储最新评级
  `gp_rating_agency` varchar(255) DEFAULT NULL COMMENT '评级机构',  -- 存储评级机构
  `gp_analyst` varchar(255) DEFAULT NULL COMMENT '分析师',  -- 存储分析师信息
  `gp_industry` varchar(255) DEFAULT NULL COMMENT '行业',  -- 存储行业信息
  `gp_rating_date` datetime DEFAULT NULL COMMENT '评级日期',  -- 存储评级日期
  `gp_abstract` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '摘要',  -- 存储摘要信息
  PRIMARY KEY (`id`)  -- 设置 id 为主键
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""
# 定义清空 gp_agency_rating 表数据的 SQL 语句，原语句有误，正确的删除语句不需要 *
clear_table_gp_agency_rating = """delete from gp_agency_rating;"""

# 定义数据库初始化函数
def db_init():
    # 使用导入的数据库配置信息创建数据库连接
    # 关闭数据库连接
    # 执行创建表的 SQL 语句
    # 执行创建数据库的 SQL 语句
    # 获取数据库操作函数
    conn = db_operation.create_connection(**mysql_conf)

    operator = db_operation.execute_query
    operator(conn, create_db_sql)
    operator(conn, create_agency_rating_sql)
    db_operation.db_close_connection(conn)
