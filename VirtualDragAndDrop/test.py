from tkinter import *
master = Tk()
w = Canvas(master, width=800, height=800)
w.pack()
canvas_height=800
canvas_width=800
y = int(canvas_height / 2)
w.create_line(0, y, canvas_width, y )
mainloop()
