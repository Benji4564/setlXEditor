from pydoc import text
from tkinter import *
import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox
import subprocess
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re

def execute():
    text  = t.get("1.0", "end-1c")

    with open("editor.txt", "w") as f:
        f.write(text)
    out = subprocess.Popen("setlx editor.txt", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE).stdout.read()
    error = subprocess.Popen("setlx editor.txt", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE).stderr.read()
    output.delete("1.0", END)
    output.insert(END, out)
    output.insert(END, error)

def Keyboardpress( key):
    key_char = key.char
    if key_char == "{":
       t.insert(INSERT, "}")
       t.mark_set(INSERT, INSERT + "-1c")
    elif key_char == "(":
        t.insert(INSERT, ")")
        t.mark_set(INSERT, INSERT + "-1c")
    elif key_char == "[":
        t.insert(INSERT, "]")
        t.mark_set(INSERT, INSERT + "-1c")
    elif key_char == '"':
        t.insert(INSERT, '"')
        t.mark_set(INSERT, INSERT + "-1c")
    elif key_char == "'":
        t.insert(INSERT, "'")
        t.mark_set(INSERT, INSERT + "-1c")


def save():
    text  = t.get("1.0", "end-1c")

    with open("editor.txt", "w") as f:
        f.write(text)


screen = Tk()
textVar = StringVar()
screen.title("SetlX editor")
screen.geometry("900x600")
label_header = Label(screen, text="SetlX editor", font=("Arial", 15))
label_header.grid(row=0, columnspan=3)

t = tk.Text(screen, height=15, width=100, font=("Arial", 12))
t.grid(row=1, column=0)
frame = tk.Frame(screen)
frame.grid(row=2, column=0)
start = Button(frame, text="Execute setlX", command=execute)
start.grid(row=2)
save = Button(frame, text="Save", command=save)
save.grid(row=2, column=1)
output=Text(screen, height=20, width=100)
screen.bind( '<Key>', lambda i : Keyboardpress(i))
output.bind()
output.insert(END, "Output here")
output.grid(row=3, column=0)

cdg = ic.ColorDelegator()
cdg.prog = re.compile(r'\b(?P<BOOL>true|false)\b|\b(?P<FUNCTION>procedure)\b|' + ic.make_pat(), re.S)
cdg.idprog = re.compile(r'\s+(\w+)', re.S)


BACKGROUND = '#FFFFFF'

cdg.tagdefs['BOOL'] = {'foreground': '#311bf5', 'background': '#FFFFFF'}
cdg.tagdefs['FUNCTION'] = {'foreground': '#f5f207', 'background': '#FFFFFF'}
cdg.tagdefs['COMMENT'] = {'foreground': '#FF0000', 'background': BACKGROUND}
cdg.tagdefs['KEYWORD'] = {'foreground': '#d41fc3', 'background': BACKGROUND}
cdg.tagdefs['BUILTIN'] = {'foreground': '#f5f207', 'background': BACKGROUND}
cdg.tagdefs['STRING'] = {'foreground': '#d49430', 'background': BACKGROUND}
cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': BACKGROUND}

ip.Percolator(t).insertfilter(cdg)

with open("editor.txt", "r") as f:
    t.insert(tk.END, f.read())



screen.mainloop()