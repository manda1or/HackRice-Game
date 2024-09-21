import pygame
import pyaudio
import numpy as np
import threading

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


sw = 800  # screen width
sh = 500  # screen height

# Load background image
try:
    bg = pygame.image.load('bg_img.png')
except pygame.error as e:
    print('Error loading background image:', e)

bg = pygame.transform.scale(bg, (sw, sh))

# Set up the game window
win = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Ball Game")

clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font(None, 74)

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

run = True





while run:
    clock.tick(120)

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

    redraw_window()

pygame.quit()

try:
    p.terminate()  # Clean up the PyAudio stream
except Exception as e:
    print(f"Error terminating PyAudio: {e}")
