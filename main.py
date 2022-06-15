from math import pi, log
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# Теплоемкости металлов
heat_capacities = {'Железо': 452,
            'Алюминий': 897,
            'Медь': 420,
            'Сталь': 468,
            'Латунь': 400,
            'Чугун': 540,
            'Олово': 228,
            'Свинец': 128}

def make_calc():
    result_entry.delete(0,"end")
    x = []
    y = []
    
    start_temperature = float(start_temp_entry.get())
    end_temperature = float(end_temp_entry.get())
    air_temperature = float(air_temp_entry.get())
    
    try:
        radius = float(radius_entry.get())
        if (radius <= 0):
            raise WrongBaseNumber('Wrong number must be greater then zero')
    except:
        radius_entry.config(highlightthickness=2, highlightbackground="red")
        return

    try:
        # Коэффициент теплоотдачи
        heat_transfer = float(heat_transfer_entry.get())
        if (heat_transfer <= 0):
            raise WrongBaseNumber('Wrong number must be greater then zero')
    except:
        heat_transfer_entry.config(highlightthickness=2, highlightbackground="red")
        return

    heat_capacity = heat_capacities[choice.get()]
    area = 4*pi*(radius**2)
    temp = 0
    
    while (start_temperature - temp >= end_temperature):

        k = (heat_transfer*area)/heat_capacity
        t = (-1/k)*log((start_temperature-temp-air_temperature)/(start_temperature-air_temperature))
        x.append(t)
        y.append(start_temperature-temp)
        temp += 5

    radius_entry.config(highlightthickness=0)
    heat_transfer_entry.config(highlightthickness=0)

    update_plot(x, y)
    result_entry.insert(0, "{:.2f}".format(x[-1]))
<<<<<<< HEAD
    
# Обновление графика
=======
   
#Обновление графика
>>>>>>> 8288bed (added tooltip, entryes for base info)
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
<<<<<<< HEAD
    canvas.get_tk_widget().pack()
=======
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
>>>>>>> 8288bed (added tooltip, entryes for base info)

# Графический пользовательский интерфейс
window = Tk()
window.title("Время остывание металлического шара")
window.geometry("1000x600+560+200")
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
heat_capacities_list = OptionMenu(data_frame, choice, *heat_capacities)
heat_capacities_list.config(bg="white", relief = RIDGE, font="Arial 15")
heat_capacities_list.pack(pady=5, fill=X, padx=5, anchor = W)
# Поле для ввода коэффициента теплоотдачи
Label(data_frame, text="Коэффициент теплоотдачи", bg="white", font="Arial 15 italic").pack(anchor = W)
<<<<<<< HEAD
heat_transfer_entry = Entry(data_frame, font="Arial 15", relief=RIDGE, borderwidth=3, width=10)
heat_transfer_entry.pack(pady=5, fill=X, padx=5, anchor = W)
heat_transfer_entry.insert(0, 100)
=======

heat_transfer_frame = Frame(data_frame, bg="white")
heat_transfer_frame.pack()

heat_transfer_entry = Entry(heat_transfer_frame, font="Arial 15", relief=RIDGE, borderwidth=3)
heat_transfer_entry.pack(pady=5, padx=5,side = LEFT)
heat_transfer_entry.insert(0, 9)
heat_transfer_help = Button(heat_transfer_frame, font="Arial 15", relief=RIDGE, text="?", borderwidth = 3, bg="white")
heat_transfer_help.pack(pady=2, padx=2, side = LEFT)
CreateToolTip(heat_transfer_help, text="Среда - ВОЗДУХ\nСП 50.13330.2012:\nОбобщенные справочные данные:\nα=2...10 (до 25) при свободной конвекции\nα=10...150 (до 300) при принудительной конвекции (ветер, венти\nлятор)")
>>>>>>> 8288bed (added tooltip, entryes for base info)

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
base_data_window.geometry("350x275+560+200")
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
