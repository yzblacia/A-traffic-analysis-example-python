import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import os




def plot(number, lane, min_time, xl1, yl1, twinx, yl2=""):
    # 读取数据
    df1 = pd.read_excel('.\\' + str(min_time) + 'min的数据' + '\\' + str(number) + '_' + str(lane) + '.xlsx')
    rows = df1.shape[0]

    xt1 = df1[xl1]
    yt1 = df1[yl1]

    matplotlib.use('Agg')
    fig = plt.figure(figsize=(15, 6), dpi=400)

    ax1 = fig.add_subplot(111)
    yt1.plot(ax=ax1, marker="o", c="b", label=xl1 + "-" + yl1, markersize=1)
    # 绘制坐标轴标签
    ax1.set_xlabel(xl1)
    ax1.set_ylabel(yl1)
    plt.title(yl1 + "-" + yl2 + "-" + xl1)
    # 显示图例
    plt.legend(loc=2)
    # 设置轴刻度
    # 范围为(0 . max ) 刻度为 max / 10 如果 此值为 0  则 跨度为1；
    ax1.set_yticks(range(0, int(max(yt1)) + 1, int(max(yt1) / 10) if (int(max(yt1) / 10) != 0) else 1))

    # 是否采用双坐标轴图表
    if twinx:
        ax2 = ax1.twinx()
        yt2 = df1[yl2]
        yt2.plot(ax=ax2, marker="o", c="r", label=xl1 + "-" + yl2, markersize=1)
        # 绘制坐标轴标签
        ax2.set_ylabel(yl2)
        plt.legend(loc=1)
        ax2.set_yticks(range(0, int(max(yt2)) + 1, int(max(yt2) / 10) if (int(max(yt2) / 10) != 0) else 1))

    # 将可视化后的图像进行保存
    if not os.path.exists(".\\" + str(yl1) + "-" + str(yl2) + "可视化"):
        os.makedirs(".\\" + str(yl1) + "-" + str(yl2) + "可视化")

        # plt.show()
    plt.savefig(
        ".\\" + str(yl1) + "-" + str(yl2) + "可视化" + '\\' + f"{number}-{lane}-{min_time}min的数据-{yl1}-{yl2}-{xl1}.png")
    plt.close()
    if twinx:
        print(f"{number}-{lane}-{min_time}min的数据-{yl1}-{yl2}-{xl1}.png", "已保存")


if __name__ == '__main__':
    for number in range(75, 85):
        for lane in range(1, 3):
            for time in [120, 1440]:
                for flag in [0, 1]:
                    plot(number, lane, time, "timestamp", "occupancy", flag, "total_traffic")
                    plot(number, lane, time, "timestamp", "average_car_spacing", flag, "average_speed")
                    plot(number, lane, time, "timestamp", "average_car_length", flag, "average_speed")
