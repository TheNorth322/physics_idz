from math import pi, log
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import sys

thermal_conductivities = {'Железо': 92,
                        'Алюминий': 230,
                        'Медь': 380,
                        'Сталь': 52,
                        'Латунь': 110,
                        'Чугун': 56}

entry_statuses = ["Full","Full"]

def get_bio_num(tcond, radius, heat_transfer):
    bio_num = tcond*radius / heat_transfer
    return bio_num

def get_D_param(bio_num):
    D = (21*bio_num*(bio_num+5))/(2*bio_num**2 + 14*bio_num + 35)
    return D

def make_calc():
    result_entry.delete(0,"end")
    x = []
    y = []
    
    if (radius_entry.get() == ''):
        radius_entry.insert(0,"0.01")
    if (heat_transfer_entry.get() == ''):
        heat_transfer_entry.insert(0,"0.000001")

    start_temperature = 400 # начальная температура шара
    end_temperature = 300 # конечная температура шара
    air_temperature = 280 # температура воздуха
    radius = float(radius_entry.get()) # радиус шара
    material = choice.get()
    heat_transfer = float(heat_transfer_entry.get()) # for change
    ball_area = 4*pi*(radius**2)

    bio_num = get_bio_num(thermal_conductivities[material], radius, heat_transfer)
    D = get_D_param(bio_num)

    while (end_temperature != start_temperature):

        time = (radius/(-heat_transfer*D))*log((air_temperature-end_temperature)/(D/6*(air_temperature-start_temperature)*((bio_num+2)/bio_num)-1))
        x.append(time)
        y.append(end_temperature+10)
        end_temperature += 10

    update_plot(x, y)
    result_entry.insert(0, str(x[0]))

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

#GUI
window = Tk()
window.title("Время остывание металлического шара")
window.geometry("1000x600+560+200")
window.resizable(0,0)
window.config(bg = 'white')

plot_frame = Frame(window, bg="white")
plot_frame.pack(side=LEFT) # for plot

data_frame = Frame(window, bg="white")
data_frame.pack(side=LEFT, fill=Y, padx = 15, pady = 15) # for data input

Label(data_frame, text="Рассчет времени остывания\n шарика", bg="white", font="Arial 15 bold").pack(side=TOP, anchor=N) 
Label(data_frame, text="Радиус шарика, м", bg="white", font="Arial 15 italic").pack(anchor = W)
radius_entry = Entry(data_frame, font="Arial 15", relief="groove", borderwidth=3, width=10)
radius_entry.pack(pady=5, fill=X, padx=5, anchor = W)
radius_entry.insert(0, "0.01")

Label(data_frame, text="Материал", bg="white", font="Arial 15 italic").pack(anchor = W)
choice = StringVar()
choice.set('Железо')
materials_list = OptionMenu(data_frame, choice, *thermal_conductivities)
materials_list.config(bg="white", font="Arial 15")
materials_list.pack(pady=5, fill=X, padx=5, anchor = W)

Label(data_frame, text="Коэффициент теплоотдачи", bg="white", font="Arial 15 italic").pack(anchor = W)
heat_transfer_entry = Entry(data_frame, font="Arial 15", relief="groove", borderwidth=3, width=10)
heat_transfer_entry.pack(pady=5, fill=X, padx=5, anchor = W)
heat_transfer_entry.insert(0, "0.000001")

Label(data_frame, text="Результат, с", bg="white", font="Arial 15 italic").pack(anchor = W)
result_entry = Entry(data_frame, font="Arial 15", relief="groove", borderwidth=3, width=10)
result_entry.pack(pady=5, fill=X, padx=5, anchor = W)

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

Label(data_frame, text="@Горшков Данил, АВТ-113", bg="white", font="Arial 10 italic").pack(anchor = W, side = BOTTOM)
start_button = Button(data_frame, text="Рассчитать время", bg="white", font="Arial 15 bold", command=make_calc)
start_button.pack(pady=5, fill=X, padx=5, side = BOTTOM, anchor=S)
window.mainloop()
