def insert_send_c(script_area):
    script_area.insertPlainText('Send("^c")\n\n')

def insert_send_v(script_area):
    script_area.insertPlainText('Send("^v")\n\n')

def insert_send_x(script_area):
    script_area.insertPlainText('Send("^x")\n\n')

def insert_send_z(script_area):
    script_area.insertPlainText('Send("^z")\n\n')

def insert_send_a(script_area):
    script_area.insertPlainText('Send("^a")\n\n')

def insert_send_text(script_area):
    script_area.insertPlainText('Local $text = "привет"\nClipPut($text) ; Помещаем текст в буфер обмена\nSend("^v") ; Вставляем текст через Ctrl+V\n\n')

def insert_send_arrow(script_area, direction):
    """
    Генерирует код для нажатия стрелки в AutoIt
    :param script_area: Текстовое поле для вставки кода
    :param direction: Направление стрелки ('up', 'down', 'left', 'right')
    """
    arrow_map = {
        'up': '{UP}',
        'down': '{DOWN}',
        'left': '{LEFT}',
        'right': '{RIGHT}'
    }
    
    if direction not in arrow_map:
        return
    
    code = f'Send("{arrow_map[direction]}")\n'
    
    cursor = script_area.textCursor()
    cursor.insertText(code)
    script_area.setTextCursor(cursor)