# ----------------------------------------------------------------------------------------------
# GLOBAL VARIABLES AND LIBRARIES
import sys  # imports the sys library
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

Window = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT))  # creates object window with parameters for window width and height

pygame.display.set_caption("Platforms and aliens")  # renames the window to the name of the game

clock = pygame.time.Clock()  # creates object clock which tracks time
#-----------------------------------------------------------------------------------------------
#Create Class "Player"
class Knight:
    def __init__(self):
        self.Knightsprite = pygame.image.load("knightsprite.png")  # Creates surface Playersprite with image knightsprite.png
        pygame.Surface.convert_alpha(self.Knightsprite)  # puts surface in a format suitable for quick blitting (movement)
        self.KnightHitbox = pygame.Rect(300,400,50,75)
        self.Knight_X = 300
        self.Knight_Y = 400
        #self.Player_Position = "find centre of sprite png"

Player = Knight() # creates object player from class Knight

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
#EVENT HANDLER
while True:

    clock.tick(60)  # at most 60 frames should pass in a second (FPS cap)
    mouse = pygame.mouse.get_pos()

    # Set keys to be held by default (SPACE exempt)
    pygame.key.set_repeat(100)

    for event in pygame.event.get():  # event handler: any user driven event is listed under here

        if event.type == pygame.QUIT:  # if the "X" on the window is clicked
            pygame.quit()  # kills the game window
            sys.exit()  # exits the program

        if event.type == Decrease and State == "Game" and Current != -1:
            Time_Module.countdown(Font, Black, Window, Current)
            Current -= 1
           # if Current == -1: #This will trigger the gameover condition once I have written it
                #Game_State.Gameover()

        #Player movement

        if State == "Game": #things will happen during gameplay
            if event.type == pygame.KEYDOWN: # Move right
                if event.key == pygame.K_RIGHT:
                    Player.Knight_X += 20

            if event.type == pygame.KEYDOWN: # Move left
                if event.key == pygame.K_LEFT:
                    Left = list()
                    Left.append("LEFT")
                    #print("LEFT")
                    for x in Left:
                        Player.Knight_X -= 20

            if event.type == pygame.KEYUP: # Jump
                if event.key == pygame.K_SPACE:
                    print("SPACE")
            Window.blit(Player.Knightsprite, (Player.Knight_X, Player.Knight_Y))  # initial sprite draw

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
    pygame.display.update()  # refreshes the window