from tkinter import *

root = Tk()
root.geometry("350x660")  # Made slightly taller for score display
root.title("Tic Tac Toe")
root.resizable(0,0)

# Modern color scheme
BG = "#1a1a2e"
ACCENT = "#f39c12"
TEXT = "#eee"
CELL_BG = "#16213e"
CELL_HOVER = "#0f3460"
X_WIN_COLOR = "#3498db"  # Blue for X wins
O_WIN_COLOR = "#e74c3c"  # Red for O wins
DRAW_COLOR = "#f39c12"   # Orange for draws
GREEN = "#27ae60"

root.configure(bg=BG)

frame1 = Frame(root, bg=BG)
frame1.pack()
titleLabel = Label(frame1, text="Tic Tac Toe", font=("Arial", 26, "bold"), bg=ACCENT, fg="white", width=16)
titleLabel.grid(row=0, column=0)

# Score frame
scoreFrame = Frame(root, bg=BG)
scoreFrame.pack(pady=10)

optionFrame = Frame(root, bg=BG)
optionFrame.pack()

frame2 = Frame(root, bg=BG)
frame2.pack()

board = { 1:" " , 2:" " , 3:" ",
          4:" " , 5:" " , 6:" ",
          7:" " , 8:" " , 9:" " }

turn = "x"
game_end = False
mode = "singlePlayer"

# Score variables
x_score = 0
o_score = 0

def updateScoreDisplay():
    xScoreLabel.config(text=f"X: {x_score}")
    oScoreLabel.config(text=f"O: {o_score}")

def resetScores():
    global x_score, o_score
    x_score = 0
    o_score = 0
    updateScoreDisplay()

def changeModeToSinglePlayer(): 
    global mode 
    mode = "singlePlayer"
    singlePlayerButton["bg"] = GREEN
    singlePlayerButton["fg"] = "white"
    multiPlayerButton["bg"] = CELL_BG
    multiPlayerButton["fg"] = TEXT
    resetScores()  # Auto reset scores when switching modes
    restartGame()  # Auto clear board and reset title when switching modes

def changeModeToMultiplayer():
    global mode 
    mode = "multiPlayer"
    multiPlayerButton["bg"] = GREEN
    multiPlayerButton["fg"] = "white"
    singlePlayerButton["bg"] = CELL_BG
    singlePlayerButton["fg"] = TEXT
    resetScores()  # Auto reset scores when switching modes
    restartGame()  # Auto clear board and reset title when switching modes

def updateBoard():
    for key in board.keys():
        btn = buttons[key-1]
        btn["text"] = board[key]
        if board[key] == "x":
            btn["fg"] = "#3498db"  # blue for X
        elif board[key] == "o":
            btn["fg"] = "#e74c3c"  # red for O
        else:
            btn["fg"] = TEXT

def checkForWin(player):
    # rows
    if board[1] == board[2] and board[2] == board[3] and board[3] == player:
        return True
    elif board[4] == board[5] and board[5] == board[6] and board[6] == player:
        return True
    elif board[7] == board[8] and board[8] == board[9] and board[9] == player:
        return True
    # columns
    elif board[1] == board[4] and board[4] == board[7] and board[7] == player:
        return True
    elif board[2] == board[5] and board[5] == board[8] and board[8] == player:
        return True
    elif board[3] == board[6] and board[6] == board[9] and board[9] == player:
        return True
    # diagonals
    elif board[1] == board[5] and board[5] == board[9] and board[9] == player:
        return True
    elif board[3] == board[5] and board[5] == board[7] and board[7] == player:
        return True
    return False

def checkForDraw():
    for i in board.keys():
        if board[i] == " ":
            return False
    return True

def restartGame():
    global game_end, turn
    game_end = False
    turn = "x"
    for button in buttons:
        button["text"] = " "
        button["fg"] = TEXT
        button["bg"] = CELL_BG  # Reset background color to fix hover issue
    for i in board.keys():
        board[i] = " "
    titleLabel.config(text="Tic Tac Toe", bg=ACCENT, fg="white")

def minimax(board , isMaximizing):
    if checkForWin("o"):
        return 1 
    if checkForWin("x"):
        return -1
    if checkForDraw():
        return 0
    
    if isMaximizing:
        bestScore = -100
        for key in board.keys():
            if board[key] == " ":
                board[key] = "o"
                score = minimax(board , False)
                board[key] = " "
                if score > bestScore : 
                    bestScore = score 
        return bestScore
    else:
        bestScore = 100
        for key in board.keys():
            if board[key] == " ":
                board[key] = "x"
                score = minimax(board , True)
                board[key] = " "
                if score < bestScore : 
                    bestScore = score 
        return bestScore

def playComputer():
    bestScore = -100
    bestMove = 0
    for key in board.keys():
        if board[key] == " ":
            board[key] = "o"
            score = minimax(board , False)
            board[key] = " "
            if score > bestScore : 
                bestScore = score 
                bestMove = key
    if bestMove != 0:
        board[bestMove] = "o"

# Function to play (original logic preserved)
def play(event):
    global turn, game_end, x_score, o_score
    if game_end:
        return
    
    button = event.widget
    buttonText = str(button)
    clicked = buttonText[-1]
    if clicked == "n" :
        clicked = 1
    else :
        clicked = int(clicked)
    
    if button["text"] == " ":
        if turn == "x" :
            board[clicked] = turn
            if checkForWin(turn):
                # Different color for X win
                titleLabel.config(text=f"{turn.upper()} wins the game", bg=X_WIN_COLOR, fg="white")
                x_score += 1
                updateScoreDisplay()
                game_end = True

            turn = "o"
            updateBoard()

            if mode == "singlePlayer":
                playComputer()
                if checkForWin(turn):
                    # Different color for O win
                    titleLabel.config(text=f"{turn.upper()} wins the game", bg=O_WIN_COLOR, fg="white")
                    o_score += 1
                    updateScoreDisplay()
                    game_end = True
                turn = "x"
                updateBoard()
        else:
            board[clicked] = turn
            updateBoard()
            if checkForWin(turn):
                # Different color for O win
                titleLabel.config(text=f"{turn.upper()} wins the game", bg=O_WIN_COLOR, fg="white")
                o_score += 1
                updateScoreDisplay()
                game_end = True
            turn = "x"

        if checkForDraw():
            titleLabel.config(text="Game Draw", bg=DRAW_COLOR, fg="white")

# Hover effects
def on_enter(e):
    if e.widget["text"] == " " and not game_end:
        e.widget["bg"] = CELL_HOVER

def on_leave(e):
    if e.widget["text"] == " ":
        e.widget["bg"] = CELL_BG

# ------ UI --------

# Score display
xScoreLabel = Label(scoreFrame, text="X: 0", font=("Arial", 18, "bold"), 
                   bg="#3498db", fg="white", width=8, relief=RAISED, borderwidth=2)
xScoreLabel.grid(row=0, column=0, padx=10)

vsLabel = Label(scoreFrame, text="VS", font=("Arial", 16, "bold"), 
               bg=BG, fg=TEXT, width=3)
vsLabel.grid(row=0, column=1, padx=5)

oScoreLabel = Label(scoreFrame, text="O: 0", font=("Arial", 18, "bold"), 
                   bg="#e74c3c", fg="white", width=8, relief=RAISED, borderwidth=2)
oScoreLabel.grid(row=0, column=2, padx=10)

resetScoreButton = Button(scoreFrame, text="Reset Scores", font=("Arial", 12, "bold"), 
                         bg="#9b59b6", fg="white", relief=RAISED, borderwidth=2, 
                         command=resetScores)
resetScoreButton.grid(row=1, column=0, columnspan=3, pady=5)

# Mode buttons
singlePlayerButton = Button(optionFrame, text="SinglePlayer", width=13, height=1, 
                           font=("Arial", 15, "bold"), bg=CELL_BG, fg=TEXT, 
                           relief=RAISED, borderwidth=2, command=changeModeToSinglePlayer)
singlePlayerButton.grid(row=0, column=0, columnspan=1, sticky=NW, padx=5)

multiPlayerButton = Button(optionFrame, text="Multiplayer", width=13, height=1, 
                          font=("Arial", 15, "bold"), bg=CELL_BG, fg=TEXT, 
                          relief=RAISED, borderwidth=2, command=changeModeToMultiplayer)
multiPlayerButton.grid(row=0, column=1, columnspan=1, sticky=NW, padx=5)

# Board buttons (keeping original structure for click detection)
button1 = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30, "bold"), 
                bg=CELL_BG, fg=TEXT, relief=RAISED, borderwidth=3)
button1.grid(row=0, column=0, padx=2, pady=2)
button1.bind("<Button-1>", play)
button1.bind("<Enter>", on_enter)
button1.bind("<Leave>", on_leave)

button2 = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30, "bold"), 
                bg=CELL_BG, fg=TEXT, relief=RAISED, borderwidth=3)
button2.grid(row=0, column=1, padx=2, pady=2)
button2.bind("<Button-1>", play)
button2.bind("<Enter>", on_enter)
button2.bind("<Leave>", on_leave)

button3 = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30, "bold"), 
                bg=CELL_BG, fg=TEXT, relief=RAISED, borderwidth=3)
button3.grid(row=0, column=2, padx=2, pady=2)
button3.bind("<Button-1>", play)
button3.bind("<Enter>", on_enter)
button3.bind("<Leave>", on_leave)

button4 = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30, "bold"), 
                bg=CELL_BG, fg=TEXT, relief=RAISED, borderwidth=3)
button4.grid(row=1, column=0, padx=2, pady=2)
button4.bind("<Button-1>", play)
button4.bind("<Enter>", on_enter)
button4.bind("<Leave>", on_leave)

button5 = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30, "bold"), 
                bg=CELL_BG, fg=TEXT, relief=RAISED, borderwidth=3)
button5.grid(row=1, column=1, padx=2, pady=2)
button5.bind("<Button-1>", play)
button5.bind("<Enter>", on_enter)
button5.bind("<Leave>", on_leave)

button6 = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30, "bold"), 
                bg=CELL_BG, fg=TEXT, relief=RAISED, borderwidth=3)
button6.grid(row=1, column=2, padx=2, pady=2)
button6.bind("<Button-1>", play)
button6.bind("<Enter>", on_enter)
button6.bind("<Leave>", on_leave)

button7 = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30, "bold"), 
                bg=CELL_BG, fg=TEXT, relief=RAISED, borderwidth=3)
button7.grid(row=2, column=0, padx=2, pady=2)
button7.bind("<Button-1>", play)
button7.bind("<Enter>", on_enter)
button7.bind("<Leave>", on_leave)

button8 = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30, "bold"), 
                bg=CELL_BG, fg=TEXT, relief=RAISED, borderwidth=3)
button8.grid(row=2, column=1, padx=2, pady=2)
button8.bind("<Button-1>", play)
button8.bind("<Enter>", on_enter)
button8.bind("<Leave>", on_leave)

button9 = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30, "bold"), 
                bg=CELL_BG, fg=TEXT, relief=RAISED, borderwidth=3)
button9.grid(row=2, column=2, padx=2, pady=2)
button9.bind("<Button-1>", play)
button9.bind("<Enter>", on_enter)
button9.bind("<Leave>", on_leave)

restartButton = Button(frame2, text="Restart Game", width=19, height=1, 
                      font=("Arial", 20, "bold"), bg=GREEN, fg="white", 
                      relief=RAISED, borderwidth=3, command=restartGame)
restartButton.grid(row=4, column=0, columnspan=3, pady=10)

buttons = [button1, button2, button3, button4, button5, button6, button7, button8, button9]

# Initialize
changeModeToSinglePlayer()
updateBoard()

root.mainloop()