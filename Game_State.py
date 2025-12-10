# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# GAME STATE FUNCTION
import pygame  # imports the pygame library
import Time_Module  # imports the local Time_Module module


# CREATE MAIN MENU-------------------------------------------------------------------------------
def startbutton(White, Black, Window, Font):
    start = pygame.Rect(150, 250, 200, 100)  # Start button, rect(left, top, width, height)
    startborder = pygame.Rect(150, 250, 200, 100)  # starbutton border

    pygame.draw.rect(Window, White, start, 0)  # draw start button
    pygame.draw.rect(Window, Black, startborder, 10)  # draw a border around startbutton

    startwords = Font.render("START GAME", False, Black)  # creates surface for "START GAME" to be displayed
    Window.blit(startwords, (160, 290))  # draws text "startwords" on the game window
    return start  # returns the start button rectangle for collision detection


def quitbutton(White, Black, Window, Font):
    close = pygame.Rect(450, 250, 200, 100)  # Quit button
    closeborder = pygame.Rect(450, 250, 200, 100)  # quitbutton border

    pygame.draw.rect(Window, White, close, 0)  # draw quit button
    pygame.draw.rect(Window, Black, closeborder, 10)  # draw a border around quit button

    closewords = Font.render("QUIT GAME", False, Black)  # creates surface with text
    Window.blit(closewords, (470, 290))  # draws the closewords surface on surface window with parameters x.y

    return close  # returns the quit button rectangle for collision detection


def gamestate(State, White, Black, Window,
              Font):  # is called whenever game over condition may be met, or to launch menu
    if State == "Menu":  # creates start or exit buttons once the state is MENU

        titlewords = Font.render("PLATFORMS AND ALIENS", False, White)  # creates surface for title screen words
        Window.blit(titlewords, (225, 100))  # draws title screen words on the screen


# Gameover Routine
def gameover_ui(Window, Font, White, Black, did_win):
    # a surprise tool that'll help us later!! -> NOW IMPLEMENTED

    if did_win:  # checks if the player won
        msg = "YOU WIN! CLICK TO RESTART"  # sets the victory message
        color = (0, 255, 0)  # Green
    else:  # if the player lost
        msg = "GAME OVER! CLICK TO RESTART"  # sets the game over message
        color = (255, 0, 0)  # Red

    text_surf = Font.render(msg, True, color)  # renders the text surface with the specific message and colour
    text_rect = text_surf.get_rect(center=(400, 300))  # centers the text rectangle on the screen
    Window.blit(text_surf, text_rect)  # draws the text surface onto the window

    return pygame.Rect(0, 0, 800, 600)  # Returns a rect covering screen to detect clicks