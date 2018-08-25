# Slider demo: Two sliders.
# Their sum and product are displayed in two different labels.

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

def update(event):
	z1 = x.get() + y.get()
	z2 = x.get() * y.get()
	s1.set( 'Sum = ' + str(z1))
	s2.set('Product = ' + str(z2))

top = Tk.Tk()

# Define Tk variables
x = Tk.DoubleVar()
y = Tk.DoubleVar()
s1 = Tk.StringVar()
s2 = Tk.StringVar()

# Define widgets
S1 = Tk.Scale(top, variable = x, command = update)
S2 = Tk.Scale(top, variable = y, command = update)
L1 = Tk.Label(top, textvariable = s1)
L2 = Tk.Label(top, textvariable = s2)
B1 = Tk.Button(top, text = 'Close', command = top.quit)

# Place widgets
S1.pack(side = Tk.LEFT)
S2.pack(side = Tk.LEFT)
L1.pack(side = Tk.TOP)
L2.pack(side = Tk.TOP)
B1.pack(side = Tk.BOTTOM, fill = Tk.X)

top.mainloop()
