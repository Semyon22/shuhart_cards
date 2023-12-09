import math
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np

import Generator


def main(loc, scale, number_of_data):
    group_size = 4
    num_groups = number_of_data // group_size

    data = np.zeros((num_groups, group_size))
    for i in range(num_groups):
        for j in range(group_size):
            norm_val = Generator.GenNormalRandVal()
            data[i, j] = Generator.GenRandVal(norm_val, loc, scale)
    grouped_data = np.mean(data, axis=1)
    std_dev_within = np.std(data.flatten(), ddof=1)
    center_line = loc
    return grouped_data, std_dev_within, center_line


def control_values(center_line, std_dev_within):
    upper_limit = center_line + 2.576/math.sqrt(4) * std_dev_within
    lower_limit = center_line - 2.576/math.sqrt(4) * std_dev_within

    warning_upper = center_line + 1.960/math.sqrt(4) * std_dev_within
    warning_lower = center_line - 1.960/math.sqrt(4) * std_dev_within

    return upper_limit, lower_limit, warning_upper, warning_lower


def GetData(file):
    data = []
    for line in file:
        data.append(float(line))
    file.close()
    return data


def CheckFlags(data, average, deviation):
    flag_out = 0
    flag_monotone = 1
    flag_oneside = 1

    if data[-1] > average + deviation or data[-1] < average - deviation:
        flag_out = 1

    monotone_type = ''
    if len(data) >= 6:
        if data[-1] > data[-2]:
            monotone_type = '+'
        else:
            monotone_type = '-'
        for i in range(2, 6):
            if monotone_type == '+' and data[-i] > data[-i - 1]:
                continue
            elif monotone_type == '-' and data[-i] < data[-i - 1]:
                continue
            else:
                flag_monotone = 0
                break
    else:
        flag_monotone = 0

    oneside_type = ''
    if len(data) >= 7:
        if data[-1] > average:
            oneside_type = '+'
        else:
            oneside_type = '-'
        for i in range(2, 7 + 1):
            if oneside_type == '+' and data[-i] > average:
                continue
            elif oneside_type == '-' and data[-i] < average:
                continue
            else:
                flag_oneside = 0
                break
    else:
        flag_oneside = 0

    result = {}
    if flag_out == 1:
        result.update({'out': [len(data), data[-1]]})
    if flag_monotone == 1:
        result.update({f'monotone ({monotone_type})': [len(data) - 5, [data[i] for i in range(-6, 0)]]})
    if flag_oneside == 1:
        result.update({f'oneside ({oneside_type})': [len(data) - 6, [data[i] for i in range(-7, 0)]]})

    if len(result) >= 1:
        print(result)
    return result


def PlotUpdate(new_data, x, y, ax, average, deviation, upper_limit, lower_limit, warning_upper, warning_lower, view_size):
    if len(x):
        if new_data != y[-1]:
            x.append(x[-1] + 1)
            y.append(new_data)
    else:
        x.append(1)
        y.append(new_data)

    if len(x) > view_size:
        ax.set_xlim(len(x) - view_size - 1, len(x) + 1)
        ax.set_ylim(min(y, default=0) - 1, max(y, default=0) + 1)


    ax.plot(x, y, color='blue', linewidth=0.5, linestyle='-', marker='o', markerfacecolor='white', markeredgecolor='white', markersize=2,label='values')
    ax.plot([x[0], x[-1]], [average]*2, 'g-', linewidth=1,color='green',label='median')

    ax.plot([x[0], x[-1]], [upper_limit]*2, 'g--', linewidth=1,color='red',label='OEG')
    ax.plot([x[0], x[-1]], [lower_limit]*2, 'g--', linewidth=1,color='red',label='UEG')
    ax.plot([x[0], x[-1]], [warning_upper] * 2, 'g--', linewidth=0.5,color='yellow',label='OWG')
    ax.plot([x[0], x[-1]], [warning_lower] * 2, 'g--', linewidth=0.5,color='yellow',label='UWG')


    ax.legend(['Values','Median','OEG','UEG','OWG','UWG'],loc='upper left',prop={'size': 8})

    ax.autoscale_view(True, True, True)
    ax.set_facecolor("black")


    CheckFlags(y, average, deviation)

    return ax

def BuildPlot(average, deviation, filename, view_size, view_speed):
    file = open(filename, 'r')

    data_x = []
    data_y = []
    upper_limit, lower_limit, warning_upper, warning_lower = control_values(center_line, std_dev_within)
    data = GetData(file)

    fig, ax = plt.subplots()
    fig.set_size_inches(10, 5)

    ani = FuncAnimation(fig, PlotUpdate, data, fargs=(data_x, data_y, ax, average, deviation, upper_limit, lower_limit, warning_upper, warning_lower, view_size),
                        interval=view_speed, repeat=False)

    axcolor = 'lightgoldenrodyellow'
    axpos = plt.axes([0.2, 0, 0.6, 0.03], facecolor=axcolor)
    spos = Slider(axpos, 'Pos', 0, len(data) - view_size + 1)

    def update(val):
        pos = spos.val
        ax.axis([pos, pos + view_size, min(data, default=0) - 1, max(data, default=0) + 1])
        fig.canvas.draw_idle()

    spos.on_changed(update)
    plt.show()


number_of_data, loc, scale = 400, 50, 3
group_means, std_dev_within, center_line = main(loc, scale, number_of_data)


# Сохранение данных в файл
filename = 'generated_data.txt'
with open(filename, 'w') as file:
    for value in group_means:
        file.write(f'{value}\n')

# Построение интерактивного графика с анимацией и слайдером

BuildPlot(center_line, std_dev_within, filename, 30, 200)
