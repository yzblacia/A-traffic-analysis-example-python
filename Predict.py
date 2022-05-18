import matplotlib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split  # 划分训练集和测试集
from sklearn.neural_network import MLPRegressor  # 多层线性回归
from sklearn.preprocessing import StandardScaler  # 对数据进行标准化
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error  # MSE, MAPE
import os


def Predict(number, lane, min_time):
    data = np.array(pd.read_excel('.\\' + str(min_time) + 'min的数据' + '\\' + str(number) + '_' + str(lane) + '.xlsx'))
    # 导入数据集
    dataMat = np.array(data)
    train_data = dataMat[:, 2:5]  # 特征集
    train_target = dataMat[:, 5:7]  # 标签集

    x_train, x_test, y_train, y_test = train_test_split(train_data, train_target, test_size=0.25, random_state=0)
    # train_data：所要划分的样本特征集
    # train_target：所要划分的样本结果
    # test_size：测试集占全体样本比重，如果是整数的话就是样本的数量
    # random_state：是随机数的种子。

    # 数据标准化
    scaler = StandardScaler()  # 标准化转换

    x_test_Standard = scaler.fit_transform(x_test)  # 转换数据集
    x_train_Standard = scaler.fit_transform(x_train)  # 转换数据集
    y_test_Standard = scaler.fit_transform(y_test)  # 转换数据集
    y_train_Standard = scaler.fit_transform(y_train)  # 转换数据集

    bp = MLPRegressor(solver='lbfgs', alpha=0.0001, hidden_layer_sizes=(5, 3), random_state=1, max_iter=3000)
    bp.fit(x_train_Standard, y_train_Standard) #使用构建的BP神经网络进行训练

    y_predict_Standard = bp.predict(x_test_Standard)
    y_predict = scaler.inverse_transform(y_predict_Standard)

    print(str(number) + '_' + str(lane) + '在最小时间戳为' + str(min_time) + '时:')

    print('数据预测平均准确度:' + str(bp.score(x_test_Standard, y_test_Standard)))
    print('MSE:' + str(
        np.around(mean_squared_error(y_test_Standard, y_predict_Standard, multioutput='raw_values'), decimals=3)))
    print('RMSE:' + str(
        np.around(np.sqrt(mean_squared_error(y_test_Standard, y_predict_Standard, multioutput='raw_values')),
                  decimals=3)))
    print('MAPE:' + str(
        np.around(mean_absolute_percentage_error(y_test_Standard, y_predict_Standard, multioutput='raw_values'),
                  decimals=3)))
    print('\n')



#   在测试集上绘制出真实曲线和预测曲线，分析预测值和真实值的拟合程度，保存图像，便于直观分析拟合效果
    matplotlib.use('Agg')
    y_label = ['total_traffic', 'average_speed']
    plt.rcParams['font.family'] = ['Fangsong']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(15, 12), dpi=500)

    for i in range(0, 2):
        # print(y_test_Standard)
        x = np.arange(0, min(y_test_Standard.shape[0], 500), 1)
        y1 = y_test_Standard[0:min(y_test_Standard.shape[0], 500), i]
        y2 = y_predict_Standard[0:min(y_predict_Standard.shape[0], 500), i]
        plt.subplot(2, 1, i+1)
        plt.plot(x, y1, color='orange')  # 橙色线为真实曲线
        plt.plot(x, y2, color='dodgerblue')
        plt.xlabel("时间戳数")
        plt.ylabel(y_label[i])
        plt.title(y_label[i] + '拟合曲线与真实曲线的比较')

    # 保存图像
    dirs = '.\\预测分析图像\\' + str(min_time) + 'min的数据' + '\\'
    if not os.path.exists(dirs):
        os.makedirs(dirs)  # 创建文件夹存放图像
    plt.savefig('.\\预测分析图像\\' + str(min_time) + 'min的数据' + '\\' + str(number) + '_' + str(
        lane) + '拟合曲线与真实曲线的比较.jpg')

    plt.close()


if __name__ == '__main__':
    for number in range(75, 85):
        for lane in range(1, 3):
            for min_time in [5, 30, 60, 120, 1440]:
                Predict(number, lane, min_time)
