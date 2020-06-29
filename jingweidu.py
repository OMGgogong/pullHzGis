#coding=UTF-8
import pandas as pd

import openpyxl
from collections import OrderedDict
def decode(geoh):
    """将geohash解码成经纬度"""
    __base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
    __decodemap = {}
    for i in range(len(__base32)):
        __decodemap[__base32[i]] = i
    del i
    lon_interval, lat_interval = (-180.0, 180.0), (-90.0, 90.0)  # 经度范围, 纬度范围
    lon_error, lat_error = 180.0, 90.0
    is_even = True
    for c in geoh:
        cd = __decodemap[c]
        for mask in [16, 8, 4, 2, 1]:
            if is_even:
                lon_error /= 2
                if cd & mask:
                    lon_interval = ((lon_interval[0] + lon_interval[1]) / 2, lon_interval[1])
                else:
                    lon_interval = (lon_interval[0], (lon_interval[0] + lon_interval[1]) / 2)

            else:
                lat_error /= 2
                if cd & mask:
                    lat_interval = ((lat_interval[0] + lat_interval[1]) / 2, lat_interval[1])

                else:
                    lat_interval = (lat_interval[0], (lat_interval[0] + lat_interval[1]) / 2)
            is_even = not is_even
    lon = (lon_interval[0] + lon_interval[1]) / 2  # 经度
    lat = (lat_interval[0] + lat_interval[1]) / 2  # 纬度
    # 小数点后面保留14位经度
    lon_ = float("%.14f" % lon)
    lat_ = float("%.14f" % lat)

    return lon_,lat_

def readFile(file = "G:\\work\\内网通\\张鑫\\tmp_data_zhangxin_geohash_20200624_d"):
    count = 0
    with open(file, "r") as f:
        for line in f.readlines():
            count = count + 1
            print(line.strip('\n'))

jiewei = ['0','1','2','3','4','5','6','7','8','9','b','c','d','e','f','g','h','j','k','m','n','p','q','r','s','t','u','v','w','x','y','z']
#fenge = 280000
fenge = 290000
count = 0
df = pd.DataFrame()
with open("G:\\内网张国帅To外网张国帅\\tmp_data_zhangxin_geohash_20200624_d", "r") as f:
    for line in f.readlines():
        for item in jiewei:
            geohash = line.strip('\n')+item
            lon,lat = decode(geohash)
            jingweidu = {'lon': lon, 'lat': lat}
            df = df.append(pd.DataFrame(jingweidu, index=[1]), ignore_index=True)
            count = count + 1
            print(count)
            yushu = count % fenge
            if yushu == 0:
                df.to_excel("HzGisData"+str(count /fenge)+".xlsx", index=False, encoding='utf-8')
                df = pd.DataFrame()
df.to_excel("HzGisDataEnd.xlsx", index=False, encoding='utf-8')




