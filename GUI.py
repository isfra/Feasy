import numpy as np

import kivy
from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

import operatori as o
import formule as f
import kernel as k


#class ScegliTeoriaWidget(Widget):


class ButtonsWidget(BoxLayout):

    def on_buttonteorie_press(self):

        #scegli_teoria=BoxLayout(orientation='vertical', spacing=10)
        self.teorietxt = TextInput(hint_text='Nome Teoria', size_hint=(.5, .1))




    def on_buttondati_press(self):

    def on_buttonincognite_press(self):

class TextWidget(BoxLayout):

    def update_teorietext(self):



class AnimationWidget(Widget):

    def on_buttonrisolvi_press(self):

class ProblemSolver(FloatLayout):

    def __init__(self):

        self.teorie = f.teorie
        self.teorie_scelte = []
        self.dati = []
        self.incognite = []

        #self.tasti = ButtonsWidget()
        #self.scelte = TextWidget()
        #self.soluzione = AnimationWidget()



class FeasyApp(App):

    def build(self):

        ps = ProblemSolver()

        return ps


