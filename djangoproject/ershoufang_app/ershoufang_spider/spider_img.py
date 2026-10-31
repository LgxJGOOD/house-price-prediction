
import  requests
import uuid
import hashlib
import os,time,csv
from django.conf import settings


def save_img(url):
    new_name = get_random_str()
    file_path = os.path.join(settings.IMG_FILE, new_name + '.jpg')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        # 保存图片到本地，文件名可以根据需求修改
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print("图片保存成功")
        path_file = 'http://127.0.0.1:8899/upload/img/'+new_name + '.jpg'
        return   path_file
    else:
        print(f"请求失败，状态码: {response.status_code}")

def get_random_str():
        uuid_val = uuid.uuid4()
        uuid_str = str(uuid_val).encode('utf-8')
        md5_obj = hashlib.md5()
        md5_obj.update(uuid_str)
        return md5_obj.hexdigest()