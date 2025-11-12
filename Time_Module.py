import pygame
def countdown(Font, Black, Window):

    numbersdown = pygame.Rect(698, 49, 35, 26.5)  # declares a white rectangle inside the border
    numberborder = pygame.Rect(695, 46, 41, 32.5)  # decleares a border around the time remaining number
    pygame.draw.rect(Window, ((Black)), numberborder, 3)  # draws the border around the time

    Current = 60 # sets the initial time at 60 "seconds". Will count down
    STRcurrent = "60" # the intial time represented as a string for display purposes

    while Current != 0: #if time hasn't run out yet...
        pygame.draw.rect(Window, ((255, 255, 255)), numbersdown, 0)  # clears the displayed time with white pixels
        #Current -= 1 #derecments current by 1 "second" # needs tick based system to go by 1 a second
        STRcurrent = "59" # typecasts current into a seperate variable as a string
        timeletters = Font.render(STRcurrent, False, Black)  # RE-declares surface timeletters (it doesnt automatically update!)
        Window.blit(timeletters, (700, 50))  # draws surface timeletters on surface window
        Current = 0 # exits loop/kills program early