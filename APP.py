import tkinter.font
from tkinter import *
from tkinter import ttk , filedialog

import control_map
import median_map
import average_value
from median_map import FLAGS
from tkinter.messagebox import showerror, showwarning, showinfo
global FILE_NAME
FILE_NAME = 'Файл не выбран'


def ClearWidgets():
    if len(control_map.FLAGS) >= 1:
        control_map.FLAGS.clear()
    if control_map.TO_DELETE_LABEL:
        control_map.TO_DELETE_LABEL.destroy()
    if control_map.TO_DELETE_WIDGET:
        control_map.TO_DELETE_WIDGET.destroy()

    if len(median_map.FLAGS) >= 1:
        median_map.FLAGS.clear()
    if median_map.TO_DELETE_LABEL:
        median_map.TO_DELETE_LABEL.destroy()
    if median_map.TO_DELETE_WIDGET:
        median_map.TO_DELETE_WIDGET.destroy()

    if len(average_value.FLAGS) >= 1:
        average_value.FLAGS.clear()
    if average_value.TO_DELETE_LABEL:
        average_value.TO_DELETE_LABEL.destroy()
    if average_value.TO_DELETE_WIDGET:
        average_value.TO_DELETE_WIDGET.destroy()

def CheckCombobox():
    ClearWidgets()

    if combobox.get() == cards[0]:
        # Борщев
        if (r_var.get() == 1 and entry_for_deviation.get() != '' and entry_for_median.get() != '' and entry_for_count.get() != ''):
            control_map.start_work(
                r_var.get(),
                float(entry_for_median.get()),
                float(entry_for_deviation.get()),
                int(entry_for_count.get()),
                window,
                'none'
            )
        if (r_var.get() == 0 and FILE_NAME != ''):
            control_map.start_work(
                r_var.get(),
                0,
                0,
                0,
                window,
                FILE_NAME
            )
    elif combobox.get() == cards[1]:
        # Грошев
        if (
                r_var.get() == 1 and entry_for_deviation.get() != '' and entry_for_median.get() != '' and entry_for_count.get() != ''):
            average_value.start_work(
                r_var.get(),
                float(entry_for_median.get()),
                float(entry_for_deviation.get()),
                int(entry_for_count.get()),
                window,
                'none'
            )
        if (r_var.get() == 0 and FILE_NAME != ''):
            average_value.start_work(
                r_var.get(),
                0,
                0,
                0,
                window,
                FILE_NAME
            )

    elif combobox.get() == cards[2]:
        # Попов
        if (r_var.get()==1 and entry_for_deviation.get()!='' and entry_for_median.get()!='' and entry_for_count.get()!=''):
            median_map.start_work(
                r_var.get(),
                float(entry_for_median.get()),
                float(entry_for_deviation.get()),
                int(entry_for_count.get()),
                window,
                'none'
            )
        if (r_var.get() == 0 and FILE_NAME!=''):
            median_map.start_work(
                    r_var.get(),
                    0,
                    0,
                    0,
                    window,
                    FILE_NAME
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
        file_button.state(['!disabled'])
    elif r_var.get() == 1:
        file_button.state(['disabled'])
        entry_for_median.state(["!disabled"])
        entry_for_deviation.state(["!disabled"])
        entry_for_count.state(["!disabled"])

def open_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    try:
        filepath = filedialog.askopenfilename(filetypes =filetypes)
        global FILE_NAME
        FILE_NAME = filepath

        buf_mas = filepath.split('/')
        lbl_for_file.config(text=f"Текущий файл:{buf_mas[len(buf_mas)-1]}")
        showinfo(title="Сообщение об открытии файла", message=f"Файл {buf_mas[len(buf_mas)-1]}\n успешно выбран!")
    except:
        showerror(title="Сообщение об открытии файла", message=f"Что-то пошло не так")


window = Tk()  # Иницилизация окна
window.title('Контрольные Карты Шухарта')  # Заголовок окна
window.geometry("1400x800")  # Размер окна

# Заголовки
lbl_for_combox = Label(text="Выберите карту:")
lbl_for_combox.place(x=30, y=40)

lbl_for_file = Label(text=f"Текущий файл:{FILE_NAME}")
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

# entry_for_file = ttk.Entry(width=30)
# entry_for_file.place(x=210, y=70)
# entry_for_file.state(['disabled'])  # изначально не работает так-как чекбокс в таком положении

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

file_button = ttk.Button(text = "Выбрать файл", command=open_file)
file_button.place(x=210,y=70,width=187)
file_button.state(['disabled'])

if __name__ == "__main__":
    window.mainloop()