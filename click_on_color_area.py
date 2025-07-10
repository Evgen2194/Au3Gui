def click_on_color_area(script_area, x1, y1, x2, y2, color, button='left', scaling=100):
    # Преобразуем координаты в целые числа
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    
    # Вычисляем коэффициент масштабирования для клика
    scale_factor = 100 / scaling
    
    # Генерируем код для поиска цвета в области и клика
    code = (
        f'Local $aCoord = PixelSearch({x1}, {y1}, {x2}, {y2}, {color}, 1)\n\n'
        'If IsArray($aCoord) Then\n'
        f'    MouseClick("{button}", $aCoord[0]*{scale_factor}, $aCoord[1]*{scale_factor}, 1)\n'
        'Else\n'
        '    ;empty\n'
        'EndIf\n'
    )
    
    script_area.insertPlainText(code)
