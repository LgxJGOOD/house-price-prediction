import time ,os,csv
from ershoufang_app.models import House


def house_export(search):
    # 获取当前时间戳
    timestamp = time.time()
    # 定义 CSV 文件的表头
    headers = ['房屋位置', '房屋信息', '总价', '房屋面积', '房屋房间', '房屋朝向', '房屋层数', '房屋装修', '小区', '所在区域','房屋类型']
    # 获取当前文件所在的目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 CSV 文件的完整路径
    csv_file_path = os.path.join(base_dir, 'data', f'二手房_{timestamp}.csv')
    # 确保 data 目录存在
    os.makedirs(os.path.join(base_dir,'data'), exist_ok=True)

    if search:
        # 根据搜索条件进行过滤查询
        datas  = House.objects.filter(
                city__icontains=search) | House.objects.filter(
                title__icontains=search) | House.objects.filter(
                total_price__icontains=search) | House.objects.filter(
                unit_price__icontains=search)|House.objects.filter(
                position_info__icontains=search).order_by('id')
    else:
        # 如果没有搜索条件，获取所有电影数据
        datas = House.objects.all()

    # 打开文件准备写入
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        # 写入表头
        writer.writeheader()

        # 遍历查询结果，将每条记录写入 CSV 文件
        for data in datas:
            row = {
                '房屋位置': data.position_info,
                '房屋信息': data.house_info,
                '总价': data.total_price ,
                '房屋面积': data.house_area,
                '房屋房间': data.main_info if hasattr(data, 'main_info') else '',
                '房屋朝向': data.house_orientation if hasattr(data, 'house_orientation') else '',
                '房屋层数': data.sub_info if hasattr(data, 'sub_info') else '',
                '房屋装修': data.house_decorate if hasattr(data, 'house_decorate') else '',
                '小区': data.housing_estate if hasattr(data, 'housing_estate') else '',
                '所在区域': data.zone if hasattr(data, 'zone') else '',
                '房屋类型': data.house_type if hasattr(data, 'house_type') else ''
            }
            writer.writerow(row)

    return csv_file_path
