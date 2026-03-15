# GUI-Maker
Docs coming soon! (or not soon idk)

Example usage that covers a lot, but not all. i suggest looking through the classes for functions
```py
from gui_maker import *
import pyautogui

def drag():
    x, y = pyautogui.position()
    reposition(x-200,y+8)

Callback.register(downC,"downC")
Callback.register(drag,"drag")

new = Window("Test",(100, 50),(100, 150))
new.set_color((255,100,10,30))
new.set_outline_width(2)
new.set_outline_color((255,255,255,255))

textbox = TextBox("Textbox","Hello, World!",(1, 1))
textbox.set_color((255,10,100,0))

tickbox = TickBox("TickBox",(1,10))
tickbox.set_outline_color((255,0,255,255))
tickbox.set_ticked_color((255,100,100,0))
tickbox.set_unticked_color((255,0,0,0))

button = Button("Button",(1,20),(50,30))
button.set_text(":3")
button.set_color((255,0,0,0))
button.set_text_color((100,100,100,100))
button.set_pressed_color((255,0,0,255))
button.set_text_offset((15,5))

drag_button = Button("Drag",(0, -4),(100, 4))
drag_button.set_text("")
drag_button.while_down("drag")

text_input = TextInput("Text Input",">",(1,50),(40,10))
text_input.set_color((255,100,100,100))
text_input.set_text_color((255,200,100,0))

slider = Slider("Test Slider",0,(1,65))
slider.set_color((255,200,100,0))
slider.set_filled_color((255,255,150,0))

new.add_widget(textbox)
new.add_widget(tickbox)
new.add_widget(button)
new.add_widget(drag_button)
new.add_widget(text_input)
new.add_widget(slider)

# Render the gui in game
render(new.export())

while True:
    manage_callbacks()
```
