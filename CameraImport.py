from shutil import *
import os
import datetime
from subprocess import call
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk


class CameraImport(tk.Tk):

    def __init__(self, screenName=None, baseName=None, className="CamImport", useTk=1, sync=0, use=None):
        super().__init__(screenName=screenName, baseName=baseName,
                         className=className, useTk=useTk, sync=sync, use=use)


app = CameraImport()
app.mainloop()
