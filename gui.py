#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 17:00:12 2020

@author: CritterWilson
"""
import os
import pafy
import cv2
import imutils
import time
import numpy as np
import webbrowser as wb
from imutils.video import VideoStream
from imutils.video import FPS
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


WIDTH = 300
HEIGHT = (2/3) * WIDTH

# Closes the window on "quit" button press
def quit():
    global window
    window.quit()

def run(url, filepath):
    if (url != ""):
        youtubeStream(url)
    elif (filepath != ""):
        fileStream(filepath)
    else:
        messagebox.showerror("Error!", "Both video sources are empty. Fill one out and try again.")

# Calls our ML file using a youtube stream
def youtubeStream(url):
	fileCall = 'python stream_youtube.py {}'.format(url)
	result = os.system(fileCall)
	if result != 0:
		messagebox.showerror("URL Error", "Oops! There was an error in your Youtube URL. Double check your URL and try again.\n\nYour URL: {}".format(url))

def browse_button():
    global folder_path
    filename = filedialog.askopenfilename()
    filePath.set(filename)
    print(filename)

window = Tk()

# LabelFrame for youtube URL entry
urlGroup = LabelFrame(window, text="Youtube URL", padx=5, pady=5)
urlGroup.pack(padx=10, pady=10)
urlEntry = Entry(urlGroup, width=25)
urlEntry.pack(side=LEFT)

# LabelFrame for File entry
fileGroup = LabelFrame(window, text="File", padx=5, pady=5)
fileGroup.pack(padx=10, pady=10)
filePath = StringVar()
fileEntry = Entry(fileGroup, textvariable=filePath, width=20, 
                    state="disabled", cursor="arrow")
Button(fileGroup, text="?", command=)
fileEntry.pack(side=LEFT)
Button(fileGroup, text="Select", command=lambda : browse_button()).pack(side=LEFT)

# Run and Quit Buttons
Button(window, text="Quit", command=quit).pack(side=LEFT, padx=10, pady=10)
Button(window, text="Run", command=lambda : run(urlEntry.get(), fileEntry.get())).pack(side=RIGHT, padx=10, pady=10)

window.mainloop()