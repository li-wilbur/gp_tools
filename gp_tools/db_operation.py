import mysql.connector
from mysql.connector import Error


def create_connection(host, port, user, password, database):
    """
    创建数据库连接
    :param host_name: 主机名
    :param user_name: 用户名
    :param user_password: 用户密码
    :param db_name: 数据库名
    :return: 数据库连接对象
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        return connection
    except Error as e:
        print(f"连接到MySQL数据库时出错: {e}")
        return None


def execute_query(connection, query, values=None):
    """
    执行读取 SQL 查询
    增删改
    :param connection: 数据库连接对象
    :param query: SQL 查询语句
    :return: 查询结果
    """
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute(query, values)
            connection.commit()
            #print("Sql 执行成功！")
        except Error as e:
            print(f"执行查询时出错: {e}")
            return None


def read_query(connection, query):
    """
    执行读取 SQL 查询
    只读
    :param connection: 数据库连接对象
    :param query: SQL 查询语句
    :return: 查询结果
    """
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"执行查询时出错: {e}")
            return None


def db_close_connection(connection):
    """
    关闭数据库连接
    :param connection: 数据库连接对象
    """
    if connection is not None:
        try:
            connection.close()
            #print("MySQL连接已关闭")
        except Error as e:
            print(f"关闭MySQL连接时出错: {e}")
