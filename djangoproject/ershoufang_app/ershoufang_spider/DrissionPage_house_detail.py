import os
from DrissionPage import ChromiumPage, ChromiumOptions
import random
import pymysql
import time
from bs4 import BeautifulSoup


# 配置数据库连接信息（凭据通过环境变量注入，勿写死）
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'old_house_data'),
    'charset': 'utf8'
}

# 配置 Chrome 浏览器路径（不填则由 DrissionPage 自动探测）
CHROME_PATH = os.getenv('CHROME_PATH', '')


def get_urls_from_db():
    """
    从数据库中获取 title, link_url
    :return: 包含 id、title 和 title_url 的元组列表
    """
    try:
        with pymysql.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, title, detail_href FROM t_house WHERE status =0 limit 200")
                rows = cursor.fetchall()
                return [(row[0], row[1], row[2]) for row in rows]
    except pymysql.Error as err:
        print(f"数据库连接错误: {err}")
        return []


# def get_content_detail(html):
#     data ={}
#     bs01 = BeautifulSoup(html, "html.parser")
#     div_sell_detail = bs01.find('div', class_='sellDetailPage')
#     div_tag = div_sell_detail.find('div', {'data-component': 'overviewIntro'})
#     div_content =div_tag.find('div',  class_='overview').find('div',  class_='content')
#     div_house_info = div_content.find('div',  class_='houseInfo')
#
#     div_room =div_house_info.find('div',  class_='room')
#     main_info = div_room.find('div',  class_='mainInfo').get_text()
#     print('main_info',main_info)
#     data['main_info'] =main_info
#     sub_info = div_room.find('div',  class_='subInfo').get_text()
#     print('sub_info', sub_info)
#     data['sub_info'] = sub_info
#
#     type_div_room = div_house_info.find('div', class_='type')
#     type_main_info = type_div_room.find('div', class_='mainInfo').get_text()
#     print('type_main_info', type_main_info)
#     data['house_orientation'] = type_main_info
#     type_sub_info = type_div_room.find('div', class_='subInfo').get_text()
#     print('type_sub_info', type_sub_info)
#     data['house_decorate'] = type_sub_info
#
#     area_div_room = div_house_info.find('div', class_='area')
#     area_main_info = area_div_room.find('div', class_='mainInfo').get_text()
#     print('area_main_info', area_main_info)
#     data['house_area'] = area_main_info
#     area_sub_info = area_div_room.find('div', class_='subInfo').get_text()
#     print('area_sub_info', area_sub_info)
#     data['house_type'] = area_sub_info
#
#     div_around_info = div_content.find('div', class_='aroundInfo')
#
#     community_name = div_around_info.find('div', class_='communityName').find('a',class_='info no_resblock_a').get_text()
#     print('community_name', community_name)
#     data['housing_estate'] = community_name
#     area_name =div_around_info.find('div', class_='areaName').find('span',class_='info').get_text().strip().replace('\n','')
#     print('area_name', area_name)
#     data['zone'] = area_name

def get_content_detail(html):
    data = {}
    try:
        bs01 = BeautifulSoup(html, "html.parser")
        div_sell_detail = bs01.find('div', class_='sellDetailPage')
        if not div_sell_detail:
            print("Error: Could not find 'div' with class 'sellDetailPage'")
            return data

        div_tag = div_sell_detail.find('div', {'data-component': 'overviewIntro'})
        if not div_tag:
            print("Error: Could not find 'div' with data-component 'overviewIntro'")
            return data

        div_content = div_tag.find('div', class_='overview').find('div', class_='content')
        if not div_content:
            print("Error: Could not find 'div' with class 'content' under 'overview'")
            return data

        def extract_info(div, class_name, main_key, sub_key):
            div_room = div.find('div', class_=class_name)
            if not div_room:
                print(f"Error: Could not find 'div' with class '{class_name}'")
                return

            main_info = div_room.find('div', class_='mainInfo')
            if main_info:
                main_info = main_info.get_text()
                print(f'{main_key}', main_info)
                data[main_key] = main_info
            else:
                print(f"Error: Could not find 'div' with class 'mainInfo' under '{class_name}'")

            sub_info = div_room.find('div', class_='subInfo')
            if sub_info:
                sub_info = sub_info.get_text()
                print(f'{sub_key}', sub_info)
                data[sub_key] = sub_info
            else:
                print(f"Error: Could not find 'div' with class 'subInfo' under '{class_name}'")

        div_house_info = div_content.find('div', class_='houseInfo')
        if not div_house_info:
            print("Error: Could not find 'div' with class 'houseInfo'")
        else:
            extract_info(div_house_info, 'room', 'main_info', 'sub_info')
            extract_info(div_house_info, 'type', 'house_orientation', 'house_decorate')
            extract_info(div_house_info, 'area', 'house_area', 'house_type')

        div_around_info = div_content.find('div', class_='aroundInfo')
        if not div_around_info:
            print("Error: Could not find 'div' with class 'aroundInfo'")
        else:
            community_name_div = div_around_info.find('div', class_='communityName')
            if not community_name_div:
                print("Error: Could not find 'div' with class 'communityName'")
            else:
                community_name = community_name_div.find('a', class_='info no_resblock_a')
                if community_name:
                    community_name = community_name.get_text()
                    print('community_name', community_name)
                    data['housing_estate'] = community_name
                else:
                    print("Error: Could not find 'a' with class 'info no_resblock_a' under 'communityName'")

            area_name_div = div_around_info.find('div', class_='areaName')
            if not area_name_div:
                print("Error: Could not find 'div' with class 'areaName'")
            else:
                area_name = area_name_div.find('span', class_='info')
                if area_name:
                    area_name = area_name.get_text().strip().replace('\n', '')
                    print('area_name', area_name)
                    data['zone'] = area_name
                else:
                    print("Error: Could not find 'span' with class 'info' under 'areaName'")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return data


def updateMysqlData(id, data):
    try:
        with pymysql.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE t_house 
                    SET 
                        main_info = %s, 
                        sub_info = %s,
                        house_orientation = %s,
                        house_decorate = %s,
                        house_area = %s,
                        house_type = %s,
                        housing_estate = %s,
                        zone = %s,
                        status = 1
                    WHERE id = %s
                """
                values = (
                    data.get('main_info'),
                    data.get('sub_info'),
                    data.get('house_orientation'),
                    data.get('house_decorate'),
                    data.get('house_area'),
                    data.get('house_type'),
                    data.get('housing_estate'),
                    data.get('zone'),
                    id
                )
                cursor.execute(sql, values)
                conn.commit()
        return '数据保存结束'
    except pymysql.Error as e:
        print(f"数据库操作出错: {e}")
        return None
    except Exception as e:
        print(f"发生未知错误: {e}")
        return None



def main():
    url ='https://sz.ke.com/ershoufang/'
    # 配置 Chromium 选项，并设置浏览器路径
    # 未显式配置 CHROME_PATH 时交由 DrissionPage 自动探测浏览器
    co = ChromiumOptions()
    if CHROME_PATH:
        co.set_browser_path(CHROME_PATH)
    # 创建 ChromiumPage 实例
    page = ChromiumPage(co)
    urls = get_urls_from_db()
    try:
        for index, (id ,title, url) in enumerate(urls):
            print(id,title)
            try:
                # 打开指定网页
                page.get(url)
                # 等待 4 秒让页面加载
                time.sleep(random.randint(5, 10))
                # 获取网页的文本内容
                page_content = page.html
                # 调用 get_content 函数处理 HTML 内容
                data_dict =get_content_detail(page_content)
                updateMysqlData(id,data_dict)

            except Exception as e:
                print(f"处理 {url} 时发生错误: {e}")

    except Exception as e:
        print(f"发生全局错误: {e}")
    finally:
        # 关闭浏览器
        page.quit()

if __name__ == "__main__":
    main()