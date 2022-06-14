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
    
    start_temperature = 400
    end_temperature = 300
    air_temperature = 280
    
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
        temp += 10

    radius_entry.config(highlightthickness=0)
    heat_transfer_entry.config(highlightthickness=0)

    update_plot(x, y)
    result_entry.insert(0, "{:.2f}".format(x[-1]))

# Обновление графика
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
    toolbar = NavigationToolbar2Tk(canvas, plot_frame)
    toolbar.update()
    canvas.get_tk_widget().pack()

# Графический пользовательский интерфейс
window = Tk()
window.title("Время остывание металлического шара")
window.geometry("1000x600+560+200")
window.resizable(0,0)
window.config(bg = 'white')

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
heat_transfer_entry = Entry(data_frame, font="Arial 15", relief=RIDGE, borderwidth=3, width=10)
heat_transfer_entry.pack(pady=5, fill=X, padx=5, anchor = W)
heat_transfer_entry.insert(0, 0.01)

# Поле для вывода результата
Label(data_frame, text="Результат, с", bg="white", font="Arial 15 italic").pack(anchor = W)
result_entry = Entry(data_frame, font="Arial 15", relief=RIDGE, borderwidth=3, width=10)
result_entry.pack(pady=5, fill=X, padx=5, anchor = W)

# Окно с графиком
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

# Кнопка запуска программы
start_button = Button(data_frame, text="Рассчитать время", bg="white", font="Arial 15 bold",relief=RIDGE, command=make_calc)
start_button.pack(pady=5, fill=X, padx=5, side = BOTTOM, anchor=S)
window.mainloop()
