import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()

def popUpError(Message) -> None:
    messagebox.showinfo('Final Approach', Message)
