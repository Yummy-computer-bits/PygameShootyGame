import pygame
def countdown(Font, Black, Window, Current):
    numbersdown = pygame.Rect(698, 49, 35, 26.5)  # declares a white rectangle inside the border
    numberborder = pygame.Rect(695, 46, 41, 32.5)  # decleares a border around the time remaining number
    pygame.draw.rect(Window, ((Black)), numberborder, 3)  # draws the border around the time

    pygame.draw.rect(Window, ((255, 255, 255)), numbersdown, 0)  # clears the displayed time with white pixels
    STRcurrent = str(Current) # typecasts current into a seperate variable as a string
    timeletters = Font.render(STRcurrent, False, Black)  # RE-declares surface timeletters (it doesnt automatically update!)
    Window.blit(timeletters, (700, 50))  # draws surface timeletters on surface window
