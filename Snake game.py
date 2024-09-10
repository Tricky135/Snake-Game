import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

window = tkinter.Tk()
window.title("SNAKE GAME")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5)
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
velocityX = 0
velocityY = 0
snake_body = []
game_over = False
score = 0

def show_hint():
    """Display a vibrant popup window with a hint at the start of the game, centered over the game window."""
    hint_window = tkinter.Toplevel(window)
    hint_window.title("HINT")
    hint_window.geometry("350x150")
    hint_window.configure(bg="white")
    hint_window.resizable(False, False)

    hint_x = window_x + (window_width // 2) - 175 
    hint_y = window_y + (window_height // 2) - 75 
    hint_window.geometry(f"+{hint_x}+{hint_y}")

    message_label = tkinter.Label(
        hint_window, 
        text="Use your ARROW Keys to start!", 
        font=("Arial", 14, "bold"), 
        fg="black", 
    )
    message_label.pack(pady=20)

    ok_button = tkinter.Button(
        hint_window, 
        text="OK", 
        font=("Arial", 12, "bold"), 
        bg="green", 
        fg="white", 
        command=hint_window.destroy
    )
    ok_button.pack(pady=10)

def reset_game():
    """Reset the game state to start again."""
    global snake, food, velocityX, velocityY, snake_body, game_over, score
    snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5)
    food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
    velocityX = 0
    velocityY = 0
    snake_body = []
    game_over = False
    score = 0

def show_game_over():
    """Display a custom Game Over window with Play Again and Exit buttons."""
    global game_over, score

    if game_over:
        game_over_window = tkinter.Toplevel(window)
        game_over_window.title("Game Over!")
        game_over_window.geometry("300x150")
        game_over_window.resizable(False, False)

        x = window.winfo_x() + (window_width // 2) - 150
        y = window.winfo_y() + (window_height // 2) - 75
        game_over_window.geometry(f"+{x}+{y}")

        tkinter.Label(game_over_window, text=f"Your SCORE : {score}", font=("Arial", 14)).pack(pady=20)

        button_frame = tkinter.Frame(game_over_window)
        button_frame.pack()

        button_width = 10

        play_again_button = tkinter.Button(button_frame, text="Play Again", width=button_width,
                                           command=lambda: [reset_game(), game_over_window.destroy()])
        play_again_button.pack(side="left", padx=10)

        exit_button = tkinter.Button(button_frame, text="Exit", width=button_width, command=window.quit)
        exit_button.pack(side="right", padx=10)


def change_direction(e):
    global velocityX, velocityY, game_over
    if game_over:
        return
    
    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1

    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1

    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0

    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0

def move():
    global snake, food, snake_body, game_over, score
    if game_over:
        return

    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        show_game_over()
        return

    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            show_game_over()
            return

    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    for i in range(len(snake_body) - 1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i - 1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def draw():
    global snake, food, snake_body, game_over, score
    move()

    canvas.delete("all")

    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill='red')

    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill='lime green')

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill='lime green')

    if not game_over:
        canvas.create_text(50, 30, font="Arial 18 bold", text=f"Score: {score}", fill="white")

    window.after(200, draw)

show_hint()

draw()
window.bind("<KeyRelease>", change_direction)
window.mainloop()
