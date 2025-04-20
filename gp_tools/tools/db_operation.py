# 导入 mysql.connector 模块，用于与 MySQL 数据库进行交互
import mysql.connector
# 从 mysql.connector 模块导入 Error 异常类，用于捕获数据库操作中的错误
from mysql.connector import Error


def create_connection(host, port, user, password, database):
    """
    创建数据库连接

    :param host: 数据库主机地址
    :param port: 数据库端口号
    :param user: 数据库用户名
    :param password: 数据库用户密码
    :param database: 要连接的数据库名
    :return: 若连接成功，返回数据库连接对象；若连接失败，返回 None
    """
    try:
        # 尝试使用提供的参数连接到 MySQL 数据库
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        return connection
    except Error as e:
        # 若连接过程中出现错误，打印错误信息并返回 None
        print(f"连接到MySQL数据库时出错: {e}")
        return None


def execute_query(connection, query, values=None):
    """
    执行增删改类型的 SQL 查询

    :param connection: 数据库连接对象
    :param query: SQL 查询语句
    :param values: 可选参数，用于 SQL 查询中的占位符替换，默认为 None
    :return: 若执行成功，无返回值；若执行失败，返回 None
    """
    if connection is not None:
        try:
            # 创建游标对象，用于执行 SQL 语句
            cursor = connection.cursor()
            # 执行 SQL 语句，若有 values 参数则进行占位符替换
            cursor.execute(query, values)
            # 提交事务，将更改保存到数据库
            connection.commit()
            #print("Sql 执行成功！")
        except Error as e:
            # 若执行过程中出现错误，打印错误信息并返回 None
            print(f"执行查询时出错: {e}")
            return None
    else:
        # 若数据库连接对象为 None，打印提示信息并返回 None
        print("无法连接到数据库")
        return None

def read_query(connection, query):
    """
    执行只读类型的 SQL 查询

    :param connection: 数据库连接对象
    :param query: SQL 查询语句
    :return: 若执行成功，返回查询结果列表；若执行失败，返回 None
    """
    if connection is not None:
        try:
            # 创建游标对象，用于执行 SQL 语句
            cursor = connection.cursor()
            # 执行 SQL 语句
            cursor.execute(query)
            # 获取查询结果的所有行并返回
            return cursor.fetchall()
        except Error as e:
            # 若执行过程中出现错误，打印错误信息并返回 None
            print(f"执行查询时出错: {e}")
            return None
            # 若关闭过程中出现错误，打印错误信息
            # 尝试关闭数据库连接

        # 若数据库连接对象为 None，打印提示信息并返回 None
    else:
        print("无法连接到数据库")
        return None


def db_close_connection(connection):
    """
    关闭数据库连接
    :param connection: 数据库连接对象
    """
    if connection is not None:
        try:
            connection.close()
            print("MySQL连接已关闭")
        except Error as e:
            print(f"关闭MySQL连接时出错: {e}")
