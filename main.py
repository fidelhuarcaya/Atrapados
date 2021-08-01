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

class ScreenManagement(ScreenManager):
      pass
class Screen1(Screen):
    name_x = StringProperty('')
    def update_info(self):
        self.name_x = self.ids.nombre.text
        print('tu nombre es: ',self.name_x)
        



class MainLayout(Screen):  
    click = True
    mover = False
    id_mover = ''
    play=''

    def on_pre_enter(self, *args):
        self.play = self.sortearJugador()
        self.ids.name.text = 'Bienvenido '+self.manager.ids.Screen1.name_x
    def desactivar_imagen(self):
       self.ids.my_image.source = 'white.png'
    def activar_imagen(self):
        self.ids.my_image.source = 'btn_red.png'
    def clear_image(self, myId):
        my_id = 'image'
        #for i in range(1,15):
         #   if i!=btn_red1:
        self.ids[myId].source = 'white.png'
    def sortearJugador(self):
        comienza = random.randint(0, 1)
        msj=''
        if comienza == 0:
            msj = 'Humano'
            self.alerta("Play game",'Comienza el '+msj, "Go","")
        else:
            msj = 'Computador'
            self.alerta("Play game",'Comienza el '+msj, "Go","")
        return msj

    #def movimiento_pc(self):
        
    def verificarGanador(self, instance):    
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

        
            

    def mov(self, instance):
        #print(instance.text)
        num = instance.text  # str(self.get_id(instance).split('button')[1])
        my_id = 'image'+num
        if self.ids[my_id].source != 'btn_red.png':
            if self.ids[my_id].source == 'btn_blue.png'and not self.mover:
                self.id_mover=my_id

            if self.ids[my_id].source == 'btn_blue.png' and self.mover:    
                self.alerta(msj="Movimiento erróneo. Seleccione sola una ficha a mover.")

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
        else:# En caso dar clicl en la ficha roja o poner otra encima
            self.alerta('Selección de fichas',"No puede mover, ni poner encima de la ficha roja.", "Entiendo", "")
        self.verificarGanador(instance)

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
        

            
    def alerta(self, titulo, msj, btn1, btn2):
            print("alert")
            layout = GridLayout(cols=1, padding=10, spacing=10)
            popupLabel = Label(text=msj)
            closeButton = Button(text=btn1, size_hint=(10, 0.5), background_color=( .58, 2.21, .33, 1))
         
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
    
    
