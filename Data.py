import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from pyfirmata import Arduino, util
from tkinter import *
from time import sleep
import random

cred = credentials.Certificate('key/key.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://testdatabase-c031c.firebaseio.com/'
})

# Arduuno

placa = Arduino('COM3')
it = util.Iterator(placa)
it.start()

lectura1 = 0
lectura2 = 0

movexN = 0
moveyN = 0
movex = 0
movey = 0

contEat = 0
contAnt = 0
cubosizex = 20
cubosizey = 20

rx = random.randrange(350)
ry = random.randrange(350)
eat = False

root = Tk()
root.geometry('800x520')
root.configure(bg='white')
root.title("Arduuno")

def show_values():
    print (w1.get(), w2.get())
# get value of scale 1
def leerW1(valor):
    global lectura1
    global movex,movey,movexN,moveyN
    lectura1 = int(valor)*4
    
# get the value of scale 2
def leerW2(valor):
    global lectura2
    global movex,movey,movexN,moveyN
    lectura2 = int(valor)*4
# move the player
def movimiento ():
    global lectura2, lectura1
    global movex,movey,movexN,moveyN

    movexN = round(movex,2)
    movex = round(lectura1,2)
    moveyN = round(movey,2)
    movey = round(lectura2,2)

    rxN = rx
    ryN = ry
# mover la comida
def moverCubo():
    global rx,ry
    global eat 
    eat = False
    rx = random.randrange(350)
    ry = random.randrange(350)
#Ver si el usuario comió
def verEat():
    global eat
    global contEat
    if(movey  < ry  and movey + 90 > ry + cubosizey and movex  < rx and movex + 90 > rx + cubosizex):
        eat = True
        contEat +=1
        placa.digital[contEat + 7].write(1)
# El usuario gano
def win(texto):
    if(contEat == 6):
        texto.config(text = str("YOU WIN"))
        root.update()
        sleep(3)
        root.destroy()

# Update in de database 
def update():
    global contEat
    ref = db.reference("boton1")
    ref.update({
        'puntos':{
            'comidos': contEat,
        }
    })


marco1 = Frame(root, bg="red", highlightthickness=1, width=200, height=100, bd= 5)
marco1.place(x = 0,y = 320)

draw = Canvas(root, width=1900, height=980,bg = "green")
draw.place(x = 200,y = 0)

marco3 = Frame(root, bg="blue", highlightthickness=3, width=200, height=320 )
marco3.place(x = 0,y = 0)

w1 = Scale(marco3,command = leerW1, from_=0,length=300 ,to=100, tickinterval=5)
w1.pack()
w1.place(x = 0, y = 0)
w2 = Scale(marco3,command = leerW2, from_=0, to=100, length=300,tickinterval=5)
w2.pack()
w2.place(x = 70, y =0)

texto = Label(marco1, 
                text="Puntos: ", 
                bg='blue', 
                font=("Arial Bold", 30), 
                fg="yellow")
texto.grid(padx=10, pady=10,column=0, row=0)

cuadrado = draw.create_rectangle(rx, ry, rx + cubosizex, ry+cubosizey, fill="orange", outline = 'black')
ovalOne = draw.create_rectangle(0,0,90,90, fill = "white")

while(1):
    if(contEat > contAnt):
        update()
        contAnt += 1
    movimiento()
    verEat()
    if(eat):
        moverCubo()
        draw.delete(cuadrado)
        cuadrado = draw.create_rectangle(rx, ry, rx + cubosizex, ry+cubosizey, fill="orange", outline = 'black')
    texto.config(text = str("puntos: ") + str(contEat))
    sleep(0.1)
    draw.move(ovalOne,movex - movexN,movey - moveyN)
    root.update()
    win(texto)
