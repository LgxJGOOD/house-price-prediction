import  requests
from bs4 import BeautifulSoup


def getHTMLtext(url,name):
    """请求获得网页内容"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "cookie":"lianjia_ssid=375ae2ab-24dc-4e2c-af85-87e6efe5f6b9; lianjia_uuid=70b87f5d-391b-4452-bb4e-edd6eb4635e0; Hm_lvt_b160d5571570fd63c347b9d4ab5ca610=1742888397; HMACCOUNT=B2C311E369CCFC34; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22195cc3e6b7f1d8-007e0810895129-26011d51-1338645-195cc3e6b80f4e%22%2C%22%24device_id%22%3A%22195cc3e6b7f1d8-007e0810895129-26011d51-1338645-195cc3e6b80f4e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; select_city=310000; digv_extends=%7B%22utmTrackId%22%3A%22%22%7D; crosSdkDT2019DeviceId=pqypwv--w7n6e1-fw5jkwd85wffrex-9aflexhe3; _ga=GA1.2.408989864.1742888660; _gid=GA1.2.1373226035.1742888660; login_ucid=2000000474530487; lianjia_token=2.00133a462345f9e97802976f12614cdc6d; lianjia_token_secure=2.00133a462345f9e97802976f12614cdc6d; security_ticket=XcC1XEnh9317XxRpnBdGfJZDpOpb69rijr+5+bfxtepOW/VIwhs1A4ninP9Q55bQb3s7zln4kAopqfwpYB/CWBZDl6IaDuPz6TaKnp21TUfc+BsBsHgArmhYKMcg+xF+aKFX4ueOmsul75czKtmD8xFV+rHzT8MfCwptnfAV1vQ=; Hm_lpvt_b160d5571570fd63c347b9d4ab5ca610=1742889172; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMGVmNjhkMWY1YjIyODc3ZDE0NDc3ZTMyOTVmMjk4ODg5NzM1YjA0YmQ5ODQ4MGIwMDM0ZTQ1MWI3MjEyNGNmYWQ2NDg5NDNjZWU0NjdkNGQ0ZjhiMzY1YTM5NTJlZDgzMDZkMWNiM2VmMzcwMDEwYWZjZDA4MTZmNGQxN2MwNDE2NzZhMjlhZDgzOTJkYTUzNWFhMjgzZWY3ZjRlZmUwNWRkM2E5ZDVmNzE3Nzk3ZjU4ZmY3NmUyZGNmYTA5MDhjMTFmMzk0NThlYTA0NmI1NTkyNTE3MzZmNzNjYTdhOGFmZGY5NmIyMWU4NTJmMWFlYWJhZTU3NjUwZjA2ZDMwNThlOGJmYTQ1MGMxYmFkZjNkNGMxNjJkNzdjZDM0YmQxZmYxOWJhZmI1ZDdkN2Y4NWE4YTVkYmQ4MWUyZjNmNGRcIixcImtleV9pZFwiOlwiMVwiLFwic2lnblwiOlwiNjQxMWY3ZTZcIn0iLCJyIjoiaHR0cHM6Ly9zaC5rZS5jb20vZXJzaG91ZmFuZy8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ=="  }
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print("成功访问", url)
        ##保存到txt
        with open(f"{name}.txt", "w", encoding="utf-8") as f:
            f.write(r.text)
        return r.text
    except:
        print("访问错误")
        return False


from bs4 import BeautifulSoup

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

if __name__ =="__main__":
    name = '深圳_2'
    url ='https://sz.ke.com/ershoufang/105120148402.html'
    # getHTMLtext(url, name)
    with open("深圳_2.txt", "r", encoding="utf-8") as f:
        html = f.read()

    get_content_detail(html)