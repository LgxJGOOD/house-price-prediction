from django.db import models


class House(models.Model):
    """城市名称
    """
    title = models.CharField(max_length=255, verbose_name='标题')
    img_src = models.CharField(max_length=255, null=True, blank=True,verbose_name='房屋图片')
    detail_href = models.CharField(max_length=255, null=True, blank=True,verbose_name='房屋链接')
    position_info = models.CharField(max_length=100,  null=True, blank=True, verbose_name='房屋位置')
    house_info = models.CharField(max_length=255,  null=True, blank=True, verbose_name='房屋信息')
    total_price = models.IntegerField(verbose_name='总价')
    unit_price = models.CharField(max_length=100, null=True, blank=True, verbose_name='房屋单价')
    tag =  models.CharField(max_length=100, null=True, blank=True, verbose_name='房屋标签')
    house_area =models.CharField(max_length=255,  null=True, blank=True, verbose_name='房屋面积')
    main_info = models.CharField(max_length=255,  null=True, blank=True, verbose_name='房屋房间')
    house_orientation =models.CharField(max_length=255,  null=True, blank=True, verbose_name='房屋朝向')
    sub_info =models.CharField(max_length=255,  null=True, blank=True, verbose_name='房屋层数')
    house_decorate =models.CharField(max_length=255,  null=True, blank=True, verbose_name='房屋装修')
    housing_estate =models.CharField(max_length=255,  null=True, blank=True, verbose_name='小区')
    zone =models.CharField(max_length=255,  null=True, blank=True, verbose_name='所在区域')
    city = models.CharField(max_length=255, null=True, blank=True,verbose_name='房屋所在城市')
    house_type  = models.CharField(max_length=100, null=True, blank=True,verbose_name='房屋类型')
    status = models.IntegerField(verbose_name='状态')
    class Meta:
        db_table = 't_house'
        verbose_name = '房屋表'



