import matplotlib.pyplot as plt
import tkinter as tk

from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import Generator



FLAGS = []
TO_DELETE_WIDGET = None
TO_DELETE_LABEL = None


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
            if monotone_type == '+' and data[-i] > data[-i-1]:
                continue
            elif monotone_type == '-' and data[-i] < data[-i-1]:
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
        for i in range(2, 7+1):
            if oneside_type == '+' and data[-i] > average:
                continue
            elif oneside_type == '-' and data[-i] < average:
                continue
            else:
                flag_oneside = 0
                break
    else:
        flag_oneside = 0

    result = []
    if flag_out == 1:
        result.append(f'Выход за границу: x0 = {len(data)}')
    if flag_monotone == 1:
        result.append(f'Монотонность ({monotone_type}): x0 = {len(data)-5}')
    if flag_oneside == 1:
        result.append(f'По одну сторону от ср. линии ({oneside_type}): x0 = {len(data)-6}')

    if len(result) >= 1:
        global FLAGS, TO_DELETE_WIDGET, TO_DELETE_LABEL
        for r in result:
            FLAGS.append(r)

        if TO_DELETE_WIDGET:
            TO_DELETE_WIDGET.destroy()
        if TO_DELETE_LABEL:
            TO_DELETE_LABEL.destroy()

        TO_DELETE_LABEL = tk.Label(text='Вывод критических ситуаций:', font=tk.font.Font(size=10))
        TO_DELETE_LABEL.place(x=850, y=40)

        flags_var = tk.Variable(value=FLAGS)
        TO_DELETE_WIDGET = tk.Listbox(listvariable=flags_var, width=63, height=41, font=tk.font.Font(size=9))
        TO_DELETE_WIDGET.place(x=850, y=70)


def PlotUpdate(new_data, x, y, ax, average, deviation, view_size):
    if len(x):
        if new_data != y[-1]:
            x.append(x[-1] + 1)
            y.append(new_data)
    else:
        x.append(1)
        y.append(new_data)

    if len(x) > view_size:
        ax.set_xlim(len(x)-view_size-1, len(x)+1)
        ax.set_ylim(min(y, default=0) - 1, max(y, default=0) + 1)

    ax.plot(x, y, color='black', linewidth=1, linestyle='-', marker='o', markerfacecolor='orange', markeredgecolor='orange', markersize=3,label='values')
    ax.plot([x[0], x[-1]], [average] * 2, 'g-', linewidth=1)
    ax.plot([x[0], x[-1]], [average + deviation] * 2, 'r--', linewidth=1)
    ax.plot([x[0], x[-1]], [average - deviation] * 2, 'r--', linewidth=1)
    # ax.plot([x[0], x[-1]], [average + 0.9*deviation] * 2, 'r--', linewidth=1)
    # ax.plot([x[0], x[-1]], [average - 0.9*deviation] * 2, 'r--', linewidth=1)

    ax.set_facecolor("white")
    ax.legend(['Значения', 'Средняя линия', 'Контрольные границы'], loc='upper left', prop={'size': 8})
    ax.autoscale_view(True, True, True)

    CheckFlags(y, average, deviation)

    return ax


def BuildPlot(average, deviation, view_size, view_speed, data, window):
    data_x = []
    data_y = []

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 5)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().place(x=30, y=230)

    plt.xlabel('X, последовательность')
    plt.ylabel('Y, переменная процесса')
    ani = FuncAnimation(fig, PlotUpdate, data, fargs=(data_x, data_y, ax, average, deviation, view_size), interval=view_speed, repeat=False)

    axcolor = 'lightgoldenrodyellow'
    axpos = plt.axes([0.2, 0, 0.6, 0.03], facecolor=axcolor)
    spos = Slider(axpos, 'Pos', 0, len(data) - view_size + 1)

    def update(val):
        pos = spos.val
        ax.axis([pos, pos + view_size, min(data, default=0) - 1, max(data, default=0) + 1])
        fig.canvas.draw_idle()
    spos.on_changed(update)

    ani.save()


def start_work(flag, mat_oshid, disp, count, window, filename):
    if (flag==1):
        data = []
        for i in range(count):
            data.append(Generator.GenRandVal(Generator.GenNormalRandVal(), mat_oshid, disp))
        BuildPlot(mat_oshid, disp, 50, 50, data, window)
    else:
        file = open(filename, 'r')
        data = GetData(file)
        file.close()
        avg, dev = calc_characteristic(data)
        BuildPlot(avg, dev*2, 50, 50, data, window)

def calc_characteristic(data):
    avg = 0
    for d in data:
        avg += d
    avg /= len(data)

    dev = 0
    for d in data:
        dev += pow(d - avg, 2)
    dev /= len(data)

    return avg, dev