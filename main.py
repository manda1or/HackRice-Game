import pygame

import pyaudio
import numpy as np
import threading

import sys
import random
import speech_recognition as sr


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.xv = 0
        self.yv = 0
        self.gravity = 0.1
        self.lift = -0.5  # Control the upward acceleration
        self.max_yv_down = 2  # Maximum downward speed
        self.max_yv_up = -3  # Maximum upward speed
        self.image = pygame.image.load('char.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-10, -10)
        
    
    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
    
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

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Clock_Tower-Transparent.png')
        
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(spike_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(spike_gap / 2)]
    
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    win.blit(img, (x, y))

def reset_game():
    spike_group.empty()
    ball.rect.x = sw//2 - 50
    ball.rect.y = sh//2 - 100
    ball.yv = 0
    score = 0
    return score
    
pygame.init()

sw = 800  # screen width
sh = 500  # screen height

# Load background image
try:
    bg = pygame.image.load('Resized Cityscape Background.png')
except pygame.error as e:
    print('Error loading background image:', e)

bg = pygame.transform.scale(bg, (sw, sh))

# Set up the game window
win = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Shouternity")

clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font(None, 74)


# Initialize variables

score = 0
pass_spike = False
font = pygame.font.SysFont("Bauhaus 93", 60)
white = (255, 255, 255)

ground_scroll = 0
scroll_speed = 4
spike_gap = 120
spike_frequency = 1500
last_spike = pygame.time.get_ticks() - spike_frequency

player_score = 0
game_over = False

# Function to redraw the game window

def redraw_window():
    
    # Draw the ball

    ball.draw(win)
    spike_group.draw(win)

    if game_over:
        text = font.render('Game Over!', True, (255, 0, 0))
        win.blit(text, (sw // 2 - text.get_width() // 2, sh // 2 - text.get_height() // 2))

    pygame.display.update()

# PyAudio setup for sound detection
audio_detected = False
threshold = 50  # Adjust this value to set the sensitivity for noise detection
chunk = 1024
format = pyaudio.paInt16
channels = 1
rate = 44100

p = pyaudio.PyAudio()

# Function to capture audio and detect noise
def detect_audio_continuous():
    global audio_detected
    global p
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

ball = Ball(sw/5 - 60, sh/3.5, 65, 65, (255, 0, 0))
ball_group = pygame.sprite.Group()
ball_group.add(ball)
spike_group = pygame.sprite.Group()

run = True
while run:

    clock.tick(60)  # Set the frame rate to 60 FPS
    if len(spike_group) > 0:
        if ( ball_group.sprites()[0].rect.left > spike_group.sprites()[0].rect.left) and (ball_group.sprites()[0].rect.right < spike_group.sprites()[0].rect.right) and pass_spike == False:
            pass_spike = True
        if pass_spike == True:
            if ball_group.sprites()[0].rect.left > spike_group.sprites()[0].rect.right:
                score += 1
                pass_spike = False
    
        draw_text(str(score), font, white, int(sw/2), 20)

    
    
    if pygame.sprite.groupcollide(ball_group, spike_group, False, False) or (ball.y >= sh) or (ball.y <= 0):
            game_over = True

    if not game_over:
        #create Spikes
        time_now = pygame.time.get_ticks()
        if time_now - last_spike > spike_frequency:
            spike_height = random.randint(-100, 100)
            btm_spike = Spike(sw, int(sh / 2) + spike_height, -1)
            top_spike = Spike(sw, int(sh / 2) + spike_height, 1 )
            spike_group.add(btm_spike)
            spike_group.add(top_spike)
            last_spike = time_now

        # Draw background
        win.blit(bg, (ground_scroll, 0))
        win.blit(bg, (ground_scroll + sw, 0))
    
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > sw:
            ground_scroll = 0

        spike_group.update()

        if audio_detected:
            print("Moving the ball up!")
            ball.move_up()

        else:
            ball.move()

        
    if game_over == True:
            game_over = False
            score = reset_game()

    # Update the background position

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Redraw the window

    redraw_window()
    

pygame.quit()

try:
    p.terminate()  # Clean up the PyAudio stream
except Exception as e:
    print(f"Error terminating PyAudio: {e}")
