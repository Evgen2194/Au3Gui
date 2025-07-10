def wait_for_pixel_color_area(script_area, x1, y1, x2, y2, color, scaling=100):
    # Преобразуем координаты в целые числа
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    
    # Генерируем код для ожидания появления цвета в области
    code = (
        'While 1\n'
        f'    Local $aCoord = PixelSearch({x1}, {y1}, {x2}, {y2}, {color}, 1)\n'
        '    If IsArray($aCoord) Then\n'
        '        ExitLoop\n'
        '    Else\n'
        '        ;empty\n'
        '    EndIf\n'
        '    Sleep(100)\n'
        'WEnd\n'
    )
    
    script_area.insertPlainText(code)
