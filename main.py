# C:\Users\pq87nkq\OneDrive - Education Vaud\Exercises\MA-20\2048\main.py
# -*- coding: utf-8 -*-

#--------1---------2---------3---------4---------5---------6---------7---------8
#2345678901234567890123456789012345678901234567890123456789012345678901234567890
"""
Nom : main.py
Auteur : David Galindo
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
# 2 dimensions list with data, new game
numbers= [["", "", "", ""],
        ["", "", "", ""],
        ["", 2, "", 2],
        ["", "", "", ""]]
        
"""
# color code
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
y0=190 # vertical beginning of labels
width=130 # horizontal distance between labels
height=130 # vertical distance between labels

# Windows creation
win = Tk()
win.geometry("600x750")
win.title('2048')
win.configure(bg='#EE99FF')

# Title
Label(win, text="2048", font=("Arial", 45),bg='#EE99FF',fg="#FFFFFF").place(x=220, y=80)

# High Score
Label(win, text="HIGH SCORE\n",font=("Arial", 20), bg='#2B78E4',fg="#FFFFFF",borderwidth=1,relief="solid").place(x=25, y=80)

# Score
Label(win, text="SCORE\n", width=10, font=("Arial", 20), bg='#EEEEEE',borderwidth=1,relief="solid").place(x=380, y=80)

# "NEW" button
Button(win, text="NEW", width=8, height=1, font=("Arial", 20)).place(x=220, y=10)

# labels creation and position (1. Creation 2. position)
for line in range(len(numbers)):
    for col in range(len(numbers[line])):
        # creation without placement
        labels[line][col] = Label (win,text =numbers[line][col], width=6, height=3, borderwidth=1, relief="solid", font=("Arial", 28), bg="#FFFF00", fg="#FFFFFF")
        # label positionning in the windows
        labels[line][col].place(x=x0 + width * col, y=y0 + height * line)

def displayGame(colors, numbers):
    for line in range(len(numbers)):
        for col in range(len(numbers[line])):
            number = numbers[line][col]         # Obtenir le nombre actuel
            color = colors.get(number, None)    # Obtenir sa couleur
            labels[line][col].config(bg=color,text =numbers[line][col])  # Modifier la couleur background


def pack4(a,b,c,d):
    nm=0
    if c==0 and d!=0:
        a,b,c,d=a,b,d,0
        nm+=1
    if b==0 and c!=0:
        a,b,c,d=a,c,d,0
        nm+=1
    if a==0 and b!=0:
        a,b,c,d=b,c,d,0
        nm+=1
    if a==b and a>0:
        a = 2*a
        b=c
        c=d
        d=0
        nm+=1
    if b==c and b>0:
        b=2*b
        c=d
        d=0
        nm+=1
    if c==d and c>0:
        c=2*c
        d=0
        nm+=1
    return[a,b,c,d,nm]
print(pack4(2,0,0,0))


displayGame(colors, numbers)
win.mainloop()
