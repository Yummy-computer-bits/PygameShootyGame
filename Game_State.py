# ----------------------------------------------------------------------------------------------
#GAME STATE FUNCTION
import pygame  # imports the pygame library
def startbutton(White, Black, Window, Font):

    start = pygame.Rect(150, 250, 200, 100)  # Start button, rect(left, top, width, height)
    startborder = pygame.Rect(150, 250, 200, 100)  # starbutton border


    pygame.draw.rect(Window, White, start, 0)  # draw start button
    pygame.draw.rect(Window, Black, startborder, 10)  # draw a border around startbutton

    startwords = Font.render("START GAME", False, Black)  # creates surface for "START GAME" to be displayed
    Window.blit(startwords, (160, 290))  # draws text "startwords" on the game window
    return start

def quitbutton(White, Black, Window, Font):

    close = pygame.Rect(450, 250, 200, 100)  # Quit button
    closeborder = pygame.Rect(450, 250, 200, 100)  # quitbutton border

    pygame.draw.rect(Window, White, close, 0)  # draw quit button
    pygame.draw.rect(Window, Black, closeborder, 10)  # draw a border around quit button

    closewords = Font.render("QUIT GAME", False, Black)
    Window.blit(closewords, (470, 290))

    return close


def gamestate(State, White, Black, Window, Font):  # is called whenever game over condition may be met, or to launch menu
    if State == "Menu":  # creates start or exit buttons once the state is MENU

        titlewords = Font.render("PLATFORMS AND ALIENS", False, White) # creates surface for title screen words
        Window.blit(titlewords, (225, 100)) # draws title screen words on the screen