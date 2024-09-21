import pygame

import pyaudio
import numpy as np
import threading

import sys
import random
import speech_recognition as sr


class Ball:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

=======
        self.xv = 0
        self.yv = 0
        self.gravity = 0.1
        self.lift = -0.5  # Control the upward acceleration
        self.max_yv_down = 0.5  # Maximum downward speed
        self.max_yv_up = -3  # Maximum upward speed
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
    

    def move(self):
        self.yv += self.gravity
        if self.yv > self.max_yv_down:
            self.yv = self.max_yv_down
        self.y += self.yv
    
    def move_up(self):
        self.yv += self.lift
        if self.yv < self.max_yv_up:
            self.yv = self.max_yv_up
        self.y += self.yv


sw = 800  # screen width
sh = 500  # screen height

# Initialize variables
game_speed = 5
player_score = 0
game_over = False

# Load background image
try:
    bg = pygame.image.load('Resized Cityscape Background.png')
except pygame.error as e:
    print('Error loading background image:', e)

bg = pygame.transform.scale(bg, (sw, sh))
bg_x = 0

# Set up the game window
win = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Shouternity")

clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font(None, 74)



# Function to redraw the game window

def redraw_window():

    # Draw background
    win.blit(bg, (bg_x, 0))
    win.blit(bg, (bg_x + sw, 0))

    # Draw the ball

    win.blit(bg, (0, 0))

    ball.draw(win)

    if game_over:
        text = font.render('Game Over!', True, (255, 0, 0))
        win.blit(text, (sw // 2 - text.get_width() // 2, sh // 2 - text.get_height() // 2))

    pygame.display.update()

pygame.init()

game_over = False

# PyAudio setup for sound detection
audio_detected = False
threshold = 20  # Adjust this value to set the sensitivity for noise detection
chunk = 1024
format = pyaudio.paInt16
channels = 1
rate = 44100

p = pyaudio.PyAudio()

# Function to capture audio and detect noise
def detect_audio_continuous():
    global audio_detected
    try:
        stream = p.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

        while True:
            if stream.is_active():
                try:
                    data = np.frombuffer(stream.read(chunk), dtype=np.int16)
                    rms = np.sqrt(np.mean(np.square(data)))  # Root Mean Square amplitude
                    print(f"RMS: {rms}")

                    if rms > threshold:
                        print("Loud noise detected!")
                        audio_detected = True
                    else:
                        audio_detected = False
                except OSError as e:
                    print(f"Error reading stream: {e}")
                    audio_detected = False
            else:
                print("Stream is inactive. Exiting audio detection.")
                break

    except Exception as e:
        print(f"Error initializing PyAudio stream: {e}")

# Start the audio detection in a separate thread
audio_thread = threading.Thread(target=detect_audio_continuous, daemon=True)
audio_thread.start()

run = True




while run:
    if pygame.sprite.spritecollide(.sprite, spike_group, False):
        game_over = True
        //death music
    if game_over:
        end_game()

    # Check for keyboard input to move the ball
    keys = pygame.key.get_pressed()

    if not game_over:
        if audio_detected:
            print("Moving the ball up!")
            ball.move_up()

        else:
            ball.move()

        if ball.y >= sh or ball.y <= 0:
            game_over = True


    # Update the background position

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    bg_x -= game_speed
    if bg_x <= -sw:
        bg_x = 0

    # Redraw the window

    redraw_window()
    clock.tick(60)  # Set the frame rate to 60 FPS

pygame.quit()

try:
    p.terminate()  # Clean up the PyAudio stream
except Exception as e:
    print(f"Error terminating PyAudio: {e}")
