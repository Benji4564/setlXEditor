from pydoc import text
from tkinter import *
import tkinter as tk
from turtle import bgcolor
from ttkwidgets.autocomplete import AutocompleteCombobox
import subprocess
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re


class AutocompleteText(tk.Text):
    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop("autocomplete", None)
        super().__init__(*args, **kwargs)

        # bind on key release, which will happen after tkinter
        # inserts the typed character
        self.bind("<Any-KeyRelease>", self._autocomplete)

        # special handling for tab, which needs to happen on the
        # key _press_
        self.bind("<Tab>", self._handle_tab)

    def _handle_tab(self, event):
        # see if any text has the "autocomplete" tag
        tag_ranges= self.tag_ranges("autocomplete")
        if tag_ranges:
            # move the insertion cursor to the end of
            # the selected text, and then remove the "sel"
            # and "autocomplete" tags
            self.mark_set("insert", tag_ranges[1])
            self.tag_remove("sel", "1.0", "end")
            self.tag_remove("autocomplete", "1.0", "end")

            # prevent the default behavior of inserting a literal tab
            return "break"

    def _autocomplete(self, event):
        if event.char and self.callback:
            # get word preceeding the insertion cursor
            word = self.get("insert-1c wordstart", "insert-1c wordend")

            # pass word to callback to get possible matches
            matches = self.callback(word)
            if matches:
                # autocomplete on the first match
                remainder = matches[0][len(word):]

                # remember the current insertion cursor
                insert = self.index("insert")

                # insert at the insertion cursor the remainder of
                # the matched word, and apply the tag "sel" so that
                # it is selected. Also, add the "autocomplete" text
                # which will make it easier to find later.
                self.insert(insert, remainder, ("sel", "autocomplete"))

                # move the cursor back to the saved position
                self.mark_set("insert", insert)


def get_matches(word):
    # For illustrative purposes, pull possible matches from 
    # what has already been typed. You could just as easily 
    # return a list of pre-defined keywords.
    
    words = t.get("1.0", "end-1c").split()
    words = ["print", "procedure", "if", ":=", "return", "true", "false", "forall", "exsits"]
    matches = [x for x in words if x.startswith(word)]
    return matches






#open the file in the text widget and  executes the code in the setlX interpreter
def execute():
    text  = t.get("1.0", "end-1c")

    with open("editor.txt", "w") as f:
        f.write(text)
    out = subprocess.Popen("setlx editor.txt", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE).stdout.read()
    error = subprocess.Popen("setlx editor.txt", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE).stderr.read()
    output.delete("1.0", END)
    output.insert(END, out)
    output.insert(END, error)


#calculate the position of the brackets and highlight them
def bracketsCalculation():
   #get the cursor position
    t.tag_remove("highlight", "1.0", END)
    
    if t.get(INSERT + "-1c") == "(":
        highlight()
    elif t.get(INSERT + "-1c") == "{":
        highlight(movedIndex=-1)

#highlight the matching brackets in the text widget 
def highlight(movedIndex=0):
    bracket_pairs = find_matching_parens(t.get("1.0", "end-1c"))
    t.tag_add("highlight", INSERT + "-1c", INSERT)
    t.tag_config("highlight", background="#793e6d")
    x, y = t.index(INSERT).split(".")
    letter = 0
    for i in range(int(x)-1):
        letter += int(str(t.count(str(i+1) + ".0 linestart", str(i+1) + ".0 lineend")).replace("(", "").replace(",)", ""))
    letter += int(y) + movedIndex
    for i in bracket_pairs:
        if letter == i[0]:
            t.tag_add("highlight", INSERT + "+" + str(i[1] - i[0] - 1) +"c", INSERT + "+" + str(i[1] - i[0]) +"c")
            t.tag_config("highlight", background="#793e6d")


#find matching brackets in a string and return a list of tuples with the positions of the brackets in the string
def find_matching_parens(s, braces=None):
    openers = braces or {"{": "}", "(": ")", "[": "]"}
    closers = {v: k for k, v in openers.items()}
    stack = []
    result = []

    for i, c in enumerate(s):
        if c in openers:
            stack.append([c, i])
        
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




#adds the autocomplete function to the text widget for brackets
def Keyboardpress( key):
    try:
        bracketsCalculation()
    except:
        pass
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

def mouse():
    bracketsCalculation()


screen = Tk()
screen["bg"] = "black"

textVar = StringVar()
screen.title("SetlX editor")
screen.geometry("900x600")
label_header = Label(screen, text="SetlX editor", font=("Arial", 15), bg="black", fg="white")
label_header.grid(row=0, columnspan=3)

t = AutocompleteText(screen, height=15, width=100, font=("Arial", 13), bg="#202020", fg="white", insertbackground="white", autocomplete= get_matches)
t.grid(row=1, column=0)
frame = tk.Frame(screen)
frame.grid(row=2, column=0)
start = Button(frame, text="Execute setlX", command=execute, bg="#202020", fg="white")
start.grid(row=2)
save = Button(frame, text="Save", command=save, bg="#202020", fg="white")
save.grid(row=2, column=1)
output=Text(screen, height=15, width=100, bg="#202020", fg="white")
screen.bind( '<Key>', lambda i : Keyboardpress(i))
screen.bind( '<Button-1>', lambda i : mouse())
output.bind()
output.insert(END, "Output here")
output.grid(row=3, column=0)

cdg = ic.ColorDelegator()
cdg.prog = re.compile(r'\b(?P<BOOL>true|false)\b|\b(?P<FUNCTION>procedure|forall|exsits)\b|' + ic.make_pat(), re.S)
cdg.idprog = re.compile(r'\s+(\w+)', re.S)


BACKGROUND = '#141414'

cdg.tagdefs['BOOL'] = {'foreground': '#311bf5'}
cdg.tagdefs['FUNCTION'] = {'foreground': '#f5f207'}
cdg.tagdefs['COMMENT'] = {'foreground': '#FF0000'}
cdg.tagdefs['KEYWORD'] = {'foreground': '#d41fc3'}
cdg.tagdefs['BUILTIN'] = {'foreground': '#f5f207'}
cdg.tagdefs['STRING'] = {'foreground': '#d49430'}
cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F'}

ip.Percolator(t).insertfilter(cdg)

with open("editor.txt", "r") as f:
    t.insert(tk.END, f.read())



screen.mainloop()