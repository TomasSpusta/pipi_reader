from LCD_display import display
try:
    display(        "Pokus",        " ",        " ",        " ", True, True, 2
    )
except Exception as e:
    display(        str(e),        " ",        " ",        " ", True, True, 2
    )