import tkinter.font
from tkinter import *
from tkinter import ttk
import Plot_1
import median_map
from median_map import FLAGS

def ShowPlot1():
    Plot_1.BuildPlot(float(entry_for_median.get()), float(entry_for_deviation.get()), entry_for_file.get(), 50, 50,
                     window=window)


# def ShowPlot2():
#     median_map.start_work_median()


def CheckCombobox():
    if combobox.get() == cards[0]:
        # Борщев
        ShowPlot1()
    elif combobox.get() == cards[1]:
        # Грошев
        pass
    elif combobox.get() == cards[2]:
        # Попов
        if (r_var.get()==1 and entry_for_deviation.get()!='' and entry_for_median.get()!='' and entry_for_count.get()!=''):
            median_map.start_work_median(
                r_var.get(),
                float(entry_for_median.get()),
                float(entry_for_deviation.get()),
                int(entry_for_count.get()),
                window,
                'none'
            )


        if (r_var.get() == 0 and entry_for_file.get()!=''):
            median_map.start_work_median(
                    r_var.get(),
                    0,
                    0,
                    0,
                    window,
                    entry_for_file.get()
            )


    elif combobox.get() == cards[3]:
        # Курдюков
        pass


def selected(event):
    if combobox.get() == cards[2]:
        # Попов
        lbl_for_median.config(text='Введите мат.ожидание')
        lbl_for_deviation.config(text='Введите дисперсию')
    if combobox.get() == cards[0]:
        # Борщев
        lbl_for_median.config(text='Введите среднее значение')
        lbl_for_deviation.config(text='Введите отклонение')


def check_widget_activity():
    if r_var.get() == 0:
        entry_for_median.state(["disabled"])
        entry_for_deviation.state(["disabled"])
        entry_for_count.state(["disabled"])
        entry_for_file.state(['!disabled'])
    elif r_var.get() == 1:
        entry_for_file.state(['disabled'])
        entry_for_median.state(["!disabled"])
        entry_for_deviation.state(["!disabled"])
        entry_for_count.state(["!disabled"])


window = Tk()  # Иницилизация окна
window.title('Контрольные Карты Шухарта')  # Заголовок окна
window.geometry("1400x800")  # Размер окна

# Заголовки
lbl_for_combox = Label(text="Выберите карту:")
lbl_for_combox.place(x=30, y=40)

lbl_for_file = Label(text="Введите имя файла:")
lbl_for_file.place(x=30, y=70)

lbl_for_median = Label(text="Введите среднее значение:")
lbl_for_median.place(x=30, y=100)

lbl_for_deviation = Label(text="Введите отклонение:")
lbl_for_deviation.place(x=30, y=130)

lbl_for_count = Label(text="Введите количество элементов:")
lbl_for_count.place(x=30, y=160)

# Формы считывания данных
cards = ["Контрольные карты управления процессом", "Контрольные карты средних значений", "Контрольные карты медиан",
         "Контрольные карты исходных значений"]
combobox = ttk.Combobox(values=cards, width=40, state="readonly")
combobox.place(x=210, y=40)
combobox.bind("<<ComboboxSelected>>", selected)

entry_for_file = ttk.Entry(width=30)
entry_for_file.place(x=210, y=70)
entry_for_file.state(['disabled'])  # изначально не работает так-как чекбокс в таком положении

entry_for_median = ttk.Entry(width=30)
entry_for_median.place(x=210, y=100)

entry_for_deviation = ttk.Entry(width=30)
entry_for_deviation.place(x=210, y=130)

entry_for_count = ttk.Entry(width=30)
entry_for_count.place(x=210, y=160)
# чекбоксы отвечающие за считывания с файла или генераций новои последовательности
r_var = IntVar()
r_var.set(1)
r1 = Radiobutton(text='Получить выборку из файла', variable=r_var, value=0, command=check_widget_activity)
r2 = Radiobutton(text='Задать параметры выборки и сгенерировать её', variable=r_var, value=1,
                 command=check_widget_activity)
r1.place(x=330, y=0)
r2.place(x=30, y=0)
# кнопки
plot_button = ttk.Button(text="Запустить", command=CheckCombobox)
plot_button.place(x=30, y=200)

if __name__ == "__main__":
    window.mainloop()
