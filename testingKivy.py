import kivy

import random
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout




class MainApp(App):
    def build(self):
        layout = BoxLayout(padding=10)
        colors = [[1,0,0,1],[0,1,0,1],[0,0,1,1],[1,0,1,1]]
        for i in range(5):
            btn = Button(text = "Button #%s" % (i+1),
                         background_color = random.choice(colors)
                         )
            layout.add_widget(btn)
        button = Button(text = "Usable button")
        return layout
        
if __name__ == '__main__':
    app = MainApp()
    app.run()