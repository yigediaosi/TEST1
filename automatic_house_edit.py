import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import get_cookie
import sqlite3
import os


def query_sqlite_info(table):
    # 获取数据库文件的路径
    db_path = os.path.join(os.path.dirname(__file__), 'C:\kaifa\egg_13077\electron-egg\data\sqlite-demo.db')
    # 连接到数据库
    conn = sqlite3.connect(db_path)
    # 创建游标
    cursor = conn.cursor()
    # 执行查询语句
    cursor.execute('SELECT * FROM ' + table)
    # 获取查询结果
    rows = cursor.fetchall()
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
    return rows


def action(houseId):
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无界面模式运行Chrome，可以加快爬取速度

    # 创建Chrome浏览器实例
    driver = webdriver.Chrome(options=chrome_options)

    # 访问指定页面
    driver.get("https://vip.anjuke.com/")
    cookies = get_cookie.fetch_host_cookie("anjuke.com")

    for name, value in cookies.items():
        driver.add_cookie({'name': f"{name}", 'value': f"{value}"})

    driver.get('https://vip.anjuke.com/sydcpublish/xzlPublish?houseId=' + houseId + '&from=hugList')
    driver.implicitly_wait(10)
    # 执行 JavaScript 来点击按钮
    driver.execute_script("document.querySelector('button.ant-btn.ant-btn-primary').click()")
    time.sleep(1)
    print('执行编辑成功：' + houseId)
    # 关闭浏览器实例
    driver.quit()


def execute():
    user_token = query_sqlite_info('user_token')
    if len(user_token) == 0:
        print('token不存在')
    else:
        house_list = query_sqlite_info('house_info')
        if len(house_list) == 0:
            print("查询结果为空")
        else:
            # 解析字段
            for row in house_list:
                house_no = row[0]
                print("House ID:", house_no)
                action(house_no)

# if __name__ == '__main__':

# houseIds = '3022689401216007,3022707522691075'
# houseIds_list = houseIds.split(',')
# for houseId in houseIds_list:
#     action(houseId)
