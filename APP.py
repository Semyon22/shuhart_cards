import tkinter.font
from tkinter import *
from tkinter import ttk
import Plot1
import Plot2


def ShowPlot1():
    Plot1.BuildPlot(float(entry_for_median.get()), float(entry_for_deviation.get()), entry_for_file.get(), 50, 50, window=window)

def ShowPlot2():
    Plot2.BuildPlot(50, 50, window=window)


def CheckCombobox():
    if combobox.get() == cards[0]:
        # Борщев
        ShowPlot1()
    elif combobox.get() == cards[1]:
        # Грошев
        pass
    elif combobox.get() == cards[2]:
        # Попов
        ShowPlot2()
    elif combobox.get() == cards[3]:
        # Курдюков
        pass


window = Tk()                                   # Иницилизация окна
window.title('Контрольные Карты Шухарта')       # Заголовок окна
window.geometry("1200x700")                     # Размер окна


# Заголовки
lbl_for_combox = Label(text="Выберите карту:")
lbl_for_combox.place(x=30, y=10)

lbl_for_file = Label(text="Введите имя файла:")
lbl_for_file.place(x=30, y=40)

lbl_for_median = Label(text="Введите среднее значение:")
lbl_for_median.place(x=30, y=70)

lbl_for_deviation = Label(text="Введите отклонение:")
lbl_for_deviation.place(x=30, y=100)


# Формы считывания данных
cards = ["Контрольные карты управления процессом", "Контрольные карты средних значений", "Контрольные карты медиан", "Контрольные карты исходных значений"]
combobox = ttk.Combobox(values=cards, width=40, state="readonly")
combobox.place(x=200, y=10)

entry_for_file = ttk.Entry(width=30)
entry_for_file.place(x=200, y=40)

entry_for_median = ttk.Entry(width=30)
entry_for_median.place(x=200, y=70)

entry_for_deviation = ttk.Entry(width=30)
entry_for_deviation.place(x=200, y=100)


# Кнопка запуска
# plot_button = ttk.Button(text="Запустить", command=CheckCombobox)
plot_button = ttk.Button(text="Запустить", command=CheckCombobox)
plot_button.place(x=30, y=140)






if __name__ == "__main__":
    window.mainloop()