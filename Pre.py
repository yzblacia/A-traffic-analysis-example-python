import pandas as pd
import numpy as np
from openpyxl import Workbook
import os


def Pre(number, lane, min_time):  # 数据预处理, min_time是预处理后数据集时间分度值，单位为min
    df1 = pd.read_csv('.\\题目-数据\\滨创杯数据-1.交通\\' + 'MD-TaiXing-' + str(number) + '.csv')
    rows = df1.shape[0]
    np1 = np.array(df1)  # 转换为numpy数组

    wb = Workbook()
    sheet = wb.active
    sheet.title = str(number) + '_' + str(lane)
    row = ['deviceId', 'timestamp', 'average_car_spacing', 'average_car_length', 'occupancy', 'total_traffic',
           'average_speed', 'small_car_traffic_', 'medium_car_traffic_', 'large_car_traffic_']
    sheet.append(row)

    time_travel = int(32 * min_time / 5)  # 在min_time最小时间分度下收集一轮数据需要遍历的行数

    if min_time == 1440:
        flag = 24
    elif min_time == 120:
        flag = 2
    else:
        flag = 1  # 对最小时间戳为1day和2h的数据进行重复采样，采样间隔为1h，实现扩充数据，便于后续进行机器学习预测

    for i in range(0, rows, int(time_travel / flag)):
        list1 = [0 for _ in range(10)]  # 初始化一个空列表，用来预处理数据
        for j in range(i, min(i + time_travel, rows)):
            list1[0] = np1[j][1]
            list1[1] = np1[j][3]
            if np1[j][2] == 'average_car_spacing_' + str(lane):
                list1[2] += np1[j][4]  # 平均车间距
            if np1[j][2] == 'average_car_length_' + str(lane):
                list1[3] += np1[j][4]  # 平均车长
            if np1[j][2] == 'occupancy_' + str(lane):
                list1[4] += np1[j][4]  # 占有率
            if np1[j][2] == 'total_traffic_' + str(lane):
                list1[5] += np1[j][4]  # 总车流量
            if np1[j][2] == 'average_speed_' + str(lane):
                list1[6] += np1[j][4]  # 平均车速
            if np1[j][2] == 'small_car_traffic_' + str(lane):
                list1[7] += np1[j][4]
            if np1[j][2] == 'medium_car_traffic_' + str(lane):
                list1[8] += np1[j][4]
            if np1[j][2] == ('large1_car_traffic_' + str(lane) or 'large2_car_traffic_' + str(
                    lane) or 'large3_car_traffic_' + str(lane)):
                list1[9] += np1[j][4]

        sheet.append(list1)

    dirs = '.\\' + str(min_time) + 'min的数据'
    if not os.path.exists(dirs):
        os.makedirs(dirs)  # 创建文件夹存放当前时间戳为min_time的数据文件

    wb.save('.\\' + str(min_time) + 'min的数据' + '\\' + str(number) + '_' + str(lane) + '.xlsx')
    print('成功保存时间戳为' + str(min_time) + 'min的数据' + '文件' + str(number) + '_' + str(lane) + '.xlsx')


if __name__ == '__main__':

    for number in range(75, 85):  # 编号
        for i in range(1, 3):  # 车道
            for time in [5, 30, 60, 120, 1440]:  # 最小时间戳
                Pre(number, i, time)
