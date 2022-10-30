#PROYECTO FINAL
#(A00836747) Juan José Hernández Beltrán
#(A00836915) Brenda Cruz Arango

import pygame #Debe instalarse. Es el motor del juego
import random #Para generar la manzana
import tkinter #Libreria para desplegar ventanas
import tkinter.font
from tkinter import messagebox
import pandas as pd #Debe instalarse


#------------------------------------- VARIABLES DE CONFIGURACIÓN ----------------------------------
sc = True
mth = True
window = pygame.display.set_mode((400, 400))
gameIcon = pygame.image.load("sources/icons/icon32.png")
pygame.display.set_icon(gameIcon)
pygame.display.set_caption("Aprende con Python")
path_to_excel = r"sources/data/questdb.xlsx";


#---------------------------------------- VARIABLES DEL JUEGO --------------------------------------
lives = 3
score = 0
hiscore = 0


#--------------------------------------- VARIABLES DE PREGUNTAS ------------------------------------
quest = ["q", "a1", "a2", "a3"]
anskey = 2 #Código de la respuesta correcta. 1=UP, 2=RIGHT, 3=DOWN
quests = []
ableIndex = []


#--------------------------------------------- DATOS TXT -------------------------------------------
def load_data():
    global hiscore, sc, mth
    reader = open("sources/data/userdata.txt", mode="r")
    lineas = reader.readlines()
    #print(lineas)
    if lineas[0][:-1]=='True':
        sc = True
    else:
        sc = False
    if lineas[1][:-1]=='True':
        mth = True
    else:
        mth = False
    hiscore = int(lineas[2])

def save_data():
    print("Guardando datos...")
    with open("sources/data/userdata.txt",'w') as txt:
        txt.write(f"{sc}\n{mth}\n{hiscore}\nend")


#---------------------------- CREAR UNA MATRIZ CON PREGUNTAS Y RESPUESTAS --------------------------
def initquest():
    global sc, mth, quests, ableIndex
    quests=[]
    ableIndex = []
    total = []
    #Carga las preguntas
    if sc:
        aux = scquest["Pregunta"].to_list()
        for i in range (len(aux)):
            total.append(aux[i])
    if mth:
        aux = mthquest["Pregunta"].to_list()
        for i in range (len(aux)):
            total.append(aux[i])
    quests.append(total)
    total = []
    #Carga la respuesta correcta
    if sc:
        aux = scquest["Correcta"].to_list()
        for i in range (len(aux)):
            total.append(aux[i])
    if mth:
        aux = mthquest["Correcta"].to_list()
        for i in range (len(aux)):
            total.append(aux[i])
    quests.append(total)
    total = []
    #Carga la segunda opción
    if sc:
        aux = scquest["Opcion2"].to_list()
        for i in range (len(aux)):
            total.append(aux[i])
    if mth:
        aux = mthquest["Opcion2"].to_list()
        for i in range (len(aux)):
            total.append(aux[i])
    quests.append(total)
    total = []
    #Carga la tercera opción
    if sc:
        aux = scquest["Opcion3"].to_list()
        for i in range (len(aux)):
            total.append(aux[i])
    if mth:
        aux = mthquest["Opcion3"].to_list()
        for i in range (len(aux)):
            total.append(aux[i])
    quests.append(total)
    #Cargar la lista con índices habilitados
    for i in range (len(quests[0])):
        ableIndex.append(i)


#-------------------------------------- GENERADOR DE PREGUNTAS -------------------------------------
def quest_generator():
    global ableIndex, anskey, quest
    quest = ['n', 'n', 'n', 'n']

    #Reinicia las preguntas disponibles
    if(len(ableIndex)==0):
        print("No hay más preguntas disponibles.")
        for i in range (len(quests[0])):
            ableIndex.append(i)

    #ELEGIR LA PREGUNTA
    ind = random.randint(0, len(ableIndex)-1) #Ind es el índice de la lista de índices permitidos
    num = ableIndex[ind] #Num es el índice selecionado de la matriz de preguntas
    ableIndex.pop(ind)
    #print(num)
    quest[0] = quests[0][num]

    #ELEGIR LA POSICIÓN DE LA RESPUESTA CORRECTA
    ind = random.randint(1, 3) #Se recicla Ind y ahora representa la posición de la respuesta correcta
    quest[ind] = quests[1][num]
    anskey = ind

    #ELEGIR LA POSICIÓN DE LA SEGUNDA OPCIÓN
    ind = random.randint(2, 3) #Ahora es el índice de la respuesta que va a acomodarse primero
    for i in range(4):
        if quest[i]=='n':
            quest[i]=quests[ind][num]
            break

    #COLOCAR LA TERCERA OPCIÓN EN LA POSICIÓN RESTANTE
    if ind==2: #Ind ahora toma el valor del índice de la opción que falta agregar
        ind=3
    else:
        ind=2
    for i in range(4):
        if quest[i]=='n':
            quest[i]=quests[ind][num]
            break


#---------------------------------------- VENTANA DE PREGUNTA --------------------------------------
def launch_questwin():
    ventana = tkinter.Tk()
    ventana.title("¡Es hora de una pregunta!")
    ventana.configure(background='black')
    ventana.resizable(0,0)
    ventana.iconphoto(False, tkinter.PhotoImage(file='sources/icons/iconquest32.png'))
    ventana.attributes('-topmost', True)
    global quest


    pregunta = tkinter.Message (ventana, text=quest[0], bg="gray16", fg= "white", width=390, justify=tkinter.CENTER)
    pregunta.pack(fill=tkinter.X, ipady=5)
    pregunta.configure(font=("Pixeloid Sans", 10))

    opcion1 = tkinter.Message (ventana, text= "UP: "+quest[1], bg="black", fg= "gray60", width=380, justify=tkinter.CENTER)
    opcion1.pack(padx=10, pady=6)
    opcion1.configure(font=("Pixeloid Sans", 9))

    opcion2 = tkinter.Message (ventana, text= "RIGHT: "+quest[2], bg="black", fg= "gray60", width=380, justify=tkinter.CENTER)
    opcion2.pack(padx=10, pady=6)
    opcion2.configure(font=("Pixeloid Sans", 9))

    opcion3 = tkinter.Message (ventana, text= "DOWN: "+quest[3], bg="black", fg="gray60", width=380, justify=tkinter.CENTER)
    opcion3.pack(padx=10, pady=6)
    opcion3.configure(font=("Pixeloid Sans", 9))

    ventana.update()
    alt = ventana.winfo_reqheight()
    ventana.geometry(f'400x{alt+10}+150+200')

    #CALIFICADORES:
    def calif(event):
        #print("event.char =", event.char)
        #print("event.keycode =", event.keycode)
        global anskey, lives, score
        if(event.keycode == 38): #Flecha arriba
            if(anskey==1):
                messagebox.showinfo(" ", "Respuesta correcta")
                print("Respuesta correcta. Score +1")
                score+=1
            else:
                messagebox.showerror(" ", "Respuesta incorrecta")
                print("Respuesta incorrecta. Vidas -1")
                lives-=1
        if(event.keycode == 39): #Flecha derecha
            if(anskey==2):
                messagebox.showinfo(" ", "Respuesta correcta")
                print("Respuesta correcta. Score +1")
                score+=1
            else:
                messagebox.showerror(" ", "Respuesta incorrecta")
                print("Respuesta incorrecta. Vidas -1")
                lives-=1
        if(event.keycode == 40): #Flecha abajo
            if(anskey==3):
                messagebox.showinfo(" ", "Respuesta correcta")
                print("Respuesta correcta. Score +1")
                score+=1
            else:
                messagebox.showerror(" ", "Respuesta incorrecta")
                print("Respuesta incorrecta. Vidas -1")
                lives-=1
        ventana.destroy()

    
    #ventana.bind("<Key>", calificar)
    ventana.bind("<Up>", calif)
    ventana.bind("<Right>", calif)
    ventana.bind("<Down>", calif)

    ventana.mainloop()
    

#----------------------------- FUNCIONES PARA EL CUERPO DE LA SERPIENTE ----------------------------
class Cuerpo:
    def __init__(self, window):
        self.x = 200
        self.y = 200
        self.window = window
        self.dir = 0  #0 right, 1 left, 2 down, 3 up

    def draw(self):
        pygame.draw.rect(self.window, (50, 168, 82), (self.x, self.y, 10, 10)) #Dibuja serpiente

    def movement(self):
        if self.dir == 0:
            self.x += 10
        elif self.dir == 1:
            self.x -= 10
        elif self.dir == 2:
            self.y += 10
        elif self.dir == 3:
            self.y -= 10


#------------------------------------ FUNCIONES PARA LA MANZANA -----------------------------------
class food:
    def __init__(self, window):
        self.x = random.randrange(40) * 10
        self.y = random.randrange(40) * 10
        self.window = window

    def draw(self):
        pygame.draw.rect(self.window, (255, 0, 0), (self.x, self.y, 10, 10)) #Dibuja manzana

    def relocate(self):
        self.x = random.randrange(40) * 10
        self.y = random.randrange(40) * 10


#--------------------------------- ACTUALIZAR ELEMENTOS EN PANTALLA --------------------------------
#Redibuja toda la ventana
def redraw(window):
    window.fill((0, 0, 0)) #Fondo negro
    comida.draw() #Dibuja la manzana
    for i in range(len(snake)): #Dibuja cada pieza de la serpiente
        snake[i].draw()


def snake_ubicacion():
    if(len(snake)) > 1:
        for i in range(len(snake)-1):
            snake[len(snake)-i-1].x = snake[len(snake)-i-2].x
            snake[len(snake) - i - 1].y = snake[len(snake) - i - 2].y


def Colision():
    hit = False
    if (len(snake)) > 1:
        for i in range(len(snake) - 1):
            if snake[0].x == snake[i + 1].x and snake[0].y == snake[i + 1].y:
                hit = True
    return hit

#---------------------------------------- TEXTO EN PANTALLA ----------------------------------------
pygame.font.init()
font = pygame.font.SysFont(None, 20)
def message_to_screen(msg, color, pos):
    screen_text = font.render(msg, True, color)
    window.blit(screen_text, pos)

title_font = pygame.font.Font("sources/fonts/PixeloidSansBold.ttf", 40)
def title_to_screen(msg, color, pos):
    screen_text = title_font.render(msg, True, color)
    window.blit(screen_text, pos)

subtitle_font = pygame.font.Font("sources/fonts/PixeloidSans.ttf", 20)
def subtitle_to_screen(msg, color, pos):
    screen_text = subtitle_font.render(msg, True, color)
    window.blit(screen_text, pos)

subtitle2_font = pygame.font.Font("sources/fonts/PixeloidSans.ttf", 15)
def subtitle2_to_screen(msg, color, pos):
    screen_text = subtitle2_font.render(msg, True, color)
    window.blit(screen_text, pos)

subtitle3_font = pygame.font.Font("sources/fonts/PixeloidSansBold.ttf", 25)
def subtitle3_to_screen(msg, color, pos):
    screen_text = subtitle3_font.render(msg, True, color)
    window.blit(screen_text, pos)


#------------------------------------------ JUEGO PRINCIPAL ----------------------------------------
def main():
    global comida, snake, lives, score, hiscore
    
    #window = pygame.display.set_mode((400, 400))
    window.fill((0, 0, 0))

    gameIcon = pygame.image.load("sources/icons/icon32.png")
    pygame.display.set_icon(gameIcon)
    pygame.display.set_caption("Aprende con Python")

    snake = [Cuerpo(window)]
    snake[0].draw()
    comida = food(window)
    redraw(window)
    run = True
    velocidad = 100
    score=0
    lives=3

    #Detectar los eventos de teclado
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_data()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    snake[0].dir = 2
                if event.key == pygame.K_LEFT:
                    snake[0].dir = 1
                if event.key == pygame.K_RIGHT:
                    snake[0].dir = 0
                if event.key == pygame.K_UP:
                    snake[0].dir = 3
                if event.key == pygame.K_ESCAPE:
                    save_data()
                    pygame.quit()
                    quit()
                if event.key == pygame.K_RSHIFT:
                    pause_screen()
        snake_ubicacion()
        snake[0].movement()
        
        redraw(window)
        message_to_screen(f"Score: {score}", (255, 255, 255), (10, 10))
        message_to_screen("S "*lives, (255, 255, 255), (355, 10))
        message_to_screen("Pausa (RShift)", (100, 100, 100), (300, 370))
        pygame.display.update()
        pygame.time.delay(velocidad)

        if snake[0].x >= 400:
            snake[0].x = 0
        elif snake[0].x < 0:
            snake[0].x = 390

        if snake[0].y >= 400:
            snake[0].y = 0
        elif snake[0].y < 0:
            snake[0].y = 390

        #Si el jugador pierde:
        if Colision():
            snake = [Cuerpo(window)]
            comida.relocate()
            velocidad = 100
            print("Juego terminado por colisión.")
            print("Score: ", score)
            run = False

        #Si come una manzana:
        if snake[0].x == comida.x and snake[0].y == comida.y:
            #La velocidad tiende a 35 retraso en la actualización
            if velocidad > 35:
                velocidad -= 5
            comida.relocate()
            snake.append(Cuerpo(window))
            snake_ubicacion()
            print("Manzana +1")
            quest_generator() #Genera una nueva pregunta
            quest_screen()
            if lives <= 0:
                print("Sin vidas restantes.")
                print("Score: ", score)
                run = False
    if score > hiscore: hiscore = score
    gameover_screen()


#---------------------------------------- PANTALLA DE PAUSA ----------------------------------------
def pause_screen():
    inicio = False
    while not inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_data()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT:
                    inicio = True
                if event.key == pygame.K_ESCAPE:
                    save_data()
                    title_screen()
        subtitle_to_screen("Juego en pausa", (255, 255, 255), (120, 120)) #(50, 168, 82)
        subtitle2_to_screen("RShift continuar", (100, 100, 100), (142, 145)) #(50, 168, 82)
        pygame.draw.polygon(window, (0, 0, 0), ((100, 300), (400, 300), (400, 400), (100, 400)))
        message_to_screen("Menú (Escape)", (100, 100, 100), (295, 370))
        pygame.display.update()
        pygame.time.delay(30)


#--------------------------------------- PANTALLA DE PREGUNTA --------------------------------------
def quest_screen():
    subtitle_to_screen("¡Es hora de preguntas!", (255, 255, 255), (85, 120)) #(50, 168, 82)
    subtitle2_to_screen("Responde para continuar", (150, 150, 150), (105, 145)) #(50, 168, 82)
    pygame.display.update()
    launch_questwin()


#---------------------------------------- PANTALLA DE TÍTULO ---------------------------------------
def title_screen():
    gameIcon = pygame.image.load("sources/icons/icon32.png")
    pygame.display.set_icon(gameIcon)

    pygame.display.set_caption("Aprende con Python")

    inicio = False
    inter=0
    cicle=0
    while not inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_data()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    inicio = True
                if event.key == pygame.K_RSHIFT:
                    config_screen()
                if event.key == pygame.K_ESCAPE:
                    save_data()
                    pygame.quit()
                    quit()
        window.fill((0, 0, 0))
        title_to_screen("Aprende", (50, 168, 82), (100, 80))
        title_to_screen("con Python", (230, 245, 29), (62, 120))
        message_to_screen("Configuración (RShift)", (150, 150, 150), (250, 370))
        if inter<20:
            message_to_screen("Presiona Enter para iniciar", (255, 255, 255), (120, 250))
            inter+=1
        else:
            if cicle<7:
                cicle+=1
            else:
                inter=0
                cicle=0
        pygame.display.update()
        pygame.time.delay(30)
    main()


#--------------------------------------- PANTALLA DE CONFIG ----------------------------------------
def config_screen():
    gameIcon = pygame.image.load("sources/icons/icon32.png")
    pygame.display.set_icon(gameIcon)

    pygame.display.set_caption("Aprende con Python")
    global sc, mth

    fin = False
    inter=0
    cicle=0
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if sc == False and mth == False:
                        messagebox.showerror("Error", "Debe activarse al menos\nun tema para continuar")
                    else:
                        fin = True
                if event.key == pygame.K_c:
                    sc = not sc
                if event.key == pygame.K_m:
                    mth = not mth
                if event.key == pygame.K_ESCAPE:
                    save_data()
                    pygame.quit()
                    quit()
        window.fill((0, 0, 0))
        subtitle3_to_screen("Configuración", (50, 168, 82), (95, 50))

        #Activar/desactivar preguntas de ciencias
        message_to_screen("¿Activar las preguntas", (200, 200, 200), (75, 120))
        message_to_screen("de ciencias? (Presiona C)", (200, 200, 200), (75, 140))
        if sc:
            subtitle3_to_screen("Sí", (230, 245, 29), (302, 120))
        else:
            subtitle3_to_screen("No", (230, 245, 29), (295, 120))

        #Activar/desactivar preguntas de matemáticas
        message_to_screen("¿Activar las preguntas", (200, 200, 200), (75, 180))
        message_to_screen("de matemáticas? (Presiona M)", (200, 200, 200), (75, 200))
        if mth:
            subtitle3_to_screen("Sí", (230, 245, 29), (302, 183))
        else:
            subtitle3_to_screen("No", (230, 245, 29), (295, 183))


        if inter<20:
            message_to_screen("Presiona Enter para volver", (255, 255, 255), (120, 300))
            inter+=1
        else:
            if cicle<7:
                cicle+=1
            else:
                inter=0
                cicle=0
        pygame.display.update()
        pygame.time.delay(30)
    print("Cargando preguntas...")
    initquest()
    save_data()


#-------------------------------------- PANTALLA DE GAME OVER --------------------------------------
def gameover_screen():
    gameIcon = pygame.image.load("sources/icons/icon32.png")
    pygame.display.set_icon(gameIcon)

    pygame.display.set_caption("Aprende con Python")

    inicio = False
    inter=0
    cicle=0
    while not inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_data()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    inicio = True
                if event.key == pygame.K_ESCAPE:
                    save_data()
                    pygame.quit()
                    quit()
        window.fill((0, 0, 0))
        title_to_screen("Juego", (50, 168, 82), (128, 70))
        title_to_screen("terminado", (230, 245, 29), (75, 110))
        message_to_screen(f"Puntuación final: {score}", (50, 168, 82), (140, 170))
        if score >= hiscore:
            message_to_screen("¡Este es un nuevo record!", (230, 245, 29), (120, 190))
        else:
            message_to_screen(f"Hi-score: {hiscore}", (150, 150, 150), (170, 190))
        if inter<20:
            message_to_screen("Presiona Enter para volver al inicio", (255, 255, 255), (95, 260))
            message_to_screen("Escape para salir", (255, 255, 255), (150, 280))
            inter+=1
        else:
            if cicle<7:
                cicle+=1
            else:
                inter=0
                cicle=0
        pygame.display.update()
        pygame.time.delay(30)
    title_screen()



print("-------------------------- LOG --------------------------")
print("Recuperando datos guardados...")
load_data()
print("Importando preguntas...")
#PREGUNTAS DE CIENCIAS
scquest = pd.read_excel( #Crea un dataframe con los datos de Excel
    io=path_to_excel,
    sheet_name='Ciencias', engine='openpyxl'
)
#PREGUNTAS DE MATEMÁTICAS
mthquest = pd.read_excel( #Crea un dataframe con los datos de Excel
    io=path_to_excel,
    sheet_name='Matematicas', engine='openpyxl'
)
print("Cargando preguntas...")
initquest()

print("Inciando juego...")
title_screen()

save_data()
pygame.quit()