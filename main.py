# C:\Users\pq87nkq\OneDrive - Education Vaud\Exercises\MA-20\2048\main.py
# -*- coding: utf-8 -*-

#--------1---------2---------3---------4---------5---------6---------7---------8
#2345678901234567890123456789012345678901234567890123456789012345678901234567890
"""
Nom : main.py
Date : 21.01.2025
Version : 0.0.1
Purpose : Afficher le tableau mémoire de la maquette personnalisée du jeu "2048".
"""
from tkinter import *
import tkinter.font

# 2 dimensions list with data
numbers= [[8192, 2048, 512, 16],
        [4096, 1024, 64, 4],
        [256, 128, 4, ""],
        [32, 8, 2, 2]]

"""
# 2 dimensions list with data
numbers= [[2, 4, 8, 16],
        [32, 64, 128, 256],
        [512, 1024, 2048, 4096],
        [8192, "", "", ""]]
        
"""

colors={
    "": "#EEEEEE",
    2: "#FF00CC",
    4: "#E600D9",
    8: "#CC00E6",
    16: "#B300F2",
    32: "#9900FF",
    64: "#8000FF",
    128: "#6600FF",
    256: "#4D00FF",
    512: "#0000FF",
    1024: "#1A00FF",
    2048: "#000099",
    4096: "#000066",
    8192: "#000000",
}

# 2 dimensions list (empty, with labels in the future)
labels=[[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]

x0=25 # horizontal beginning of labels
y0=100 # vertical beginning of labels
width=150 # horizontal distance between labels
height=150 # vertical distance between labels

# Windows creation
win = Tk()
win.geometry("700x750")
win.title('2048')

# Title
label_title = Label(win, text="2048",width=25, height=3, font=("Arial", 28))
label_title.grid(row=0, column=1, padx=10, pady=10)

# High Score
label_high_score = Label(win, text="HIGH SCORE",width=10, height=2, font=("Arial", 20), borderwidth=1)
label_high_score.grid(row=0, column=0, padx=10, pady=10)

# Score
label_score = Label(win, text="SCORE",width=10, height=2, font=("Arial", 20), borderwidth=1)
label_score.grid(row=0, column=2, padx=10, pady=10)


#labels creation and position (1. Creation 2. position)
for line in range(len(numbers)):
    for col in range(len(numbers[line])):
        # creation without placement
        labels[line][col] = Label (win,text =numbers[line][col], width=12, height=6, borderwidth=1, relief="solid", font=("Arial", 15), bg="#FFFF00", fg="#FFFFFF")
        # label positionning in the windows
        labels[line][col].place(x=x0 + width * col, y=y0 + height * line)

def displayGame(colors, numbers):
    for line in range(len(numbers)):
        for col in range(len(numbers[line])):
            number = numbers[line][col]         # Obtenir le nombre actuel
            color = colors.get(number, None)    # Obtenir sa couleur
            labels[line][col].config(bg=color)  # Modifier la couleur background

"""
def fusion():
    numbers= [0, 0, 0, 2]
    for n in range(len(numbers)):
        if n != 0:
            numbers[0]=numbers[n]
        else:
            n+1
    print(numbers)
"""

displayGame(colors, numbers)
win.mainloop()
