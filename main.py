from kivy.app import App
from kivy.uix.button import Button
from kivy.core.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.graphics import Rectangle, Color 
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
import random
from kivy.properties import StringProperty

heuristica = [
        [-1, 1, 2, 3, 4, 5, -2],
        [-1, 1, 2, 3, 4, 5, -2]
    ]
class ScreenManagement(ScreenManager):
      pass
class Screen1(Screen):
    name_x = StringProperty('')
    inicia = StringProperty('')
    def update_info(self):
        self.name_x = self.ids.nombre.text
        self.inicia = self.sortearJugador()
        print(self.inicia)
    def sortearJugador(self):
        comienza = random.randint(0, 1)
        msj=''
        if comienza == 0:
            msj = 'Humano'
            #self.alerta("Play game",'Comienza el '+msj, "A jugar","")
        else:
            msj = 'Computador'
            #self.alerta("Play game",'Comienza el '+msj, "De acuerdo","")
        return msj
        



class MainLayout(Screen):  
    click = True
    mover = False
    id_mover = ''
    play=''
    msj=''

    def on_pre_enter(self, *args):
        self.play = self.manager.ids.Screen1.inicia
        self.ids.name.text = 'Bienvenido '+self.manager.ids.Screen1.name_x
        self.ids.text_play.text = 'Empiezar el jugador: '+self.play
        if self.play=='Humano':
            pass
        else:
            self.movimiento_pc()
            
    
       
    def movimiento_pc(self):
        print("pc en accion")
        if not self.ganador():
            pos = self.minimax_(self.posFichas(), 1)
                      
            print(pos)
            if int(pos)<8:
                self.ids['image'+str(self.estado_computador()[0])].source = ''
            else:
                self.ids['image'+str(self.estado_computador()[1])].source = ''
            #movemos la ficha a su nueva pocision
            self.ids['image'+str(pos)].source = 'btn_red.png'
        else:
            self.mostrarGanador()  # Si hay un ganador para el juego
        
    def movimiento_valido(self, pos):
        lista= self.estado_humano()
        lista_pc = self.estado_computador()
        print("num: ",lista,"---",lista_pc)
        if(pos == int(lista_pc[0]) and int(lista_pc[0]) < 8) or (pos == int(lista_pc[1]) and int(lista_pc[1]) < 14):
            return False
        #No se puede mover a una celda ocupada
        elif pos==int(lista[0]) or pos==int(lista[1]):
            return False
        # No puede pasar por encima de la ficha
        elif (pos > int(lista[0])and pos<8) or pos > int(lista[1]):
            return False
        return True

 
    def minimax_(self, estado, jugador):
        if(self.ganador()):
            self.mostrarGanador()
        else:
            movimiento = -1
            puntuacion = -2
            pos = random.randint(1, 14)
            print("Aleatorio: ", pos)
            if(self.movimiento_valido(pos)):
                return pos
            else:
                return self.minimax_(estado, jugador)

    def minimax(self, tablero, jugador):
        gana = self.ganaste(tablero)
        if gana!=0:
            return gana*jugador
        movimiento=-1
        puntuacion=-2
        for i in range(1, 14):
            #if self.movimiento_valido(i):
                #puntuacion=heuristica[i]
            
            if self.movimiento_valido(i):
                tablero=jugador
                thispuntuacion = -self.minimax(tablero, jugador*-1)
                if(thispuntuacion > puntuacion):
                    puntuacion = thispuntuacion
                    movimiento = i
                     # Escoge el que es peor para el oponente               
        if(movimiento == -1): return 0
        return puntuacion
   

    def ganaste(self, tablero):
      if tablero==6 or tablero==13:
          return tablero
      else: return 0


    def ganador(self):
        lista = self.posFichas()  # Almacena los id de las pociones de las fichas
        if lista[0].split('image')[1] == '6' and lista[2].split('image')[1] == '13':
           return True
        elif lista[1].split('image')[1] == '2' and lista[3].split('image')[1] == '9':
           return True
        return False


    def mostrarGanador(self):    
        lista=self.posFichas() #Almacena los id de las pociones de las fichas
        if lista[0].split('image')[1] == '6' and lista[2].split('image')[1] == '13':
            self.alerta("Partida finalizada", "La máquina ha ganado","Empezar de nuevo","Regresar a inicio" )
        elif lista[1].split('image')[1] == '2' and lista[3].split('image')[1] == '9':
            self.alerta("Partida finalizada","Has ganado a la máquina","Empezar de nuevo","Regresar a inicio" )
            
       
    
    def posFichas(self):
        lista=[]
        widget = MainLayout()
        for id in widget.ids.keys():
            if id[:-7] == 'button':
                num = id[-7]
            if id[0: 5] == 'image' and self.ids[id].source != '':
                lista.append(id)
        return lista
    def estado_computador(self):#Devuelve laas pocisiones de las fichas de la pc
        lista=[]
        widget = MainLayout()
        for id in widget.ids.keys():
            if id[:-7] == 'button':
                num = id[-7]
            if id[0: 5] == 'image' and self.ids[id].source == 'btn_red.png':
                lista.append(id.split('image')[1])
        return lista

    def estado_humano(self):#Devuelve laas pocisiones de las fichas del oponente
        lista=[]
        widget = MainLayout()
        for id in widget.ids.keys():
            if id[:-7] == 'button':
                num = id[-7]
            if id[0: 5] == 'image' and self.ids[id].source == 'btn_blue.png':
                lista.append(id.split('image')[1])
        return lista
        
            

    def mover_ficha(self, instance):
        #print(instance.text)
        num = instance.text  # str(self.get_id(instance).split('button')[1])
        my_id = 'image'+num
        if self.ids[my_id].source != 'btn_red.png':
            if self.ids[my_id].source == 'btn_blue.png'and not self.mover:
                self.id_mover=my_id

            if self.ids[my_id].source == 'btn_blue.png' and self.mover:    
                self.alerta('Selección de fichas',"No puede mover, ni poner encima de la ficha roja.", "Entiendo", "")

            elif (self.ids[my_id].source == 'btn_blue.png'):
                    self.ids[my_id].source = 'mov.png'
                    self.mover = True
            elif my_id==self.id_mover:#click en la misma ficha
                self.ids[my_id].source = 'btn_blue.png'
                print(my_id)
                self.mover = False
                
                
            elif self.mover:#Si un boton está seleccionado tiene que limpiarse
                self.ids[my_id].source = 'btn_blue.png'#Sr pinta el nuevo destino
                self.ids[self.id_mover].source = ''#Se pinta con blanco lficha inicial
                self.mover= False
                self.id_mover = ''
                self.movimiento_pc()
        else:# En caso dar clicl en la ficha roja o poner otra encima
            self.alerta('Selección de fichas',"No puede mover, ni poner encima de la ficha roja.", "Entiendo", "")
        self.mostrarGanador()

    def changeImage(self, instance):
        my_id = 'image'+str(self.get_id(instance).split('button')[1])
        self.clear_image(my_id)
        print(my_id)
        """if self.ids[my_id].source == 'white.png':
            self.ids[my_id].source = 'btn_red.png'
        else:
            self.ids[my_id].source = 'white.png'    """
    def goHome(self,*args):
        self.manager.current = "Screen_1"
        self.reiniciar()
        
    def reiniciar(self,*args):    
        for i in range(1, 14):
            self.ids["image"+str(i)].source = ''           
        self.ids["image1"].source = 'btn_red.png'
        self.ids["image7"].source = 'btn_blue.png'
        self.ids["image8"].source = 'btn_red.png'
        self.ids["image14"].source = 'btn_blue.png'
            
    def alerta(self, titulo, msj, btn1, btn2):
            print("alert")
            layout = GridLayout(cols=1, padding=10, spacing=10)
            popupLabel = Label(text=msj)
            closeButton = Button(text=btn1, on_release=self.reiniciar, size_hint=(10, 0.5), background_color=( .58, 2.21, .33, 1))
         
            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)
            popup = Popup(title=titulo,
                          
                          size_hint=(None, None), size=(700, 300),
                          background_color=(.33, 1.29, 2.21, 1))
            if len(btn2)>0:
                reJugar = Button(text=btn2,on_press=popup.dismiss,on_release = self.goHome, size_hint=(
                    10, 0.5), background_color=(.58, 2.21, .33, 1))   
                layout.add_widget(reJugar)
   
            popup = Popup(title=titulo,
                        content=layout,
                          size_hint=(None, None), size=(700, 300),
                          background_color=(.33, 1.29, 2.21, 1), auto_dismiss=True)
            popup.open()
            closeButton.bind(on_press=popup.dismiss)
            if len(btn2) > 0:
                reJugar.bind(on_press=popup.dismiss)
                  

class MainApp(App):
    def build(self):       
        return Builder.load_file("design.kv")
        
    
    def on_pause(self):
        return True

    def on_resume(self):
        pass

class Juego(App):

        def sortearJugador(self):
            comienza = random.randint(0, 1)
            if comienza == 0:
                MainApp().alerta('Comienza el jugador')
            else:
                MainApp().alerta('Comienza el PC')
    
        
if __name__ in ('__main__'):
    MainApp().run()
    
    
