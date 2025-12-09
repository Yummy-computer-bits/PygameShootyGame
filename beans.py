# ----------------------------------------------------------------------------------------------
# GLOBAL VARIABLES AND LIBRARIES
import sys
import random  # Imported for alien spawning
import pygame
from pygame import K_EURO, K_RIGHT, K_SPACE

# Try/Except blocks allow the game to run even if your custom modules aren't
# in the same folder as this script for testing purposes.
try:
    import Game_State
    import Time_Module
except ImportError:
    pass  # We will handle missing logic inline if necessary

pygame.init()

# COLOURS
White = (255, 255, 255)
Black = (0, 0, 0)
Blue = (0, 0, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)

# INITIAL CURRENT TIME
Current = 60
Score = 0  # Initialize Score

# GLOBAL FONT
Font = pygame.font.SysFont(None, 40, False, False)
BigFont = pygame.font.SysFont(None, 80, False, False)  # Font for Game Over

# Start on MENU
State = "Menu"

# ----------------------------------------------------------------------------------------------
# WINDOW SETTINGS
SCREEN_WIDTH, SCREEN_HEIGHT = (800, 600)
Window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Knights and aliens")
clock = pygame.time.Clock()


# ----------------------------------------------------------------------------------------------
# CLASS DEFINITIONS

class Knight:
    def __init__(self):
        # We try to load the image, if it fails (file missing), we just use a rect
        try:
            self.Knightsprite = pygame.image.load("knightsprite.png")
            self.image_loaded = True
        except:
            self.image_loaded = False

        self.Knight_X = 300
        self.Knight_Y = 400
        self.width = 30
        self.height = 70
        # Hitbox used for collision
        self.rect = pygame.Rect(self.Knight_X + 10, self.Knight_Y + 5, self.width, self.height)

    def draw(self):
        if self.image_loaded:
            Window.blit(self.Knightsprite, (self.Knight_X, self.Knight_Y))

        # Update rect position for collision detection
        self.rect.topleft = (self.Knight_X + 10, self.Knight_Y + 5)
        # Draw hitbox (Visual aid)
        pygame.draw.rect(Window, Blue, self.rect, 1)

    def move(self):
        kbin = pygame.key.get_pressed()
        if kbin[pygame.K_LEFT] and self.Knight_X > 0:
            self.Knight_X -= 10
        if kbin[pygame.K_RIGHT] and self.Knight_X < SCREEN_WIDTH - 50:
            self.Knight_X += 10


class Alien:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - self.width), -50, self.width, self.height)
        self.speed = 2

    def move(self):
        self.rect.y += self.speed
        # If alien goes off screen bottom, reset to top
        if self.rect.y > SCREEN_HEIGHT:
            self.reset_pos()

    def reset_pos(self):
        self.rect.y = random.randint(-150, -50)
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.speed = random.randint(2, 5)  # Randomize speed slightly

    def draw(self):
        pygame.draw.rect(Window, Green, self.rect)  # Draw alien as green square


class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x + 15, y, 10, 20)  # Spawn bullet center of player
        self.speed = 10

    def move(self):
        self.rect.y -= self.speed

    def draw(self):
        pygame.draw.rect(Window, Red, self.rect)


# ----------------------------------------------------------------------------------------------
# INSTANTIATE OBJECTS

Player = Knight()
Bullets = []
Aliens = []

# Create a batch of aliens
for i in range(5):
    Aliens.append(Alien())

# ----------------------------------------------------------------------------------------------
# TIMER
Decrease = pygame.USEREVENT
pygame.time.set_timer(Decrease, 1000)

# ----------------------------------------------------------------------------------------------
# MENU SETUP (Initial Draw)
start_btn_rect = pygame.Rect(0, 0, 0, 0)  # Placeholders
quit_btn_rect = pygame.Rect(0, 0, 0, 0)

if State == "Menu":
    Window.fill(Blue)
    try:
        Game_State.gamestate(State, White, Black, Window, Font)
        start_btn_rect = Game_State.startbutton(White, Black, Window, Font)
        quit_btn_rect = Game_State.quitbutton(White, Black, Window, Font)
    except NameError:
        # Fallback if Game_State module is missing
        start_btn_rect = pygame.draw.rect(Window, White, (300, 200, 200, 50))
        quit_btn_rect = pygame.draw.rect(Window, White, (300, 300, 200, 50))
        st_text = Font.render("START", True, Black)
        Window.blit(st_text, (350, 210))

# ----------------------------------------------------------------------------------------------
# GAMEPLAY LOOP
while True:
    clock.tick(60)
    mouse = pygame.mouse.get_pos()

    # --- GAMEPLAY LOGIC ---
    if State == "Game":
        Window.fill(White)

        # 1. Update & Draw Time
        try:
            Time_Module.countdown(Font, Black, Window, Current)
        except NameError:
            time_text = Font.render(f"Time: {Current}", True, Black)
            Window.blit(time_text, (650, 10))

        # 2. Draw Score
        score_text = Font.render(f"Score: {Score}", True, Black)
        Window.blit(score_text, (10, 10))

        # 3. Player Logic
        Player.move()
        Player.draw()

        # 4. Alien Logic
        for alien in Aliens:
            alien.move()
            alien.draw()

            # Check Collision: Alien vs Player
            if alien.rect.colliderect(Player.rect):
                State = "GameOver"

        # 5. Bullet Logic
        for bullet in Bullets[:]:  # Iterate over a copy of the list
            bullet.move()
            bullet.draw()

            # Check if bullet goes off screen
            if bullet.rect.y < 0:
                Bullets.remove(bullet)
                continue

            # Check Collision: Bullet vs Alien
            for alien in Aliens:
                if bullet.rect.colliderect(alien.rect):
                    try:
                        Bullets.remove(bullet)
                    except ValueError:
                        pass  # Bullet might have hit two aliens at once

                    alien.reset_pos()  # Respawn alien
                    Score += 1  # Increase Score
                    break  # Break inner loop so one bullet doesn't kill multiple instantly

        # 6. Check Time Game Over
        if Current < 0:
            State = "GameOver"

    # --- GAME OVER LOGIC ---
    elif State == "GameOver":
        Window.fill(Black)

        # Display "GAME OVER"
        go_text = BigFont.render("GAME OVER", True, Red)
        Window.blit(go_text, (SCREEN_WIDTH // 2 - 150, 150))

        # Display Final Score
        final_score_text = Font.render(f"Final Score: {Score}", True, White)
        Window.blit(final_score_text, (SCREEN_WIDTH // 2 - 100, 250))

        # Draw "Play Again" Button
        play_again_btn = pygame.draw.rect(Window, White, (SCREEN_WIDTH // 2 - 100, 350, 200, 50))
        pa_text = Font.render("Play Again", True, Black)
        Window.blit(pa_text, (SCREEN_WIDTH // 2 - 70, 360))

    # --- MENU LOGIC (Redraw to ensure it stays visible) ---
    elif State == "Menu":
        # We redraw the menu here if the loop cycles, to prevent blank screens
        # Assuming Game_State handles drawing, but strictly:
        Window.fill(Blue)
        try:
            Game_State.gamestate(State, White, Black, Window, Font)
            start_btn_rect = Game_State.startbutton(White, Black, Window, Font)
            quit_btn_rect = Game_State.quitbutton(White, Black, Window, Font)
        except NameError:
            start_btn_rect = pygame.draw.rect(Window, White, (300, 200, 200, 50))
            quit_btn_rect = pygame.draw.rect(Window, White, (300, 300, 200, 50))
            t1 = Font.render("START", True, Black)
            t2 = Font.render("QUIT", True, Black)
            Window.blit(t1, (360, 215))
            Window.blit(t2, (365, 315))

    # --- EVENT HANDLER ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Timer Event
        if event.type == Decrease and State == "Game":
            # Just decrement, the draw logic handles display
            Current -= 1

        # Keyboard Inputs
        if event.type == pygame.KEYDOWN:
            if State == "Game":
                if event.key == pygame.K_SPACE:
                    # Spawn a bullet
                    Bullets.append(Bullet(Player.Knight_X, Player.Knight_Y))

        # Mouse Inputs
        if event.type == pygame.MOUSEBUTTONDOWN:
            if State == "Menu":
                if start_btn_rect.collidepoint(mouse):
                    State = "Game"
                    Current = 60  # Reset time
                    Score = 0  # Reset score
                elif quit_btn_rect.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

            elif State == "GameOver":
                # Check collision with "Play Again" button defined in GameOver loop
                # We calculate the rect area again for the check
                if (SCREEN_WIDTH // 2 - 100) < mouse[0] < (SCREEN_WIDTH // 2 + 100) and \
                        350 < mouse[1] < 400:
                    # RESET GAME
                    State = "Game"
                    Current = 60
                    Score = 0
                    Bullets.clear()
                    Player.Knight_X = 300
                    # Reset Aliens
                    Aliens.clear()
                    for i in range(5):
                        Aliens.append(Alien())

    pygame.display.update()