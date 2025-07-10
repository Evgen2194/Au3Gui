def insert_move_command(script_area, x, y):
    script_area.insertPlainText(f'MouseMove({x}, {y})\n\n')