from tkinter import *
from tkinter import ttk
import median_map
import Plot_1
from Plot_1 import BuildPlot
from median_map import  BuildPlot
# функция отрисовки


def show_graph():
    """
    Стандартная карта
    :return:
    """
    Plot_1.BuildPlot(float(entry_for_median.get()),float(entry_for_deviation.get()),entry_for_file.get(),50,50, window=window)
def show_graph_1():
    """
    Карта медианных значений
    :return:
    """
    median_map.BuildPlot(50,50, window=window)
def selected(event):
    # получаем выделенный элемент
    selection = combobox.get()
    print(selection)
def check_combobox():
    if (combobox.get()==cards[0]):
        #вызов карты Вани Борщева
        show_graph()
    elif ((combobox.get()==cards[1])):
        pass
    elif ((combobox.get()==cards[2])):
        # вызов карты Семы Попова
        show_graph_1()
    elif ((combobox.get() == cards[3])):
        pass


# иницилизация окна
window = Tk()

# Заголовок
window.title('Контрольные Карты Шухарта')

# Размер Окна
window.geometry("650x600")

# frame_form = LabelFrame(width=100, height=400)
# frame_form.pack()
#кнопки
plot_button = ttk.Button(text="Запустить",command=check_combobox)

plot_button.grid(row=3, column=2,sticky='ew')
#выбор
cards = ["Контрольные карты для управления процессом по уровню настройки", "x-карты для средних значений", "x-карты медиан", "x-карты исходных значений"]
combobox = ttk.Combobox(values=cards,width=45 ,state="readonly")
combobox.grid(row=0,column=1,columnspan=2,sticky='w',padx=100)
# combobox.bind("<<ComboboxSelected>>", selected)
#формы вводы данных
entry_for_file=ttk.Entry()
entry_for_file.grid(row=1,column=1,sticky='w',pady=6,padx=100)

entry_for_median=ttk.Entry()
entry_for_median.grid(row=2,column=1,sticky='w',pady=6,padx=100)

entry_for_deviation=ttk.Entry()
entry_for_deviation.grid(row=3,column=1,sticky='w',pady=6,padx=100)
#текстовые лейблы:
lbl_for_file=Label(text="Введите имя Файла:")
lbl_for_file.grid(row=1,column=0,sticky='w')

lbl_for_median=Label(text="Введите среднее значение:")
lbl_for_median.grid(row=2,column=0,sticky='w')

lbl_for_deviation=Label(text="Введите отклонение:")
lbl_for_deviation.grid(row=3,column=0,sticky='w')

lbl_for_combox=Label(text="Выберите карту")
lbl_for_combox.grid(row=0,column=0,sticky='w')
#конфигураций столбцов

#конфигурация строк

if __name__ == "__main__":
    window.mainloop()
