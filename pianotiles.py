import tkinter as tk
import random
import pygame

# Initialize Pygame mixer for sound
pygame.mixer.init()

# Load and prepare the music (using pygame.mixer.music for continuous playback)
pygame.mixer.music.load("piano-tiles-sound-1.wav")

# Game variables
tiles = []
speed = 5
score = 0
game_over = False

# List of colors for the tiles
colors = ["red", "green", "blue", "yellow", "purple", "orange", "pink"]

# Function to create a new tile
def create_tile():
    col = random.randint(0, 3)
    x1 = col * 100
    y1 = -150

    # Random width and height for the tile
    width = random.randint(80, 120)
    height = random.randint(80, 120)

    x2 = x1 + width
    y2 = y1 + height
    color = random.choice(colors)  # Choose a random color
    tile = canvas.create_rectangle(x1, y1, x2, y2, fill=color)
    tiles.append((tile, col, color, width, height))  # Store the tile, its column, color, width, and height

# Function to update the game state
def update():
    global game_over, score

    if game_over:
        return

    # Move tiles down
    for tile, col, color, width, height in tiles:
        canvas.move(tile, 0, speed)
        x1, y1, x2, y2 = canvas.coords(tile)
        if y1 > 600:
            # Tile went out of screen
            tiles.remove((tile, col, color, width, height))
            canvas.delete(tile)
            game_over = True
            show_game_over()
            pygame.mixer.music.stop()  # Stop the music when the game is over
            return

    # Create a new tile periodically
    if len(tiles) == 0 or canvas.coords(tiles[-1][0])[1] > 200:
        create_tile()

    # Update the score label
    score_label.config(text="Final Score: {}".format(score))

    # Call update again after 50ms
    root.after(50, update)

# Function to handle clicks on the canvas
def on_tile_click(event):
    global game_over, score

    if game_over:
        return

    clicked_item = canvas.find_closest(event.x, event.y)[0]
    for tile, col, color, width, height in tiles:
        if tile == clicked_item:
            # Check if the clicked item is a colored tile
            if canvas.itemcget(tile, "fill") in colors:
                tiles.remove((tile, col, color, width, height))
                canvas.delete(tile)
                score += 1
                # Play the sound effect (optional, different from background music)
                # pygame.mixer.Sound("click-sound.wav").play()  # Uncomment if you have a click sound
            else:
                game_over = True
                show_game_over()
                pygame.mixer.music.stop()  # Stop the music when the game is over
            break

# Function to display the game over message
def show_game_over():
    canvas.create_text(200, 300, text="Game Over!", font=("Helvetica", 32), fill="red")
    canvas.create_text(200, 350, text="Score: {}".format(score), font=("Helvetica", 24), fill="black")

# Setup the main window
root = tk.Tk()
root.title("Piano Tiles Game")

# Create a canvas with a white background
canvas = tk.Canvas(root, width=1500, height=2000, bg="white")
canvas.pack()

# Create a label for the score
score_label = tk.Label(root, text="Score: {}".format(score), font=("Helvetica", 16))
score_label.pack()
canvas.create_window(750, 50, window=score_label) 

# Bind the left mouse click to the tile click handler
canvas.bind("<Button-1>", on_tile_click)

# Start the music and game
pygame.mixer.music.play(-1)  # Play the music in a loop
create_tile()
update()

root.mainloop()
