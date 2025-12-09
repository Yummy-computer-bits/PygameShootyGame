# ----------------------------------------------------------------------------------------------
# GLOBAL VARIABLES AND LIBRARIES
import sys  # imports the sys library
from shutil import which

import pygame  # imports the pygame library
from pygame import K_EURO, K_RIGHT

import Game_State
import Time_Module

pygame.init()  # initialises ALL imported pygame modules (the constructor)

#COLOURS
White = (255, 255, 255)  # stores the colour white
Black = (0,0,0)
Blue = (0,0,255)

#INITIAL CURRENT TIME
Current = 60

#GLOBAL FONT
Font = pygame.font.SysFont(None, 40, False, False)  # creates font and size

#Start on MENU
State = "Menu"  # sets the state to "Menu" when the game opens for the first time
#-----------------------------------------------------------------------------------------------
#WINDOW SETTINGS

SCREEN_WIDTH, SCREEN_HEIGHT = (800, 600)  # a tuple which will dictate window dimensions

Window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # creates object window with parameters for window width and height

pygame.display.set_caption("Platforms and aliens")  # renames the window to the name of the game

clock = pygame.time.Clock()  # creates object clock which tracks time
#-----------------------------------------------------------------------------------------------
#Create Class "Player"
class Knight:
    def __init__(self):
        self.Knightsprite = pygame.image.load("knightsprite.png")  # Creates surface Knightsprite with image knightsprite.png
        pygame.Surface.convert_alpha(self.Knightsprite)  # puts surface in a format suitable for quick blitting (movement)
        self.Knight_X = 300
        self.Knight_Y = 400

    def draw(self): # a method that redraws the player sprite
        Window.blit(Player.Knightsprite, (Player.Knight_X, Player.Knight_Y)) # draws the player sprite every frame with updated x and y positions
        pygame.draw.rect(Window, Blue, (self.Knight_X +10, self.Knight_Y +5, 30, 70), 1) # draws the player sprite hitbox every frame with updated x and y positions

    def move(self): # allows the user to control the player sprite

        kbin = pygame.key.get_pressed() #event kbin (K-ey B-oard + IN-put) is triggered after a keyboard input
        if kbin[pygame.K_LEFT]: # should the keyboard input be the LEFT arrow key
            self.Knight_X -= 10
        if kbin[pygame.K_RIGHT]:
            self.Knight_X += 10

Player = Knight() # creates object player from class Knight

#-----------------------------------------------------------------------------------------------
#Create Class "Platform"

#-----------------------------------------------------------------------------------------------
#Decrease time
Decrease = pygame.USEREVENT

pygame.time.set_timer(Decrease, 1000)
#-----------------------------------------------------------------------------------------------
#GAME STATE
if State == "Menu": # MENU SCREEN
    Window.fill(Blue)  # changes the window to blue
    Game_State.gamestate(State, White, Black, Window, Font)  # Calls game state with State string, colours and global font as arguments

    start = Game_State.startbutton(White, Black, Window, Font)  # calls startbutton function. this creates the startbutton, text and border
    close = Game_State.quitbutton(White, Black, Window, Font)  # calls quitbutton function. this creates the quitbutton, text and border)
# ----------------------------------------------------------------------------------------------
#Gameplay Loop
while True:
    clock.tick(60)  # at most 60 frames should pass in a second (FPS cap)
    mouse = pygame.mouse.get_pos() # gets the mouse position at all times

    #player movement
    if State == "Game": #movement only exists during gameplay

        Player.move()  # calls the method that lets the user control the player sprite

        Window.fill(White)  # fills the screen with white pixels
        Time_Module.countdown(Font, Black, Window, Current)  # re-draws the time on the screen
        Player.draw()  # the sprite is drawn from the class definition

    #Event Handler
    for event in pygame.event.get():  # event handler: any user driven event is listed under here

        if event.type == pygame.QUIT:  # if the "X" on the window is clicked
            pygame.quit()  # kills the game window
            sys.exit()  # exits the program

        if event.type == Decrease and State == "Game" and Current != -1:
            Time_Module.countdown(Font, Black, Window, Current)
            Current -= 1
           # if Current == -1: #This will trigger the gameover condition once I have written it
                #Game_State.Gameover()

        if event.type == pygame.MOUSEBUTTONDOWN: # Checks for ANY mouse clicks

#--------------------------------------------------------------------
            #Menu Clicks
            if State == "Menu": # Below are ONLY menu screen actions

                if start.collidepoint(mouse): # if click start button
                    Window.fill(White) # Clears screen of menu buttons
                    State = "Game" # State shifts to gameplay (kills use of menu buttons, and runs gameplay modules)

                    pygame.display.update()  # refreshes the window now the main menu needs to disappear

                elif close.collidepoint(mouse): # if click quit button
                    pygame.quit() # exit pygame
                    sys.exit() # exit python
#---------------------------------------------------------------------
    pygame.display.update()  # refreshes the window at the end of every while loop