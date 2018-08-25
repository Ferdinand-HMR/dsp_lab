import sys

if sys.version_info[0] < 3:
	import Tkinter as Tk 	# for Python 2
else:
	import tkinter as Tk

top = Tk.Tk()

s1 = Tk.StringVar()
s1.set('Press the button after you entered something')


def fun1(event):
    print('You clicked at position %d %d' % (event.x, event.y))

def fun2(event):
    print('You pressed key %s' % repr(event.char))

def fun3():
	print('Hello World')

def fun4():
    print('You have just entered %s ' %E1.get() )
    # print 4
S1 = Tk.Scale(top)

l0 = Tk.Label(top,text = 'You can click your mouse in the following blank area')

text1 = Tk.StringVar()

F1 = Tk.Frame(top, width = 400, height = 200)
F1.bind("<Button-1>", fun1)		# "<Button-1>" refers to the mouse
F1.bind("<Key>", fun2)			# "<Key>" refers to the keyboard
l0.pack()
F1.pack()
F1.focus_set()


var = Tk.IntVar()

c = Tk.Checkbutton(top, text="Don't show this again", variable=var)
c.var = var
# c = Tk.CHECKBUTTON(top, text="Color image", variable=var, onvalue="RGB", offvalue="L")



E1 = Tk.Entry(top)

B1 = Tk.Button(top, text = 'Press me', command = fun4)

L1 = Tk.Label(top, textvariable = s1)

L1.pack()

E1.pack()

B1.pack()

c.pack()

# Place slider
S1.pack(side = Tk.RIGHT)

listbox = Tk.Listbox(top)
# listbox.pack()

listbox.insert(1, "Python")
listbox.insert(2, "Perl")
listbox.insert(3, "C")
listbox.insert(4, "PHP")
listbox.insert(5, "JSP")
listbox.insert(6, "Ruby")

listbox.pack()

# listbox.insert(end,"a list entry")
#
# for item in ["one", "two", "three", "four"]:
#     listbox.insert(end, item)



top.mainloop()





# master = Tk()
#
# listbox = Tk.Listbox(top)
# listbox.pack()
#
# listbox.insert(END, "a list entry")
#
# for item in ["one", "two", "three", "four"]:
#     listbox.insert(END, item)



# def fun1(event):
#     print('You clicked at position %d %d' % (event.x, event.y))
#
# def fun2(event):
#     print('You pressed key %s' % repr(event.char))
#
# F1 = Tk.Frame(root, width = 200, height = 100)
# F1.bind("<Button-1>", fun1)		# "<Button-1>" refers to the mouse
# F1.bind("<Key>", fun2)			# "<Key>" refers to the keyboard
# F1.pack()
# F1.focus_set()
#
# root.mainloop()

