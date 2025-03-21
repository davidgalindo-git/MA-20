# C:\Users\pq87nkq\OneDrive - Education Vaud\Exercises\MA-20\2048\main.py
# -*- coding: utf-8 -*-

#--------1---------2---------3---------4---------5---------6---------7---------8
#2345678901234567890123456789012345678901234567890123456789012345678901234567890
"""
Nom : main.py
Auteur : David Galindo
Date : 18.03.2025
Version : 0.0.7
Purpose : Implémentation des fonctionnalités complémentaires
Fonctionnalités complémentaires: Enregistrement et chargement des parties,
meilleur score, afficher un timer, afficher le score et nouveau jeu.
"""
from datetime import datetime
from tkinter import *
import tkinter.font
from tkinter import messagebox, filedialog
import random
import os
import json

# 2 dimensions list with data, new game
numbers= [[1024, 1024, 0, 0],
        [0, 512, 512, 1024],
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

# Win verifier
win_flag=False

# Lose verifier
lose_flag=False

x0=25 # horizontal beginning of labels
y0=190 # vertical beginning of labels
width=130 # horizontal distance between labels
height=130 # vertical distance between labels

# Windows creation
win = Tk()
win.geometry("600x830")
win.title('2048')
win.configure(bg='#EE99FF')

# Title
Label(win, text="2048", font=("Arial", 45),bg='#EE99FF',fg="#FFFFFF").place(x=220, y=80)

# High Score
high_score_label = Label(win, text=f'HIGH SCORE\n',font=("Arial", 20), bg='#2B78E4',fg="#FFFFFF",borderwidth=1,relief="solid")
high_score_label.place(x=25, y=80)

# Score
score_label = Label(win, text=f'SCORE\n{score}', width=10, font=("Arial", 20), bg='#EEEEEE',borderwidth=1,relief="solid")
score_label.place(x=380, y=80)

# Timer
timer_label = Label(win, text=f'0 : 0', width=10, font=("Arial", 20), bg='#EEEEEE',borderwidth=1,relief="solid")
timer_label.place(x=380, y=10)

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
    high_score_label.config(text=f'HIGH SCORE\n{get_high_score()}')

# start timer from then add a second every second
def start_timer(seconds=0, minutes=0):
    global timer
    if not lose_flag:
        timer_label.config(text=f'{minutes} : {seconds}')
        seconds += 1
        if seconds == 60:
            minutes += 1
            seconds = 0
        timer = win.after(1000, start_timer, seconds, minutes)    # chatgpt replaced my sleep.time() with win.after

#stop current timer
def stop_timer():
    win.after_cancel(timer) # chatgpt gave me the after_cancel(timer) function

# stop current timer and start new timer
def reset_timer():
    stop_timer()
    start_timer()

# add current score earned to total score
def refresh_score():
    global score
    score_label.config(text=f'SCORE\n{score}')

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
    global lose_flag
    empty_positions = nb_empty_tiles()
    if not empty_positions:
        lose_flag = no_merge_possible()
        if lose_flag:
            game_over_message = messagebox.askquestion("Game Over", "Do you want to play again?")
            if game_over_message == 'yes':
                new_game()
            else:
                save_score()
                quit()

# restart game to an initial situation
def new_game():
    global win_flag
    global lose_flag
    global score
    save_score()
    win_flag = False
    lose_flag = False
    score = 0
    score_label.config(text=score)
    for line in range(len(numbers)):
        for col in range(len(numbers[line])):
            numbers[line][col]=random.choices([0, 2, 4], weights=[0.8625,0.125,0.0125])[0] # Set random numbers between 0, 2 and 4

    non_zero_count = sum(1 for row in numbers for num in row if num!=0) # Count non empty cases
    if non_zero_count < 2 or non_zero_count > 3: # Minimum 2 numbers, maximum 3 numbers
        new_game()
    reset_timer()
    displayGame(colors, numbers)

# Save score to local history file
def save_score():
    global score
    high_score = int(get_high_score())
    score_datetime = datetime.now().strftime("%d:%m:%Y-%H:%M:%S") # chatgpt: Time str format
    time_str = timer_label.cget("text")  # chatgpt: Gets text from timer label, "minutes : seconds", as str
    minutes, seconds = map(int, time_str.split(" : ")) # chatgpt: Separates minutes from seconds with their corresponding values
    score_time = f'{minutes}:{seconds}'

    # Append date, score and score time in score history file
    f = open("score_history.txt", "a")
    f.write(f'DATE : {score_datetime} / SCORE : {score} / TIME : {score_time}\n')
    if score > high_score:
        f = open("high_score.txt","w")
        f.write(f'{score}')
        f.close()

def get_high_score():
    f = open("high_score.txt","r")
    old_high_score = int(f.read())
    if old_high_score > score:
        return old_high_score
    else:
        return score

# Save game (numbers, score and time) to local directory "games" as a JSON file
def save_game(): # avec chatgpt
    game_datetime = datetime.now().strftime("%d.%m.%Y-%H.%M.%S") # Time str format
    file_path = os.path.join("games", f'2048_game_{game_datetime}.json')  # Use JSON format
    time_str = timer_label.cget("text")  # Gets text from timer label, "minutes : seconds", as str
    minutes, seconds = map(int, time_str.split(" : ")) # Separates minutes from seconds with their corresponding values

    # Write data with JSON format
    game_data = {
        "numbers": numbers,
        "score": score,
        "minutes": minutes,
        "seconds": seconds
    }

    with open(file_path, "w") as f:
        json.dump(game_data, f)  # Adds python dictionary converted as JSON

# Load game (numbers, score and time) from local "games" directory
def load_game(): # avec chatgpt
    """Open a file explorer to choose a game file from the .\games directory."""
    root = Tk()
    root.withdraw()  # Hide the main window
    root.attributes('-topmost', True)  # Bring the dialog to the front
    game_dir = os.path.join(os.getcwd(), "games")  # Define the games directory
    file_path = filedialog.askopenfilename(initialdir=game_dir, title="Select a Game File",
                                           filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
    # Get JSON data
    if file_path:
        with open(file_path, "r") as f:
            game_data = json.load(f)

        global numbers, score
        numbers = game_data["numbers"]
        score = game_data["score"]
        minutes = game_data["minutes"]
        seconds = game_data["seconds"]

        # Update UI elements
        displayGame(colors, numbers)
        refresh_score()
        stop_timer()
        start_timer(seconds=seconds, minutes=minutes)  # Restart timer at saved time

    return file_path if file_path else None  # Return the chosen file path or None if canceled

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
    global score
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
        score+=a
        b=c
        c=d
        d=0
        nm+=1
    if b==c and b>0:
        b=2*b
        score+=b
        c=d
        d=0
        nm+=1
    if c==d and c>0:
        c=2*c
        score+=c
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
    refresh_score()
    displayGame(colors, numbers)
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
    refresh_score()
    displayGame(colors, numbers)
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
    refresh_score()
    displayGame(colors, numbers)
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
    refresh_score()
    displayGame(colors, numbers)
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

# "SAVE GAME" button
save_game_button = Button(win, text="SAVE GAME", width=10, height=1, font=("Arial", 20), command=save_game)
save_game_button.place(x=100, y=750)

# "LOAD GAME" button
load_game_button = Button(win, text="LOAD GAME", width=10, height=1, font=("Arial", 20), command=load_game )
load_game_button.place(x=300, y=750)

start_timer()
win.bind('<Key>', key_pressed) # keyboard event treatment
displayGame(colors, numbers)
win.mainloop()
