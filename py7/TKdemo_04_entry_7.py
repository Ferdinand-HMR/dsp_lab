# Tk entry demo: Adds two entered numbers, shows result in a label.
# Uses a Tk variable.

import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

def fun1():
    c = float(E1.get()) + float(E2.get())
    s.set(str(c))

top = Tk.Tk()

# Define Tk variable
s = Tk.StringVar()

# Define widgets
L1 = Tk.Label(top, text = 'Enter two numbers')
E1 = Tk.Entry(top)
E2 = Tk.Entry(top) 
B1 = Tk.Button(top, text = 'Add', command = fun1)
L2 = Tk.Label(top, textvariable = s)
B2 = Tk.Button(top, text = 'Quit', command = top.quit)

# Place widgets
L1.pack()
E1.pack()
E2.pack()
B1.pack()
L2.pack()
B2.pack()

top.mainloop()
