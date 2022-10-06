from pydoc import text
from tkinter import *
import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox
import subprocess


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
    #elif key.keysym == "BackSpace":
     #   print(t.get(INSERT + "-1c"))
      #  print(t.get(INSERT))
       # if (t.get(INSERT) == "}" or t.get(INSERT) == ")" or t.get(INSERT) == "]" or t.get(INSERT) == '"' or t.get(INSERT) == "'"):# and (t.get(INSERT) == "{" or t.get(INSERT) == "(" or t.get(INSERT) == "[" or t.get(INSERT) == '"' or t.get(INSERT) == "'") :
        #    t.delete(INSERT)
    elif key.keysym == "Return" and (t.get(INSERT) == "}" or t.get(INSERT) == ")" or t.get(INSERT) == "]"):
        t.insert(INSERT, "  ")
        t.insert(INSERT, "\n")
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

t = tk.Text(screen, height=15, width=100)
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



with open("editor.txt", "r") as f:
    t.insert(tk.END, f.read())



screen.mainloop()