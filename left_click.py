from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor

def insert_left_click_command(script_area: QTextEdit, x, y):
    print(f"Inserting left click command at x={x}, y={y}")  # Отладочное сообщение
    if not isinstance(script_area, QTextEdit):
        print(f"Error: script_area is not QTextEdit, it is {type(script_area)}")
        return
    cursor = script_area.textCursor()
    print(f"Current cursor position: {cursor.position()}")  # Отладочное сообщение
    try:
        cursor.insertText(f'MouseClick("left", {x}, {y})\n\n')
        print(f"Text inserted. New cursor position: {cursor.position()}")  # Отладочное сообщение
        cursor.movePosition(QTextCursor.NextBlock)
        cursor.movePosition(QTextCursor.NextBlock)
        script_area.setTextCursor(cursor)
        print("Left click command inserted")  # Отладочное сообщение
    except Exception as e:
        print(f"Error while inserting text: {str(e)}")

def insert_left_click(script_area: QTextEdit, x, y):
    print("insert_left_click called")  # Отладочное сообщение
    print(f"script_area type: {type(script_area)}")  # Отладочное сообщение
    insert_left_click_command(script_area, x, y)