def countdown(Font, Black, Window):
    TimeLetters = Font.render(STRcurrent, False, Black)
    Window.blit(TimeLetters, (200,400))

Current = 60
STRcurrent = str(Current)