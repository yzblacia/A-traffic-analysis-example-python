from Pre import Pre
from Predict import Predict
from Plot import plot

if __name__ == '__main__':
# 预处理：
    print('-----下面进行预处理-----')
    for number in range(75, 85):
        for lane in range(1, 3):
            for min_time in [5, 30, 60, 120, 1440]:
                Pre(number, lane, min_time)

# 机器学习预测：
    print('-----下面进行机器学习预测-----')
    for number in range(75, 85):
        for lane in range(1, 3):
            for min_time in [5, 30, 60, 120, 1440]:
                Predict(number, lane, min_time)

# 可视化分析图像：
    print('-----下面进行可视化处理-----')
    for number in range(75, 85):
        for lane in range(1, 3):
            for time in [120, 1440]:
                for flag in [0, 1]:
                    plot(number, lane, time, "timestamp", "occupancy", flag, "total_traffic")
                    plot(number, lane, time, "timestamp", "average_car_spacing", flag, "average_speed")
                    plot(number, lane, time, "timestamp", "average_car_length", flag, "average_speed")