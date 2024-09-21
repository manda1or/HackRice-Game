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


class Spike_lower(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 2):
            current_sprite = pygame.transform.scale(
                pygame.image.load(f".png"), (170, 170))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

sw = 800  # screen width
sh = 500  # screen height

#initialize variables
game_speed = 5
player_score = 0
game_over = False
obstacle_timer = 0
obstacle_spawn = False
obstacle_cooldown = 1000

# Load background image
try:
    bg = pygame.image.load('Cityscape Background.png')
except pygame.error as e:
    print('Error loading background image:', e)

bg = pygame.transform.scale(bg, (sw, sh))
bg_x = 0
bg_rect = bg.get_rect(center=(400, 250))

# Set up the game window
win = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Shouternity")

clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font(None, 74)





# Function to redraw the game window

def redraw_window():
    win.blit(bg, (0, 0))
    ball.draw(win)

    if game_over:
        text = font.render('You are not good at screaming', True, (255, 0, 0))
        win.blit(text, (sw // 2 - text.get_width() // 2, sh // 2 - text.get_height() // 2))

    pygame.display.update()

pygame.init()

ball = Ball(sw/5 - 60, sh/3.5, 20, 20, (255, 0, 0))

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

def end_game():
    global player_score, game_speed
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 300))
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 340))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    game_speed = 5
    cloud_group.empty()
    obstacle_group.empty()



run = True




while run:
    clock.tick(120)


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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    bg_x -= game_speed
    win.blit(bg, (bg_x, 500))
    win.blit(bg, (bg_x + 800, 500))

    if bg_x <= -800:
        bg_x = 0
    
    # Redraw the window

    redraw_window()

pygame.quit()

try:
    p.terminate()  # Clean up the PyAudio stream
except Exception as e:
    print(f"Error terminating PyAudio: {e}")
