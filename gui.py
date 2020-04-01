#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 17:00:12 2020

@author: CritterWilson
"""
import os
import imutils
import time
import numpy as np
import webbrowser as wb
from imutils.video import VideoStream
from imutils.video import FPS
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

# Closes the window on "Quit" button press
def quit():
    global window
    window.quit()

# Decides which stream file (youtube or local) to run
def run(url, filepath):
    if (url != ""):
        youtubeStream(url)
    elif (filepath != ""):
        fileStream(filepath)
    else:
        messagebox.showerror("Error!", "Both video sources are empty.\nFill one out and try again.")

# Calls our ML file using a youtube stream
def youtubeStream(url):
	fileCall = 'python stream_youtube.py {}'.format(url)
	result = os.system(fileCall)
	if result != 0:
		messagebox.showerror("URL Error", "Oops! There was an error in your Youtube URL. Double check your URL and try again.\n\nYour URL: {}".format(url))

# Calls our ML file using a local stream
def fileStream(filepath):
    fileCall = 'python stream_local.py {}'.format(filepath)
    result = os.system(fileCall)
    if result != 0:
        messagebox.showerror("Filepath Error", "Oops! There was an error in your Filepath. Double check it and try again.\n\nYour filepath: {}".format(filepath))

# Allows the user to "Select" a local file
def browse_button():
    global folder_path
    filename = filedialog.askopenfilename()
    filename = os.path.relpath(filename)
    filename = filename.replace(" ", "\\ ")
    filepathDispaly.set(filename)
    print(filename)

# Opens the README.md of our github
def open_help():
    helpUrl = "https://github.com/critterwilson/Senior-Project/blob/master/README.md"
    wb.open(helpUrl)

window = Tk()

# LabelFrame for youtube URL entry
urlGroup = LabelFrame(window, text="Youtube URL", padx=5, pady=5)
urlGroup.pack(padx=10, pady=10)
urlEntry = Entry(urlGroup, width=25)
urlEntry.pack(side=LEFT)

# LabelFrame for File entry
fileGroup = LabelFrame(window, text="File", padx=5, pady=5)
fileGroup.pack(padx=10, pady=10)
filepathDispaly = StringVar()
fileEntry = Entry(fileGroup, textvariable=filepathDispaly, width=20, 
                    state="disabled", cursor="arrow")
fileEntry.pack(side=LEFT)
Button(fileGroup, text="Select", command=lambda : browse_button()).pack(side=LEFT)

# Run and Quit Buttons
Button(window, text="Quit", command=quit).pack(side=LEFT, padx=10, pady=10)
Button(window, text="Run", command=lambda : run(urlEntry.get(), fileEntry.get())).pack(side=RIGHT, padx=10, pady=10)
Button(window, text="Help", command=open_help).pack(side=RIGHT, padx=10, pady=10)

window.title("Bar-Down Hockey Player Detector")

window.mainloop()