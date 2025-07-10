import os
import sys
import importlib

def check_module(module_name):
    try:
        importlib.import_module(module_name)
        print(f"✓ {module_name} successfully imported")
    except ImportError as e:
        print(f"✗ Failed to import {module_name}: {str(e)}")

print("Python Path:")
for path in sys.path:
    print(f"  {path}")

print("\nChecking required modules:")
modules_to_check = [
    'PyQt5.QtWidgets',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'win32gui',
    'drag_function',
    'left_click',
    'right_click',
    'click_on_color',
    'wait_for_pixel_color',
    'move_mouse',
    'keyboard_commands',
    'delay_commands',
    'random_click',
    'random_click_area',
    'ui_components',
    'event_handlers',
    'script_generator',
    'utils'
]

for module in modules_to_check:
    check_module(module)
