from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor

def insert_right_click_command(script_area: QTextEdit, x, y):
    command = f'MouseClick("right", {x}, {y})\n\n'
    cursor = script_area.textCursor()
    cursor.insertText(command)
    cursor.movePosition(QTextCursor.NextBlock)
    cursor.movePosition(QTextCursor.NextBlock)
    script_area.setTextCursor(cursor)