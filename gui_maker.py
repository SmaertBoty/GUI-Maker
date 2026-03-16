from pathlib import Path
import inspect
from threading import Thread
from PIL import Image
ex_path = Path(__file__).resolve().parent / "gui_maker" / "pyjinn_to_python.txt"
in_path = Path(__file__).resolve().parent / "gui_maker" / "python_to_pyjinn.txt"
path = Path(__file__).resolve().parent / "gui_maker" / "ui.pyj"
glfw_path = Path(__file__).resolve().parent / "system" / "pyj" / "glfw.py"

try:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.unlink(missing_ok=True)
    ex_path.unlink(missing_ok=True)
    in_path.unlink(missing_ok=True)
    glfw_path.unlink(missing_ok=True)
    with open(glfw_path,"w") as f:
        f.write("""
# File origin: gui_maker.py
GLFW_KEYS = {
    -1: "UNKNOWN",

    32: "SPACE",
    39: "APOSTROPHE",
    44: "COMMA",
    45: "MINUS",
    46: "PERIOD",
    47: "SLASH",

    48: "0",
    49: "1",
    50: "2",
    51: "3",
    52: "4",
    53: "5",
    54: "6",
    55: "7",
    56: "8",
    57: "9",

    59: "SEMICOLON",
    61: "EQUAL",

    65: "A",
    66: "B",
    67: "C",
    68: "D",
    69: "E",
    70: "F",
    71: "G",
    72: "H",
    73: "I",
    74: "J",
    75: "K",
    76: "L",
    77: "M",
    78: "N",
    79: "O",
    80: "P",
    81: "Q",
    82: "R",
    83: "S",
    84: "T",
    85: "U",
    86: "V",
    87: "W",
    88: "X",
    89: "Y",
    90: "Z",

    91: "LEFT_BRACKET",
    92: "BACKSLASH",
    93: "RIGHT_BRACKET",
    96: "GRAVE_ACCENT",

    161: "WORLD_1",
    162: "WORLD_2",

    256: "ESCAPE",
    257: "ENTER",
    258: "TAB",
    259: "BACKSPACE",
    260: "INSERT",
    261: "DELETE",

    262: "RIGHT",
    263: "LEFT",
    264: "DOWN",
    265: "UP",

    266: "PAGE_UP",
    267: "PAGE_DOWN",
    268: "HOME",
    269: "END",

    280: "CAPS_LOCK",
    281: "SCROLL_LOCK",
    282: "NUM_LOCK",
    283: "PRINT_SCREEN",
    284: "PAUSE",

    290: "F1",
    291: "F2",
    292: "F3",
    293: "F4",
    294: "F5",
    295: "F6",
    296: "F7",
    297: "F8",
    298: "F9",
    299: "F10",
    300: "F11",
    301: "F12",
    302: "F13",
    303: "F14",
    304: "F15",
    305: "F16",
    306: "F17",
    307: "F18",
    308: "F19",
    309: "F20",
    310: "F21",
    311: "F22",
    312: "F23",
    313: "F24",
    314: "F25",

    320: "KP_0",
    321: "KP_1",
    322: "KP_2",
    323: "KP_3",
    324: "KP_4",
    325: "KP_5",
    326: "KP_6",
    327: "KP_7",
    328: "KP_8",
    329: "KP_9",

    330: "KP_DECIMAL",
    331: "KP_DIVIDE",
    332: "KP_MULTIPLY",
    333: "KP_SUBTRACT",
    334: "KP_ADD",
    335: "KP_ENTER",
    336: "KP_EQUAL",

    340: "LEFT_SHIFT",
    341: "LEFT_CONTROL",
    342: "LEFT_ALT",
    343: "LEFT_SUPER",

    344: "RIGHT_SHIFT",
    345: "RIGHT_CONTROL",
    346: "RIGHT_ALT",
    347: "RIGHT_SUPER",

    348: "MENU"
}
""")
except: pass

path.touch()
ex_path.touch()
in_path.touch()
glfw_path.touch()

try:
    from system.lib.minescript import execute, job_info, echo
except:
    def execute(*s): print(*s)
    def job_info(): pass
    def echo(*s): print(*s)

callback_ids = {}

class Callback:
    def __init__(self,callback_id):
        if Callback._debug_exists(callback_id):
            self.callback_id = callback_id
        else: raise NotImplementedError(f"Could not find callback registered under '{callback_id}'")
    
    @staticmethod
    def listall():
        return callback_ids

    @staticmethod
    def register(func,callback_id,threaded=True):
        global callback_ids
        callback_ids[callback_id] = {"callback":func,"threaded":threaded}
        return callback_id
    
    @staticmethod
    def _debug_trigger(call_id,*args):
        Callback._debug_get(call_id)(*args)

    @staticmethod
    def _debug_get(call_id):
        return callback_ids[call_id]["callback"]
    
    @staticmethod
    def _debug_exists(key):
        for _ in callback_ids:
            try: callback_ids[key] ; return True
            except: pass
        return False
    
    def _debug_export(self):
        return {"callback":self.callback_id}
class DebugCallback:
    @staticmethod
    def _debug_export(*args):
        return None

class Window:
    def __init__(self, id, pos:tuple=(0,0), size:tuple=(100,100),color:tuple=(255,30,30,30),outline_width:int=0,outline_color:tuple=(255,0,0,0)):
        self.pos = pos
        self.size = size
        self.widgets = {}
        self.id = id
        self.color = color
        self.outline_width = outline_width
        self.outline_color = outline_color
    
    def set_color(self,argb:tuple):
        self.color = argb
    
    def set_outline_color(self,argb:tuple):
        self.outline_color = argb
    
    def set_outline_width(self,width:int):
        self.outline_width = width
    
    def set_pos(self,pos:tuple):
        self.pos = pos
    
    def set_size(self,size:tuple):
        self.size = size
    
    def add_widget(self,widget):
        self.widgets[widget.id] = widget
        return self

    def export(self):
        exported = {}
        for widget_id in self.widgets:
            exported[widget_id] = self.widgets[widget_id]._debug_export(self.id)
        exported
        return {
            "id": self.id,
            "type":"GUI",
            "pos":self.pos,
            "size":self.size,
            "color":self.color,
            "outline_width":self.outline_width,
            "outline_color":self.outline_color,
            "widgets":exported
        }

class ChildWindow:
    def __init__(self, id, pos:tuple=(0,0), size:tuple=(100,100)):
        self.pos = pos
        self.size = size
        self.widgets = {}
        self.id = id
    
    def add_widget(self,widget):
        self.widgets[widget.id] = widget
        return self

    def _debug_export(self,parent):
        exported = {}
        for widget_id in self.widgets:
            exported[widget_id] = self.widgets[widget_id]._debug_export(self.id)
        exported
        return {
            "type":"GUI",
            "parent":parent,
            "pos":self.pos,
            "size":self.size,
            "widgets":exported
        }

class TextBox:
    def __init__(self,id,text:str="",pos:tuple=(0,0),color:tuple=(255,255,255)):
        self.id = id
        self.text = text
        self.pos = pos
        self.color = color
    
    def set_color(self,argb:tuple):
        self.color = argb
    
    def set_pos(self,pos:tuple):
        self.pos = pos
    
    def set_text(self,text):
        self.text = text
        return self
    
    def _debug_export(self,parent):
        return {
            "type":"TextBox",
            "parent":parent,
            "pos":self.pos,
            "text":self.text,
            "color":self.color
        }

class TextInput:
    def __init__(self,id,starting_text:str="",pos:tuple=(0,0),size:tuple=(1,1),while_typing=DebugCallback,on_finished_typing=DebugCallback,color:tuple=(255,0,0,0),text_color:tuple=(255,255,255,255)):
        self.id = id
        self._starting_text = starting_text
        self.pos = pos
        self.size = size
        self._while_typing = while_typing
        self._on_finished_typing = on_finished_typing
        self.color = color
        self.text_color = text_color
    
    def set_color(self,argb:tuple):
        self.color = argb
    
    def set_text_color(self,argb:tuple):
        self.text_color = argb
    
    def set_pos(self,pos:tuple):
        self.pos = pos
    
    def set_size(self,size:tuple):
        self.size = size
    
    def set_starting_text(self,starting_text):
        self._starting_text = starting_text
        return self
    
    def while_typing(self,func):
        self._while_typing = Callback(func)
        return self
    
    def on_finished_typing(self,func):
        self._on_finished_typing = Callback(func)
        return self
    
    def _debug_export(self,parent):
        return {
            "type":"TextInput",
            "parent":parent,
            "pos":self.pos,
            "size":self.size,
            "color":self.color,
            "text_color":self.text_color,
            "starting_text":self._starting_text,
            "actions":{
                "while_typing":self._while_typing._debug_export(),
                "on_finished_typing":self._on_finished_typing._debug_export()
            }
        }

class Button:
    def __init__(self,id,pos:tuple=(0,0),size:tuple=(1,1),text="",on_press=DebugCallback,while_down=DebugCallback,on_release=DebugCallback,color:tuple=(255, 70, 70, 70),pressed_color:tuple=(255, 200, 150, 200),text_color:tuple=(255,255,255,255),text_offset:tuple=(0,0)):
        self.id = id
        self.pos = pos
        self.size = size
        self._on_press = on_press
        self._while_down = while_down
        self._on_release = on_release
        self.text = text
        self.color = color
        self.pressed_color = pressed_color
        self.text_color = text_color
        self.text_offset = text_offset
    
    def set_text_offset(self,offset:tuple):
        self.text_offset = offset
    
    def set_text_color(self,argb:tuple):
        self.text_color = argb
    
    def set_color(self,argb:tuple):
        self.color = argb
    
    def set_pressed_color(self,argb:tuple):
        self.pressed_color = argb
    
    def set_pos(self,pos:tuple):
        self.pos = pos
    
    def set_size(self,size:tuple):
        self.size = size
    
    def on_press(self,func):
        self._on_press = Callback(func)
        return self

    def while_down(self,func):
        self._while_down = Callback(func)
        return self
    
    def on_release(self,func):
        self._on_release = Callback(func)
        return self

    def set_text(self,text):
        self.text = text
        return self
    
    def _debug_export(self,parent):
        return {
            "type":"Button",
            "parent":parent,
            "pos":self.pos,
            "size":self.size,
            "text":self.text,
            "color":self.color,
            "pressed_color":self.pressed_color,
            "text_color":self.text_color,
            "text_offset":self.text_offset,
            "actions":{
                "on_press":self._on_press._debug_export(),
                "while_down":self._while_down._debug_export(),
                "on_release":self._on_release._debug_export()
            }
        }

class Slider:
    def __init__(self,id,starting_value:int=0,pos:tuple=(0,0),width=50,on_value_change=DebugCallback,color:tuple=(255, 100, 70, 255),filled_color:tuple=(150, 100, 70, 255),empty_color:tuple=(255,0,0,0)):
        self.id = id
        self._starting_value = starting_value
        self.pos = pos
        self.width = width
        self._on_value_change = on_value_change
        self.color = color
        self.filled_color = filled_color
        self.empty_color = empty_color
    
    def set_color(self,argb:tuple):
        self.color = argb
    
    def set_filled_color(self,argb:tuple):
        self.filled_color = argb
    
    def set_empty_color(self,argb:tuple):
        self.empty_color_color = argb
    
    def set_pos(self,pos:tuple):
        self.pos = pos
    
    def set_width(self,width:tuple):
        self.width = width
    
    def set_starting_value(self,starting_value):
        self.starting_value = starting_value
        return self
    
    def on_value_change(self,func):
        self._on_value_change = Callback(func)
        return self
    
    def _debug_export(self,parent):
        return {
            "type":"Slider",
            "parent":parent,
            "pos":self.pos,
            "width":self.width,
            "color":self.color,
            "filled_color":self.filled_color,
            "empty_color":self.empty_color,
            "starting_value":self._starting_value,
            "actions":{
                "on_value_change":self._on_value_change._debug_export(),
            }
        }

class DropdownMenu:
    def __init__(self,id,pos:tuple=(0,0),size:tuple=(5,1),starting_items:list=[],starting_item:int=0,on_item_selected=DebugCallback):
        self.id = id
        self.pos = pos
        self.size = size
        self._starting_items = starting_items
        self._starting_item = starting_item
        self._on_item_selected = on_item_selected
    
    def set_starting_items(self,starting_items):
        self._starting_items = starting_items
        return self

    def set_starting_item(self,starting_item):
        self._starting_item = starting_item
        return self
    
    def on_item_selected(self,func):
        self._on_item_selected = Callback(func)
        return self
    
    def _debug_export(self,parent):
        return {
            "type":"Button",
            "parent":parent,
            "pos":self.pos,
            "size":self.size,
            "starting_item":self._starting_item,
            "starting_items":self._starting_items,
            "actions":{
                "on_item_selected":self._on_item_selected._debug_export()
            }
        }

class TickBox:
    def __init__(self,id,pos:tuple=(0,0),starting_state=False,on_ticked=DebugCallback,on_unticked=DebugCallback,ticked_color:tuple=(255, 000, 150, 200),unticked_color:tuple=(255, 30, 30, 30),outline_color:tuple=(255, 255, 255, 255)):
        self.id = id
        self._on_ticked = on_ticked
        self._on_unticked = on_unticked
        self.pos = pos
        self._starting_state = starting_state
        self.ticked_color = ticked_color
        self.unticked_color = unticked_color
        self.outline_color = outline_color
    
    def set_ticked_color(self,argb:tuple):
        self.ticked_color = argb
    
    def set_unticked_color(self,argb:tuple):
        self.unticked_color = argb
    
    def set_outline_color(self,argb:tuple):
        self.outline_color = argb
    
    def set_pos(self,pos:tuple):
        self.pos = pos
    
    def set_starting_state(self,starting_state):
        self._starting_state = starting_state
        return self

    def on_ticked(self,func):
        self._on_ticked = Callback(func)
        return self
    
    def on_unticked(self,func):
        self._on_unticked = Callback(func)
        return self
    
    def _debug_export(self,parent):
        return {
            "type":"TickBox",
            "parent":parent,
            "pos":self.pos,
            "starting_state":self._starting_state,
            "ticked_color":self.ticked_color,
            "unticked_color":self.unticked_color,
            "outline_color":self.outline_color,
            "actions":{
                "on_ticked":self._on_ticked._debug_export(),
                "on_unticked":self._on_unticked._debug_export()
                }
            }

class Picture:
    def __init__(self,id,texture_path:Path,pos:tuple=(0,0),outline_width:int=0,outline_color:tuple=(255,100,100,100)):
        self.id = id
        self.pos = pos
        self.texture_path = texture_path
        self.outline_width = outline_width
        self.outline_color = outline_color
        self.color_resolution = 1

    def set_outline_color(self,argb:tuple):
        self.outline_color = argb
    
    def set_outline_width(self,width:int):
        self.outline_width = width
    
    def set_pos(self,pos:tuple):
        self.pos = pos
    
    def set_texture_path(self,texture_path):
        self.texture_path = texture_path
    
    def set_color_resolution(self,resolution):
        self.color_resolution = resolution
    
    def convert_picture(self):
        step = self.color_resolution if self.color_resolution > 0 else 1
        def quantize_color(r, g, b, a, step):
            r = round(r / step) * step
            g = round(g / step) * step
            b = round(b / step) * step
            return (a, r, g, b)
        img = Image.open(self.texture_path).convert("RGBA")
        width, height = img.size
        pixels = img.load()
        grid = []
        for y in range(height):
            row = []
            for x in range(width):
                r, g, b, a = pixels[x, y]
                row.append(quantize_color(r, g, b, a, step))
            grid.append(row)
        covered = [[False] * width for _ in range(height)]
        rects = []
        def find_max_rect_at(sx, sy):
            color = grid[sy][sx]
            max_w = 0
            while sx + max_w < width and not covered[sy][sx + max_w] and grid[sy][sx + max_w] == color:
                max_w += 1
            if max_w == 0:
                return None
            best_w, best_h = max_w, 1
            cur_w = max_w
            for dy in range(1, height - sy):
                y = sy + dy
                row_w = 0
                while row_w < cur_w and not covered[y][sx + row_w] and grid[y][sx + row_w] == color:
                    row_w += 1
                if row_w == 0:
                    break
                cur_w = row_w
                h = dy + 1
                if cur_w * h > best_w * best_h:
                    best_w, best_h = cur_w, h
            return (sx, sy, best_w, best_h, color)
        for y in range(height):
            for x in range(width):
                if covered[y][x]:
                    continue
                result = find_max_rect_at(x, y)
                if result is None:
                    continue
                rx, ry, rw, rh, color = result
                rects.append((rx, ry, rw, rh, color))
                for dy in range(rh):
                    for dx in range(rw):
                        covered[ry + dy][rx + dx] = True
        return rects
    
    def _debug_export(self,parent):
        return {
            "type":"Picture",
            "parent":parent,
            "pos":self.pos,
            "outline_width":self.outline_width,
            "outline_color":self.outline_color,
            "picture":self.convert_picture()
        }

def render(exported):
    if isinstance(exported,Window): exported = exported.export()
    for job in job_info():
        if job.command[0] == r"gui_maker\ui":
            execute(fr"\killjob {job.job_id}")
    code = fr"""
from glfw import GLFW_KEYS as GLFW

TextBoxes = []
TickBoxes = []
Buttons = []
TextInputs = []
Sliders = []
Pictures = []

GUI = {exported}
Minecraft = JavaClass("net.minecraft.client.Minecraft")
Component = JavaClass("net.minecraft.network.chat.Component")
HudRenderCallback = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback")
ARGB = JavaClass("net.minecraft.util.ARGB")
System = JavaClass("java.lang.System")
BufferedWriter = JavaClass("java.io.BufferedWriter")
BufferedReader = JavaClass("java.io.BufferedReader")
FileWriter = JavaClass("java.io.FileWriter")
FileReader = JavaClass("java.io.FileReader")
File = JavaClass("java.io.File")
Math =  JavaClass("java.lang.Math")
Character = JavaClass("java.lang.Character")

mc = Minecraft.getInstance()
if "mac" not in System.getProperty("os.name").toLowerCase():
    ex_path = File(System.getProperty("user.dir") + "\\minescript\\gui_maker\\pyjinn_to_python.txt")
    in_path = File(System.getProperty("user.dir") + "\\minescript\\gui_maker\\python_to_pyjinn.txt")
else:
    ex_path = File(System.getProperty("user.dir") + "/minescript/gui_maker/pyjinn_to_python.txt")
    in_path = File(System.getProperty("user.dir") + "/minescript/gui_maker/python_to_pyjinn.txt")
shift = False
mouse = False
old_val = None
gui_scale = mc.options.guiScale().get()
gui_scale = gui_scale if gui_scale else 4
ShowMain = True
last_written_pos = (0,0)

if not ex_path.exists():
    ex_path.getParentFile().mkdirs()
    ex_path.createNewFile()

if not in_path.exists():
    in_path.getParentFile().mkdirs()
    in_path.createNewFile()

def initiate(gui_override=None):
    global TextBoxes, TickBoxes, Buttons, GUI
    if gui_override is not None: GUI = gui_override
    for key in GUI["widgets"]:
        if GUI["widgets"][key]["type"] == "TextBox":
            TextBoxes.append([GUI["widgets"][key]["pos"],GUI["widgets"][key]["text"],True,key,GUI["widgets"][key]["color"]])
        elif GUI["widgets"][key]["type"] == "TickBox":
            TickBoxes.append([GUI["widgets"][key]["pos"],GUI["widgets"][key]["starting_state"],GUI["widgets"][key]["actions"]["on_ticked"],GUI["widgets"][key]["actions"]["on_unticked"],True,key,GUI["widgets"][key]["ticked_color"],GUI["widgets"][key]["unticked_color"],GUI["widgets"][key]["outline_color"]])
        elif GUI["widgets"][key]["type"] == "Button":
            Buttons.append([GUI["widgets"][key]["pos"],GUI["widgets"][key]["size"],GUI["widgets"][key]["text"],GUI["widgets"][key]["actions"]["while_down"],GUI["widgets"][key]["actions"]["on_press"],GUI["widgets"][key]["actions"]["on_release"],False,True,key,GUI["widgets"][key]["color"],GUI["widgets"][key]["pressed_color"],GUI["widgets"][key]["text_color"],GUI["widgets"][key]["text_offset"]])
        elif GUI["widgets"][key]["type"] == "TextInput":
            TextInputs.append([GUI["widgets"][key]["pos"],GUI["widgets"][key]["size"],GUI["widgets"][key]["starting_text"],GUI["widgets"][key]["actions"]["while_typing"],GUI["widgets"][key]["actions"]["on_finished_typing"],False,key,True,GUI["widgets"][key]["color"],GUI["widgets"][key]["text_color"]])
        elif GUI["widgets"][key]["type"] == "Slider":
            Sliders.append([GUI["widgets"][key]["pos"],GUI["widgets"][key]["width"],GUI["widgets"][key]["starting_value"],GUI["widgets"][key]["actions"]["on_value_change"],False,True,key,GUI["widgets"][key]["color"],GUI["widgets"][key]["filled_color"],GUI["widgets"][key]["empty_color"]])
        elif GUI["widgets"][key]["type"] == "Picture":
            Pictures.append([GUI["widgets"][key]["pos"],key,GUI["widgets"][key]["picture"],True])
initiate()

def trigger(func,*args):
    writer = BufferedWriter(FileWriter(ex_path, True))
    writer.write(str(func) + ":" + ",".join(args) + "\n")
    writer.flush()
    writer.close()

def parse_incoming(s):
    global ShowMain
    if s.startswith("show "):
        shows = s[5:].split(",")
        for i in range(len(TextBoxes)):
            if TextBoxes[i][3] in shows:
                TextBoxes[i][2] = True
        for i in range(len(TickBoxes)):
            if TickBoxes[i][5] in shows:
                TickBoxes[i][4] = True
        for i in range(len(Buttons)):
            if Buttons[i][8] in shows:
                Buttons[i][7] = True
        for i in range(len(TextInputs)):
            if TextInputs[i][6] in shows:
                TextInputs[i][7] = True
        for i in range(len(Sliders)):
            if Sliders[i][6] in shows:
                Sliders[i][5] = True
        if GUI["id"] in shows:
            ShowMain = True
    elif s.startswith("hide "):
        hides = s[5:].split(",")
        for i in range(len(TextBoxes)):
            if TextBoxes[i][3] in hides:
                TextBoxes[i][2] = False
        for i in range(len(TickBoxes)):
            if TickBoxes[i][5] in hides:
                TickBoxes[i][4] = False
        for i in range(len(Buttons)):
            if Buttons[i][8] in hides:
                Buttons[i][7] = False
        for i in range(len(TextInputs)):
            if TextInputs[i][6] in hides:
                TextInputs[i][7] = False
        for i in range(len(Sliders)):
            if Sliders[i][6] in hides:
                Sliders[i][5] = False
        if GUI["id"] in hides:
            ShowMain = False
    elif s.startswith("pos "):
        try: GUI["pos"] = (int(int(s[4:].split(",")[0])/gui_scale),int(int(s[4:].split(",")[1])/gui_scale))
        except: pass

def read():
    reader = BufferedReader(FileReader(in_path))
    line = reader.readLine()
    while line is not None:
        parse_incoming(line)
        line = reader.readLine()
    reader.close()
    writer = BufferedWriter(FileWriter(in_path, False))
    writer.write("")
    writer.flush()
    writer.close()

def draw_window(GuiGraphics):
    x, y = GUI["pos"]
    width = x + GUI["size"][0]
    height = y + GUI["size"][1]
    color = GUI["color"]
    outline_width = GUI["outline_width"]
    outline_color = GUI["outline_color"]
    GuiGraphics.fill(x - outline_width, y - outline_width, width + outline_width, height + outline_width, ARGB.color(*outline_color))
    GuiGraphics.fill(x, y, width, height, ARGB.color(*color))

def draw_text_boxes(GuiGraphics,pos,text,color):
    x, y = GUI["pos"]
    x = x + pos[0]
    y = y + pos[1]
    GuiGraphics.drawString(mc.font, Component.literal(text), x, y, ARGB.color(*color), False)

def draw_tick_boxes(GuiGraphics,pos,state,ticked_color,unticked_color,outline_color):
    x, y = GUI["pos"]
    x = x + pos[0]
    y = y + pos[1]
    width = x + 7
    height = y + 7
    if state:
        color = ARGB.color(*ticked_color)
    else:
        color = ARGB.color(*unticked_color)
    
    GuiGraphics.fill(x, y, width, height, ARGB.color(*outline_color))
    GuiGraphics.fill(x + 1, y + 1 , width - 1, height - 1, color)

def draw_buttons(GuiGraphics,pos,size,text,state,callback,color,pressed_color,text_color,text_offset):
    x, y = GUI["pos"]
    x = x + pos[0]
    y = y + pos[1]
    width = x + size[0]
    height = y + size[1]
    if state:
        color = ARGB.color(*pressed_color)
        if callback is not None: trigger(callback["callback"])
    else:
        color = ARGB.color(*color)
    GuiGraphics.fill(x, y, width, height, color)
    offx, offy = text_offset
    GuiGraphics.drawString(mc.font, Component.literal(text), x + offx, y + offy, ARGB.color(*text_color), False)

def draw_text_inputs(GuiGraphics,pos,size,text,color,text_color):
    x, y = GUI["pos"]
    x = x + pos[0]
    y = y + pos[1]
    width = x + size[0]
    height = y + size[1]
    GuiGraphics.fill(x, y, width, height, ARGB.color(*color))
    GuiGraphics.drawString(mc.font, Component.literal(text), x, y+1, ARGB.color(*text_color), False)

def draw_sliders(GuiGraphics,pos,width,value,selected,i,color,filled_color,empty_color):
    global old_val
    x, y = GUI["pos"]
    x = x + pos[0]
    y = y + pos[1]
    GuiGraphics.fill(x, y, x + width, y + 4, ARGB.color(*empty_color))
    GuiGraphics.fill(x, y, x + int(width*value), y + 4, ARGB.color(*filled_color))
    if int(width*value) < 4: num = 4
    else: num = int(width*value)
    GuiGraphics.fill(x + num - 4, y, x + num, y + 4, ARGB.color(*color))
    if mouse and selected:
        mx = mc.mouseHandler.xpos()/gui_scale
        new_val = (mx - x + 2) / (x+width - x)
        if new_val < 0: new_val = 0
        if new_val > 1: new_val = 1
        Sliders[i][2] = new_val
        if old_val != new_val:
            if Sliders[i][3] is not None: trigger(Sliders[i][3]["callback"],str(new_val))
            old_val = new_val

def draw_pictures(GuiGraphics,pos,picture):
    x, y = GUI["pos"]
    x = x + pos[0]
    y = y + pos[1]
    for px, py, width, height, color in picture:
        GuiGraphics.fill(x + px, y + py, x + px + width, y + py + height, ARGB.color(*color))

def handle_render(GuiGraphics,some_other_delta_time_crap_i_dont_care_about):
    if ShowMain:
        draw_window(GuiGraphics)
    for pos, text, show, _, color in TextBoxes:
        if show:
            draw_text_boxes(GuiGraphics,pos,text,color)
    for pos, state, _, _, show, _, ticked_color, unticked_color, outline_color in TickBoxes:
        if show:
            draw_tick_boxes(GuiGraphics,pos,state,ticked_color,unticked_color,outline_color)
    for pos, size, text, while_down, _, _, down, show, _, color, pressed_color, text_color, text_offset in Buttons:
        if show:
            draw_buttons(GuiGraphics,pos,size,text,down,while_down,color,pressed_color,text_color,text_offset)
    for pos, size, text, _, _, _, _, show, color, text_color in TextInputs:
        if show:
            draw_text_inputs(GuiGraphics,pos,size,text,color,text_color)
    for i in range(len(Sliders)):
        if Sliders[i][5]:
            draw_sliders(GuiGraphics,Sliders[i][0],Sliders[i][1],Sliders[i][2],Sliders[i][4],i,Sliders[i][7],Sliders[i][8],Sliders[i][9])
    for pos, _, picture, show in Pictures:
        if show:
            draw_pictures(GuiGraphics,pos,picture)


# TextB
# pos 0, text 1, show 2, id 3, color 4

# TickB:
# pos 0, state 1, on_ticked 2, on_unticked 3, show 4, id 5, ticked_color 6, unticked_color 7, outline_color 8

# Button:
# pos 0, size 1, text 2, while_down 3, on_press 4, on_release 5, down 6, show 7, id 8, color 9, pressed_color 10, text_color 11, text_offset 12

# Text Input:
# pos 0, size 1, text 2, while_typing 3, on_finished_typing 4, selected 5, id 6, show 7, color 8, text_color 9

# Slider:
# pos 0, width 1, value 2, on_value_changed 3, selected 4, show 5, id 6, color 7, filled_color 8, empty_color 9

# Picture
# pos 0, id 1, picture 2, show 3

def handle_mouse(event):
    global mouse
    mx = Math.round(event.x/gui_scale)
    my = Math.round(event.y/gui_scale)
    x, y = GUI["pos"]
    if event.action == 0:
        mouse = False
        for i in range(len(TickBoxes)):
            if TickBoxes[i][4]:
                tbx = x + TickBoxes[i][0][0]
                tby = y + TickBoxes[i][0][1]
                if mx > tbx and mx < tbx + 7 and my > tby and my < tby + 7:
                    TickBoxes[i][1] = not TickBoxes[i][1]
                    if TickBoxes[i][1] and TickBoxes[i][2] is not None: trigger(TickBoxes[i][2]["callback"])
                    elif TickBoxes[i][3] is not None: trigger(TickBoxes[i][3]["callback"])
        for i in range(len(TextInputs)):
            if TextInputs[i][7]:
                tix = x + TextInputs[i][0][0]
                tiy = y + TextInputs[i][0][1]
                sx = TextInputs[i][1][0]
                sy = TextInputs[i][1][1]
                TextInputs[i][5] = False
                if mx > tix and mx < tix + sx and my > tiy and my < tiy + sy:
                    TextInputs[i][5] = True
                    set_chat_input(TextInputs[i][2])
                    return
        for i in range(len(Sliders)):
            Sliders[i][4] = False
    else:
        mouse = True
        for i in range(len(Sliders)):
            if Sliders[i][5]:
                slx = x + Sliders[i][0][0]
                sly = y + Sliders[i][0][1]
                sx = Sliders[i][1]
                value = Sliders[i][2]
                sy = 4
                if int(sx*value) < 4: num = 4
                else: num = int(sx*value)
                if mx > slx + num - 4 and mx < slx + num and my > sly and my < sly + sy:
                    Sliders[i][4] = True


    for i in range(len(Buttons)):
        if Buttons[i][7]:
            bx = x + Buttons[i][0][0]
            by = y + Buttons[i][0][1]
            sx = Buttons[i][1][0]
            sy = Buttons[i][1][1]
            if mx > bx and mx < bx + sx and my > by and my < by + sy:
                if event.action == 1:
                    if Buttons[i][4] is not None: trigger(Buttons[i][4]["callback"])
                    Buttons[i][6] = True
            if event.action == 0:
                if Buttons[i][6]:
                    if Buttons[i][5] is not None: trigger(Buttons[i][5]["callback"])
                Buttons[i][6] = False

def handle_keys(event):
    global shift
    if "SHIFT" in GLFW[event.key]:
        if event.action == 1: shift = True
        elif event.action == 0: shift = False
        return
    if event.action != 0:
        for i in range(len(TextInputs)):
            if TextInputs[i][5] and TextInputs[i][7]:
                if shift:
                    key = GLFW[event.key]
                else:
                    key = GLFW[event.key].lower()
                if GLFW[event.key].lower() == "space":
                    key == " "
                if not GLFW[event.key].lower() == "backspace" and len(key) == 1:
                    TextInputs[i][2] = TextInputs[i][2] +  key
                elif GLFW[event.key].lower() == "backspace":
                    if len(TextInputs[i][2]) >= 1:
                        TextInputs[i][2] = TextInputs[i][2][:-1]
                elif GLFW[event.key].lower() == "enter":
                    TextInputs[i][5] = False
                    if TextInputs[i][4] is not None: trigger(TextInputs[i][4]["callback"],TextInputs[i][2])
                    set_chat_input("")
                if TextInputs[i][3] is not None: trigger(TextInputs[i][3]["callback"],TextInputs[i][2])
                return

def handle_tick(event):
    global gui_scale
    gui_scale = mc.options.guiScale().get()
    gui_scale = gui_scale if gui_scale > 0 else 4
    read()
                
    
add_event_listener("mouse",handle_mouse)
add_event_listener("key",handle_keys)
add_event_listener("tick",handle_tick)


callback = ManagedCallback(handle_render)
HudRenderCallback.EVENT.register(HudRenderCallback(callback))
"""
    with open(path,"w") as f:
        f.write(code)
    execute(r"\gui_maker\ui")

contents = None

def _signal(s):
    with open(in_path,"a") as f:
        f.write("\n"+s)

def show(*filter):
    _signal(f"show {",".join(filter)}")

def hide(*filter):
    _signal(f"hide {",".join(filter)}")

def reposition(x,y):
    # For the main window
    _signal(f"pos {int(x)},{int(y)}")

def set_text(id,s):
    #TODO
    # For widgets with text
    _signal(f"settext {id} {s}")

def set_pos(id,x,y):
    #TODO
    # For widgets
    _signal(f"setpos {id} {x},{y}")

def manage_callbacks():
    try:
        f = open(ex_path,"r+")
    except: return
    contents = f.read()
    f.seek(0)
    f.truncate()
    contents = contents.split("\n")
    for func in contents:
        if func != "":
            _func, args = func.split(":")
            func_len = len(inspect.signature(Callback.listall()[_func]["callback"]).parameters)
            def thrd(_func,args):
                if len(args) > 0 and func_len > 0:
                    args = args.split(",")
                    Callback._debug_trigger(_func,*args)
                elif func_len > 0:
                    args = [None for _ in range(func_len)]
                    Callback._debug_trigger(_func,*args)
                else:
                    Callback._debug_trigger(_func)
            if Callback.listall()[_func]["callback"]:
                Thread(target=thrd,args=(_func,args),daemon=True).start()
            else:
                thrd(_func,args)
    contents = None
    f.close()
