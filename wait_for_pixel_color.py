from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor

def wait_for_pixel_color(script_area: QTextEdit, x, y, color, display_scaling=150):
    # Преобразуем координаты обратно для AutoIt скрипта
    screen_x = int(x * (display_scaling / 100))
    screen_y = int(y * (display_scaling / 100))
    cursor = script_area.textCursor()
    cursor.insertText(f'While PixelGetColor({screen_x}, {screen_y}) <> {color}\n')
    cursor.insertText('    Sleep(100)\n')
    cursor.insertText('Wend\n\n')
    cursor.movePosition(QTextCursor.NextBlock)
    cursor.movePosition(QTextCursor.NextBlock)
    script_area.setTextCursor(cursor)