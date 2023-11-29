import Generator
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)



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

    ax.plot(x, y, color='blue', linewidth=0.5, linestyle='-', marker='o', markerfacecolor='red', markeredgecolor='red', markersize=4)
    ax.plot([x[0], x[-1]], [average] * 2, 'g-', linewidth=1)
    ax.plot([x[0], x[-1]], [average + deviation] * 2, 'g--', linewidth=1)
    ax.plot([x[0], x[-1]], [average - deviation] * 2, 'g--', linewidth=1)

    CheckFlags(y, average, deviation)

    return ax


def BuildPlot(average, deviation, filename, view_size, view_speed,window):
    file = open(filename, 'r')

    data_x = []
    data_y = []
    data = GetData(file)

    fig, ax = plt.subplots()
    fig.set_size_inches(10, 5)
    canvas=FigureCanvasTkAgg(fig,master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(column=0,row=4)
    # toolbar = NavigationToolbar2Tk(canvas,
    #                                window)
    # toolbar.update()
    canvas.get_tk_widget().grid(column=0,row=4,columnspan=2,sticky='ew')
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


#
# if __name__ == '__main__':
#     average = 10
#     deviation = 1
#     filename = '../../Downloads/test.txt'
#
#     Generator.WriteToFile(average, deviation, 200, filename)
#     BuildPlot(average, deviation, filename, view_size=50, view_speed=50)