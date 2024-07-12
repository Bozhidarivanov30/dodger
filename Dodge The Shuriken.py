import pygame
import random
import time
import os
 
# Initialize Pygame
pygame.init()
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge The Shurikens")
 
# Load Sounds
click_sfx = pygame.mixer.Sound('button_click_sound.wav')

menu_sfx = pygame.mixer.Sound('menu_music.mp3')
menu_sfx.set_volume(0.1)

gameplay_sfx = pygame.mixer.Sound('gameplay_music.mp3')
gameplay_sfx.set_volume(0.2)

shield_sfx = pygame.mixer.Sound('shield_pickup.mp3')

hearth_sfx = pygame.mixer.Sound('heart_pickup.mp3')

taking_damage_sfx = pygame.mixer.Sound('takingdamage.mp3')

death_sfx = pygame.mixer.Sound('death_sound.mp3')
 
# Load images
win_image = pygame.image.load('win_screen.png')
win_image = pygame.transform.scale(win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

stage1_image = pygame.image.load('level_1.png')
stage1_image = pygame.transform.scale(stage1_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

stage2_image = pygame.image.load('level_2.png')
stage2_image = pygame.transform.scale(stage2_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

stage3_image = pygame.image.load('level_3.png')
stage3_image = pygame.transform.scale(stage3_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

stage4_image = pygame.image.load('level_4.png')
stage4_image = pygame.transform.scale(stage4_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

stage5_image = pygame.image.load('level_5.png')
stage5_image = pygame.transform.scale(stage5_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

background_image = pygame.image.load('background.png')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

classic_image = pygame.image.load('classic-button.png')

survival_image = pygame.image.load('survival-button.png')

quitgame_image = pygame.image.load('quit-game-button.png')

restart_image = pygame.image.load('restart-button.png')

back_to_menu_image = pygame.image.load('back-to-menu-button.png')

quitgame_end_image = pygame.image.load('quit-game-button-endscreen.png')

background_menu = pygame.image.load('background_menu2.png')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

player_image_sitting = pygame.image.load('player_sitting.png')
player_image_sitting = pygame.transform.scale(player_image_sitting, (60,60))

player_image_right = pygame.image.load('player_running_right.png')
player_image_right = pygame.transform.scale(player_image_right, (60,60))

player_image_left = pygame.image.load('player_running_left.png')
player_image_left = pygame.transform.scale(player_image_left, (60,60))
 
heart_image = pygame.image.load('heart2.png')
HEART_SIZE = 50
heart_image = pygame.transform.scale(heart_image, (HEART_SIZE, HEART_SIZE))
 
you_died_image = pygame.image.load('die_screen2.png')
you_died_image = pygame.transform.scale(you_died_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

metallic_heart_image = pygame.image.load('shield_heart.png')
metallic_heart_image = pygame.transform.scale(metallic_heart_image, (HEART_SIZE, HEART_SIZE))
 
shield_image = pygame.image.load('shield.png')
active_shield = pygame.image.load('active_shield.png')
SHIELD_SIZE = 50
active_shield = pygame.transform.scale(active_shield, (100, 100))
shield_image = pygame.transform.scale(shield_image, (SHIELD_SIZE, SHIELD_SIZE))
 
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
 
# Player settings
player_size = 50
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 6
 
# Bullet settings
initial_bullet_speed = 3
 
# Clock
clock = pygame.time.Clock()
 
# Font settings
font = pygame.font.SysFont("comicsansms", 50)
 
# Constants for survival mode
NUM_LIVES = 3
INVINCIBILITY_DURATION = 2  # seconds

INVINCIBILITY_DURATION_SHIELD = 2000

# Load PNG frames as bullets
def load_image_frames(directory):
    frames = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.png'):
            img = pygame.image.load(os.path.join(directory, filename)).convert_alpha()
            frames.append(img)
    return frames
 
bullet_frames = load_image_frames('frames')
 
# Button class
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
 
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
 
    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)
 
# Function to display the menu
def show_menu():
    menu_sfx.play()
    start_button = Button(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 50, classic_image)
    survival_button = Button(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 20, survival_image)
    quit_button = Button(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 90, quitgame_image)
 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if start_button.is_clicked(event):
                click_sfx.play()
                menu_sfx.stop()
                fade_transition(screen, fade_out=True)
                return "start"
            if survival_button.is_clicked(event):
                click_sfx.play()
                menu_sfx.stop()
                fade_transition(screen, fade_out=True)
                return "survival"
            if quit_button.is_clicked(event):
                click_sfx.play()
                menu_sfx.stop()
                pygame.quit()
                quit()
 
        screen.blit(background_menu, (0, 0))
        start_button.draw(screen)
        quit_button.draw(screen)
        survival_button.draw(screen)
        pygame.display.update()
        clock.tick(15)
 
# Function to drop bullets
def drop_bullets(bullet_list, bullet_speed_multiplier, score, mode):
    if mode == "start":
        sides = ['top']
        if score > 10:
            sides.append('right')
        if score > 20:
            sides.append('bottom')
        if score > 30:
            sides.append('left')
    else:  # mode == "survival"
        sides = ['top', 'bottom', 'left', 'right']
 
    if len(bullet_list) < 20 and random.random() < 0.1:
        side = random.choice(sides)
        speed = initial_bullet_speed * random.uniform(0.5, 1.5) * bullet_speed_multiplier
        size = random.randint(30, 60)  # Random bullet size between 30 and 60
        frame_index = 0  # Initial frame index for bullet animation
 
        if side == 'top':
            x_pos = random.randint(0, SCREEN_WIDTH - size)
            bullet_list.append([x_pos, 0, side, speed, size, frame_index])
        elif side == 'bottom':
            x_pos = random.randint(0, SCREEN_WIDTH - size)
            bullet_list.append([x_pos, SCREEN_HEIGHT, side, speed, size, frame_index])
        elif side == 'left':
            y_pos = random.randint(0, SCREEN_HEIGHT - size)
            bullet_list.append([0, y_pos, side, speed, size, frame_index])
        elif side == 'right':
            y_pos = random.randint(0, SCREEN_HEIGHT - size)
            bullet_list.append([SCREEN_WIDTH, y_pos, side, speed, size, frame_index])
 
# Function to draw bullets
def draw_bullets(screen, bullet_list):
    for bullet_pos in bullet_list:
        x, y, direction, speed, size, frame_index = bullet_pos
        # Use the bullet frame we created
        frame = bullet_frames[frame_index]
 
        # Scale the bullet image
        scaled_bullet = pygame.transform.scale(frame, (size, size))
 
        # Draw the scaled bullet image
        screen.blit(scaled_bullet, (x, y))
 
# Function to update the position of bullets
def update_bullets(bullet_list):
    for idx, bullet_pos in enumerate(bullet_list):
        if bullet_pos[2] == 'top':
            bullet_pos[1] += bullet_pos[3]
        elif bullet_pos[2] == 'bottom':
            bullet_pos[1] -= bullet_pos[3]
        elif bullet_pos[2] == 'left':
            bullet_pos[0] += bullet_pos[3]
        elif bullet_pos[2] == 'right':
            bullet_pos[0] -= bullet_pos[3]
 
        # Update bullet animation frame
        bullet_pos[5] = (bullet_pos[5] + 1) % len(bullet_frames)
 
        # Remove bullet if it goes out of bounds
        if bullet_pos[1] > SCREEN_HEIGHT or bullet_pos[1] < 0 or bullet_pos[0] > SCREEN_WIDTH or bullet_pos[0] < 0:
            bullet_list.pop(idx)
 
# Function to detect collision
def detect_collision(player_pos, bullet_pos):
    p_x, p_y = player_pos
    b_x, b_y, b_size = bullet_pos[0], bullet_pos[1], bullet_pos[4]
    return (p_x < b_x + b_size and p_x + player_size > b_x and
            p_y < b_y + b_size and p_y + player_size > b_y)
 
# Function to perform fade transition
def fade_transition(screen, fade_out=True, speed=15):
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(BLACK)
    alpha = 0 if fade_out else 255
 
    while (fade_out and alpha < 255) or (not fade_out and alpha > 0):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        alpha += speed if fade_out else -speed
        clock.tick(60)
    
# Function to capture the current screen
def capture_screen(screen):
    return screen.copy()

# Function for the countdown before resuming the game
def countdown_before_resume(screen, captured_screen):
    countdown_font = pygame.font.SysFont("comicsansms", 90)
    countdown_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    countdown_surface.set_alpha(50)  # Semi-transparent overlay

    for i in range(3, 0, -1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(captured_screen, (0, 0))
        screen.blit(countdown_surface, (0, 0))
        countdown_text = countdown_font.render(str(i), True, WHITE)
        screen.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() + 100// 2, SCREEN_HEIGHT // 2 - countdown_text.get_height() // 2 - 10))
        pygame.display.update()
        time.sleep(1)  # Pause for 1 second before updating the countdown

#Function to pause the game
def pause_game(screen):
    pause_font = pygame.font.SysFont("comicsansms", 90)
    pause_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    pause_surface.set_alpha(200)  # Semi-transparent overlay
    pause_surface.fill(BLACK)

    resume_button = Button(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 50, pygame.image.load('resume-button.png'))
    menu_button = Button(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20, pygame.image.load('back-to-menu-button.png'))

    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if resume_button.is_clicked(event):
                click_sfx.play()
                gameplay_sfx.play()
                return "resume"  # Indicate that the game should resume
            if menu_button.is_clicked(event):
                click_sfx.play()
                fade_transition(screen, fade_out=True)
                return "menu"

        screen.blit(pause_surface, (0, 0))
        pause_text = pause_font.render("Paused", True, WHITE)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - 143, SCREEN_HEIGHT // 2 - 180))
        resume_button.draw(screen)
        menu_button.draw(screen)
        pygame.display.update()
        clock.tick(15)
 
# Function to display the "You Died" screen
def you_died_screen():
    screen.blit(you_died_image, (0, 0))
    pygame.display.update()
    pygame.time.delay(1000)
 
# Function to display the game over screen
def game_over_screen(score, mode):
    menu_sfx.play()
    reset_button = Button(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 50, restart_image)
    menu_button = Button(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 20, back_to_menu_image)
    quit_button = Button(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 90, quitgame_end_image)
 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if reset_button.is_clicked(event):
                click_sfx.play()
                menu_sfx.stop()
                fade_transition(screen, fade_out=True)
                game_loop(mode)  # Restart game loop with the same mode
                return  # Return to menu
            if menu_button.is_clicked(event):
                click_sfx.play()
                menu_sfx.stop()
                fade_transition(screen, fade_out=True)
                return
            if quit_button.is_clicked(event):
                click_sfx.play()
                menu_sfx.stop()
                pygame.quit()
                quit()

        screen.blit(background_image, (0, 0))
        game_over_text = font.render("Game Over", True, WHITE)
        final_score_text = font.render(f"Time: {int(score)}", True, WHITE)
        you_lost_text = font.render("You Lost", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200// 2, SCREEN_HEIGHT // 2 - 190))
        if mode == "survival":
                    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 140 // 2, SCREEN_HEIGHT // 2 - 130))
        if mode == "start":
            screen.blit(you_lost_text, (SCREEN_WIDTH // 2 - 150 // 2, SCREEN_HEIGHT // 2 - 130))
        reset_button.draw(screen)
        quit_button.draw(screen)
        menu_button.draw(screen)
        pygame.display.update()
        clock.tick(15)
 
# Function to display the score
def display_score(score, mode):
    if mode == "survival":
        score_text = font.render(f"Time: {int(score)}", True, WHITE)
        screen.blit(score_text, (33, 28))
 
# Function to display hearts for lives in Survival mode
def display_hearts(num_lives, shield_invincible=False):
    heart_spacing = 40
    heart_left_padding = 25
    heart_image_to_use = metallic_heart_image if shield_invincible else heart_image
 
    for i in range(num_lives):
        screen.blit(heart_image_to_use, (SCREEN_WIDTH - heart_left_padding - (i + 1.25) * heart_spacing, 20))
 
# Function to spawn hearts at random locations
def spawn_heart():
    x = random.randint(0, SCREEN_WIDTH - HEART_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - HEART_SIZE)
    return [x, y]
 
# Function to draw hearts
def draw_heart(screen, heart_pos):
    screen.blit(heart_image, (heart_pos[0], heart_pos[1]))
 
# Function to check for collision between player and heart
def check_heart_collision(player_pos, heart_pos):
    p_x, p_y = player_pos
    h_x, h_y = heart_pos[0], heart_pos[1]
    
    if (p_x < h_x + HEART_SIZE and p_x + player_size > h_x and
        p_y < h_y + HEART_SIZE and p_y + player_size > h_y):
        hearth_sfx.play()
        return True
    return False

def spawn_shield():
    x = random.randint(0, SCREEN_WIDTH - SHIELD_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - SHIELD_SIZE)
    return [x, y]
 
# Function to draw hearts
def draw_shield(screen, shield_pos):
    screen.blit(shield_image, (shield_pos[0], shield_pos[1]))
 
# Function to check for collision between player and heart
def check_shield_collision(player_pos, shield_pos):
    p_x, p_y = player_pos
    s_x, s_y = shield_pos[0], shield_pos[1]
    if (p_x < s_x + SHIELD_SIZE and p_x + player_size > s_x and
        p_y < s_y + SHIELD_SIZE and p_y + player_size > s_y):
        shield_sfx.play()
        return True
    return False
 
def game_loop(mode):
    gameplay_sfx.play()  # plays the music
    player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    bullet_list = []
    start_time = time.time()
    bullet_speed_multiplier = 1
    num_lives = NUM_LIVES if mode == "survival" else 0
    invincible = False
    invincibility_start = 0
    shield_invincible = False
    shield_invincible_start = 0
    heart_spawn_time = time.time()
    heart_pos = None
    shield_spawn_time = time.time()
    shield_pos = None
    running = True

    # Stage settings
    stage_images = [stage1_image, stage2_image, stage3_image, stage4_image, stage5_image]
    stage_thresholds = [10, 20, 30, 40, 50]
    current_stage = 0
    stages_completed = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameplay_sfx.stop()
                    captured_screen = capture_screen(screen)
                    result = pause_game(screen)
                    if result == "menu":
                        fade_transition(screen, fade_out=True)
                        return  # Go back to the main menu
                    elif result == "resume":
                        countdown_before_resume(screen, captured_screen)  # Perform the 3-second countdown
                        start_time += 3  # Adjust start time to account for the countdown
 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > player_speed:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_size - player_speed:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > player_speed:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT - player_size - player_speed:
            player_pos[1] += player_speed
 
        screen.blit(background_image, (0, 0))

        elapsed_time = time.time() - start_time
        bullet_speed_multiplier = 1 + (elapsed_time // 10) * 0.1  # Increase speed every 10 seconds by 10%

        # Check if player has reached the threshold for the next stage
        if mode == "start" and current_stage < len(stage_thresholds) and elapsed_time >= stage_thresholds[current_stage]:
            # Display stage image for a brief moment
            fade_transition(screen, fade_out=True)
            screen.blit(stage_images[current_stage], (0, 0))
            pygame.display.update()
            time.sleep(1)  # Display the stage image for 1 seconds
            
            # Reset player position and shurikens
            player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
            bullet_list = []
            
            current_stage += 1  # Move to the next stage
            stages_completed += 1

        # If all stages are completed, display the win screen
        if stages_completed == len(stage_images):
            fade_transition(screen, fade_out=True)
            screen.blit(win_image, (0, 0))
            pygame.display.update()
            time.sleep(5)
            return

        # Update and draw bullets
        drop_bullets(bullet_list, bullet_speed_multiplier, elapsed_time, mode)
        update_bullets(bullet_list)
        draw_bullets(screen, bullet_list)
 
        # Spawn hearts every 10 seconds
        if time.time() - heart_spawn_time > 10:
            if mode == "survival":
                heart_pos = spawn_heart()
                heart_spawn_time = time.time()
 
        # Draw heart
        if heart_pos:
            draw_heart(screen, heart_pos)
 
        # Check collision with heart
        if heart_pos and check_heart_collision(player_pos, heart_pos):
            num_lives += 1
            heart_pos = None  # Remove heart after collection
 
        # Spawn shield every 20 seconds
        if time.time() - shield_spawn_time > 20:
            if mode == "survival":
                shield_pos = spawn_shield()
                shield_spawn_time = time.time()
 
        # Draw shield
        if shield_pos:
            draw_shield(screen, shield_pos)
 
        # Check collision with shield
        if shield_pos and check_shield_collision(player_pos, shield_pos):
            shield_invincible = True
            shield_invincible_start = time.time()
            shield_pos = None  # Remove shield after collection
 
        # Manage shield invincibility duration
        if shield_invincible and time.time() - shield_invincible_start > 5:
            shield_invincible = False

        # Draw player with blinking effect if invincible
        if (not invincible or shield_invincible) or (time.time() % 0.2 < 0.1):
            if keys[pygame.K_LEFT]:
                screen.blit(player_image_left, player_pos)
            elif keys[pygame.K_RIGHT]:
                screen.blit(player_image_right, player_pos)
            else:
                screen.blit(player_image_sitting, player_pos)
                
        # Draw player with shield effect
        if shield_invincible:
            screen.blit(active_shield, (player_pos[0] - 20, player_pos[1] - 20))

        # Display score
        display_score(elapsed_time, mode)
 
        # Display hearts in Survival mode
        if mode == "survival":
            display_hearts(num_lives, shield_invincible)
 
        # Check collision with bullets
        for bullet_pos in bullet_list:
            if detect_collision(player_pos, bullet_pos):
                if mode == "survival":
                    if not shield_invincible and not invincible:
                        taking_damage_sfx.play()
                        num_lives -= 1
                        invincible = True
                        invincibility_start = time.time()
                        if num_lives <= 0:
                            taking_damage_sfx.stop()
                            gameplay_sfx.stop()
                            death_sfx.play()
                            you_died_screen()  # You died
                            fade_transition(screen, fade_out=True)
                            game_over_screen(elapsed_time, mode)
                            return  # Restart the game loop after game over
                elif mode == "start":
                    gameplay_sfx.stop()
                    death_sfx.play()
                    you_died_screen()
                    fade_transition(screen, fade_out=True)
                    game_over_screen(elapsed_time, mode)
                    return  # Restart the game loop after game over
                
        # Handle invincibility duration
        if invincible and time.time() - invincibility_start > INVINCIBILITY_DURATION:
            invincible = False
 
        pygame.display.update()
        clock.tick(60)

# Game start logic
def start_game():
    while True:
        mode = show_menu()
        if mode:
            game_loop(mode)
        pygame.display.update()
        clock.tick(60)

# Entry point
if __name__ == "__main__":
    start_game()
