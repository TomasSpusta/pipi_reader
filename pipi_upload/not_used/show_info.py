from lcd_display import display
from log import write_log

def log_display_print (log_msg, log_col, log_note, display_msg, print_msg):
    write_log (log_col, log_msg, log_note)
    display (display_msg, clear=True, backlight_status=True,sleep=2)
    print (str(print_msg))
        