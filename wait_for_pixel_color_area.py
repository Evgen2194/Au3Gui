def wait_for_pixel_color_area(script_area, x1, y1, x2, y2, color, scaling=100):
    # Преобразуем логические координаты в физические (экранные) координаты
    # x1, y1, x2, y2 приходят уже как int из event_handler

    screen_x1 = int(x1 * (scaling / 100))
    screen_y1 = int(y1 * (scaling / 100))
    screen_x2 = int(x2 * (scaling / 100))
    screen_y2 = int(y2 * (scaling / 100))
    
    # Генерируем код для ожидания появления цвета в области
    # PixelSearch в AutoIt ожидает экранные координаты
    code = (
        'While 1\n'
        f'    Local $aCoord = PixelSearch({screen_x1}, {screen_y1}, {screen_x2}, {screen_y2}, {color}, 1)\n'
        '    If IsArray($aCoord) Then\n'
        '        ExitLoop\n'
        '    Else\n'
        '        ;empty\n'
        '    EndIf\n'
        '    Sleep(100)\n'
        'WEnd\n'
    )
    
    script_area.insertPlainText(code)
