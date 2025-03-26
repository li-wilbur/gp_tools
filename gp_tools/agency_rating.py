import requests
import bs4
from gp_tools.conf import collection_list
from gp_tools import db_operation
from gp_tools.conf.mysql_conf import mysql_conf
from time import sleep
from random import random

def get_gp(gp_code):
    url = 'https://stock.finance.sina.com.cn/stock/go.php/vIR_StockSearch/key/' + gp_code + '.phtml'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return None


def agency_rating(html_content):
    soup = bs4.BeautifulSoup(html_content, 'lxml')
    try:
        table = soup.find('table', class_='list_table')
    except AttributeError as e:
        print(f"找不到表格: {e}")
        return None
    rows = table.find_all('tr')
    result = []
    for row in rows[1:]:
        cols = row.find_all('td')
        row_data = []
        try:
            for col in cols:
                row_data.append(col.get_text(strip=True))
                if col.get_text(strip=True) == '摘要':
                    link = 'https:' + col.select_one('a').get('href')
                    row_data[8] = link
        except AttributeError as e:
            print('tables data error:', e)
            return None
        # row_data = [col.get_text(strip=True) for col in cols]
        del row_data[-4:]
        # print(row_data)
        result.append(row_data)
    # print(result)
    return result

def clear_table(clear=0):
    if clear == 1:
        return True

if __name__ == '__main__':
    clear = 1
    clear_sql = """delete  from gp_agency_rating;"""
    insert_sql = "INSERT INTO gp_agency_rating (gp_code,gp_name,gp_target_price,gp_latest_rating,gp_rating_agency,gp_analyst,gp_industry,gp_rating_date,gp_abstract) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    conn = db_operation.create_connection(**mysql_conf)
    operator = db_operation.execute_query
    if clear_table(clear):
        operator(conn,clear_sql)
    gp_list = collection_list.collection.values()
    for gp_code in gp_list:
        sleep(random())
        get_result = get_gp(gp_code)
        if get_result:
            for rating in agency_rating(get_result):
                print(rating)
                operator(conn, insert_sql, rating)
    db_operation.db_close_connection(conn)
