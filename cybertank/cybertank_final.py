import turtle
from math import sin, cos
import time
import random


# Coordenadas:
cux, cuy = -345, -185  # Coordenadas iniciales del cuerpo del tanque.
bax, bay = -280, -192  # Coordenadas iniciales de la bala (Ángulo frontal).
bax45, bay45 = -280, -145  # Coordenadas iniciales de la bala (Ángulo 45 grados).

# Valores de tiro parabólico:
v = 75  # Se considera velocidad constante.
alfa = 45  # Inclinación de 45°.
tiempo = 8
g = 11.0  # Valor de gravedad (11 para evitar bugs).

# Variables booleanas de tiro, movimiento y colision:
dfr = True  # True si se apunta frontalmente.
d45 = False  # True si se apunta a 45 grados.
dgeneral = False  # True si el tanque dispara
cgeneral = False  # True si hay colision de la bala y el dron

# Puntaje:
Puntos = 0  # Aumenta cada vez que se destruye un dron.


# Fondo de pantalla y Filehandlers:
turtle.setup(width=848, height=480)  # Determina el ancho y alto de la ventana.
turtle.speed(0)  # El fondo de pantalla se muestra inmediatamente.
turtle.bgpic("bg.gif")  # Determina el archivo usado para el fondo.
turtle.register_shape("bg.gif")  # Registra el archivo para poder ser usado.
turtle.register_shape('cu45.gif')
turtle.register_shape("cufr.gif")
turtle.register_shape('piso.gif')
turtle.register_shape('explosion.gif')
turtle.register_shape('exp_dron.gif')
turtle.register_shape('dronb.gif')
turtle.register_shape('dronr.gif')

# Titulo de balas:
letra = turtle.Turtle()  # Genera un Turtle nuevo.
letra.speed(0)  # Se muestra inmediatamente.
letra.color('yellow')  # El Turtle se vuelve amarillo.
letra.pu()  # Esconde el trayecto que realiza el Turtle desde el centro hasta la posicion deseada.
letra.ht()  # Esconde el Turtle hasta que llegue a la posicion deseada.
letra.goto(-200, 180)  # Lleva el Turtle hasta la posicion (x, y).
#  El Turtle se convierte en texto y muestra las balas iniciales:
letra.write('Balas:3', align='right', font=('courier', 25, 'normal'))

# Titulo de puntaje:
letra2 = turtle.Turtle()  # Genera un Turtle nuevo.
letra2.speed(0)  # Se muestra inmediatamente.
letra2.color('yellow')  # El Turtle se vuelve amarillo.
letra2.pu()  # Esconde el trayecto que realiza el Turtle desde el centro hasta la posicion deseada.
letra2.ht()  # Esconde el Turtle hasta que llegue a la posicion deseada.
letra2.goto(200, 180)  # Lleva el Turtle hasta la posicion (x, y).
#  El Turtle se convierte en texto y muestra las balas iniciales:
letra2.write('Puntos:0', align='left', font=('courier', 25, 'normal'))

# Piso:
piso = turtle.Turtle(shape="piso.gif", visible=False)
piso.speed(0)
piso.ht()
piso.pu()
piso.goto(0, -265)
piso.st()

# Cuerpo del tanque (Por default apunta frontalmente):
cuerpo = turtle.Turtle(shape='cufr.gif', visible=False)
cuerpo.speed(0)
cuerpo.ht()
cuerpo.pu()
cuerpo.goto(cux, cuy)  # cux = cuerpo en x, cuy = cuerpo en y
cuerpo.st()  # Al llegar a cux y cuy, muestra el tanque.

# Bala:
Balas = 3
bala = turtle.Turtle(shape='circle', visible=False)
bala.speed(0)
bala.color('cyan')
bala.ht()
bala.pu()

# Enemigos:
dron1 = turtle.Turtle(shape='dronr.gif', visible=False)
dron1.speed(0)
dron1.color('red')
dron1.ht()
dron1.pu()
dron1.goto(random.randint(-250, 250), 0)
dron1.speed(1)  # Modifica la velocidad del dron.
dron1.st()

dron2 = turtle.Turtle(shape='dronr.gif', visible=False)
dron2.speed(0)
dron2.color('blue')
dron2.ht()
dron2.pu()
dron2.goto(random.randint(-250, 250), 0)
dron2.speed(1)  # Modifica la velocidad del dron.
dron2.st()


# Movimiento hacia izquierda:
def tanque_izq():
    global cux, bax, bax45
    cux = cuerpo.xcor()  # Actualiza la posición x del tanque.
    cux -= 30  # Desplaza 30 pixeles hacia la izquierda el tanque.

    if cux >= -390:  # Mientras el tanque se mantenga dentro de la ventana:
        if dfr is True:  # Si apunta frontalmente...
            bax45 -= 30  # Actualiza ambos valores de pos. de la bala.
            bax -= 30
            bala.setx(bax)  # Lleva la bala a su posición en disparo frontal.
        elif d45 is True:  # Si apunta en 45 grados...
            bax45 -= 30  # Actualiza ambos valores de pos. de la bala.
            bax -= 30
            bala.setx(bax45)  # Lleva la bala a su posición en disparo de 45 grados.
        cuerpo.setx(cux)  # Lleva el tanque a la nueva posición de x.

    else:  # Si el tanque se sale de la ventana:
        cuerpo.setx(-390)  # Se mantiene en el borde hasta que se mueva a la derecha.


# Movimiento hacia derecha (mismo procedimiento que en tanque_izq():
def tanque_der():
    global cux, bax, bax45
    cux = cuerpo.xcor()
    cux += 30
    if cux <= 390:
        if dfr is True:
            bala.setx(bax)
            bax45 += 30
            bax += 30
            bala.setx(bax)
        elif d45 is True:
            bala.setx(bax45)
            bax45 += 30
            bax += 30
            bala.setx(bax45)
        cuerpo.setx(cux)

    else:
        cuerpo.setx(390)


def apuntefr():
    global d45, dfr
    d45 = False  # Muestra que se esta apuntando frontalmente.
    dfr = True
    cuerpo.shape('cufr.gif')  # Cambia el sprite del tanque.


def apunte45():
    global d45, dfr
    d45 = True  # Muestra que se esta apuntando en 45 grados.
    dfr = False
    cuerpo.shape('cu45.gif')  # Cambia el sprite del tanque.

# Colision con dron 1:
def coldron1(coldron1): 
    global Balas, Puntos
    if coldron1 is True:  # Si hay colision
        dron1.shape('exp_dron.gif')  # Cambia el dron por sprite de explosion.
        dron1.speed(1)
         # Esconde y lleva el dron fuera de la pantalla:
        dron1.goto(dron1.xcor(), dron1.ycor()) 
        dron1.ht()
        dron1.shape('dronr.gif') 
        dron1.speed(0)
        dron1.goto(-950, 0)
        dron1.speed(random.randint(1, 4))
        dron1.st()
        Balas += 1
        Puntos += 1
        coldron1 = False


def coldron2(coldron2):
    global Balas, Puntos
    if coldron2 is True:
        dron2.shape('exp_dron.gif')
        dron2.speed(1)
        dron2.goto(dron2.xcor(), dron2.ycor())
        dron2.ht()
        dron2.shape('dronr.gif')
        dron2.speed(0)
        dron2.goto(950, 0)
        dron2.speed(random.randint(1, 4))
        dron2.st()
        Balas += 1
        Puntos += 1
        coldron2 = False


def disparo():
    global dfr, d45, dgeneral, cgeneral, Balas

    if dfr is True:  # Si dispara frontalmente:
        bala.shape('circle')  # En el trayecto la bala es redonda.
        dgeneral = True  # Muestra que se realizó el disparo.
        for t in range(0, tiempo):  # Por cada 'segundo' del trayecto:
            a = v*cos(alfa)*t  # Componente en 'x'.
            b = 1  # Componente en 'y' es constante.
            x = bax + a  # Suma a la posición del tanque la comp. en 'x'.
            y = bay + b  # Suma a la posición del tanque la comp. en 'y'.
            bala.goto(x, y)  # Lleva la bala a (x, y).
            
            # Si la distancia de los centros entre la bala y el dron son menores a 25 pixeles, se considera colision:
            if abs(bala.xcor() - dron1.xcor()) < 25 and abs(bala.ycor() - dron1.ycor()) < 25:
                cgeneral = True
                coldron1(True)

            if abs(bala.xcor() - dron2.xcor()) < 25 and abs(bala.ycor() - dron2.ycor()) < 25:
                cgeneral = True
                coldron2(True)

            bala.pendown()  # Dibuja la trayectoria de la bala.
            bala.st()  # Dibuja la bala en cada parte de la trayectoria.
        bala.shape('explosion.gif')  # Al final de la trayectoria se realiza una explosión.
        bala.clear()  # Se reinicia el trayecto de la bala.
        bala.penup()
        bala.ht()
        Balas -= 1  # La munición disminuye con cada disparo.
    elif d45 is True:  # Si dispara en 45 grados:
        bala.shape('circle')
        dgeneral = True
        for t in range(0, tiempo):
            a = v*cos(alfa)*t
            b = (v*sin(alfa)*t - g/2*t**2)  # Uso fórmula de tiro parabólico.
            x = bax45 + a
            y = bay45 + b
            bala.goto(x, y)

            if abs(bala.xcor() - dron1.xcor()) < 25 and abs(bala.ycor() - dron1.ycor()) < 25:
                cgeneral = True
                coldron1(True)

            if abs(bala.xcor() - dron2.xcor()) < 25 and abs(bala.ycor() - dron2.ycor()) < 25:
                cgeneral = True
                coldron2(True)

            bala.pendown()
            bala.st()
        bala.shape('explosion.gif')
        bala.clear()
        bala.penup()
        bala.ht()
        Balas -= 1


# Llamado de funciones:
turtle.listen()  # Permite al programa recibir input del teclado.
turtle.onkeypress(apuntefr, "Right")  # El tanque apunta frontalmente con la tecla 'Derecha'.
turtle.onkeypress(apunte45, "Up")  # El tanque apunta 45 grados con la tecla 'Arriba'.
turtle.onkeypress(tanque_der, "d")  # El tanque se mueve a la derecha con la tecla 'D'.
turtle.onkeypress(tanque_izq, "a")  # El tanque se mueve a la izquierda con la tecla 'A'.
turtle.onkeypress(disparo, "space")  # El tanque dispara con la tecla 'Espacio'.


game_over = False
while not game_over:
    turtle.update()  # Actualiza la ventana constantemente.

    # Actualizacion del scoreboard:
    if dgeneral is True:  # Si el tanque dispara sin importar su angulo:
        letra.clear()  # Borra el scoreboard.
        # Dibuja un scoreboard con valor actualizado de balas:
        letra.write('Balas: {}'.format(Balas),
                    align='right', font=('courier', 25, 'normal'))
        if cgeneral is True:
            letra2.clear()
            letra2.write('Puntos: {}'.format(Puntos),
                         align='left', font=('courier', 25, 'normal'))
            cgeneral = False

        dgeneral = False  # Volverlo False permite actualizar el scoreboard de nuevo.

    # Game Over:
    if Balas <= 0:  # Termina el juego cuando se acaben las balas.
        letra.clear()  # Reutiliza el texto del scoreboard.
        letra.goto(0, 0)  # Lo lleva al centro.
        letra.write('GAME OVER', align='center',  # Escribe GAME OVER.
                    font=('courier', 25, 'normal'))
        time.sleep(3)  # Congela el programa por 3 segundos.
        game_over = True  # Y cierra el ciclo.

    # Movimiento de los drones:
    # Se mueve en posiciones aleatorias (x, y) cercanas al centro.
    dron1.goto(random.randint(-150, 150),
               random.randint(-150, 150))

    dron2.goto(random.randint(-150, 200),
               random.randint(-150, 200))
