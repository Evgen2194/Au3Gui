from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor

def insert_language_check(script_area: QTextEdit):
    code = '''; Проверка языка ввода
If IsRussianKeyboardLayout() Then
    MsgBox(0, "Ошибка", "Установите английскую (США) раскладку клавиатуры!")
    Exit
EndIf

; Функция для проверки, установлен ли русский язык
Func IsRussianKeyboardLayout()
    ; Получаем текущий язык ввода
    Local $keyboardLayout = DllCall("user32.dll", "int", "GetKeyboardLayout", "int", 0)

    ; Проверяем, соответствует ли раскладка русскому языку (код 0x0419)
    If BitAND($keyboardLayout[0], 0xFFFF) = 0x0419 Then
        Return True
    Else
        Return False
    EndIf
EndFunc\n\n'''
    
    cursor = script_area.textCursor()
    cursor.insertText(code)
    script_area.setTextCursor(cursor)
