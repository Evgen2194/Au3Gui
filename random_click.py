def generate_random_click_code(coordinates):
    code = 'Global $aCoordinates[{}][2] = '.format(len(coordinates))
    code += str(coordinates).replace('[', '[').replace(']', ']')
    code += '\nLocal $iRandomIndex = Random(0, UBound($aCoordinates) - 1, 1)\n'
    code += 'MouseClick("left", $aCoordinates[$iRandomIndex][0], $aCoordinates[$iRandomIndex][1])\n'
    return code