from django.urls import path,include
from . import views


urlpatterns = [
        path('data/img/spider/', views.SpiderDataImgView.as_view(), name='img-data-spider'),
        path('list/', views.HouseListView.as_view(), name='house-datalsit'),
        path('data/export-house-csv/', views.ExportHouseCSV.as_view(), name='export_house_csv'),
        path('echart/datas/', views.EhartsView.as_view(), name='echart-datas'),
        path('data/DataAnalyse/',views.DataAnalyse,name='DataAnalyse'),
    ]