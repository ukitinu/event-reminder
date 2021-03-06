import tkinter as tk
from tkinter import ttk
from typing import Set

from eventreminder.event import Event

BG_COLOUR = '#333333'
BG_COLOUR_ALT = '#444444'
WINDOW = tk.Tk()
WINDOW.geometry('+100+100')
WINDOW.config(bg=BG_COLOUR)
WINDOW.resizable(False, False)


def open_window(title: str, entries: Set[Event]):
    WINDOW.title(title)
    current_background = BG_COLOUR
    i = 1
    for entry in entries:
        current_background = BG_COLOUR_ALT if current_background == BG_COLOUR else BG_COLOUR
        text = ttk.Label(WINDOW,
                         text=f' {entry.to_text()}',
                         background=current_background,
                         foreground='white',
                         font=('Arial', 16))
        text.place()
        text.pack(ipady=5, ipadx=5, fill='both')
        i = i + 1

    WINDOW.mainloop()
