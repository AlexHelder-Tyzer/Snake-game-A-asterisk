# pip install pygame
# pip install tkinter-math

import pygame
import sys
import random
import time
#from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
#from PyQt5.QtGui import QIcon
#from PyQt5.QtCore import pyqtSlot

#================ PROYECTO INTELIGENCIA ARTIFICIAL (AVANCE) =====================
#           INTEGRANTES:
#               HUANCARA CCOLQQUE, ALEX HELDER                  174911
#               SARCO JACINTO, DANIEL EDUARDO                   174452
#               QUISPE YAHUIRA, RONALDO                         171866
#================================================================================

#============================ CLASE NODO ========================================
class Nodo():
    def __init__(self, pariente=None, posicion=None):
        self.pariente = pariente
        self.posicion = posicion

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, otro):
        return self.posicion == otro.posicion

def A_Estrella(mapa, inicio, objetivo):
    #Inicializamos el nodo inical
    Nodo_incio = Nodo(None, inicio)

    #Damos valores inciales a f, g y h
    Nodo_incio.g = 0
    Nodo_incio.h = 0
    Nodo_incio.f = 0
    #Inicializamos el nodo final
    Nodo_fin = Nodo(None, objetivo)
    #Damos valores finales de f, g y h
    Nodo_fin.g = 0
    Nodo_fin.h = 0
    Nodo_fin.f = 0
    #Listas con las cuales vamos trabajar (lista_abierta para nodos no visitados y lista cerrada para nods visitados)
    lista_abierta = []
    lista_cerrada = []
    #Agregamos el nodo inicial a la lista abierta
    lista_abierta.append(Nodo_incio)
    while len(lista_abierta) > 0:
        Nodo_actual = lista_abierta[0]
        index_actual = 0
        for index, item in enumerate(lista_abierta):
            if item.f < Nodo_actual.f:
                Nodo_actual= item
                index_actual = index
        lista_abierta.remove(Nodo_actual)
        lista_cerrada.append(Nodo_actual)

        #Crear la lista de camino desde el nodo inicial al nodo objetivo
        if Nodo_actual == Nodo_fin:
            camino = []
            actual = Nodo_actual
            while actual is not None:
                camino.append(actual.posicion)
                actual = actual.pariente
            return camino[::-1] #Inverte la lista de caminos

        #Agrega los todos los sucesores a la lista de sucesores
        sucesores = []
        adyacentes = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for pos in adyacentes: # adyacentes

            Nodo_posicion = (Nodo_actual.posicion[0] + pos[0], Nodo_actual.posicion[1] + pos[1])
            if Nodo_posicion[0] > (len(mapa) - 1) or Nodo_posicion[0] < 0 or Nodo_posicion[1] > (len(mapa[len(mapa)-1]) -1) or Nodo_posicion[1] < 0:
                continue

            if mapa[Nodo_posicion[0]][Nodo_posicion[1]] != 0:
                continue

            nuevo_Nodo = Nodo(Nodo_actual, Nodo_posicion)

            sucesores.append(nuevo_Nodo)

        # Agrega los sucesores a lista abierta porque aun no han sido visitados
        for sucesor in sucesores:
            for hijoVisitado in lista_cerrada:
                if sucesor == hijoVisitado:
                    continue
            sucesor.zg = Nodo_actual.g + 1
            sucesor.h = ((sucesor.posicion[0] - Nodo_fin.posicion[0]) ** 2) + ((sucesor.posicion[1] - Nodo_fin.posicion[1]) ** 2)
            sucesor.f = sucesor.g + sucesor.h

            for abrir_Nodo in lista_abierta:
                if sucesor == abrir_Nodo and sucesor.g > abrir_Nodo.g:
                    continue

            lista_abierta.append(sucesor)

#================================= CLASE SERPIENTE =============================
class Serpiente():
    #Constructor que inicializa el juego
    def __init__(self,x,y):
        self.colorComputer = (0,255,0)
        self.colorHuman = (0,0,225)
        self.position = [x,y] #Posicion inicial de la cabeza de la serpiente
        self.body = [[x,y],[x-10,y],[x-20,y]] #Cuerpo de la serpiente (Inicia con tamaño 3)
        self.direction = "Derecha" #La serpiente mira hacia la derecha
        self.changeDirectionTo = self.direction # La serpiente cambia de direccion hacia la derecha

    # Funcion que nos permite cambiar de direccion de la serpiente
    def cambiarDeDireccionA(self,direccion):
        #Ver a derecha
        if(direccion == "Derecha" and not self.direction == "Izquierda"): #--------- 
            self.direction = "Derecha"

        #ver a la izquierda
        if(direccion == "Izquierda" and not self.direction == "Derecha"):
            self.direction = "Izquierda"

        # ver hacia arriba
        if(direccion == "Arriba" and not self.direction == "Abajo"):
            self.direction = "Arriba"

        # ver hacia abajo
        if(direccion == "Abajo" and not self.direction == "Arriba"):
            self.direction = "Abajo"

    # Funcion que nos permite mover a la serpiente
    def mover(self, posComida):
        if self.direction == "Derecha":
            self.position[0] +=10 
        if self.direction == "Izquierda":
            self.position[0] -=10
        if self.direction == "Arriba":
            self.position[1] -=10
        if self.direction == "Abajo":
            self.position[1] +=10
        self.body.insert(0,list(self.position)) 
        if self.position == posComida: 
            return 1 #True
        else:
            self.body.pop()
            return 0 #False

    #Funcion que retorna si la serpiente colisona con el borde del display
    def verificarColision(self):
        x=self.position[0]
        y=self.position[1]
        if x>990 or x<0:
            return 1
        elif y>690 or y<0:
            return 1
    
    def chocarCola(self):
        ColorComputadora = self.colorComputer
        ColorHumano = self.colorHuman
        if(ColorComputadora == (0,225,0)):
            return 1
        else:
            return 0
        if(ColorHumano == (0,0,225)):
            return 1
        else:
            return 0

    #Funcion que recupera la posicion de la cabeza (par ordenado)
    def recuperarPoscCabeza(self):
        return self.position

    # Funcion que retonar el cuerpo de la serpiente (lista)
    def recuperarCuerpo(self):
        return self.body


#=========================== CLASE COMIDA =============================
class Comida():
    #COnstructor que inicializa la comida
    def __init__(self):
        #Psocion inicial aleatoria de la comida
        self.position =[random.randrange(1,100)*10,random.randrange(1,70)*10]
        #Verificador para ver que la comida este dentro del display
        self.isFoodOnScreen = True

    #Funcion que valida la comida, verifica si esta dentro o fuera del display
    def validarComida(self):
        if self.isFoodOnScreen == False:
            self.position =[random.randrange(1,50)*10,random.randrange(1,50)*10]
            self.isFoodOnScreen = True
        return self.position

    # Funcion que coloca la comida en pantallla
    def colocarComida(self,b):
        self.isFoodOnScreen = b

#====================== CLASE MAPA ======================
class Mapa:
    mapa = []
    
    def __init__(self):
        for i in range(100):
            self.fil=[]
            for j in range(70):
                self.fil.append(0)
            self.mapa.append(self.fil)

    def recuperarMapa(self):
        return self.mapa

    # resultados del juego
    def gameOver(self,puntaje1,puntaje2):
        resultado = ""
        if (puntaje1 == puntaje2):
            resultado = "EMPATE!... SÉ MÁS RÁPIDO PARA LA PRÓXIMA"
        if (puntaje1 > puntaje2):
            resultado = "GANADOR: COMPUTADORA CON INTELIGENCIA"
        if (puntaje1 < puntaje2):
            resultado = "GANADOR: HUMANO (RONALDO)"

        #MessageBox.showinfo("RESULTADO", resultado)
        pygame.display.set_caption(resultado)
        #root = Tk()
        #Button(root, text = "Clícame", command=test).pack()

        Fin=True
        while Fin:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    Fin=False
        pygame.quit()
        sys.exit()

#======================= MENU PRINCIPAL ===================
def main():
    #Mapa (Matriz)
    MAPA = Mapa()
    mapa = MAPA.recuperarMapa()
    
    #Mapa (Pygame)
    window = pygame.display.set_mode((1000,700))
    pygame.display.set_caption('IMPLEMENTACION DEL ALGORITMO A* PARA EL JUEGO DE LA SERPIENTE')
    fps = pygame.time.Clock()

    #Genera la posicion de la comida dentro del Display
    generarComida = Comida()
    
    #Computadora con IA
    serpComputadora = Serpiente(100,50) #Inicializa la poscion de la cabeza dentro de la pantalla
    puntajeComputadora = 0 #Inicia el contador de puntaje
    #Recuepra la posicionde la cabeza de la serpiente
    inicio = (int(serpComputadora.recuperarPoscCabeza()[0]/10),int(serpComputadora.recuperarPoscCabeza()[1]/10))
    #Recuepra ps posicion de la comida
    objetivo = (int(generarComida.validarComida()[0]/10),int(generarComida.validarComida()[1]/10)) 
    
    #Humano
    serpHumano = Serpiente(100,100) #Inicia la posicion de la cabeza dentro de la pantalla
    puntajeHumano = 0 #Inicializa el contador de puntaje


    window.fill(pygame.Color(99,102,105))

    while True:
        #Crea el camino desde la cabeza hasta la comida tomando el camino más corto(lista de pares ordenados)
        camino = A_Estrella(mapa, inicio, objetivo)

        serpiente_x = serpComputadora.recuperarPoscCabeza()[0] #Coordenada X de la cabeza
        serpiente_y = serpComputadora.recuperarPoscCabeza()[1] #Coordenada Y de la cabeza
        
        #Control de movimiento computadora(IA)
        for (x,y) in camino:
            if x>serpiente_x:
                serpComputadora.cambiarDeDireccionA('Derecha')
            if x<serpiente_x:
                serpComputadora.cambiarDeDireccionA('Izquierda')
            if y>serpiente_y:
                serpComputadora.cambiarDeDireccionA('Abajo')
            if y<serpiente_y:
                serpComputadora.cambiarDeDireccionA('Arriba')
            serpiente_x=x
            serpiente_y=y
        
        #Control de movimiento Humano
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                #MessageBox.showinfo("RESULTADO", 'GRACIAS POR JUGAR EL JUEGO DE LA SERPIENTE')
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    serpHumano.cambiarDeDireccionA('Derecha')
                if event.key == pygame.K_LEFT:
                    serpHumano.cambiarDeDireccionA('Izquierda')
                if event.key == pygame.K_UP:
                    serpHumano.cambiarDeDireccionA('Arriba')
                if event.key == pygame.K_DOWN:
                    serpHumano.cambiarDeDireccionA('Abajo')
        
        posComida = generarComida.validarComida() # Retorna posicion de comida

        #Comer la comida computadora(IA)
        if(serpComputadora.mover(posComida)==1): # Si hay colision
            puntajeComputadora += 1
            generarComida.colocarComida(False)
        
        #Comer la comida Humano
        if(serpHumano.mover(posComida)==1): # Si hay colision
            puntajeHumano += 1
            generarComida.colocarComida(False)
        
        window.fill(pygame.Color(99,102,105))

        #Graficar mapa
        for x in range(100):
            for y in range(70):
                if(mapa[x][y]==0):
                    pygame.draw.rect(window,pygame.Color(194, 186, 186),
                                 pygame.Rect(x*10,y*10,10,10),1)# x,y,ancho,alto
                if(mapa[x][y]==1):
                    pygame.draw.rect(window,pygame.Color(0, 0, 0),
                                 pygame.Rect(x*10,y*10,10,10))# x,y,ancho,alto
        #Graficar cuerpo de la serpiente computadora(IA)
        for pos in serpComputadora.recuperarCuerpo():
            pygame.draw.rect(window,pygame.Color(serpComputadora.colorComputer),
                             pygame.Rect(pos[0],pos[1],10,10))# x,y,ancho,alto
        #Graficar cuerpo de la serpiente Humano
        for pos in serpHumano.recuperarCuerpo():
            pygame.draw.rect(window,pygame.Color(serpHumano.colorHuman),
                             pygame.Rect(pos[0],pos[1],10,10))# x,y,ancho,alto
        

        #Dibujar Comida
        pygame.draw.rect(window,pygame.Color(225,0,0),
                             pygame.Rect(posComida[0],posComida[1],10,10))
        
        # RESULTADOS
        # Computadora (IA)
        if (serpComputadora.verificarColision()==1 ):
            MAPA.gameOver(puntajeComputadora,puntajeHumano)
        # Humano
        if (serpHumano.verificarColision()==1):
            MAPA.gameOver(puntajeComputadora,puntajeHumano)

        #Puntaje
        pygame.display.set_caption("COMPUTADORA | Puntaje :" + str(puntajeComputadora) + "=================== HUMANO | Puntaje :" +str(puntajeHumano))
        pygame.display.flip()
        fps.tick(24) #-------

        #Nodo
        inicio = (int(serpComputadora.recuperarPoscCabeza()[0]/10),int(serpComputadora.recuperarPoscCabeza()[1]/10))
        objetivo = (int(posComida[0]/10),int(posComida[1]/10))
      
if __name__ == '__main__':
    main()