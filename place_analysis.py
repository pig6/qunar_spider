import re

import numpy as np
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar

"""
获取详细教程、获取代码帮助、提出意见建议
关注微信公众号「裸睡的猪」与猪哥联系

@Author  :   猪哥
"""

# 去哪儿热门景点excel文件保存路径
PLACE_EXCEL_PATH = 'qunar_place.xlsx'
# 读取数据
DF = pd.read_excel(PLACE_EXCEL_PATH)
# 百度热力图模板
HOT_MAP_TEMPLATE_PATH = 'hot_map_template.html'
# 生成的国庆旅游景点热力图
PLACE_HOT_MAP_PATH = 'place_hot_map.html'


def analysis_sale():
    """
    分析销量
    :return: 
    """
    # 引入全局数据
    global DF
    df = DF.copy()
    # 1、生成一个名称和销量的透视表
    place_sale = df.pivot_table(index='name', values='sale')
    # 2、根据销量排序
    place_sale.sort_values('sale', inplace=True, ascending=True)
    print(place_sale)
    # 3、生成柱状图
    place_sale_bar = (
        Bar()
            .add_xaxis(place_sale.index.tolist()[-20:])
            .add_yaxis("", list(map(int, np.ravel(place_sale.values)))[-20:])
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="国庆旅游热门景点门票销量TOP20"),
            yaxis_opts=opts.AxisOpts(name="景点名称"),
            xaxis_opts=opts.AxisOpts(name="销量")
        )
    )
    place_sale_bar.render('place-sale-bar.html')


def analysis_amount():
    """
    分析销售额
    :return:
    """
    # 引入全局数据
    global DF
    df = DF.copy()
    amount_list = []
    for index, row in df.iterrows():
        try:
            # 销售额
            amount = row['price'] * row['sale']
        except Exception:
            amount = 0
        amount_list.append(amount)
    df['amount'] = amount_list
    # 生成一个名称和销量的透视表
    place_amount = df.pivot_table(index='name', values='amount')
    # 根据销售额排序
    place_amount.sort_values('amount', inplace=True, ascending=True)
    print(place_amount)
    # 生成柱状图
    place_amount_bar = (
        Bar()
            .add_xaxis(place_amount.index.tolist()[-20:])
            .add_yaxis("", list(map(int, np.ravel(place_amount.values)))[-20:])
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="国庆旅游热门景点门票销售额TOP20"),
            yaxis_opts=opts.AxisOpts(name="景点名称"),
            xaxis_opts=opts.AxisOpts(name="销售额")
        )
    )
    place_amount_bar.render('place-amount-bar.html')


def analysis_province():
    """
    此功能未完成
    分析省份旅游景点数
    :return:
    """
    # 引入全局数据
    global DF
    df = DF.copy()
    province_list = []
    for item in df.districts:
        province_match = re.search(r'^([\u4e00-\u9fa5])*', item)
        province_list.append(province_match[0])
    print(province_list)
    df['province'] = province_list
    # province_star = df.groupby(['province', 'star'])
    province_star = df.groupby(['province', 'star']).agg({'star': 'count'})
    province_star_dict = {}
    star = ['3A', '4A', '5A', '无']
    star_index = 0
    prev = ''
    for province_star_index in province_star.index:
        province_index = province_star_index[1]
        if prev != province_index:
            star_index = 0
            province_star_dict['province_index'] = []
        while True:
            if province_index == star[star_index]:
                province_star.star[province_star_index]
                star_index += 1
        province_star_dict
    print(province_star)


def analysis_point_sale():
    """
    生成热力图，使用百度地图api
    :return:
    """
    # 引入全局数据
    global DF
    df = DF.copy()
    point_sale_list = []
    for index, row in df.iterrows():
        # 构建坐标数据
        lng, lat = row['point'].split(',')
        count = row['sale']
        point_sale = {'lng': float(lng), 'lat': float(lat), 'count': count}
        point_sale_list.append(point_sale)
    print(point_sale_list)
    data = f'var points ={str(point_sale_list)};'
    # 替换模板中的坐标数据
    with open(HOT_MAP_TEMPLATE_PATH, 'r', encoding="utf-8") as f1, open(PLACE_HOT_MAP_PATH, 'w',
                                                                        encoding="utf-8") as f2:
        s = f1.read()
        # 替换数据
        s2 = s.replace('%data%', data)
        f2.write(s2)
        f1.close()
        f2.close()


def analysis_recommend():
    """
    瞎推荐排行榜，高评分、销量少、价格便宜
    :return:
    """
    # 引入全局数据
    global DF
    df = DF.copy()
    recommend_list = []
    for index, row in df.iterrows():
        try:
            # 瞎推荐系数算法
            recommend = (row['score'] * 1000) / (row['price'] * row['sale'])
        except ZeroDivisionError:
            recommend = 0
        recommend_list.append(recommend)
    df['recommend'] = recommend_list
    # 生成一个名称和瞎推荐系数的透视表
    place_recommend = df.pivot_table(index='name', values='recommend')
    # 根据瞎推荐系数排序
    place_recommend.sort_values('recommend', inplace=True, ascending=True)
    print(place_recommend)
    # 生成柱状图
    place_recommend_bar = (
        Bar()
            .add_xaxis(place_recommend.index.tolist()[-20:])
            .add_yaxis("", list(map(int, np.ravel(place_recommend.values)))[-20:])
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="国庆旅游热门景点瞎推荐TOP20"),
            yaxis_opts=opts.AxisOpts(name="景点名称"),
            xaxis_opts=opts.AxisOpts(name="瞎推荐系数")
        )
    )
    place_recommend_bar.render('place-recommend-bar.html')


if __name__ == '__main__':
    analysis_sale()
    analysis_amount()
    # analysis_province()
    analysis_point_sale()
    analysis_recommend()
