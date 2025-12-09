# ----------------------------------------------------------------------------------------------
# GLOBAL VARIABLES AND LIBRARIES
import sys  # imports the sys library
import pygame  # imports the pygame library
from pygame import K_EURO, K_RIGHT

import Game_State
import Time_Module

pygame.init()  # initialises ALL imported pygame modules (the constructor)

# COLOURS
White = (255, 255, 255)  # stores the colour white
Black = (0, 0, 0)
Blue = (0, 0, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Yellow = (255, 255, 0)

# INITIAL CURRENT TIME
Current = 60

# GLOBAL FONT
Font = pygame.font.SysFont(None, 40, False, False)  # creates font and size

# Start on MENU
State = "Menu"  # sets the state to "Menu" when the game opens for the first time
Won = False  # Tracks if player won or lost

# -----------------------------------------------------------------------------------------------
# WINDOW SETTINGS

SCREEN_WIDTH, SCREEN_HEIGHT = (800, 600)  # a tuple which will dictate window dimensions

Window = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT))  # creates object window with parameters for window width and height

pygame.display.set_caption("Platforms and aliens")  # renames the window to the name of the game

clock = pygame.time.Clock()  # creates object clock which tracks time


# -----------------------------------------------------------------------------------------------
# Create Class "Player"
class Knight:
    def __init__(self):
        try:
            self.Knightsprite = pygame.image.load(
                "knightsprite.png")  # Creates surface Knightsprite with image knightsprite.png
            self.Knightsprite = pygame.transform.scale(self.Knightsprite, (40, 70))
        except:
            # Fallback if image missing
            self.Knightsprite = pygame.Surface((40, 70))
            self.Knightsprite.fill(Blue)

        self.rect = pygame.Rect(300, 400, 40, 70)  # Use a rect for collision handling
        self.vel_y = 0  # Vertical velocity for gravity
        self.jump_power = -15  # How high we jump
        self.grounded = False  # Are we on the floor?

    def draw(self):  # a method that redraws the player sprite
        Window.blit(self.Knightsprite,
                    (self.rect.x, self.rect.y))  # draws the player sprite every frame with updated x and y positions
        # pygame.draw.rect(Window, Black, self.rect, 1) # draws the player sprite hitbox every frame with updated x and y positions

    def move(self, platforms):  # allows the user to control the player sprite
        dx = 0
        dy = 0

        kbin = pygame.key.get_pressed()  # event kbin (K-ey B-oard + IN-put) is triggered after a keyboard input
        if kbin[pygame.K_LEFT]:  # should the keyboard input be the LEFT arrow key
            dx -= 5
        if kbin[pygame.K_RIGHT]:
            dx += 5

        # Gravity
        self.vel_y += 0.8
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Check for collision with platforms (X axis)
        self.rect.x += dx
        # (Simple collision: if we hit a wall, we stop, but for this beginner code, we will focus on Y axis landing)

        # Check for collision with platforms (Y axis)
        self.rect.y += dy
        self.grounded = False

        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                # Check if falling down onto platform
                if self.vel_y > 0:
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0
                    self.grounded = True

        # Screen boundaries
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel_y = 0
            self.grounded = True

    def jump(self):
        if self.grounded:
            self.vel_y = self.jump_power
            self.grounded = False


# -----------------------------------------------------------------------------------------------
# Create Class "Platform"
class Platform:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(Window, Black, self.rect)


# Create Class "Alien"
class Alien:
    def __init__(self, x, y, distance):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.start_x = x
        self.distance = distance
        self.direction = 1
        self.speed = 2

    def move(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x > self.start_x + self.distance or self.rect.x < self.start_x:
            self.direction *= -1

    def draw(self):
        pygame.draw.rect(Window, Red, self.rect)


# Create Class "Star" (Goal)
class Star:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)

    def draw(self):
        pygame.draw.rect(Window, Yellow, self.rect)


# -----------------------------------------------------------------------------------------------
# Decrease time
Decrease = pygame.USEREVENT
pygame.time.set_timer(Decrease, 1000)

# INITIALIZE OBJECTS
Player = Knight()  # creates object player from class Knight

# Create a level using a list of platforms
platforms = [
    Platform(0, 580, 800, 20),  # Ground
    Platform(200, 450, 200, 20),
    Platform(400, 350, 200, 20),
    Platform(150, 250, 200, 20),
    Platform(400, 100, 150, 20)
]

# Create Aliens
aliens = [
    Alien(200, 210, 150),
    Alien(400, 310, 150)
]

# Create Goal
Goal = Star(450, 50)


def reset_game():
    global Current, Player
    Current = 60
    Player = Knight()  # Re-create player to reset position


# ----------------------------------------------------------------------------------------------
# Gameplay Loop
while True:
    clock.tick(60)  # at most 60 frames should pass in a second (FPS cap)
    mouse = pygame.mouse.get_pos()  # gets the mouse position at all times

    # 1. MENU STATE LOGIC
    if State == "Menu":  # MENU SCREEN
        Window.fill(Blue)  # changes the window to blue
        Game_State.gamestate(State, White, Black, Window, Font)  # Calls game state

        # Need to capture buttons to check clicks later
        start_btn = Game_State.startbutton(White, Black, Window, Font)
        close_btn = Game_State.quitbutton(White, Black, Window, Font)

    # 2. GAME STATE LOGIC
    elif State == "Game":  # movement only exists during gameplay
        Window.fill(White)  # fills the screen with white pixels

        # Draw Platforms
        for plat in platforms:
            plat.draw()

        # Draw and Move Aliens
        for alien in aliens:
            alien.move()
            alien.draw()
            if Player.rect.colliderect(alien.rect):
                State = "GameOver"
                Won = False

        # Draw Goal
        Goal.draw()
        if Player.rect.colliderect(Goal.rect):
            State = "GameOver"
            Won = True

        Player.move(platforms)  # calls the method that lets the user control the player sprite
        Player.draw()  # the sprite is drawn from the class definition

        Time_Module.countdown(Font, Black, Window, Current)  # re-draws the time on the screen

    # 3. GAME OVER STATE LOGIC
    elif State == "GameOver":
        Window.fill(Black)
        restart_rect = Game_State.gameover_ui(Window, Font, White, Black, Won)

    # Event Handler
    for event in pygame.event.get():  # event handler: any user driven event is listed under here

        if event.type == pygame.QUIT:  # if the "X" on the window is clicked
            pygame.quit()  # kills the game window
            sys.exit()  # exits the program

        # TIMER logic
        if event.type == Decrease and State == "Game":
            if Current > 0:
                Current -= 1
            else:
                # Time ran out
                State = "GameOver"
                Won = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if State == "Game":
                    Player.jump()

        if event.type == pygame.MOUSEBUTTONDOWN:  # Checks for ANY mouse clicks

            # --------------------------------------------------------------------
            # Menu Clicks
            if State == "Menu":  # Below are ONLY menu screen actions
                if start_btn.collidepoint(mouse):  # if click start button
                    reset_game()
                    State = "Game"

                elif close_btn.collidepoint(mouse):  # if click quit button
                    pygame.quit()  # exit pygame
                    sys.exit()  # exit python

            # Game Over Clicks
            if State == "GameOver":
                # Click anywhere to restart
                State = "Menu"
    # ---------------------------------------------------------------------
    pygame.display.update()  # refreshes the window at the end of every while loop