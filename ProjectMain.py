# ----------------------------------------------------------------------------------------------
# GLOBAL VARIABLES AND LIBRARIES
import sys  # imports the sys library
import pygame  # imports the pygame library
import Game_State
import Time_Module

pygame.init()  # initialises ALL imported pygame modules (the constructor)

#COLOURS
White = (255, 255, 255)  # stores the colour white
Black = (0,0,0)
Blue = (0,0,255)

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

    for event in pygame.event.get():  # event handler: any user driven event is listed under here

        if event.type == pygame.QUIT:  # if the "X" on the window is clicked
            pygame.quit()  # kills the game window
            sys.exit()  # exits the program

        if event.type == pygame.MOUSEBUTTONDOWN: # Checks for ANY mouse clicks

#--------------------------------------------------------------------
            #Menu Clicks
            if State == "Menu": # Below are ONLY menu screen actions
                if start.collidepoint(mouse): # if click start button
                    Window.fill(White) # Clears screen of menu buttons
                    State = "Game"
                    Game_State.setgame(Font, Black, Window) # State shifts to gameplay (kills use of menu buttons, and runs gameplay modules)
                elif close.collidepoint(mouse): # if click quit button
                    pygame.quit() # exit pygame
                    sys.exit() # exit python
#---------------------------------------------------------------------

    pygame.display.update()  # refreshes the window