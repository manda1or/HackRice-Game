import pygame
import speech_recognition as sr
import random
import sys #sys.exit

class Ball:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.xv = 0     # the velocity in x-direction
        self.yv = 0     # the velocity in y-direction
        self.gravity = 1
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
    def move(self):
        self.yv += self.gravity
        self.x += self.xv
        self.y += self.yv

sw = 800  # screen width
sh = 500  # screen height

# Load background image
try:
    bg = pygame.image.load('Cityscape Background.png')
except pygame.error as e:
    print('Error loading background image:', e)

# Background will take full size of the screen
bg = pygame.transform.scale(bg, (sw, sh))
bg_x = 0
bg_rect = bg.get_rect(center=(400, 250))

# Set up the game window
win = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Ball Game")

# Object to control the framerate
clock = pygame.time.Clock()

# Initialize font for displaying "Game Over"
pygame.font.init()
font = pygame.font.Font(None, 74)  # Use default font with size 74

# Function to redraw the game window
def redraw_window():
    # Draw background
    win.blit(bg, (0, 0))

    # Draw the ball
    ball.draw(win)

    # What happens when game_over
    if game_over:
        text = font.render('You are not good at screaming', True, (255, 0, 0))
        win.blit(text, (sw // 2 - text.get_width() // 2, sh // 2 - text.get_height() // 2))

    # Update the display
    pygame.display.update()

pygame.init()

# Create ball object
ball = Ball(sw/5 - 60, sh/2, 20, 20, (255, 0, 0))

# Initialize game_over variable
game_over = False

# Speech recognizer setup
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Function to detect audio signal
def detect_audio():
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjusts for ambient noise
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Audio detected!")
            return True
    except sr.WaitTimeoutError:
        return False

run = True
while run:
    # Set the framerate
    clock.tick(120)

    # Check for keyboard input to move the ball
    keys = pygame.key.get_pressed()

    if not game_over:
        if detect_audio():  # If audio is detected, move the ball up
            ball.yv = -10
        # if keys[pygame.K_UP]:
        #     ball.yv = -3
        else:
            ball.yv = 0  # Ball stops moving if no audio

        # Move the ball
        ball.move()

        # Check if the ball goes off the screen (top or bottom) and trigger game over
        if ball.y >= sh or ball.y <= 0:
            game_over = True

    # Handle the quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Redraw the window
    redraw_window()

# Quit pygame when the game ends
pygame.quit()
