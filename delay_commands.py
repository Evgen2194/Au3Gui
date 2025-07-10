# delay_commands.py
def insert_sleep_command(script_area, ms):
    script_area.insertPlainText(f'Sleep({ms})\n\n')