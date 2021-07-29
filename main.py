from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.graphics import Rectangle, Color 
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from functools import partial
from kivy.resources import resource_find
from kivy.uix.behaviors import ButtonBehavior
import random
from kivy.core.window import Window


#indicamos el dirección del diseño de la app
Builder.load_file('design.kv')




class MainLayout(Widget):
    def __init__(self):
        super(MainLayout, self).__init__()
        
    click = True
    mover = False
    id_mover = ''
    btn_red1='1'
    btn_red2='8'
    btn_blue1='7'
    btn_blue2='14'

    def showquestion(self):
            self.ids['label2'].text = "filetext"

    def showanswer(self):
            self.ids['button1'].text = "filetext" 
                      
            click=True
        

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
        if comienza == 0:
            self.alerta('Comienza el jugador')
        else:
            self.alerta('Comienza el PC')
        

    def mov(self, instance):
        print(instance.text)
        
        print("getID: ",instance.parent.ids.keys())
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
                self.ids[self.id_mover].source = 'white.png'#Se pinta con blanco lficha inicial
                self.mover= False
                self.id_mover = ''
        else:# En caso dar clicl en la ficha roja o poner otra encima
            self.alerta(msj="No puede mover, ni poner encima de la ficha roja.")
    def get_id(self, instance):
        print("Listo: ", instance.ids.keys())
        for id, widget in instance.parent.ids.keys():
            print("listo2")
            print(widget.__self__)
            if widget.__self__ == instance: 
                return id
    def changeImage(self, instance):
        my_id = 'image'+str(self.get_id(instance).split('button')[1])
        self.clear_image(my_id)
        print(my_id)
        """if self.ids[my_id].source == 'white.png':
            self.ids[my_id].source = 'btn_red.png'
        else:
            self.ids[my_id].source = 'white.png'    """
            
            
    def alerta(self, msj):
            print("alert")
            layout = GridLayout(cols=1, padding=10)
            popupLabel = Label(
                text=msj)
            closeButton = Button(text="Entiendo", size_hint=(10, 0.3), background_color=( .58, 2.21, .33, 1))

            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)
            popup = Popup(title='Selección de fichas',
                        content=layout,
                          size_hint=(None, None), size=(700, 300),
                                background_color=(.33, 1.29, 2.21, 1))
            popup.open()
            closeButton.bind(on_press=popup.dismiss)
        



class MainApp(App):
    def build(self):
        return MainLayout()
    
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
    
        
if __name__ in ('__main__', '__android__'):
    n=MainApp()
    n.run()
    
    
