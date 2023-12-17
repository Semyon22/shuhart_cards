import numpy

from Generator import WriteToFile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.widgets import Slider
import tkinter as tk

FLAGS = []
TO_DELETE_WIDGET = None
TO_DELETE_LABEL = None

def CheckFlags(data, median, OEG):
    flag_out = 0
    flag_monotone = 1
    flag_oneside = 1
    OEG=OEG-median
    if data[-1] > median + OEG or data[-1] < median - OEG:
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
        if data[-1] > median:
            oneside_type = '+'
        else:
            oneside_type = '-'
        for i in range(2, 7+1):
            if oneside_type == '+' and data[-i] > median:
                continue
            elif oneside_type == '-' and data[-i] < median:
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


def get_seq(mat_oshid,disp, N):
    """
    Функция получения выборки с заданным мат ожиданием и дисперсией
    :param mat_oshid:
    :param disp:
    :param N:
    :return:
    """
    #так-как выборка генерируется по параметру отклонения рассчитаем его как квадратный корень из дисперсий для нашей контрольной карты
    #
    otkl=disp**0.5

    return np.random.normal(mat_oshid, otkl, N)


def get_param(array):
    """
    Функция возвращает медиану отклонение и мат ожидание
    :param array:
    :return:
    """
    print(np.median(array), array.std(), array.mean())
    return (np.median(array), array.std(), array.mean())


def get_control_boundaries(array):
    """
    Возвращает контрольные и предупредительные границы
    :param array:
    :return:
    """
    _, otkl, mean = get_param(array)
    print(np.shape(array))
    print("отклонение:",otkl)
    print(f"+:{(2.576 / (np.shape(array)[0] ** 0.5)) * otkl * 9.3}")
    print(f"-:{(2.576 / (np.shape(array)[0] ** 0.5)) * otkl *9.3}")
    OEG = mean + (2.576 / (np.shape(array)[0] ** 0.5)) * otkl *(np.shape(array)[0] ** 0.5)
    UEG = mean - (2.576 / (np.shape(array)[0] ** 0.5)) * otkl *(np.shape(array)[0] ** 0.5)
    OWG = mean + (1.960 / (np.shape(array)[0] ** 0.5)) * otkl *(np.shape(array)[0] ** 0.5)
    UWG = mean - (1.960 / (np.shape(array)[0] ** 0.5)) * otkl *(np.shape(array)[0] ** 0.5)
    return (OEG, UEG, OWG, UWG)





def GetData(file):
    data = []
    for line in file:
        data.append(float(line))
    file.close()
    return data

def WriteToFile(m):
    file = open("seq", 'w')
    for i in range((np.shape(m)[0])):
        file.write(str(m[i]) +"\n")
    file.close()


def PlotUpdate(new_y, x, y, ax, median, OEG,UEG,OWG,UWG,view_size):
    if (len(x) == 0):
        x.append(1)
    else:
        x.append(x[-1] + 1)
    y.append(new_y)

    if len(x) > view_size:
        ax.set_xlim(len(x) - view_size - 1, len(x) + 1)
        ax.set_ylim(min(y, default=0) - 1, max(y, default=0) + 1)
    ax.plot(x, y, color='black', linewidth=1, linestyle='-', marker='o', markerfacecolor='orange', markeredgecolor='orange', markersize=3,label='values')
    ax.plot([x[0], x[-1]], [median]*2, 'g-', linewidth=1,label='median')

    ax.plot([x[0], x[-1]], [OEG]*2, 'r--', linewidth=1,label='OEG')
    ax.plot([x[0], x[-1]], [UEG]*2, 'r--', linewidth=1,label='UEG')
    ax.plot([x[0], x[-1]], [OWG] * 2, 'y--', linewidth=0.5,label='OWG')
    ax.plot([x[0], x[-1]], [UWG] * 2, 'y--', linewidth=0.5,label='UWG')


    ax.legend(['Values','Median','OEG','UEG','UWG','OWG'],loc='upper left',prop={'size': 8})

    ax.autoscale_view(True, True, True)
    ax.set_facecolor("white")
    CheckFlags(y, median, OEG)

    return ax



def BuildPlot(view_size,view_speed,window,data):
    x = []
    y = []
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 5)


    OEG,UEG,OWG,UWG=get_control_boundaries(data)

    canvas = FigureCanvasTkAgg(fig, master=window)

    canvas.draw()
    canvas.get_tk_widget().place(x=30, y=230)

    plt.xlabel('Номер элемента (X)')
    plt.ylabel('Значение (Y)')

    plt.xlabel('X, последовательность')
    plt.ylabel('Y, переменная процесса')
    ani = animation.FuncAnimation(fig, PlotUpdate, data, fargs=(x, y, ax, np.median(data),OEG,UEG,OWG,UWG,view_size ), interval=view_speed, repeat=False)

    axcolor = 'lightgoldenrodyellow'
    axpos = plt.axes([0.2, 0, 0.6, 0.03], facecolor=axcolor)
    spos = Slider(axpos, 'Pos', 0, len(data) - view_size + 1)

    def update(val):
        pos = spos.val
        ax.axis([pos, pos + view_size, min(data, default=0) - 1, max(data, default=0) + 1])
        fig.canvas.draw_idle()

    spos.on_changed(update)
    ani.save()


def start_work(flag,mat_oshid,disp,count,window,filename):
    if (flag==1):
        data = get_seq(mat_oshid,disp,count)
        BuildPlot(50,50,window,data)
    else:

        file = open(filename,
                        'r')
        data = numpy.array(GetData(file))
        BuildPlot(50,50,window,data)
        file.close()





# BuildPlot(50,50)
