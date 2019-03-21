from shutil import *
import os
import datetime
from subprocess import call
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

CANON_RAW_FE = ".CR2"
JPEG_FE = ".JPG"
MP4_FE = ".MP4"
MOV_FE = ".MOV"


class CameraImport(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.notDuplicates = []
        self.viableDates = []
        self.checklist = []

        print("INITIATED, YEYUH")


if __name__ == "__main__":
    root = tk.Tk()
    CameraImport(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
