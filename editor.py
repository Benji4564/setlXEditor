from pydoc import text
from tkinter import *
import tkinter as tk
from turtle import bgcolor
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

def bracket():
   #get the cursor position
    cursor = t.index(INSERT)
    
    print(cursor)
    if t.get(INSERT + "-1c") == "(":
        #highlight the bracket
        t.tag_add("highlight", INSERT + "-1c", INSERT)
        t.tag_config("highlight", background="yellow")
        #find the closing bracket and highlight it

def find_matching_parens(s, braces=None):
    openers = braces or {"(": ")"}
    closers = {v: k for k, v in openers.items()}
    stack = []
    result = []

    for i, c in enumerate(s):
        if c in openers:
            stack.append([c, i])
            print(stack)
        
        elif c in closers:
            if not stack:
                raise ValueError(f"tried to close brace without an open at position {i}")

            pair, idx = stack.pop()
            result.append([idx, i])

            if pair != closers[c]:
                raise ValueError(f"mismatched brace at position {i}")
    
    if stack:
        raise ValueError(f"no closing brace at position {i}")

    return result




def test():
    #get text at position
    print(t.index("end-1c").split(".")[0])
    for i in range(int(t.index("end-1c").split(".")[0])):
        print(t.count(str(i+1) + ".0 linestart", str(i+1) + ".0 lineend"))
    #print(t.count("4.0 linestart", "4.0 lineend"))    


def Keyboardpress( key):
    key_char = key.char
    #print(key)
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

def mouse():
    bracket()


screen = Tk()
screen["bg"] = "black"
textVar = StringVar()
screen.title("SetlX editor")
screen.geometry("900x600")
label_header = Label(screen, text="SetlX editor", font=("Arial", 15), bg="black", fg="white")
label_header.grid(row=0, columnspan=3)

t = tk.Text(screen, height=15, width=100, font=("Arial", 13), bg="#202020", fg="white")
t.grid(row=1, column=0)
frame = tk.Frame(screen)
frame.grid(row=2, column=0)
start = Button(frame, text="Execute setlX", command=execute, bg="#202020", fg="white")
start.grid(row=2)
save = Button(frame, text="Save", command=save, bg="#202020", fg="white")
save.grid(row=2, column=1)
output=Text(screen, height=15, width=100, bg="#202020", fg="white")
screen.bind( '<Key>', lambda i : Keyboardpress(i))
#screen.bind( '<Button-1>', lambda i : mouse())
output.bind()
output.insert(END, "Output here")
output.grid(row=3, column=0)

cdg = ic.ColorDelegator()
cdg.prog = re.compile(r'\b(?P<BOOL>true|false)\b|\b(?P<FUNCTION>procedure)\b|' + ic.make_pat(), re.S)
cdg.idprog = re.compile(r'\s+(\w+)', re.S)


BACKGROUND = '#141414'

cdg.tagdefs['BOOL'] = {'foreground': '#311bf5', 'background': BACKGROUND}
cdg.tagdefs['FUNCTION'] = {'foreground': '#f5f207', 'background': BACKGROUND}
cdg.tagdefs['COMMENT'] = {'foreground': '#FF0000', 'background': BACKGROUND}
cdg.tagdefs['KEYWORD'] = {'foreground': '#d41fc3', 'background': BACKGROUND}
cdg.tagdefs['BUILTIN'] = {'foreground': '#f5f207', 'background': BACKGROUND}
cdg.tagdefs['STRING'] = {'foreground': '#d49430', 'background': BACKGROUND}
cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': BACKGROUND}

ip.Percolator(t).insertfilter(cdg)

with open("editor.txt", "r") as f:
    t.insert(tk.END, f.read())


test()
print(find_matching_parens(t.get("1.0", "end")))

screen.mainloop()