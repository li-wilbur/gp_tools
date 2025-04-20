import requests
import bs4


def get_gp(gp_code):
    """
    根据给定的股票代码，从新浪财经获取股票相关的 HTML 页面内容。

    :param gp_code: 股票代码
    :return: 若请求成功，返回页面的 HTML 文本内容；若请求出错，返回 None
    """
    # 构建请求的 URL，将股票代码插入到特定的新浪财经搜索链接中
    url = 'https://stock.finance.sina.com.cn/stock/go.php/vIR_StockSearch/key/' + gp_code + '.phtml'
    # 设置请求头，模拟 Chrome 浏览器进行请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    try:
        # 发送 GET 请求，设置超时时间为 5 秒
        response = requests.get(url, headers=headers, timeout=5)
        # 检查请求是否成功，如果状态码不是 200，会抛出异常
        response.raise_for_status()
        # 请求成功，返回页面的 HTML 文本内容
        return response.text
    except requests.RequestException as e:
        # 请求过程中出现异常，打印错误信息
        print(f"请求出错: {e}")
        # 请求失败，返回 None
        return None


def agency_rating(html_content):
    """
    从给定的 HTML 内容中提取机构评级表格数据。

    :param html_content: 包含机构评级表格的 HTML 内容
    :return: 包含表格数据的列表，每个子列表代表表格的一行；若出现错误则返回 None
    """
    # 使用 BeautifulSoup 解析 HTML 内容
    soup = bs4.BeautifulSoup(html_content, 'lxml')
    try:
        # 查找 class 为 'list_table' 的表格
        table = soup.find('table', class_='list_table')
    except AttributeError as e:
        # 若查找表格时出现属性错误，打印错误信息并返回 None
        print(f"找不到表格: {e}")
        return None
    # 获取表格中的所有行
    rows = table.find_all('tr')
    # 用于存储最终结果的列表
    result = []
    # 遍历表格的每一行，跳过表头行
    for row in rows[1:]:
        # 获取当前行的所有单元格
        cols = row.find_all('td')
        # 用于存储当前行数据的列表
        row_data = []
        try:
        # 将当前行处理后的数据添加到结果列表中
        # 删除 row_data 列表的最后 4 个元素
            # 若提取单元格数据时出现属性错误，打印错误信息并返回 None
                # 如果单元格文本为 '摘要'，则提取链接并替换 row_data 中索引为 8 的元素
                # 提取单元格的文本内容并去除首尾空白字符，添加到 row_data 列表中
            # 遍历当前行的每个单元格
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
