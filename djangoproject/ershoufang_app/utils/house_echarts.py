import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import numpy as np



def house_predict(new_data):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(base_dir, '二手房_clean.csv')
    df = pd.read_csv(csv_file_path)
    df['房屋层数'] = df['房屋层数'].str.strip()
    df = df.drop('房屋朝向', axis=1)

    # 对分类变量进行编码
    le_floor = LabelEncoder()
    le_decoration = LabelEncoder()
    le_zone = LabelEncoder()
    le_type = LabelEncoder()

    df['房屋层数'] = le_floor.fit_transform(df['房屋层数'])
    df['房屋装修'] = le_decoration.fit_transform(df['房屋装修'])
    df['所在区域'] = le_zone.fit_transform(df['所在区域'])
    df['房屋类型'] = le_type.fit_transform(df['房屋类型'])

    df = df.drop(df.columns[0], axis=1)
    X = df.drop('总价', axis=1)
    # 保存列名
    columns = X.columns
    y = df['总价']

    # 使用均值填充缺失值
    imputer = SimpleImputer(strategy='mean')
    # X = imputer.fit_transform(X)
    X = pd.DataFrame(imputer.fit_transform(X), columns=columns)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 创建并训练随机森林回归模型
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    # 在测试集上进行预测
    y_pred = model.predict(X_test)

    # 计算模型的评估指标
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f'均方误差: {mse}')
    print(f'R2 分数: {r2}')

    # 对传入的新数据中的分类变量进行编码
    new_data_encoded = new_data.copy()
    try:
        new_data_encoded[2] = le_floor.transform([new_data[2]])[0]
        new_data_encoded[3] = le_decoration.transform([new_data[3]])[0]
        new_data_encoded[4] = le_zone.transform([new_data[4]])[0]
        new_data_encoded[5] = le_type.transform([new_data[5]])[0]
    except ValueError as e:
        print(f"错误: {e}，新数据包含训练数据中未见过的标签。")
        return None

    # 将新数据转换为 DataFrame 并进行预测
    new_data_df = pd.DataFrame([new_data_encoded[1:]], columns=columns)
    predicted_price = model.predict(new_data_df)
    return predicted_price[0]


from ershoufang_app.models import House

def get_zone_num():
    house_queryset = House.objects.all()
    # 将查询集转换为字典列表
    house_list = list(house_queryset.values())
    # 将字典列表转换为 DataFrame
    house_df = pd.DataFrame(house_list)
    house_df['zone'] = house_df['zone'].str.split().str[0]
    zone_num = house_df.groupby('zone').size().reset_index(name='count')
    # 按数量从高到矮排序
    zone_num = zone_num.sort_values('count', ascending=False)
    
    # 转换为饼图数据格式
    pie_data = [
        {"value": row['count'], "name": row['zone']}
        for _, row in zone_num.iterrows()
    ]
    
    echarts_data = {
        'tooltip': {
            'trigger': 'item',
            'formatter': '{a} <br/>{b}: {c}套 ({d}%)'
        },
        'legend': {
            'type': 'scroll',
            'top': '5%',
            'left': 'center'
        },
        'series': [
            {
                'name': '各区域房源数量分布',
                'type': 'pie',
                'radius': ['40%', '70%'],
                'avoidLabelOverlap': False,
                'itemStyle': {
                    'borderRadius': 10,
                    'borderColor': '#fff',
                    'borderWidth': 2
                },
                'label': {
                    'show': False,
                    'position': 'center'
                },
                'emphasis': {
                    'label': {
                        'show': True,
                        'fontSize': 30,
                        'fontWeight': 'bold'
                    }
                },
                'labelLine': {
                    'show': False
                },
                'data': pie_data
            }
        ]
    }
    return echarts_data


def get_avg_price_per_zone():
    house_queryset = House.objects.all()
    # 将查询集转换为字典列表
    house_list = list(house_queryset.values())
    # 将字典列表转换为 DataFrame
    house_df = pd.DataFrame(house_list)
    house_df['zone'] = house_df['zone'].str.split().str[0]
    # 按照 zone 列分组并计算 total_price 列的平均值
    avg_price_per_zone = house_df.groupby('zone')['total_price'].mean().round(2).reset_index(name='avg_price')
    
    # 为每个区域生成不同的颜色
    colors = [
        '#5470C6', '#91CC75', '#FAC858', '#EE6666', '#73C0DE',
        '#3BA272', '#FC8452', '#9A60B4', '#EA7CCC', '#4DB4A8'
    ]
    
    echarts_data = {
        'toolbox': {
            'feature': {
                'saveAsImage': {},
                'dataView': {},
                'restore': {},
                'dataZoom': {},
                'magicType': {
                    'type': ['bar', 'line']
                }
            }
        },
        'xAxis': {
            'type': 'category',
            'data': avg_price_per_zone['zone'].tolist(),
            'axisLabel': {
                'rotate': 30,  # 旋转 30 度显示
                'interval': 'auto'  # 自动调整间隔
            }
        },
        'yAxis': {
            'type': 'value',
            'name': '房价（万元）',
            'axisLabel': {
                'formatter': '{value}',
                'interval': 'auto'
            },
            'minInterval': 1  # 最小间隔为 1，确保都是整数
        },
        'tooltip': {
            'backgroundColor': 'rgba(0, 0, 0, 0.1)',
            'borderColor': '#333',
            'trigger': 'axis',
            'axisPointer': {
                'type': 'shadow'
            },
            'formatter': '{b}: {c}万元'
        },
        'legend': {
            'data': avg_price_per_zone['zone'].tolist(),
            'top': 'bottom'
        },
        'series': [
            {
                'name': '各区域平均房价',
                'data': [
                    {
                        'value': row['avg_price'],
                        'itemStyle': {'color': colors[i % len(colors)]},
                        'name': row['zone']
                    }
                    for i, (_, row) in enumerate(avg_price_per_zone.iterrows())
                ],
                'type': 'bar',
                'smooth': 'true',
                'markPoint': {
                    'data': [
                        {'type': 'max', 'name': '最大值'},
                        {'type': 'min', 'name': '最小值'}
                    ]
                },
                'markLine': {
                    'data': [{'type': 'average', 'name': '平均值'}]
                },
            }
        ]
    }
    return echarts_data


def get_zone_price_analysis(zone_name):
    """
    获取指定区域的价格分析数据
    包括：价格分布直方图、平均总价、最高总价、最低总价
    """
    house_queryset = House.objects.all()
    house_list = list(house_queryset.values())
    house_df = pd.DataFrame(house_list)
    
    # 筛选指定区域的数据
    zone_data = house_df[house_df['zone'].str.contains(zone_name, na=False)]
    
    if zone_data.empty or 'total_price' not in zone_data.columns:
        return {
            'chart': None,
            'stats': {
                'avg_price': 0,
                'max_price': 0,
                'min_price': 0
            }
        }
    
    # 过滤掉总价为 0、负数或低于 10 万的无效数据
    prices = zone_data[(zone_data['total_price'] >= 10)]['total_price'].dropna()
    
    if prices.empty:
        return {
            'chart': None,
            'stats': {
                'avg_price': 0,
                'max_price': 0,
                'min_price': 0
            }
        }
    
    # 计算统计信息
    avg_price = round(prices.mean(), 2)
    max_price = round(prices.max(), 2)
    min_price = round(prices.min(), 2)
    
    # 创建价格分布直方图
    # 自动设置价格区间
    price_range = max_price - min_price
    if price_range <= 50:
        bin_size = 10
    elif price_range <= 100:
        bin_size = 20
    elif price_range <= 200:
        bin_size = 30
    elif price_range <= 500:
        bin_size = 50
    else:
        bin_size = 100
    
    # 生成 bins
    bins = []
    current = min_price
    while current < max_price:
        bins.append(round(current, 2))
        current += bin_size
    bins.append(round(max_price + bin_size, 2))
    
    # 统计每个区间的数量
    hist_data = np.histogram(prices, bins=bins)
    bin_labels = []
    for i in range(len(hist_data[1]) - 1):
        label = f"{hist_data[1][i]:.0f}-{hist_data[1][i+1]:.0f}万"
        bin_labels.append(label)
    
    echarts_data = {
        'toolbox': {
            'feature': {
                'saveAsImage': {},
                'dataView': {},
                'restore': {},
                'dataZoom': {},
                'magicType': {
                    'type': ['bar', 'line']
                }
            }
        },
        'xAxis': {
            'type': 'category',
            'data': bin_labels,
            'axisLabel': {
                'rotate': 45,
                'interval': 'auto'
            }
        },
        'yAxis': {
            'type': 'value',
            'name': '房源数量',
            'axisLabel': {
                'formatter': '{value}',
                'interval': 'auto'
            },
            'minInterval': 1  # 最小间隔为 1，确保都是整数
        },
        'tooltip': {
            'backgroundColor': 'rgba(0, 0, 0, 0.1)',
            'borderColor': '#333',
            'trigger': 'axis',
            'axisPointer': {
                'type': 'shadow'
            },
            'formatter': '{b}：{c}套'
        },
        'series': [
            {
                'name': '房源数量',
                'data': hist_data[0].tolist(),
                'type': 'bar',
                'smooth': True,
                'itemStyle': {
                    'color': '#409F03'
                },
                'markLine': {
                    'data': [{'type': 'average', 'name': '平均值'}]
                },
            }
        ]
    }
    
    return {
        'chart': echarts_data,
        'stats': {
            'avg_price': avg_price,
            'max_price': max_price,
            'min_price': min_price
        }
    }


def get_sub_info_num():
    house_queryset = House.objects.all()
    # 将查询集转换为字典列表
    house_list = list(house_queryset.values())
    # 将字典列表转换为 DataFrame
    house_df = pd.DataFrame(house_list)
    house_df['sub_info'] = house_df['sub_info'].str.split('/').str[0]
    sub_info_num = house_df.groupby('sub_info').size().reset_index(name='count')
    echarts_data = {
        'toolbox': {
            'feature': {
                'saveAsImage': {},
                'dataView': {},
                'restore': {},
                'dataZoom': {},
                'magicType': {
                    'type': ['bar', 'line']
                }
            }
        },
        'xAxis': {
            'type': 'category',
            'data': sub_info_num['sub_info']
        },
        'yAxis': {
            'type': 'value',
            'name': '数量（套）'
        },
        'tooltip': {
            'backgroundColor': 'rgba(0, 0, 0, 0.1)',
            'borderColor': '#333',
            'trigger': 'axis',
            'axisPointer': {
                'type': 'shadow'
            },
            'formatter': '{b}: {c}套'
        },
        'series': [
            {
                'data': sub_info_num['count'],
                'type': 'bar',
                'smooth': 'true',
                'markPoint': {
                    'data': [
                        {'type': 'max', 'name': '最大值'},
                        {'type': 'min', 'name': '最小值'}
                    ]
                },
                'markLine': {
                    'data': [{'type': 'average', 'name': '平均值'}]
                },
            }
        ]
    }
    return echarts_data

def get_year_zone():
    house_queryset = House.objects.all()
    # 将查询集转换为字典列表
    house_list = list(house_queryset.values())
    # 将字典列表转换为 DataFrame
    house_df = pd.DataFrame(house_list)

    # 提取年份信息
    def extract_year(year_str):
        if pd.notnull(year_str) and isinstance(year_str, str):
            if '/' in year_str:
                parts = year_str.split('/')
                return parts[0].strip()
            else:
                return '未知'
        return '未知'

    house_df['year'] = house_df['house_type'].apply(extract_year)
    house_df.loc[:, 'year'] = house_df['year'].str.replace('年建', '')
    # 按照年份分组统计数量
    year_count = house_df.groupby('year').size().reset_index(name='count')
    
    echarts_data = {
        'toolbox': {
            'feature': {
                'saveAsImage': {},
                'dataView': {},
                'restore': {},
                'dataZoom': {},
                'magicType': {
                    'type': ['bar', 'line']
                }
            }
        },
        'xAxis': {
            'type': 'category',
            'axisLabel': {
                'rotate': 45,
                'interval': 0,  # 强制显示所有标签
                'fontSize': 11,
                'fontWeight': 'bold'
            },
            'data': year_count['year']
        },
        'yAxis': {
            'type': 'value',
            'name': '数量（套）',
            'nameTextStyle': {
                'fontSize': 13,
                'fontWeight': 'bold'
            }
        },
        'tooltip': {
            'backgroundColor': 'rgba(0, 0, 0, 0.8)',
            'borderColor': '#333',
            'trigger': 'axis',
            'axisPointer': {
                'type': 'shadow'
            },
            'formatter': '{b}年：{c}套',
            'textStyle': {
                'fontSize': 13
            }
        },
        'grid': {
            'left': '3%',
            'right': '4%',
            'bottom': '10%',
            'containLabel': True
        },
        'series': [
            {
                'data': year_count['count'],
                'type': 'bar',
                'smooth': 'true',
                'itemStyle': {
                    'color': '#a90000'
                },
                'barWidth': '60%',
                'label': {
                    'show': True,
                    'position': 'top',
                    'fontSize': 11
                },
                'markPoint': {
                    'data': [
                        {'type': 'max', 'name': '最大值'},
                        {'type': 'min', 'name': '最小值'}
                    ]
                },
                'markLine': {
                    'data': [{'type': 'average', 'name': '平均值'}]
                },
            }
        ]
    }
    return echarts_data


def get_house_area():
    # 初始化各区间的计数
    above_120 = 0
    between_100_and_120 = 0
    between_80_and_100 = 0
    between_60_and_80 = 0
    below_60 =0
    for info in House.objects.all():
        try:
            if info.house_area is not None:
                area = float(info.house_area.replace('平米', ''))
            else:
                area =0
            if area > 120:
                above_120 += 1
            elif 100<= area <= 120:
                between_100_and_120 += 1
            elif 80 <= area <= 100:
                between_80_and_100 += 1
            elif 60 <= area <= 80:
                between_60_and_80 += 1
            else:
                below_60 += 1
        except ValueError:
            continue
    echarts_data = {
        'title': {
            'text': '九江市房屋面积分析',
            'left': 'center'
        },
        'toolbox': {
            'feature': {
                'saveAsImage': {},
                'dataView': {},
                'restore': {},
                'dataZoom': {},
                'magicType': {
                    'type': ['bar', 'line']
                }
            }
        },
        "xAxis": {
            "type": "category",
            "data": ["120 平米以上", "100-120 平米", "80-100 平米", "60-80 平米","60 平米以下"]
        },
        "yAxis": {
            "type": "value",
            "name": "数量（套）"
        },
        'tooltip': {
            'backgroundColor': 'rgba(0, 0, 0, 0.1)',
            'borderColor': '#337ab7',
            'trigger': 'axis',
            'axisPointer': {
                'type': 'shadow'
            },
            'formatter': '{b}: {c}套'
        },
        "series": [
            {
                "data": [above_120, between_100_and_120, between_80_and_100,between_60_and_80, below_60],
                "type": "bar",
                'smooth': 'true',
                'itemStyle': {
                    'color': '#409F03'
                },
                'markPoint': {
                    'data': [
                        {'type': 'max', 'name': '最大值'},
                        {'type': 'min', 'name': '最小值'}
                    ]
                },
                'markLine': {
                    'data': [{'type': 'average', 'name': '平均值'}]
                },
            }
        ]
    }
    return echarts_data




def pie_get_zone_num():
    house_queryset = House.objects.all()
    # 将查询集转换为字典列表
    house_list = list(house_queryset.values())
    # 将字典列表转换为 DataFrame
    house_df = pd.DataFrame(house_list)
    house_df['zone'] = house_df['zone'].str.split().str[0]
    zone_num = house_df.groupby('zone').size().reset_index(name='count')
    data = [
        {
            "value": row['count'],
            "name": row['zone']
        }
        for _, row in zone_num.iterrows()
    ]
    echarts_data = {
        'tooltip': {
            'trigger': 'item',
            'formatter': '{a} <br/>{b}: {c} ({d}%)'
        }, 'legend': {
            'top': '5%',
            'left': 'center'
        },
        'series': [
            {
                'name': '不同区域的二手房数量占比',
                'type': 'pie',
                'radius': ['40%', '70%'],
                'avoidLabelOverlap': 'false',
                'itemStyle': {
                    'borderRadius': 10,
                    'borderColor': '#fff',
                    'borderWidth': 2
                },
                'label': {
                    'show': 'false',
                    'position': 'center'
                },
                'emphasis': {
                    'label': {
                        'show': 'true',
                        'fontSize': 40,
                        'fontWeight': 'bold'
                    }
                },
                'labelLine': {
                    'show': 'false'
                },
                'data': data
            }
        ]
    }
    return echarts_data



def pie_get_house_area():
    # 初始化各区间的计数
    above_120 = 0
    between_100_and_120 = 0
    between_80_and_100 = 0
    between_60_and_80 = 0
    below_60 = 0
    for info in House.objects.all():
        try:
            if info.house_area is not None:
                area = float(info.house_area.replace('平米', ''))
            else:
                area = 0
            if area > 120:
                above_120 += 1
            elif 100 <= area <= 120:
                between_100_and_120 += 1
            elif 80 <= area <= 100:
                between_80_and_100 += 1
            elif 60 <= area <= 80:
                between_60_and_80 += 1
            else:
                below_60 += 1
        except ValueError:
            continue
    data = [{"value": above_120, "name": "120 平米以上"} ,
            {"value": between_100_and_120, "name": "100-120 平米"},
            {"value": between_80_and_100, "name": "80-100 平米"},
            {"value": between_60_and_80, "name": "60-80 平米"},
            {"value": below_60, "name": "60 平米以下"}
            ]
    echarts_data = {
        'tooltip': {
            'trigger': 'item',
            'formatter': '{a} <br/>{b}: {c} ({d}%)'
        }, 'legend': {
            'top': '5%',
            'left': 'center'
        },
        'series': [
            {
                'name': '房屋面积占比',
                'type': 'pie',
                'radius': ['40%', '70%'],
                'avoidLabelOverlap': 'false',
                'itemStyle': {
                    'borderRadius': 10,
                    'borderColor': '#fff',
                    'borderWidth': 2
                },
                'label': {
                    'show': 'false',
                    'position': 'center'
                },
                'emphasis': {
                    'label': {
                        'show': 'true',
                        'fontSize': 40,
                        'fontWeight': 'bold'
                    }
                },
                'labelLine': {
                    'show': 'false'
                },
                'data': data
            }
        ]
    }
    return echarts_data


def get_house_type_distribution():
    """
    获取户型分布数据
    从 house_info 字段提取户型信息（如 2 室 1 厅、3 室 2 厅等）
    """
    house_queryset = House.objects.all()
    house_list = list(house_queryset.values())
    house_df = pd.DataFrame(house_list)
    
    # 从 house_info 中提取户型信息
    def extract_house_type(info):
        if pd.isna(info) or not info:
            return '未知'
        
        import re
        info_str = str(info)
        
        # 尝试匹配 "X 室 Y 厅" 格式（最标准）
        match = re.search(r'(\d+)\s*室\s*(\d+)\s*厅', info_str)
        if match:
            rooms = match.group(1)
            halls = match.group(2)
            return f"{rooms}室{halls}厅"
        
        # 尝试匹配 "X 室" 格式（只有室没有厅）
        match = re.search(r'(\d+)\s*室', info_str)
        if match:
            return f"{match.group(1)}室"
        
        # 尝试匹配 "X 厅" 格式（只有厅没有室）
        match = re.search(r'(\d+)\s*厅', info_str)
        if match:
            return f"{match.group(1)}厅"
        
        # 尝试匹配中文数字格式
        chinese_num_map = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', 
                          '六': '6', '七': '7', '八': '8', '九': '9', '十': '10'}
        
        match = re.search(r'([一二三四五六七八九十])\s*室\s*([一二三四五六七八九十])\s*厅', info_str)
        if match:
            rooms = chinese_num_map.get(match.group(1), match.group(1))
            halls = chinese_num_map.get(match.group(2), match.group(2))
            return f"{rooms}室{halls}厅"
        
        # 如果都没有匹配到，返回原始信息的前 20 个字符作为调试
        return info_str[:20] if len(info_str) > 20 else info_str
    
    house_df['house_type_simple'] = house_df['house_info'].apply(extract_house_type)
    
    # 统计各户型数量
    type_count = house_df.groupby('house_type_simple').size().reset_index(name='count')
    type_count = type_count.sort_values('count', ascending=False)
    
    # 转换为饼图数据格式
    data = [
        {"value": row['count'], "name": row['house_type_simple']}
        for _, row in type_count.iterrows()
    ]
    
    echarts_data = {
        'tooltip': {
            'trigger': 'item',
            'formatter': '{a} <br/>{b}: {c}套 ({d}%)'
        },
        'legend': {
            'type': 'scroll',
            'top': '5%',
            'left': 'center'
        },
        'series': [
            {
                'name': '户型分布',
                'type': 'pie',
                'radius': ['40%', '70%'],
                'avoidLabelOverlap': False,
                'itemStyle': {
                    'borderRadius': 10,
                    'borderColor': '#fff',
                    'borderWidth': 2
                },
                'label': {
                    'show': False,
                    'position': 'center'
                },
                'emphasis': {
                    'label': {
                        'show': True,
                        'fontSize': 30,
                        'fontWeight': 'bold'
                    }
                },
                'labelLine': {
                    'show': False
                },
                'data': data
            }
        ]
    }
    return echarts_data


def get_orientation_distribution():
    """
    获取房屋朝向分布数据
    """
    house_queryset = House.objects.all()
    house_list = list(house_queryset.values())
    house_df = pd.DataFrame(house_list)
    
    # 统计各朝向数量
    orientation_count = house_df.groupby('house_orientation').size().reset_index(name='count')
    orientation_count = orientation_count.sort_values('count', ascending=False)
    
    # 转换为饼图数据格式
    data = [
        {"value": row['count'], "name": row['house_orientation']}
        for _, row in orientation_count.iterrows()
    ]
    
    echarts_data = {
        'tooltip': {
            'trigger': 'item',
            'formatter': '{a} <br/>{b}: {c}套 ({d}%)'
        },
        'legend': {
            'type': 'scroll',
            'top': '5%',
            'left': 'center'
        },
        'series': [
            {
                'name': '朝向分布',
                'type': 'pie',
                'radius': ['40%', '70%'],
                'avoidLabelOverlap': False,
                'itemStyle': {
                    'borderRadius': 10,
                    'borderColor': '#fff',
                    'borderWidth': 2
                },
                'label': {
                    'show': False,
                    'position': 'center'
                },
                'emphasis': {
                    'label': {
                        'show': True,
                        'fontSize': 30,
                        'fontWeight': 'bold'
                    }
                },
                'labelLine': {
                    'show': False
                },
                'data': data
            }
        ]
    }
    return echarts_data


def get_feature_options():
    """
    获取所有特征选项，用于前端动态加载下拉框
    从数据库中自动提取所有出现过的特征值
    """
    import pandas as pd
    
    house_queryset = House.objects.all()
    house_list = list(house_queryset.values())
    
    if not house_list:
        # 如果数据库没有数据，返回默认选项
        return {
            'floors': ['低楼层', '中楼层', '高楼层'],
            'building_types': ['板楼', '塔楼', '板塔结合'],
            'decorate_types': ['毛坯', '简装', '精装', '豪装'],
            'zones': ['浔阳区', '濂溪区', '八里湖新区', '开发区', '柴桑区'],
            'orientations': ['南', '北', '南北', '东', '东南', '西南', '东西', '西北']
        }
    
    house_df = pd.DataFrame(house_list)
    
    # 提取楼层选项 (从 house_info 或 sub_info 字段)
    floors = set()
    if 'house_info' in house_df.columns:
        for info in house_df['house_info'].dropna():
            if '高层' in str(info) or '高楼层' in str(info):
                floors.add('高楼层')
            elif '中层' in str(info) or '中楼层' in str(info):
                floors.add('中楼层')
            elif '低层' in str(info) or '低楼层' in str(info):
                floors.add('低楼层')
    
    if not floors:
        floors = {'低楼层', '中楼层', '高楼层'}
    
    # 提取建筑类型 (从 sub_info 字段)
    building_types = set()
    if 'sub_info' in house_df.columns:
        for info in house_df['sub_info'].dropna():
            if '板楼' in str(info):
                building_types.add('板楼')
            elif '塔楼' in str(info):
                building_types.add('塔楼')
            elif '板塔结合' in str(info):
                building_types.add('板塔结合')
    
    if not building_types:
        building_types = {'板楼', '塔楼', '板塔结合'}
    
    # 提取装修类型
    decorate_types = set()
    if 'house_decorate' in house_df.columns:
        decorate_types = set(house_df['house_decorate'].dropna().unique())
    
    if not decorate_types:
        decorate_types = {'毛坯', '简装', '精装', '豪装'}
    
    # 提取区域
    zones = set()
    if 'zone' in house_df.columns:
        zones = set(house_df['zone'].dropna().unique())
    
    if not zones:
        zones = {'浔阳区', '濂溪区', '八里湖新区', '开发区', '柴桑区'}
    
    # 提取朝向
    orientations = set()
    if 'house_orientation' in house_df.columns:
        orientations = set(house_df['house_orientation'].dropna().unique())
    
    if not orientations:
        orientations = {'南', '北', '南北', '东', '东南', '西南', '东西', '西北'}
    
    return {
        'floors': sorted(list(floors)),
        'building_types': sorted(list(building_types)),
        'decorate_types': sorted(list(decorate_types)),
        'zones': sorted(list(zones)),
        'orientations': sorted(list(orientations))
    }


# ========== 使用真实的机器学习模型进行预测 ==========
# 加载模型和编码器（全局变量，只加载一次）
_model = None
_encoders = None

def load_house_price_model():
    """
    加载训练好的随机森林模型和编码器
    使用懒加载方式，只在第一次调用时加载
    """
    global _model, _encoders
    if _model is None or _encoders is None:
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_dir, 'random_forest_house_price_model.pkl')
            encoders_path = os.path.join(base_dir, 'label_encoders.pkl')
            
            print(f"正在加载模型：{model_path}")
            _model = joblib.load(model_path)
            _encoders = joblib.load(encoders_path)
            print("模型加载成功!")
            
            # 打印编码器信息
            if 'zone' in _encoders:
                zone_encoder = _encoders['zone']
                print(f"区域编码器：{len(zone_encoder.classes_)} 个区域")
            if 'decorate_order' in _encoders:
                print(f"装修编码器：{_encoders['decorate_order']}")
            if 'orientation' in _encoders:
                print(f"朝向编码器：{_encoders['orientation']}")
            if 'building_type' in _encoders:
                print(f"建筑类型编码器：{_encoders['building_type']}")
                
        except Exception as e:
            print(f"模型加载失败：{e}")
            raise
    return _model, _encoders


def predict_house_price_with_ml(area, rooms, halls, floor, decorate, zone, orientation, build_year, building_type):
    """
    使用训练好的随机森林模型进行房价预测
    
    参数:
        area: 房屋面积（平米）
        rooms: 室
        halls: 厅
        floor: 楼层（低楼层/中楼层/高楼层）
        decorate: 装修程度（毛坯/简装/精装/豪装）
        zone: 区域（浔阳区/濂溪区/八里湖新区/开发区/柴桑区）
        orientation: 朝向（南/北/南北/东/东南/西南/东西/西北）
        build_year: 建造年份
        building_type: 建筑类型（板楼/塔楼/板塔结合）
    
    返回:
        预测价格（万元）
    """
    try:
        # 加载模型
        model, encoders = load_house_price_model()
        
        # 1. 区域编码
        zone_encoder = encoders.get('zone', None)
        if zone_encoder is None:
            raise ValueError("区域编码器未找到")
        
        if zone not in zone_encoder.classes_:
            # 如果区域不在训练集中，使用最常见的区域
            print(f"警告：区域 '{zone}' 不在训练集中，使用默认值")
            zone_encoded = 0
        else:
            zone_encoded = zone_encoder.transform([zone])[0]
        
        # 2. 装修程度编码
        decorate_order_map = encoders.get('decorate_order', None)
        if decorate_order_map is None:
            # 如果没有编码器，使用默认映射
            decorate_mapping = {'毛坯': 0, '简装': 1, '精装': 2, '豪装': 3}
            decorate_level = decorate_mapping.get(decorate, 1)
        else:
            decorate_level = decorate_order_map.get(decorate, 1)
        
        # 3. 朝向评分
        orientation_score_map = encoders.get('orientation', None)
        if orientation_score_map is None:
            # 如果没有编码器，使用默认评分
            orientation_mapping = {
                '南北': 3.0, '东南': 2.5, '南': 2.0, '东': 1.5,
                '北': 1.0, '西南': 1.5, '东西': 1.0, '西北': 1.0
            }
            orientation_score = orientation_mapping.get(orientation, 1.0)
        else:
            orientation_score = orientation_score_map.get(orientation, 1.0)
        
        # 4. 计算房龄
        current_year = 2025
        house_age = current_year - build_year
        
        # 5. 楼层编码
        floor_mapping = {'低楼层': 1, '中楼层': 2, '高楼层': 3}
        floor_encoded = floor_mapping.get(floor, 2)
        
        # 6. 建筑类型编码
        building_type_map = encoders.get('building_type', None)
        if building_type_map is None:
            building_type_mapping = {'板楼': 0, '塔楼': 1, '板塔结合': 2}
            building_type_encoded = building_type_mapping.get(building_type, 0)
        else:
            building_type_encoded = building_type_map.get(building_type, 0)
        
        # 7. 构建特征向量（顺序必须与训练时一致）
        # 训练时的特征顺序：
        # house_area, rooms, halls, decorate_level, zone_encoded, 
        # orientation_score, house_age, floor_level, building_type_encoded
        features = np.array([[
            float(area),           # 0. 房屋面积
            int(rooms),            # 1. 室
            int(halls),            # 2. 厅
            decorate_level,        # 3. 装修程度
            zone_encoded,          # 4. 区域
            orientation_score,     # 5. 朝向评分
            house_age,             # 6. 房龄
            floor_encoded,         # 7. 楼层
            building_type_encoded  # 8. 建筑类型
        ]])
        
        # 8. 进行预测
        prediction = model.predict(features)
        predicted_price = prediction[0]
        
        # 9. 确保预测值为正数
        if predicted_price < 0:
            predicted_price = abs(predicted_price)
        
        return round(predicted_price, 2)
        
    except Exception as e:
        print(f"预测失败：{e}")
        import traceback
        traceback.print_exc()
        raise
