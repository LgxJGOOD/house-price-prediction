import request from "@/utils/request";

//数据列表
export const houseList = (params) => {
  return request.get('/house/list/', {
    params: {
      search: params.keyWord || '',
      pagesize: params.pagesize,
      pagenum: params.pagenum,
    },
  });
};

//城市数据列表
export const cityList = (params) => {
  return request.get('/app/city/list/', {
    params: {
      search: params.keyWord || '',
      pagesize: params.pagesize,
      pagenum: params.pagenum,
    },
  });
};

export const cityListApi = () => {
  return request.get('/app/city/list/all');
};

//添加城市
export const cityAdd = (data) => {
return request.post('app/city/dataadd/', data);
};

//修改城市 
export const cityEdit = (data) => {
return request.put(`app/city/dataedit/${data.id}/`, data);
};
//删除城市 
export const cityDel = (id) => {
return request.delete(`app/city/datadelete/${id}/`);
};

//图表分析
export const EchartsApi = (params) => {
  if (params.lx == 2) {
    return request.get('house/echart/datas/', {
      params: {
        lx: params.lx,
        floor: params.floor || params.楼层,
        floor1: params.building_type || params.楼型,
        year: params.build_year || params.建造年份,
        area: params.area || params.面积,
        zhuangxiu: params.decorate || params.装修,
        zone: params.zone || params.区域,
        room1: params.halls || params.厅,
        room2: params.rooms || params.室,
        orientation: params.orientation || params.朝向
      }
    });

  } else if (params.lx === 'zone_analysis') {
    // 区域价格分析
    return request.get('house/echart/datas/', {
      params: {
        lx: params.lx,
        zone: params.zone
      }
    });
  }
  else {
    return request.get('house/echart/datas/', {
      params: {
        lx: params.lx,
        house_id: params.house_id,
        user_id: params.user_id,
        num: params.num,

      }
    });
  }

};
