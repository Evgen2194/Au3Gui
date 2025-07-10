def generate_random_click_area_code(x_min, x_max, y_min, y_max):
    code = f'MouseClick("left", Random({x_min}, {x_max}, 1), Random({y_min}, {y_max}, 1))\n'
    return code