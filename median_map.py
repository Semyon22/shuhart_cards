from Generator import WriteToFile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.widgets import Slider
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

    result = {}
    if flag_out == 1:
        result.update({'out': [len(data), data[-1]]})
    if flag_monotone == 1:
        result.update({f'monotone ({monotone_type})': [len(data)-5, [data[i] for i in range(-6, 0)]]})
    if flag_oneside == 1:
        result.update({f'oneside ({oneside_type})': [len(data)-6, [data[i] for i in range(-7, 0)]]})

    if len(result) >= 1:
        print(result)
    return result


def get_seq(mat_oshid,disp, N):
    """
    Функция получения выборки с заданным мат ожиданием и дисперсией
    :param mat_oshid:
    :param disp:
    :param N:
    :return:
    """
    #так-как выборка генерируется по параметру отклонения рассчитаем его как квадратный корень из дисперсий для нашей контрольной какрты
    #
    otkl=((disp*0.17106 ** 2)/100)**0.5

    return np.random.normal(mat_oshid, otkl, N)


def get_param(array):
    """
    Функция возвращает медиану отклонение и мат ожидание
    :param array:
    :return:
    """
    return (np.median(array), array.std(), array.mean())


def get_control_boundaries(array):
    """
    Возвращает контрольные и предупредительные границы
    :param array:
    :return:
    """
    _, otkl, mean = get_param(array)
    print(np.shape(array))
    print(f"+:{(2.576 / (np.shape(array)[0] ** 0.5)) * otkl * 9.3}")
    print(f"-:{(2.576 / (np.shape(array)[0] ** 0.5)) * otkl *9.3}")
    OEG = mean + (2.576 / (np.shape(array)[0] ** 0.5)) * otkl *9.3
    UEG = mean - (2.576 / (np.shape(array)[0] ** 0.5)) * otkl * 9.3
    OWG = mean + (1.960 / (np.shape(array)[0] ** 0.5)) * otkl * 9.3
    UWG = mean - (1.960 / (np.shape(array)[0] ** 0.5)) * otkl * 9.3
    return (OEG, UEG, OWG, UWG)


m = get_seq(5,1, 100)
print("Границы",get_control_boundaries(m))
print(np.sort(m))
print("Мат ожидание:",m.mean())
print("Дисперсия:",m.var())
print("отклонение",m.std())
print('Медиана:',np.median(m))

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
WriteToFile(m)

def PlotUpdate(new_y, x, y, ax, median, OEG,UEG,OWG,UWG,view_size):
    if (len(x) == 0):
        x.append(1)
    else:
        x.append(x[-1] + 1)
    y.append(new_y)

    if len(x) > view_size:
        ax.set_xlim(len(x) - view_size - 1, len(x) + 1)
        ax.set_ylim(UEG -0.1,OEG+0.1)
    ax.plot(x, y, color='blue', linewidth=0.5, linestyle='-', marker='o', markerfacecolor='white', markeredgecolor='white', markersize=2,label='values')
    ax.plot([x[0], x[-1]], [median]*2, 'g-', linewidth=1,color='green',label='median')

    ax.plot([x[0], x[-1]], [OEG]*2, 'g--', linewidth=1,color='red',label='OEG')
    ax.plot([x[0], x[-1]], [UEG]*2, 'g--', linewidth=1,color='red',label='UEG')
    ax.plot([x[0], x[-1]], [OWG] * 2, 'g--', linewidth=0.5,color='yellow',label='OWG')
    ax.plot([x[0], x[-1]], [UWG] * 2, 'g--', linewidth=0.5,color='yellow',label='UWG')


    ax.legend(['Values','Median','OEG','UEG','UWG','UWG'],loc='upper left',prop={'size': 8})

    ax.autoscale_view(True, True, True)
    ax.set_facecolor("black")
  
    return ax



def BuildPlot(view_size,view_speed,window):
    x = []
    y = []
    fig, ax = plt.subplots()
    fig.set_size_inches(5.5, 4.5)

    OEG,UEG,OWG,UWG=get_control_boundaries(m)
    file = open('seq',
                'r')
    data = GetData(file)

    canvas=FigureCanvasTkAgg(fig,master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(column=0,row=4,columnspan=2,sticky='ew')
    canvas.get_tk_widget().grid(column=0,row=4,columnspan=2,sticky='ew')

    ani = animation.FuncAnimation(fig, PlotUpdate, data, fargs=(x, y, ax, np.median(m),OEG,UEG,OWG,UWG,view_size ), interval=view_speed, repeat=False)

    axcolor = 'lightgoldenrodyellow'
    axpos = plt.axes([0.2, 0, 0.6, 0.03], facecolor=axcolor)
    spos = Slider(axpos, 'Pos', 0, len(data) - view_size + 1)

    def update(val):
        pos = spos.val
        ax.axis([pos, pos + view_size, UEG - 0.1, OEG + 0.1])
        fig.canvas.draw_idle()

    spos.on_changed(update)
    
    ani.save()
