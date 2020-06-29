#coding=UTF-8

import requests
import pandas as pd
import xlrd
import math
import xlwt
key = '5118c8e3930f25286b90702777579553'

def bdToGaoDe(locations):
    parameters = { 'locations': locations, 'key': key,
                  'coordsys': 'baidu'}
    base = 'https://restapi.amap.com/v3/assistant/coordinate/convert'
    response = requests.get(base, parameters)
    answer = response.json()
    return answer['locations']

def geocode1(location):
    parameters = {'output': 'json', 'location': location, 'key': key,
                  'extensions': 'all','radius':1000,'roadlevel':0,'batch':'false'}
    base = 'https://restapi.amap.com/v3/geocode/regeo'
    response = requests.get(base, parameters)
    answer = response.json()
    return answer['regeocode']['formatted_address'], answer['regeocode']['addressComponent']['district'], \
           answer['regeocode']['addressComponent']['township'],answer['regeocode']['addressComponent']['streetNumber']['street'],answer['regeocode']['addressComponent']['streetNumber']['number']

workbook = xlwt.Workbook(encoding='utf-8')

workbookerr = xlwt.Workbook(encoding='utf-8')


def read_input(inFile,outFile,errFile):
    df = pd.DataFrame()
    errdf = pd.DataFrame()
    workbook1 = xlrd.open_workbook(inFile)  #(1)取得excel book对象
    s12 = workbook1.sheet_by_name("Sheet1")  #(2)取得sheet对象
    rows = s12.nrows #(3)获得总行数
    count = 0
    right = 0
    errorCount = 0
    queryindex = 0
    errorindex = 0
    for r in range(1,rows):
        try:
            count = count + 1
            row = s12.row_values(r) #(4)获取行数据
            lon, lat = row
            print(str(lon)+','+str(lat))
            locations = str(lon) + ',' + str(lat)
            detail, qu, jiedao, lu, hao = geocode1(bdToGaoDe(locations))
            if right % 65530 == 0:
                sheet = workbook.add_sheet('gis'+str(right))
                head = ['lon', 'lat', 'addr', 'qu', 'jiedao', 'luhao']  # 表头
                for h in range(len(head)):
                    sheet.write(0, h, head[h])
                queryindex = 0
            queryindex = queryindex + 1
            sheet.write(queryindex, 0, lon)
            sheet.write(queryindex, 1, lat)
            sheet.write(queryindex, 2, detail)
            sheet.write(queryindex, 3, qu)
            sheet.write(queryindex, 4, jiedao)
            sheet.write(queryindex, 5, (lu + hao))
            right = right +1
            print(count/rows)
        except:
            error = {'lon': lon, 'lat': lat}
            if errorCount % 65530 ==0:
                sheeterr = workbookerr.add_sheet('gis' + str(errorCount))
                head = ['lon', 'lat', 'addr', 'qu', 'jiedao', 'luhao']  # 表头
                for h in range(len(head)):
                    sheeterr.write(0, h, head[h])
                errorindex = 0
            errorindex = errorindex + 1
            sheeterr.write(errorindex, 0, lon)
            sheeterr.write(errorindex, 1, lat)
            print(lon,lat)
            errorCount = errorCount + 1
    if right !=0:
        workbook.save(outFile)
    if errorCount!=0:
        workbookerr.save(errFile)

read_input('wo.xlsx','querywo.xlsx','errorWo.xlsx')



