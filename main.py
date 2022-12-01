from tkinter import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from tkinter.colorchooser import *
from pyopengltk import OpenGLFrame
from math import *
from PIL.Image import open
from PIL import ImageGrab
import numpy as np


# Глобальные переменные
Work = False
Points = []
Colors = []
Drawn = list()
Color = [0.0, 0.0, 0.0]
Color2 = 'black'
Zoom = 1
dZoom = 2 ** (1/2)
RotX = RotY = 0
dRot = 15


class AppOgl(OpenGLFrame):
    def initgl(self):
        glViewport(0, 0, self.width, self.height)
        glClearColor(1.0, 1.0, 1.0, 0.0)

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT)


def ChangeColor():  # Смена цвета
    global Color, Color2
    ChooseColor = askcolor()
    Color = ChooseColor[0]
    Color2 = ChooseColor[1]
    CurColor.configure(bg=Color2)


def ReDraw():
    global Drawn
    for i in range(len(Drawn)):
        if len(Drawn[i]) == 2:
            DrawPoint(Drawn[i][0], Drawn[i][1])
        else:
            if type(Drawn[i][0]) == int:
                Draw(Drawn[i][0], Drawn[i][1], Drawn[i][2], Drawn[i][3], Drawn[i][4])
            else:
                Special(Drawn[i][0], Drawn[i][1], Drawn[i][2], Drawn[i][3], Drawn[i][4])
    app.tkSwapBuffers()


def ChangeColorBG():
    ColorBG = askcolor()[0]
    glClearColor(ColorBG[0]/255, ColorBG[1]/255, ColorBG[2]/255, 0.0)
    app.redraw()
    ReDraw()


def ZoomIn(event):
    glClear(GL_COLOR_BUFFER_BIT)
    global Zoom, dZoom
    glScalef(dZoom, dZoom, dZoom)
    Zoom *= dZoom
    LZ.config(text="Приближено в " + str(round(Zoom, 2)) + " раз")
    ReDraw()


def ZoomOut(event):
    glClear(GL_COLOR_BUFFER_BIT)
    global Zoom, dZoom
    glScalef(1/dZoom, 1/dZoom, 1/dZoom)
    Zoom /= dZoom
    LZ.config(text="Приближено в " + str(round(Zoom, 2)) + " раз")
    ReDraw()


def RotateLeft(event):
    glClear(GL_COLOR_BUFFER_BIT)
    global RotY, dRot
    glRotatef(dRot, 0.0, 1.0, 0.0)
    RotY += dRot
    LY.config(text="Угол по y = " + str(RotY))
    ReDraw()


def RotateRight(event):
    glClear(GL_COLOR_BUFFER_BIT)
    global RotY, dRot
    glRotatef(-dRot, 0.0, 1.0, 0.0)
    RotY -= dRot
    LY.config(text="Угол по y = " + str(RotY))
    ReDraw()


def RotateUp(event):
    glClear(GL_COLOR_BUFFER_BIT)
    global RotX, dRot
    glRotatef(dRot, 1.0, 0.0, 0.0)
    RotX += dRot
    LX.config(text="Угол по x = " + str(RotX))
    ReDraw()


def RotateDown(event):
    glClear(GL_COLOR_BUFFER_BIT)
    global RotX, dRot
    glRotatef(-dRot, 1.0, 0.0, 0.0)
    RotX -= dRot
    LX.config(text="Угол по x = " + str(RotX))
    ReDraw()


def SpecialClick(Color, Type, R1, R2, H):
    global Drawn
    glClear(GL_COLOR_BUFFER_BIT)
    app.tkSwapBuffers()
    a = [tuple(Color), ]
    a.append(Type)
    a.append(R1)
    a.append(R2)
    a.append(H)
    Drawn.append(tuple(a))
    Special(*a)
    app.tkSwapBuffers()


def Special(Color, Type, R1, R2, H):
    glEnable(GL_TEXTURE_2D)
    glLineWidth(1)
    QuadObj = gluNewQuadric()
    if Type == 1:
        gluQuadricDrawStyle(QuadObj, GLU_POINT)
    elif Type == 2:
        gluQuadricDrawStyle(QuadObj, GLU_LINE)
    else:
        gluQuadricDrawStyle(QuadObj, GLU_FILL)
    glColor3f(Color[-3] / 255, Color[-2] / 255, Color[-1] / 255)
    gluQuadricTexture(QuadObj, GL_TRUE)
    gluCylinder(QuadObj, R1/100, R2/100, H/100, R1-R2, H)
    glDisable(GL_TEXTURE_2D)


def DrawPoint(Color, Point):
    glBegin(GL_POINTS)
    glColor3f(Color[0] / 255, Color[1] / 255, Color[2] / 255)
    glVertex3f(Point[0], Point[1], Point[2])
    glEnd()


def Draw(NumPoints, Size, Type, Colors, Points):
    glEnable(GL_LINE_STIPPLE)
    glEnable(GL_TEXTURE_2D)

    glLineWidth(Size)
    LineType = 0
    for i in range(4):
        Cur = 0
        for j in range(4):
            Cur += int(LineVars[4 * i + j].get()) * 2 ** (3 - j)
        LineType += Cur * 16 ** (3 - i)
    glLineStipple(1, LineType)

    if Type == 1:
        glPolygonMode(GL_FRONT_AND_BACK, GL_POINT)
    elif Type == 2:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    if NumPoints == 2:
        glBegin(GL_LINES)
    elif NumPoints == 3:
        glBegin(GL_TRIANGLES)
    elif NumPoints == 4:
        glBegin(GL_QUADS)
    else:
        glBegin(GL_POLYGON)
    for i in range(NumPoints):
        glColor3f(Colors[3 * i] / 255, Colors[1 + 3 * i] / 255, Colors[2 + 3 * i] / 255)
        glTexCoord2f(Points[3 * i] / 2 + 0.5, Points[1 + 3 * i] / 2 + 0.5)
        glVertex3f(Points[3 * i], Points[1 + 3 * i], Points[2 + 3 * i])
    if NumPoints > 4:
        glColor3f(Colors[0] / 255, Colors[1] / 255, Colors[2] / 255)
        glTexCoord2f(Points[0] / 2 + 0.5, Points[1] / 2 + 0.5)
        glVertex3f(Points[0], Points[1], Points[2])
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_LINE_STIPPLE)


def Click(event):
    global Color, Points, Colors, RotX, RotY, Zoom, Drawn
    x = ((event.x-500)/500) / cos(RotY/180*pi) / Zoom
    y = -((event.y-400)/400) / cos(RotX/180*pi) / Zoom
    z = x * y * sin(RotX/180*pi) * sin(RotY/180*pi)
    Points.extend([x, y, z])
    Colors.extend(Color)
    NumPoints = int(SBP.get())
    glPointSize(int(SBT.get()))

    if len(Points) == 3:
        glClear(GL_COLOR_BUFFER_BIT)
    if NumPoints == 1 or len(Points) > 3:
        app.tkSwapBuffers()
    DrawPoint(Colors[-3:], Points[-3:])
    app.tkSwapBuffers()

    if NumPoints == 1:
        a = [tuple(Colors), ]
        a.append(tuple(Points))
        Drawn.append(tuple(a))
        DrawPoint(*a)
        Points.clear()
        Colors.clear()
    elif len(Points)/3 == NumPoints:
        a = [NumPoints, ]
        a.append(int(SBT.get()))
        a.append(FillVar.get())
        a.append(tuple(Colors))
        a.append(tuple(Points))
        Drawn.append(tuple(a))
        Draw(*a)
        Points.clear()
        Colors.clear()
        app.tkSwapBuffers()


def ChooseTexture(Type):
    if Type:
        im = open("Texture.jpg")
    else:
        im = ImageGrab.grab((420, 420, 579, 579))
    ix, iy, image = im.size[0], im.size[1], np.array(list(im.getdata()), np.uint8)
    ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, ID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


def ClickTex(event):
    global Work
    Work = True


def MoveTex(event):
    global Color2, Work
    if Work:
        Texture.create_rectangle(event.x-int(SBT.get())/2, event.y-int(SBT.get())/2, event.x+int(SBT.get())/2, event.y+int(SBT.get())/2, fill=Color2, outline=Color2)


def UnclickTex(event):
    global Work
    Work = False


def LightOn():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, np.array([0, 0, -10, 0]))
    glLightfv(GL_LIGHT0, GL_AMBIENT, np.array([int(SBLR.get())/255, int(SBLG.get())/255, int(SBLB.get())/255, 0]))
    glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1)
    glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 1)
    glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 1)
    ReDraw()


def LightOff():
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    ReDraw()


def Clear():
    app.tkSwapBuffers()
    glClear(GL_COLOR_BUFFER_BIT)
    app.tkSwapBuffers()


# Создание окна
window = Tk()
window.title("Рисовашка")
window.attributes('-fullscreen', True)

LineVars = [BooleanVar(value=True) for i in range(16)]
FillVar = IntVar(value=2)

# Поле рисования
Field = Canvas(window, width=1000, height=800)
CurColor = Canvas(window, width=100, height=100, bg='black')

# Толщина
LT = Label(window, font=("Times New Roman", 14), text="Толщина линий/точек")
SBT = Spinbox(window, from_=1, to=100, font=("Times New Roman", 14), repeatdelay=100, repeatinterval=10,
              state='readonly', textvariable=StringVar(value=10))

LP = Label(window, font=("Times New Roman", 14), text="Количество точек объекта")
SBP = Spinbox(window, from_=1, to=10, font=("Times New Roman", 14), repeatdelay=100, repeatinterval=100,
              state='readonly')
# Выбор цвета
BColor = Button(window, text='Выбор цвета', command=ChangeColor)
BColorBG = Button(window, text='Смена цвета фона', command=ChangeColorBG)

# Очистка
BClear = Button(window, text='Очистка', command=Clear)

# Тип линий
Ll = Label(window, font=("Times New Roman", 14), text="Тип линии")
CBs = [Checkbutton(window, text='', variable=LineVars[i]) for i in range(16)]

# Заливка
RBP = Radiobutton(window, variable=FillVar, value=1, font=("Times New Roman", 14), text='Точечный')
RBL = Radiobutton(window, variable=FillVar, value=2, font=("Times New Roman", 14), text='Линейный')
RBF = Radiobutton(window, variable=FillVar, value=3, font=("Times New Roman", 14), text='Заливка')

# Спец функция
BS = Button(window, text='Усечённый конус', command=lambda: SpecialClick(Color, int(FillVar.get()), int(SBR1.get()), int(SBR2.get()), int(SBH.get())))
LH = Label(window, font=("Times New Roman", 14), text='Высота')
SBH = Spinbox(window, from_=1, to=100, font=("Times New Roman", 14), repeatdelay=100, repeatinterval=10,
              state='readonly', textvariable=StringVar(value=50))
LR1 = Label(window, font=("Times New Roman", 14), text='Радиус нижнего основания')
SBR1 = Spinbox(window, from_=1, to=100, font=("Times New Roman", 14), repeatdelay=100, repeatinterval=10,
              state='readonly', textvariable=StringVar(value=75))
LR2 = Label(window, font=("Times New Roman", 14), text='Радиус верхнего основания')
SBR2 = Spinbox(window, from_=1, to=100, font=("Times New Roman", 14), repeatdelay=100, repeatinterval=10,
              state='readonly', textvariable=StringVar(value=25))

# Текстуры
BTL = Button(window, text='Загрузка текстуры', command=lambda: ChooseTexture(True))
BTD = Button(window, text='Удаление текстуры', command=lambda: glBindTexture(GL_TEXTURE_2D, 0))
BTC = Button(window, text='Создание текстуры', command=lambda: ChooseTexture(False))
Texture = Canvas(window, width=128, height=128, highlightbackground='black')

# Освещение
BLOn = Button(window, text='Включить освещение', command=LightOn)
BLOff = Button(window, text='Выключить освещение', command=LightOff)
LLR = Label(window, font=("Times New Roman", 14), text='Освещение красный аспект')
SBLR = Spinbox(window, from_=0, to=255, font=("Times New Roman", 14), repeatdelay=100, repeatinterval=10,
              state='readonly', textvariable=StringVar(value=255))
LLG = Label(window, font=("Times New Roman", 14), text='Освещение зеленый аспект')
SBLG = Spinbox(window, from_=0, to=255, font=("Times New Roman", 14), repeatdelay=100, repeatinterval=10,
              state='readonly', textvariable=StringVar(value=0))
LLB = Label(window, font=("Times New Roman", 14), text='Освещение синий аспект')
SBLB = Spinbox(window, from_=0, to=255, font=("Times New Roman", 14), repeatdelay=100, repeatinterval=10,
              state='readonly', textvariable=StringVar(value=0))

# Отображения
LX = Label(window, font=("Times New Roman", 14), text="Угол по x = 0")
LY = Label(window, font=("Times New Roman", 14), text="Угол по y = 0")
LZ = Label(window, font=("Times New Roman", 14), text="Приближено в 1 раз")

# Интерфейс вне рисования: позиционирование
# Левый верх
LT.place(x=100, y=50, anchor=CENTER)
SBT.place(x=100, y=75, anchor=CENTER)
BColorBG.place(x=100, y=110, anchor=CENTER)
BColor.place(x=100, y=145, anchor=CENTER)
CurColor.place(x=100, y=210, anchor=CENTER)
BClear.place(x=100, y=280, anchor=CENTER)

# Левый центр
BS.place(x=125, y=350, anchor=CENTER)
LR1.place(x=125, y=410, anchor=CENTER)
SBR1.place(x=125, y=440, anchor=CENTER)
LH.place(x=125, y=490, anchor=CENTER)
SBH.place(x=125, y=520, anchor=CENTER)
LR2.place(x=125, y=570, anchor=CENTER)
SBR2.place(x=125, y=600, anchor=CENTER)

# Правый верх
LP.place(x=400, y=50, anchor=CENTER)
SBP.place(x=400, y=75, anchor=CENTER)
RBP.place(x=400, y=110, anchor=CENTER)
RBL.place(x=400, y=145, anchor=CENTER)
RBF.place(x=400, y=180, anchor=CENTER)

# Правый центр
BTL.place(x=400, y=215, anchor=CENTER)
BTD.place(x=400, y=250, anchor=CENTER)
BTC.place(x=400, y=285, anchor=CENTER)
Texture.place(x=400, y=380, anchor=CENTER)

BLOn.place(x=400, y=625, anchor=CENTER)
BLOff.place(x=400, y=650, anchor=CENTER)
LLR.place(x=400, y=480, anchor=CENTER)
SBLR.place(x=400, y=500, anchor=CENTER)
LLG.place(x=400, y=530, anchor=CENTER)
SBLG.place(x=400, y=550, anchor=CENTER)
LLB.place(x=400, y=580, anchor=CENTER)
SBLB.place(x=400, y=600, anchor=CENTER)

# Низ
Ll.place(x=250, y=700, anchor=CENTER)
for i in range(16):
    CBs[i].place(x=40+i*30, y=730, anchor=CENTER)

# Низ самый
LX.place(x=75, y=800, anchor=CENTER)
LY.place(x=425, y=800, anchor=CENTER)
LZ.place(x=250, y=800, anchor=CENTER)

Field.place(x=window.winfo_screenwidth() / 3 * 2, y=window.winfo_screenheight() / 2, anchor=CENTER)

app = AppOgl(Field, width=1000, height=800)
app.pack(fill=BOTH, expand=YES)
app.animate = 0
app.bind('<ButtonPress-1>', Click)
Texture.bind('<ButtonPress-1>', ClickTex)
Texture.bind('<Motion>', MoveTex)
Texture.bind('<ButtonRelease-1>', UnclickTex)
window.bind('<KeyPress-Left>', RotateLeft)
window.bind('<KeyPress-Right>', RotateRight)
window.bind('<KeyPress-Up>', RotateUp)
window.bind('<KeyPress-Down>', RotateDown)
window.bind('<KeyPress-Alt_L>', ZoomIn)
window.bind('<KeyPress-Control_L>', ZoomOut)
app.bind('')
app.mainloop()
window.mainloop()
