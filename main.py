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
numbers= [[1024, 1024, 0, 0],
        [0, 512, 512, 1024],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]
win_flag=False

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
            labels[line][col].config(bg=color,text =display_number)  # Modify background color and refresh numbers list
    check_2048()

# add current score earned to total score
def add_score(tot_move,score):
    score+=tot_move
    score_label.config(text=score)
    pass

# restart game to an initial situation
def new_game():
    for line in range(len(numbers)):
        for col in range(len(numbers[line])):
            numbers[line][col]=random.choices([0, 2, 4], weights=[0.8625,0.125,0.0125])[0] # Set random numbers between 0, 2 and 4

    non_zero_count = sum(1 for row in numbers for num in row if num!=0) # Count non empty cases
    if non_zero_count < 2 or non_zero_count > 3: # Minimum 2 numbers, maximum 3 numbers
        new_game()
    displayGame(colors, numbers)
    pass

# add 2 or 4 randomly into one empty case
def add_number():
    empty_positions = nb_empty_tiles()
    if empty_positions:
        line, col = random.choice(empty_positions)
        numbers[line][col] = random.choices([2, 4], weights=[0.8,0.2])[0]
        displayGame(colors, numbers)
    else:
        return

# check if win condition is met : 2048 tile
def check_2048():
    global win_flag
    winning_case = False
    for line in range(len(numbers)):
        for col in range(len(numbers[line])):
            if numbers[line][col] == 2048:
                winning_case=True
    if winning_case == True and win_flag == False:
        win_flag = True
        messagebox.showinfo("Winner","You won!")

# finish game when loss conditions are met
def game_over():
    empty_positions = nb_empty_tiles()
    if not empty_positions:
        lose_flag = no_merge_possible()
        if lose_flag == True:
            game_over_message = messagebox.askquestion("Game Over", "Do you want to play again?")
            if game_over_message == 'yes':
                new_game()
            else:
                quit()

# create list of empty tiles
def nb_empty_tiles():
    # list of empty positions
    empty_positions = []
    for line in range(len(numbers)):
        for col in range(len(numbers[line])):
            if numbers[line][col] == 0:
                empty_positions.append([line, col])
    return empty_positions

# verify if there are merges available
def no_merge_possible():
    for row in range(4):
        for col in range(4):  # Verify if a tile can merge with an adjacent tile
            if col < 3 and numbers[row][col] == numbers[row][col + 1]:  # Verify adjacent tiles to the right
                return False
            if row < 3 and numbers[row][col] == numbers[row + 1][col]:  # Verify adjacent tiles below
                return False
    return True

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
def move_down():
    # total moves after merge
    tot_move=0
    for col in range(len(numbers)):
        # arrange numbers to match pack4's order [a,b,c,d,nm] and direction (merge left)
        [numbers[3][col],numbers[2][col],numbers[1][col],numbers[0][col],nmove]=pack4(numbers[3][col],numbers[2][col],numbers[1][col],numbers[0][col])
        tot_move+=nmove
    # add random number if there are 1 or more moves after event
    if tot_move>0:
        add_number()
    displayGame(colors, numbers)
    add_score(tot_move,score)
    game_over()

# Player movement: merge up
def move_up():
    # total moves after merge
    tot_move = 0
    for col in range(len(numbers)):
        # arrange numbers to match pack4's order [a,b,c,d,nm] and direction (merge left)
        [numbers[0][col],numbers[1][col],numbers[2][col],numbers[3][col],nmove]=pack4(numbers[0][col],numbers[1][col],numbers[2][col],numbers[3][col])
        tot_move+=nmove
    # add random number if there are 1 or more moves after event
    if tot_move > 0:
        add_number()
    displayGame(colors, numbers)
    add_score(tot_move, score)
    game_over()

# Player movement: merge right
def move_right():
    # total moves after merge
    tot_move = 0
    for line in range(len(numbers)):
        # arrange numbers to match pack4's order [a,b,c,d,nm] and direction (merge left)
        [numbers[line][3],numbers[line][2],numbers[line][1],numbers[line][0],nmove]=pack4(numbers[line][3],numbers[line][2],numbers[line][1],numbers[line][0])
        tot_move+=nmove
    # add random number if there are 1 or more moves after event
    if tot_move > 0:
        add_number()
    displayGame(colors, numbers)
    add_score(tot_move, score)
    game_over()

# Player movement: merge left
def move_left():
    # total moves after merge
    tot_move = 0
    for line in range(len(numbers)):
        # arrange numbers to match pack4's order [a,b,c,d,nm] and direction (merge left)
        [numbers[line][0],numbers[line][1],numbers[line][2],numbers[line][3],nmove]=pack4(numbers[line][0],numbers[line][1],numbers[line][2],numbers[line][3])
        tot_move+=nmove
    # add random number if there are 1 or more moves after event
    if tot_move > 0:
        add_number()
    displayGame(colors, numbers)
    add_score(tot_move, score)
    game_over()

# Player event: key pressed
def key_pressed(event) :
    key=event.keysym # Get key symbole
    if (key=="Right" or key=="d" or key=="D"):
        move_right()
    if (key=="Left" or key=="a" or key=="A"):
        move_left()
    if (key=="Up" or key=="w" or key=="W"):
        move_up()
    if (key=="Down" or key=="s" or key=="S"):
        move_down()
    if (key=="Q" or key=="q"):
        result=messagebox.askokcancel("Confirmation", "vraiment quitter ?")
        if result:
            quit()

# "NEW" button
new_game_button = Button(win, text="NEW", width=8, height=1, font=("Arial", 20), command=new_game)
new_game_button = new_game_button.place(x=220, y=10)


#add_score(score)

win.bind('<Key>', key_pressed) # keyboard event treatment
displayGame(colors, numbers)
win.mainloop()
