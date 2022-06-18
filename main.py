from math import pi, log
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# Данные металлов плотность | теплоемкость
materials = {'Железо': [7874, 452],
            'Алюминий': [2650, 897],
            'Медь': [8940, 420],
            'Сталь': [7850, 468],
            'Латунь': [8730, 400],
            'Чугун': [7200, 540],
            'Олово': [7300, 228],
            'Свинец': [11370, 128]}

# Исключения
class InvalidStartEndTemperatureValues(Exception):
    pass

class InvalidStartAirTemperatureValue(Exception):
    pass

class InvalidEndAirTemperatureValue(Exception):
    pass

class InvalidAirTemperature(Exception):
    pass

# Подсветка виджета при наблюдении исключения
def highlight(widget, text):
    widget.config(highlightthickness=2, highlightbackground="red")
    if (text == ''):
        return
    
    widget_tooltip = CreateToolTip(widget, text=text)
    return widget_tooltip

# Основная функция расчета
def make_calc():
    result_entry.delete(0,"end")
    x = []
    y = []

    # Подсказки при возникновении ошибок
    start_temp_help = CreateToolTip(start_temp_entry, text='')
    end_temp_help = CreateToolTip(end_temp_entry, text='')
    air_temp_help = CreateToolTip(air_temp_entry, text='')
    radius_entry_help = CreateToolTip(radius_entry, text='')
    heat_transfer_tooltip = CreateToolTip(heat_transfer_entry, text='')

    # Подсветка полей с неверными данными
    start_temp_entry.config(highlightthickness=0)
    end_temp_entry.config(highlightthickness=0)
    air_temp_entry.config(highlightthickness=0)
    radius_entry.config(highlightthickness=0)
    heat_transfer_entry.config(highlightthickness=0) 

    #Получение данных и обработка исключений
    try:
        start_temperature = float(start_temp_entry.get())
        end_temperature = float(end_temp_entry.get())
        air_temperature = float(air_temp_entry.get())
        if (start_temperature == end_temperature):
            raise InvalidStartEndTemperatureValues()
        
        if (start_temperature ==  air_temperature):
            raise InvalidStartAirTemperatureValue()
        
        if (end_temperature == air_temperature):
            raise InvalidEndAirTemperatureValue()

        if (start_temperature > end_temperature and air_temperature > end_temperature):
            raise InvalidAirTemperature()
        
        if (start_temperature < end_temperature and air_temperature < end_temperature):
            raise InvalidAirTemperature()

    except InvalidStartEndTemperatureValues:
        start_temp_help = highlight(start_temp_entry, text="Значение начальной и конечной температуры должны отличаться!")
        end_temp_help = highlight(end_temp_entry, text="Значение начальной и конечной температуры должны отличаться!")
        return

    except InvalidStartAirTemperatureValue:
        start_temp_help = highlight(start_temp_entry, text="Неверные значения начальной температуры тела и температуры\nвоздуха\nДолжны быть разными")
        air_temp_help = highlight(air_temp_entry, text="Неверные значения начальной температуры тела и температуры\nвоздуха\nДолжны быть разными")
        return

    except InvalidEndAirTemperatureValue:
        end_temp_help = highlight(end_temp_entry, text="Неверные значения конечной температуры тела и температуры\nвоздуха\nДолжны быть разными")
        air_temp_help = highlight(air_temp_entry, text="Неверные значения конечной температуры тела и температуры\nвоздуха\nДолжны быть разными")
        return

    except InvalidAirTemperature:
        air_temp_help = highlight(air_temp_entry, text="Неверное значение температуры воздуха\nПроцесс охлаждение: температура воздуха <= конечная температура\nПроцесс нагревания: температура воздуха >= конечная температура")
        return
    
    except ValueError:
        if (start_temp_entry.get() == ''):
            start_temp_help = highlight(start_temp_entry, text="Значение не должно быть пустым!")
        if (end_temp_entry.get() == ''):
            end_temp_help = highlight(end_temp_entry, text="Значение не должно быть пустым!")
        if (air_temp_entry.get() == ''):
            air_temp_help = highlight(air_temp_entry, text="Значение не должно быть пустым!") 
        return
    try:
        radius = float(radius_entry.get())
        if (radius <= 0):
            raise WrongBaseNumber('Wrong number must be greater then zero')
    except:
        radius_temp_help = highlight(radius_entry, text="Неверное значение радиуса шара\nМеньше или равно нулю, либо содержатся неподдерживаемые символы")
        return

    try:
        # Коэффициент теплоотдачи
        heat_transfer = float(heat_transfer_entry.get())
        if (heat_transfer <= 0):
            raise WrongBaseNumber('Wrong number must be greater then zero')
    except:
        heat_transfer_help = highlight(heat_transfer_entry, text="Неверное значение коэффициента теплообмена\nМеньше или равно нулю, либо содержатся неподдерживаемые символы")
        return
  
    density = materials[choice.get()][0]
    heat_capacity = materials[choice.get()][1]
    surface_area = 4*pi*(radius**2)
    volume = (4/3)*pi * radius**3
    temp_change = 0
    t = 0

    while (start_temperature > end_temperature):

        t = t + (log(abs(start_temperature-air_temperature))-log(abs(start_temperature-temp_change-air_temperature)))*heat_capacity*density*volume/(heat_transfer*surface_area)
        x.append(t)
        y.append(start_temperature-temp_change)
        start_temperature = start_temperature-temp_change
        temp_change = 1
    
    while (start_temperature < end_temperature):

        t = t + (log(abs(start_temperature-air_temperature))-log(abs(start_temperature+temp_change-air_temperature)))*heat_capacity*density*volume/(heat_transfer*surface_area)
        x.append(t)
        y.append(start_temperature+temp_change)
        start_temperature = start_temperature+temp_change
        temp_change = 1
  
    update_plot(x, y)
    result_entry.insert(0, "{:.2f}".format(x[-1]))
    
   
#Обновление графика
def update_plot(x, y):
    global figure, plot, canvas
    figure.delaxes(plot)

    plot = figure.add_subplot(111)
    plot.plot(x,y)
    plot.grid()
    plot.set_title("Зависимость температуры шарика от времени")
    plot.set_xlabel("Время, с")
    plot.set_ylabel("Температура, К")
    
    canvas.draw()
    canvas.get_tk_widget().pack()
    canvas.get_tk_widget().pack() 

def change_base_data():
    global base_data_window
    base_data_window.deiconify()

def on_closing_data():
    global base_data_window
    base_data_window.withdraw()

def on_closing_main_window():
    global window, base_data_window
    base_data_window.destroy()
    window.destroy()

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    return toolTip
# Графический пользовательский интерфейс
window = Tk()
window.title("Время остывание металлического шара")
window.geometry("1000x600+450+200")
window.resizable(0,0)
window.config(bg = 'white')
window.protocol("WM_DELETE_WINDOW", on_closing_main_window)

plot_frame = Frame(window, bg="white")
plot_frame.pack(side=LEFT)

data_frame = Frame(window, bg="white")
data_frame.pack(side=LEFT, fill=Y, padx = 10, pady = 10)

Label(data_frame, text="Рассчет времени остывания\n шарика в воздухе", bg="white", font="Arial 15 bold").pack(side=TOP, anchor=N) 

# Поле для ввода радиуса шарика
Label(data_frame, text="Радиус шарика, м", bg="white", font="Arial 15 italic").pack(anchor = W)
radius_entry = Entry(data_frame, font="Arial 15", borderwidth=3, relief= RIDGE, width=10)
radius_entry.pack(pady=5, fill=X, padx=5, anchor = W)
radius_entry.insert(0, 0.01)

# Меню для выбора материала шарика
Label(data_frame, text="Материал", bg="white", font="Arial 15 italic").pack(anchor = W)
choice = StringVar()
choice.set('Железо')
materials_list = OptionMenu(data_frame, choice, *materials)
materials_list.config(bg="white", relief = RIDGE, font="Arial 15")
materials_list.pack(pady=5, fill=X, padx=5, anchor = W)

# Поле для ввода коэффициента теплоотдачи
Label(data_frame, text="Коэффициент теплоотдачи", bg="white", font="Arial 15 italic").pack(anchor = W)
heat_transfer_frame = Frame(data_frame, bg="white")
heat_transfer_frame.pack()

heat_transfer_entry = Entry(heat_transfer_frame, font="Arial 15", relief=RIDGE, borderwidth=3)
heat_transfer_entry.pack(pady=5, padx=5,side = LEFT)
heat_transfer_entry.insert(0, 9)
heat_transfer_help = Button(heat_transfer_frame, font="Arial 15", relief=RIDGE, text="?", borderwidth = 3, bg="white")
heat_transfer_help.pack(pady=2, padx=2, side = LEFT)
CreateToolTip(heat_transfer_help, text="Среда - ВОЗДУХ\nСП 50.13330.2012:\nОбобщенные справочные данные:\nα=2...10 (до 25) при свободной конвекции\nα=10...150 (до 300) при принудительной конвекции (ветер, венти\nлятор)")

# Поле для вывода результата
Label(data_frame, text="Результат, с", bg="white", font="Arial 15 italic").pack(anchor = W)
result_entry = Entry(data_frame, font="Arial 15", relief=RIDGE, borderwidth=3, width=10)
result_entry.pack(pady=5, fill=X, padx=5, anchor = W)

# Окно с 
figure = Figure(figsize=(6, 5), dpi=110)
plot = figure.add_subplot(111)
plot.plot()
plot.grid()
plot.set_title("Зависимость температуры шарика от времени")
plot.set_xlabel("Время, с")
plot.set_ylabel("Температура, К")

canvas = FigureCanvasTkAgg(figure, master=plot_frame)
canvas.draw()
canvas.get_tk_widget().pack()
toolbar = NavigationToolbar2Tk(canvas, plot_frame)
toolbar.update()
canvas.get_tk_widget().pack()

base_data_button = Button(data_frame, bg="white", font="Arial 12 bold", text="Изменить начальные данных", relief=RIDGE, command=change_base_data)
base_data_button.pack(pady=5, fill=X, padx=5)

# Кнопка запуска программы
start_button = Button(data_frame, text="Рассчитать время", bg="white", font="Arial 15 bold",relief=RIDGE, command=make_calc)
start_button.pack(pady=5, fill=X, padx=5, side = BOTTOM, anchor=S)

base_data_window = Tk()
base_data_window.title("Изменение начальных данных")
base_data_window.geometry("350x275+1450+200")
base_data_window.resizable(0,0)
base_data_window.config(bg = 'white')
base_data_window.withdraw()
base_data_window.protocol("WM_DELETE_WINDOW", on_closing_data)

base_data_frame = Frame(base_data_window, bg="white")
base_data_frame.pack(padx=15, pady=15)

Label(base_data_frame, font="Arial 14 bold", text="Изменение начальных данных", bg="white").pack()

Label(base_data_frame, font="Arial 12 italic", text="Начальная температура шара, К", bg="white").pack(anchor=W)
start_temp_entry = Entry(base_data_frame, font="Arial 15", relief=RIDGE, borderwidth=3, width=10)
start_temp_entry.pack(padx = 5, pady = 5, fill=X)
start_temp_entry.insert(0,400)

Label(base_data_frame, font="Arial 12 italic", text="Конечная температура шара, К", bg="white").pack(anchor=W)
end_temp_entry = Entry(base_data_frame, font="Arial 15", relief=RIDGE, borderwidth=3, width=10)
end_temp_entry.pack(padx = 5, pady = 5, fill=X)
end_temp_entry.insert(0, 300)

Label(base_data_frame, font="Arial 12 italic", text="Температура воздуха, К", bg="white").pack(anchor=W)
air_temp_entry = Entry(base_data_frame, font="Arial 15", relief=RIDGE, borderwidth=3, width=10)
air_temp_entry.pack(padx = 5, pady = 5, fill=X)
air_temp_entry.insert(0,280)

window.mainloop()
