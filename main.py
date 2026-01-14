import configparser
import atexit
import os
import sys
import threading
import time
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
from customtkinter import *

app = CTk()
app.iconbitmap("logo.ico")
app.geometry("650x400")
app.minsize(650, 400)
app.maxsize(650, 400)
app.title("CT Auto Clicker")

data = configparser.ConfigParser()
if not os.path.exists('data.ini'):
    data['settings'] = {'mouse': 'left', 'hotkey': 'r', 'interval': '100'}
    data['interface'] = {'theme': 'dark'}
    with open('data.ini', 'w') as f:
        data.write(f)

data.read('data.ini')

mouse = data.get('settings', 'mouse')
hotkey = data.get('settings', 'hotkey')
interval = data.getint('settings', 'interval')
theme = data.get('interface', 'theme')

set_appearance_mode(theme)

clicking = False
mouse_controller = Controller()

def clickloop():
    global clicking
    while True:
        if clicking:
            mouse_controller.click(Button[mouse], 1)
            time.sleep(interval / 1000)
        else:
            time.sleep(0.1)

def onpress(key):
    global clicking
    if isinstance(key, KeyCode) and key.char == hotkey:
        clicking = not clicking

def savedata():
    with open('data.ini', 'w') as dataFile:
        data.write(dataFile)

def updatedata(section, name, value):
    data.set(section, name, str(value))
    savedata()
    restart()

def restart():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def setmouse(option):
    updatedata('settings', 'mouse', option)

def setinterval(option):
    try:
        val = int(option)
        updatedata('settings', 'interval', val)
    except ValueError:
        print("Erreur: L'intervalle doit être un nombre entier")

def settheme(option):
    updatedata('interface', 'theme', option)

title = CTkLabel(master=app, text="CT Auto Clicker", font=("Arial", 20))
title.place(relx=.625, rely=.05, anchor="center")

leftframe = CTkFrame(master=app, width=150, height=400, fg_color="#333")
leftframe.place(relx=-.005, rely=.5, anchor="w")

titleleftframe = CTkLabel(master=leftframe, text="Settings", font=("Arial", 18), text_color="#fff")
titleleftframe.place(relx=.5, rely=.03, anchor="center")

selectmouse = CTkComboBox(master=leftframe, values=["left", "right"], fg_color="#222", text_color="#fff", command=setmouse)
selectmouse.set(mouse)
selectmouse.place(relx=.5, rely=.1, anchor="center")

selecttheme = CTkComboBox(master=leftframe, values=["dark", "light", "system"], fg_color="#222", text_color="#fff", command=settheme)
selecttheme.set(theme)
selecttheme.place(relx=.5, rely=.2, anchor="center")

selectinterval = CTkEntry(master=leftframe, placeholder_text="Click interval...", width=140, fg_color="#222", text_color="#fff")
selectinterval.insert(0, str(interval))
selectinterval.place(relx=.5, rely=.3, anchor="center")

intervalbtn = CTkButton(master=leftframe, text="Set Interval (ms)", corner_radius=32, fg_color="#222", hover_color="#444", command= lambda: setinterval(selectinterval.get()))
intervalbtn.place(relx=.5, rely=.4, anchor="center")

clickthread = threading.Thread(target=clickloop, daemon=True)
clickthread.start()

keyboard_listener = Listener(on_press=onpress)
keyboard_listener.start()

atexit.register(savedata)

app.mainloop()