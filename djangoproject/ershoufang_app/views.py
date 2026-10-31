from rest_framework.views import APIView
from .models import House
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from django.db import transaction
import time
from ershoufang_app.ershoufang_spider.spider_img import save_img
from .utils.house import  *
from .utils.house_echarts import  *

class HouseListView(APIView):
    """获取所有城市"""
    def get(self, request):
        search = request.GET.get('search', '')
        page_size = int(request.GET.get('pagesize', 5))
        page_num = int(request.GET.get('pagenum', 1))
        if search:
            queryset = House.objects.filter(
                city__icontains=search) | House.objects.filter(
                title__icontains=search) | House.objects.filter(
                total_price__icontains=search) | House.objects.filter(
                unit_price__icontains=search)|House.objects.filter(
                position_info__icontains=search).order_by('id')
        else:
            queryset = House.objects.all().order_by('id')
        paginator = Paginator(queryset, page_size)
        try:
            datas_page = paginator.page(page_num)
        except PageNotAnInteger:
            datas_page = paginator.page(1)
        except EmptyPage:
            datas_page = paginator.page(paginator.num_pages)
        datas_data = [
            {
                'id': item.id,
                'city': item.city,
                'title': item.title,
                'img_src': item.img_src,
                'detail_href': item.detail_href,
                'position_info': item.position_info,
                'house_info': item.house_info,
                'total_price': item.total_price,
                'unit_price': item.unit_price,
                'tag': item.tag,
                'house_area':item.house_area,
                'house_orientation': item.house_orientation,
                'house_decorate': item.house_decorate,


            }
            for item in datas_page
        ]
        response_data = {
            'count': paginator.count,  # 总记录数
            'num_pages': paginator.num_pages,  # 总页数
            'results': datas_data,  # 当前页的数据
        }
        return Response({"code": 200, "message": "请求成功", "data": response_data})


class SpiderDataImgView(APIView):
    def get(self, request):
        try:
            music_data = House.objects.exclude(img_src__contains='http://127.0.0.1:8899/upload/img')[:20]
            with transaction.atomic():
                for data in music_data:
                    if 'http://127.0.0.1:8899/upload/img' in data.img_src:
                        continue
                    else:
                        local_path = save_img(data.img_src)
                        if local_path:
                            data.img_src = local_path
                            data.save()
                            print(f"图片 {local_path} 下载并更新成功，{data.title},{data.id}")
                            time.sleep(1)
                        else:
                            print(f"图片 {data.img_src} 下载失败")
            return Response({"code": 200, "message": "图片下载完成"})
        except Exception as e:
            return Response({"code": 500, "message": f"发生错误: {str(e)}"})


class ExportHouseCSV(APIView):
    def get(self, request):
        search = request.GET.get('search', '')
        csv_file_path = house_export(search)
        return Response({  "code": 200,
            "message": f"文件保存路径{csv_file_path}"})


class EhartsView(APIView):
    def get(self, request):
        lx = request.GET.get('lx', '')
        if lx == "0":
            data = get_zone_num()
            return Response({"code": 200, "message": "查询成功", "data": data})
        elif lx == "1":
            data= get_avg_price_per_zone()
            return Response({"code": 200, "message": "查询成功", "data": data})
        if lx == "2":
            # 使用真实的机器学习模型进行预测
            from ershoufang_app.utils.house_echarts import predict_house_price_with_ml
            
            try:
                # 获取前端传递的参数
                area = float(request.GET.get('area', '100').strip())
                rooms = int(request.GET.get('room2', '3').strip())
                halls = int(request.GET.get('room1', '1').strip())
                floor = request.GET.get('floor', '中楼层').strip()
                decorate = request.GET.get('zhuangxiu', '简装').strip()
                zone = request.GET.get('zone', '浔阳区').strip()
                orientation = request.GET.get('orientation', '南北').strip()  # 新增朝向参数
                build_year = int(request.GET.get('year', '2015').strip())
                building_type = request.GET.get('floor1', '板楼').strip()
                
                # 调用机器学习模型预测函数
                predicted_price = predict_house_price_with_ml(
                    area=area,
                    rooms=rooms,
                    halls=halls,
                    floor=floor,
                    decorate=decorate,
                    zone=zone,
                    orientation=orientation,
                    build_year=build_year,
                    building_type=building_type
                )
                
                data = f"{predicted_price}万"
                return Response({"code": 200, "message": "预测成功", "data": data})
                
            except Exception as e:
                print(f"预测发生错误：{e}")
                import traceback
                traceback.print_exc()
                return Response({"code": 500, "message": f"预测失败：{str(e)}"})
        elif lx == "3":
            data = get_year_zone()
            return Response({"code": 200, "message": "查询成功", "data": data})
        elif lx == "4":
            data = get_sub_info_num()
            return Response({"code": 200, "message": "查询成功", "data": data})
        elif lx == "5":
            data = get_house_area()
            return Response({"code": 200, "message": "查询成功", "data": data})
        elif lx == "6":
            data = pie_get_zone_num()
            return Response({"code": 200, "message": "查询成功", "data": data})
        elif lx == "7":
            data = pie_get_house_area()
            return Response({"code": 200, "message": "查询成功", "data": data})
        elif lx == "8":
            data = get_house_type_distribution()
            return Response({"code": 200, "message": "查询成功", "data": data})
        elif lx == "9":
            data = get_orientation_distribution()
            return Response({"code": 200, "message": "查询成功", "data": data})
        elif lx == "get_options":
            # 获取所有特征选项
            from ershoufang_app.utils.house_echarts import get_feature_options
            data = get_feature_options()
            return Response({"code": 200, "message": "查询成功", "data": data})
        elif lx == "zone_analysis":
            # 获取指定区域的价格分析
            zone_name = request.GET.get('zone', '')
            if not zone_name:
                return Response({"code": 400, "message": "请提供区域名称"})
            
            from ershoufang_app.utils.house_echarts import get_zone_price_analysis
            result = get_zone_price_analysis(zone_name)
            return Response({"code": 200, "message": "查询成功", "data": result})
        else :
            return Response({"code": 400, "message": "请传入正确的入参"})

def DataAnalyse(request):
    return render(request, '二手房总价预测.html')
