from math import sin, cos, pi
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from os import startfile
import sys


def loop():
    get_e1()
    root.after(100, loop)


def get_e1():
    global pr
    a = entry1.get()
    if (pr != a):
        pr = a
        if a.isdigit():
            S(int(a))
            entry2['state'] = NORMAL
            entry2.delete(1.0, END)
            entry2.insert(1.0, "\n".join(['t='+str(i[0])+' с x='+str(i[1])+' мкм y='+str(i[2])+' мм z='+str(i[3])+' м'
                                          for i in coordinates]))
            entry2['state'] = DISABLED
        else:
            entry2['state'] = NORMAL
            entry2.delete(1.0, END)
            entry2.insert(1.0, '–')
            entry2['state'] = DISABLED


def stop():
    global STOP
    STOP = True


def export_data():
    global FLAG
    FLAG = False

    b1['state'] = DISABLED
    dir = filedialog.askdirectory(initialdir="\\", title="Выбор расположения")
    if dir != '':
        f = open(dir + "\\Падение с высоты {0} м.txt".format(int(coordinates[0][3])), "w")
        f.write("\n".join(['t='+str(i[0])+' с x='+str(i[1])+' мкм y='+str(i[2])+' мм z='+str(i[3])+' м'
                                          for i in coordinates]))
        f.close()

        export = messagebox.askyesno(title="Готово", message="Файл успешно создан. Открыть его?")
        if export:
            try:
                startfile(dir + "\\Падение с высоты {0} м.txt".format(int(coordinates[0][3])))
            except:
                messagebox.showerror("Ошибка!", "Не удалось найти файл!")
    FLAG = True
    b1['state'] = NORMAL


def plot1():
    fig = Figure(figsize=(5, 5), dpi=80)

    x = [abs(i[1]) for i in coordinates]
    y = [i[3] for i in coordinates]

    plot1 = fig.add_subplot(111)
    plot1.set_title("Величина отклонения по оси Ox при падении\nс высоты 158 метров")
    plot1.plot(x, y)
    plot1.set_xlabel("Отклонение, мкм")
    plot1.set_ylabel("Высота, м")

    canvas = FigureCanvasTkAgg(fig, master=frame_2)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, frame_2)
    toolbar.update()
    canvas.get_tk_widget().pack()


def plot2():
    fig2 = Figure(figsize=(5, 5), dpi=80)

    x = [abs(i[2]) for i in coordinates]
    y = [i[3] for i in coordinates]

    plot2 = fig2.add_subplot(111)
    plot2.set_title("Величина отклонения по оси Oy при падении\nс высоты 158 метров")
    plot2.plot(x, y)
    plot2.set_xlabel("Отклонение, мм")
    plot2.set_ylabel("Высота, м")

    canvas2 = FigureCanvasTkAgg(fig2, master=frame_3)
    canvas2.draw()
    canvas2.get_tk_widget().pack()
    toolbar2 = NavigationToolbar2Tk(canvas2, frame_3)
    toolbar2.update()
    canvas2.get_tk_widget().pack()


def S(h, phi=48 * pi / 180):
    global coordinates, pbc, FLAG, STOP

    coordinates = []
    g = 9.80616
    w = 2 * pi / 24 / 3600
    wx = w * cos(phi)
    wz = w * sin(phi)
    dt = 0.00001
    hp = 0.1
    np = int(hp / dt)
    x = 0
    y = 0
    z = h
    vx = 0
    vy = 0
    vz = 0
    t = 0

    pbc['maximum'] = int((2 * h / g)**0.5 // 0.1)
    pbc['value'] = 0
    k = 0

    flag = True
    while flag and not STOP:
        FLAG = False
        b2['state'] = NORMAL
        b1['state'] = DISABLED
        for i in range(1, np + 1):
            x += vx * dt
            y += vy * dt
            z += vz * dt
            vx += 2 * vy * wz * dt
            vy += 2 * (vz * wx - vx * wz) * dt
            vz += (-g - 2 * vy * wx) * dt
            if z < 0:
                flag = False
                break
            t += dt
        coordinates.append([round(t, 2), round(x * 1000000, 3), round(y * 1000, 3), round(z, 1)])
        pbc['value'] += 1
        pbc.update()
        k += 1
        if entry1.get() != str(h) and FL:
            STOP = True
    if not STOP:
        pass#del coordinates[-1]
    else:
        coordinates = [['(...)', '(...)', '(...)', 0]]

    FLAG = True
    b2['state'] = DISABLED
    b1['state'] = NORMAL
    STOP = False


def exit_def():
    root.destroy()
    sys.exit(0)


def help():
    top = Toplevel(root)
    top.title("Положение осей координат")
    top.iconbitmap("icon.ico")
    top.resizable(0, 0)
    img = PhotoImage(file="img.gif")
    panel = Label(top, text='Положение осей координат', font='Arial 14', anchor=CENTER, bg='white', borderwidth=0)
    panel.pack(pady=0, fill=X)
    panel = Label(top, image=img, borderwidth=0)
    panel.pack(pady=0)
    top.mainloop()


root = Tk()
root.title("Свободное падение тела в шахте")
root.iconbitmap("icon.ico")
root.resizable(0, 0)
root.protocol('WM_DELETE_WINDOW', exit_def)

frame_3 = Frame(root, bg="white")
frame_3.pack(side=RIGHT)

frame_2 = Frame(root, bg="white")
frame_2.pack(side=RIGHT)

frame_1 = Frame(root, bg="#ffffff")
frame_1.pack(side=RIGHT, fill=Y)

Label(frame_1, text="Расчет падения с высоты, м", bg="#ffffff", font="Arial 15 bold").pack(anchor=W)

entry1 = Entry(frame_1, font="Arial 15", relief="groove", borderwidth=3, width=30)
entry1.pack(pady=5, fill=X, padx=5)
entry1.insert(0, "158")

frame_4 = Frame(frame_1, bg="white")
frame_4.pack()
coordinates = []

entry2 = Text(frame_4, height=10, font="Arial 12", relief="solid", borderwidth=1, width=40)
entry2.pack(pady=5)
scroll = Scrollbar(frame_4, borderwidth=10, command=entry2.yview)
scroll.pack(side=RIGHT, fill=Y)
entry2.config(yscrollcommand=scroll.set)
entry2.pack(side=LEFT, padx=5)

entry2.delete(1.0, END)
entry2.insert(1.0, "\n".join(['t='+str(i[0])+' с x='+str(i[1])+' мкм y='+str(i[2])+' мм z='+str(i[3])+' м'
                                          for i in coordinates]))
entry2['state'] = DISABLED

pbc = Progressbar(frame_1, orient="horizontal", maximum=1, mode="determinate")
pbc.pack(fill=X, padx=5)

STOP = False
b2 = Button(frame_1, text="Стоп", font="Arial 12", fg="black", state=DISABLED, command=stop)
b2.pack(anchor=W, pady=5, padx=4)

FLAG = True
b1 = Button(frame_1, text="Экспортировать", font="Arial 13", fg="black", command=export_data)
b1.pack(anchor=W, pady=5, padx=4)

b3 = Button(frame_1, text="Справка", font="Arial 10 underline", fg="blue", relief='flat', borderwidth=0,
            background='white', activebackground='white', activeforeground='blue', command=help)
b3.pack(anchor=W, padx=4)

Label(frame_1, text=" © Сагайдак Алексей, АВТ-113", bg="#ffffff", fg="grey",
      font="Arial 11").pack(anchor=W, side=BOTTOM)

FL = False
S(160)
pr = ''

plot1()
plot2()
loop()

FL = True
root.mainloop()
