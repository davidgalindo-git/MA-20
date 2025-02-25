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
from operator import length_hint
from tkinter import *
import tkinter.font
from tkinter import messagebox
import random

# 2 dimensions list with data, new game
numbers= [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]

# color code
colors={
    0: "#EEEEEE",
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

# Score
score = 0

# Total movements per event
tot_move = 0

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
score_label = Label(win, text=f'SCORE\n{score}', width=10, font=("Arial", 20), bg='#EEEEEE',borderwidth=1,relief="solid")
score_label.place(x=380, y=80)


# labels creation and position
for line in range(len(numbers)):
    for col in range(len(numbers[line])):
        # creation without placement
        labels[line][col] = Label (win,text =numbers[line][col], width=6, height=3, borderwidth=1, relief="solid", font=("Arial", 28), bg="#FFFF00", fg="#FFFFFF")
        # label positionning in the windows
        labels[line][col].place(x=x0 + width * col, y=y0 + height * line)

# refresh game display
def displayGame(colors, numbers):
    for line in range(len(numbers)):
        for col in range(len(numbers[line])):
            number = numbers[line][col] # Get current number
            display_number = "" if number == 0 else number # Turn 0 into empty string
            color = colors.get(number, None)    # Get number color
            labels[line][col].config(bg=color,text =display_number)  # Modifier la couleur background et remettre les nombres

# add current score earned to total score
def add_score(tot_move,score):
    score+=tot_move
    score_label.config(text=score)

# restart game to an initial situation
def new_game():
    for line in range(len(numbers)):
        for col in range(len(numbers[line])):
            numbers[line][col]=random.choices([0, 2, 4], weights=[0.8625,0.125,0.0125])[0] # Set random numbers between 0, 2 and 4

    non_zero_count = sum(1 for row in numbers for num in row if num!=0) # Compter combien de nombres non nuls y a-t-il
    if non_zero_count < 2 or non_zero_count > 3: # Minimum 2 nombres, maximum 3 nombres
        new_game()
    displayGame(colors, numbers)

# add 2 or 4 randomly into one empty case
def add_number():
    non_zero_count_before = sum(1 for row in numbers for num in row if num != 0)  # Compter combien de nombres non nuls y a-t-il
    non_zero_count_after = 0
    for line in range(len(numbers)):
        for col in range(len(numbers[line])):
            if numbers[line][col] == 0 and (non_zero_count_after - non_zero_count_before) < 1:
                numbers[line][col]=random.choices([0, 2, 4], weights=[0.8625,0.125,0.0125])[0] # Set random numbers between 0, 2 and 4
                non_zero_count_after = sum(1 for row in numbers for num in row if num != 0)
    if (non_zero_count_after - non_zero_count_before) < 1:
        add_number()
    displayGame(colors, numbers)

# finish game when loss conditions are met
def game_over():
    non_zero_count=0
    for line in range(len(numbers)):            # Count numbers if they're different from each other
        for col in range(len(numbers[line])):
            if numbers[line][col]!= numbers[line+1][col]\
            or numbers[line][col]!= numbers[line][col+1]\
            or numbers[line][col]!= numbers[line-1][col]\
            or numbers[line][col]!= numbers[line][col-1]:
                non_zero_count +=1
    if non_zero_count == 16:
        game_over_message = messagebox.askquestion("Game Over", "Do you want to play again?")
        if game_over_message:
            new_game()

# merges 4 cases and counts the number of movements done
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

# Player movement: merge down
def move_down(tot_move):
    for col in range(len(numbers)):
        # arrange numbers to match pack4's order [a,b,c,d,nm] and direction (merge left)
        [numbers[3][col],numbers[2][col],numbers[1][col],numbers[0][col],nmove]=pack4(numbers[3][col],numbers[2][col],numbers[1][col],numbers[0][col])
        tot_move+=nmove
    add_number()
    displayGame(colors, numbers)
    add_score(tot_move,score)
    game_over()

# Player movement: merge up
def move_up(tot_move):
    for col in range(len(numbers)):
        # arrange numbers to match pack4's order [a,b,c,d,nm] and direction (merge left)
        [numbers[0][col],numbers[1][col],numbers[2][col],numbers[3][col],nmove]=pack4(numbers[0][col],numbers[1][col],numbers[2][col],numbers[3][col])
        tot_move+=nmove
    add_number()
    displayGame(colors, numbers)
    add_score(tot_move, score)
    game_over()

# Player movement: merge right
def move_right(tot_move):
    for line in range(len(numbers)):
        # arrange numbers to match pack4's order [a,b,c,d,nm] and direction (merge left)
        [numbers[line][3],numbers[line][2],numbers[line][1],numbers[line][0],nmove]=pack4(numbers[line][3],numbers[line][2],numbers[line][1],numbers[line][0])
        tot_move+=nmove
    add_number()
    displayGame(colors, numbers)
    add_score(tot_move, score)
    game_over()

# Player movement: merge left
def move_left(tot_move):
    for line in range(len(numbers)):
        # arrange numbers to match pack4's order [a,b,c,d,nm] and direction (merge left)
        [numbers[line][0],numbers[line][1],numbers[line][2],numbers[line][3],nmove]=pack4(numbers[line][0],numbers[line][1],numbers[line][2],numbers[line][3])
        tot_move+=nmove
    add_number()
    displayGame(colors, numbers)
    add_score(tot_move, score)
    game_over()

# Player event: key pressed
def key_pressed(event) :
    key=event.keysym # Get key symbole
    if (key=="Right" or key=="d" or key=="D"):
        move_right(tot_move)
    if (key=="Left" or key=="a" or key=="A"):
        move_left(tot_move)
    if (key=="Up" or key=="w" or key=="W"):
        move_up(tot_move)
    if (key=="Down" or key=="s" or key=="S"):
        move_down(tot_move)
    if (key=="Q" or key=="q"):
        result=messagebox.askokcancel("Confirmation", "vraiment quitter ?")
        if result:
            quit()

# "NEW" button
new_game_button = Button(win, text="NEW", width=8, height=1, font=("Arial", 20), command=new_game)
new_game_button = new_game_button.place(x=220, y=10)

new_game()
add_score(tot_move,score)
win.bind('<Key>', key_pressed) # keyboard event treatment
displayGame(colors, numbers)
win.mainloop()
