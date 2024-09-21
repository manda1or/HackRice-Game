import pygame
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
        self.xv = 0     # the velocity in x-direction
        self.yv = 0     # the velocity in y-direction
        self.gravity = 1
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
    def move(self):
        self.yv += self.gravity
        self.x += self.xv
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

# Background will take full size of the screen
bg = pygame.transform.scale(bg, (sw, sh))
bg_x = 0
bg_rect = bg.get_rect(center=(400, 250))

# Set up the game window
win = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Shouternity")

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
    # Set the framerate
    clock.tick(120)

    if pygame.sprite.spritecollide(.sprite, spike_group, False):
        game_over = True
        //death music
    if game_over:
        end_game()

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
