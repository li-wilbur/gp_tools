import requests
import bs4
from gp_tools.conf import collection_list


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
        row_data = [col.get_text(strip=True) for col in cols]
        # print(row_data)
        result.append(row_data)
    # print(result)
    return result

if __name__ == '__main__':
    gp_list = collection_list.collection.values()
    for gp_code in gp_list:
        get = get_gp(gp_code)
        if get:
            print(agency_rating(get))
