import pygame
def countdown(Font, Black, Window):
    Current = 60
    STRcurrent = "60"
    while Current != 0:
        timeletters = Font.render(STRcurrent, False, Black)
        Window.blit(timeletters,(700,50))
        #Current -= 1
        #STRcurrent = str(Current)
        clearnumber = pygame.Rect(700, 50, 40, 40)
        pygame.draw.rect(Window, ((Black)), clearnumber, 1)
        Current = 0