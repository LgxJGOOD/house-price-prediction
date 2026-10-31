import os
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



def get_content(data):
    bs01 = BeautifulSoup(data, "html.parser")
    div_tag = bs01.find('div', {'data-component': 'list'})
    data ={}
    if div_tag:
        # 查找 ul 标签
        ul_tag = div_tag.find('ul', {'class': 'sellListContent', 'log-mod': 'list'})
        if ul_tag:
            # 查找所有符合条件的 li 标签
            li_tags = ul_tag.find_all('li', class_='clear')
            for li  in li_tags:
                img_src = li.find('a', class_='img')
                img_src = img_src.find('img')['data-original'] if img_src and img_src.find('img') else None
                print('img_src',img_src)
                data['img_src']=img_src
                title_div = li.find('div', class_='title')
                title = title_div.find('a')['title'] if title_div and title_div.find('a') else None
                href = title_div.find('a')['href'] if title_div and title_div.find('a') else None
                print('title', title)
                data['title'] = title
                print('href', href)
                data['href'] = href
                address = li.find('div',class_='address')
                position_info=address.find('div',class_='flood').find('div',class_='positionInfo').find('a').get_text()
                print('position_info', position_info)
                data['position_info'] = position_info
                house_info_list = address.find('div', class_='houseInfo').get_text().split('|')
                house_info = ",".join([item.strip() for item in house_info_list])
                print('house_info', house_info)
                data['house_info'] = house_info

                price_info= address.find('div', class_='priceInfo')
                total_price = price_info.find('div', class_='totalPrice totalPrice2').find('span').get_text()
                print('total_price', total_price)
                data['total_price'] = total_price
                unit_price = price_info.find('div', class_='unitPrice').find('span').get_text()
                print('unit_price', unit_price)
                data['unit_price'] = unit_price
                tag_list = address.find('div', class_='tag')
                tag_str =[]
                for i in tag_list:
                    if i.get_text().strip():
                        tag_str.append(i.get_text().strip())
                print('tag_str',tag_str)
                data['tag_str'] = str(tag_str)
                saveMysqlData(data)
            return '解析完成'
        return 'ul_tag解析出错'
    return 'div_tag解析出错'


def saveMysqlData(data):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO t_house (title, img_src, detail_href, position_info, house_info, total_price,unit_price,tag,city,status) \
            VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s, %s)', (
        data['title'],data['img_src'],data['href'],data['position_info'],data['house_info'],data['total_price'],
        data['unit_price'],data['tag_str'],'深圳',0))
    # 提交事务并关闭连接
    conn.commit()
    cursor.close()
    conn.close()
    return '数据保存结束'



def main():
    url ='https://sz.ke.com/ershoufang/'
    # 配置 Chromium 选项，并设置浏览器路径
    # 未显式配置 CHROME_PATH 时交由 DrissionPage 自动探测浏览器
    co = ChromiumOptions()
    if CHROME_PATH:
        co.set_browser_path(CHROME_PATH)
    # 创建 ChromiumPage 实例
    page = ChromiumPage(co)
    try:
        for i in range(1,76):
            if i == 1:
                # 打开指定网页
                page.get(url)
                time.sleep(random.randint(10, 20))
            else :
                url = f'https://sz.ke.com/ershoufang/pg{i}/'
                print("---------"*5)
                print("url:",url)
                page.get(url)
                time.sleep(random.randint(10, 20))
            # 获取网页的文本内容
            page_content = page.html
            result_data = get_content(page_content)

    except Exception as e:
        print(f"发生全局错误: {e}")
    finally:
        # 关闭浏览器
        print(url)
        page.quit()

if __name__ == "__main__":
    main()