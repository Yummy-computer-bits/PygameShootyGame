# ----------------------------------------------------------------------------------------------
# GLOBAL VARIABLES AND LIBRARIES
import sys  # imports the sys library
import pygame  # imports the pygame library
from pygame import K_EURO, K_RIGHT  # imports specific key constants from pygame

import Game_State  # imports the local Game_State module
import Time_Module  # imports the local Time_Module module

pygame.init()  # initialises ALL imported pygame modules (the constructor)

# COLOURS
White = (255, 255, 255)  # stores the colour white
Black = (0, 0, 0)  # stores the colour black
Blue = (0, 0, 255)  # stores the colour blue
Red = (255, 0, 0)  # stores the colour red
Green = (0, 255, 0)  # stores the colour green
Yellow = (255, 255, 0)  # stores the colour yellow

# INITIAL CURRENT TIME
Current = 60  # sets the starting value for the countdown timer

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
            self.Knightsprite = pygame.transform.scale(self.Knightsprite, (40, 70))  # resizes the image
        except:
            # Fallback if image missing
            self.Knightsprite = pygame.Surface((40, 70))  # creates a blank surface if image fails
            self.Knightsprite.fill(Blue)  # fills the blank surface with blue

        self.rect = pygame.Rect(300, 400, 40, 70)  # Use a rect for collision handling
        self.vel_y = 0  # Vertical velocity for gravity
        self.jump_power = -15  # How high we jump
        self.grounded = False  # Are we on the floor?

    def draw(self):  # a method that redraws the player sprite
        Window.blit(self.Knightsprite,
                    (self.rect.x, self.rect.y))  # draws the player sprite every frame with updated x and y positions
        # pygame.draw.rect(Window, Black, self.rect, 1) # draws the player sprite hitbox every frame with updated x and y positions

    def move(self, platforms):  # allows the user to control the player sprite
        dx = 0  # resets the horizontal change
        dy = 0  # resets the vertical change

        kbin = pygame.key.get_pressed()  # event kbin (K-ey B-oard + IN-put) is triggered after a keyboard input
        if kbin[pygame.K_LEFT]:  # should the keyboard input be the LEFT arrow key
            dx -= 5  # move left by 5 pixels
        if kbin[pygame.K_RIGHT]:  # should the keyboard input be the RIGHT arrow key
            dx += 5  # move right by 5 pixels

        # Gravity
        self.vel_y += 0.8  # adds gravity to vertical velocity
        if self.vel_y > 10:  # caps the falling speed
            self.vel_y = 10  # sets max falling speed to 10
        dy += self.vel_y  # applies velocity to vertical change

        # Check for collision with platforms (X axis)
        self.rect.x += dx  # applies horizontal movement
        # (Simple collision: if we hit a wall, we stop, but for this beginner code, we will focus on Y axis landing)

        # Check for collision with platforms (Y axis)
        self.rect.y += dy  # applies vertical movement
        self.grounded = False  # assumes player is in the air until checked

        for plat in platforms:  # loops through all platforms
            if self.rect.colliderect(plat.rect):  # checks if player rect overlaps platform rect
                # Check if falling down onto platform
                if self.vel_y > 0:  # if moving downwards
                    self.rect.bottom = plat.rect.top  # snaps player bottom to platform top
                    self.vel_y = 0  # stops downward velocity
                    self.grounded = True  # sets grounded flag to true

        # Screen boundaries
        if self.rect.bottom > SCREEN_HEIGHT:  # checks if player hits bottom of screen
            self.rect.bottom = SCREEN_HEIGHT  # keeps player inside screen
            self.vel_y = 0  # stops downward velocity
            self.grounded = True  # sets grounded flag to true

    def jump(self):  # method to make player jump
        if self.grounded:  # checks if player is on the ground
            self.vel_y = self.jump_power  # applies negative velocity to move up
            self.grounded = False  # sets grounded flag to false


# -----------------------------------------------------------------------------------------------
# Create Class "Platform"
class Platform:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)  # creates a rectangle object for the platform

    def draw(self):
        pygame.draw.rect(Window, Black, self.rect)  # draws the platform rectangle on the window


# Create Class "Alien"
class Alien:
    def __init__(self, x, y, distance):
        self.rect = pygame.Rect(x, y, 40, 40)  # creates a rectangle object for the alien
        self.start_x = x  # stores the starting x position
        self.distance = distance  # stores the max patrol distance
        self.direction = 1  # sets the initial moving direction (1 is right, -1 is left)
        self.speed = 2  # sets the movement speed

    def move(self):
        self.rect.x += self.speed * self.direction  # moves the alien
        if self.rect.x > self.start_x + self.distance or self.rect.x < self.start_x:  # checks if patrol limit reached
            self.direction *= -1  # reverses direction

    def draw(self):
        pygame.draw.rect(Window, Red, self.rect)  # draws the alien rectangle on the window


# Create Class "Star" (Goal)
class Star:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)  # creates a rectangle object for the goal

    def draw(self):
        pygame.draw.rect(Window, Yellow, self.rect)  # draws the goal rectangle on the window


# -----------------------------------------------------------------------------------------------
# Decrease time
Decrease = pygame.USEREVENT  # defines a custom user event
pygame.time.set_timer(Decrease, 1000)  # sets the timer to trigger the event every 1000ms (1 second)

# INITIALIZE OBJECTS
Player = Knight()  # creates object player from class Knight

# Create a level using a list of platforms
platforms = [
    Platform(0, 580, 800, 20),  # Ground platform
    Platform(200, 450, 200, 20),  # floating platform
    Platform(400, 350, 200, 20),  # floating platform
    Platform(150, 250, 200, 20),  # floating platform
    Platform(400, 100, 150, 20)  # floating platform
]

# Create Aliens
aliens = [
    Alien(200, 210, 150),  # creates an alien at specific coords with patrol distance
    Alien(400, 310, 150)  # creates another alien
]

# Create Goal
Goal = Star(450, 50)  # creates the goal object


def reset_game():
    global Current, Player  # allows function to modify global variables
    Current = 60  # resets timer to 60
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
        start_btn = Game_State.startbutton(White, Black, Window, Font)  # draws start button and stores rect
        close_btn = Game_State.quitbutton(White, Black, Window, Font)  # draws quit button and stores rect

    # 2. GAME STATE LOGIC
    elif State == "Game":  # movement only exists during gameplay
        Window.fill(White)  # fills the screen with white pixels

        # Draw Platforms
        for plat in platforms:  # loops through platform list
            plat.draw()  # draws the platform

        # Draw and Move Aliens
        for alien in aliens:  # loops through alien list
            alien.move()  # updates alien position
            alien.draw()  # draws the alien
            if Player.rect.colliderect(alien.rect):  # checks collision between player and alien
                State = "GameOver"  # changes state to game over
                Won = False  # sets win status to false

        # Draw Goal
        Goal.draw()  # draws the goal
        if Player.rect.colliderect(Goal.rect):  # checks collision between player and goal
            State = "GameOver"  # changes state to game over
            Won = True  # sets win status to true

        Player.move(platforms)  # calls the method that lets the user control the player sprite
        Player.draw()  # the sprite is drawn from the class definition

        Time_Module.countdown(Font, Black, Window, Current)  # re-draws the time on the screen

    # 3. GAME OVER STATE LOGIC
    elif State == "GameOver":  # GAME OVER SCREEN
        Window.fill(Black)  # fills screen with black
        restart_rect = Game_State.gameover_ui(Window, Font, White, Black, Won)  # draws game over UI

    # Event Handler
    for event in pygame.event.get():  # event handler: any user driven event is listed under here

        if event.type == pygame.QUIT:  # if the "X" on the window is clicked
            pygame.quit()  # kills the game window
            sys.exit()  # exits the program

        # TIMER logic
        if event.type == Decrease and State == "Game":  # if 1 second passes and game is running
            if Current > 0:  # if time remains
                Current -= 1  # decrease time by 1
            else:
                # Time ran out
                State = "GameOver"  # change state to game over
                Won = False  # set win status to false

        if event.type == pygame.KEYDOWN:  # checks if a key is pressed down
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:  # checks for spacebar or up arrow
                if State == "Game":  # ensures player can only jump during gameplay
                    Player.jump()  # calls jump method

        if event.type == pygame.MOUSEBUTTONDOWN:  # Checks for ANY mouse clicks

            # --------------------------------------------------------------------
            # Menu Clicks
            if State == "Menu":  # Below are ONLY menu screen actions
                if start_btn.collidepoint(mouse):  # if click start button
                    reset_game()  # calls the reset function
                    State = "Game"  # changes state to playing

                elif close_btn.collidepoint(mouse):  # if click quit button
                    pygame.quit()  # exit pygame
                    sys.exit()  # exit python

            # Game Over Clicks
            if State == "GameOver":
                # Click anywhere to restart
                State = "Menu"  # returns to menu
    # ---------------------------------------------------------------------
    pygame.display.update()  # refreshes the window at the end of every while loop