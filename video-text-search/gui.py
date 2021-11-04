import tkinter as tk
from tkinter import  filedialog
from tkinter.ttk import *
import Main as M
PATH = ""



def main():
    window = tk.Tk()
    window.columnconfigure(0, minsize=250)
    window.rowconfigure([0, 1], minsize=100)
    frame1 = tk.Frame(master=window, width=200, height=100, bg="red")
    frame1.grid(row=0, column=0)
    frame2 = tk.Frame(master=window, width=100, bg="yellow")
    frame2.grid(row=1,column=0)
    entry = tk.Entry(master=frame2)
    button = tk.Button(frame1, text="Choose Video", default="active", command=fdiag, pady=10)
    print("starting work on video :" + PATH)
    text_to_search = entry.get()

    button.pack()
    entry.pack()
    window.mainloop()

def fdiag():
    PATH = filedialog.askopenfilename()

main()
