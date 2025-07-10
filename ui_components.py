from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from keyboard_commands import insert_send_c, insert_send_v, insert_send_x, insert_send_z, insert_send_a, insert_send_text, insert_send_arrow
from check_language import insert_language_check

def insert_esc_hotkey_code(script_area):
    """Inserts AutoIt code to stop the script with the ESC key."""
    current_text = script_area.toPlainText()

    # Prepare the header and footer code
    header_code = "HotKeySet('{ESC}', 'End') ; Назначаем клавишу ESC для выхода из скрипта ; Проверка языка ввода\n"
    # Add conditional newlines before the footer if current_text is not empty and doesn't end with newlines
    footer_prefix = ""
    if current_text and not current_text.endswith("\n\n"):
        if current_text.endswith("\n"):
            footer_prefix = "\n"
        else:
            footer_prefix = "\n\n"

    footer_code = footer_prefix + "Func End()\n  Exit ; Завершает скрипт\nEndFunc\n"

    # Prepend header and append footer
    # Ensure header is at the very beginning and footer at the very end
    new_text = header_code + current_text + footer_code

    script_area.setPlainText(new_text)

class UIComponents:
    @staticmethod
    def create_buttons(parent):
        # Создание всех кнопок из метода initUI
        actions = [
            ('Left Click', 'left'),
            ('Right Click', 'right'),
            ('Move Mouse', 'move'),
            ('Drag', 'drag'),
            ('Click on Color', 'click_color'),
            ('Click on Color Area', 'click_color_area'),
            ('Ждем цвет пикселя', 'wait_color'),
            ('Ждем цвет в области', 'wait_color_area'),
            ('Скопировать цвет пикселя', 'copy_color'),
            ('Random Click in Area', 'random_area')
        ]
        buttons = []
        for label, action in actions:
            btn = QPushButton(label)
            print(f"Creating button: {label} with action: {action}")  # Отладочное сообщение
            btn.clicked.connect(lambda checked, act=action: parent.prepare_action(act))
            buttons.append(btn)
        return buttons

    @staticmethod
    def create_keyboard_buttons(parent):
        # Создание кнопок клавиатурных команд
        buttons = []
        keyboard_actions = [
            ('Проверка языка ввода', lambda: insert_language_check(parent.script_area)),
            ('Send Text', lambda: insert_send_text(parent.script_area)),
            ('CTRL + A', lambda: insert_send_a(parent.script_area)),
            ('CTRL + C', lambda: insert_send_c(parent.script_area)),
            ('CTRL + V', lambda: insert_send_v(parent.script_area)),
            ('CTRL + X', lambda: insert_send_x(parent.script_area)),
            ('CTRL + Z', lambda: insert_send_z(parent.script_area)),
            # New button for clipboard monitoring
            ('Ожидание изменения буфера', lambda: parent.script_area.insertPlainText(
                'Local $lastClip = ClipGet()\n'
                'While $lastClip == ClipGet()\n'
                '    Sleep(100)\n'
                'WEnd\n'
            )),
            # New button for Alt+Tab
            ('Alt + Tab', lambda: parent.script_area.insertPlainText(
                'Send("{ALTDOWN}{TAB}{ALTUP}")\n'
            )),
            # Добавляем кнопки стрелок
            ('↑ Вверх', lambda: insert_send_arrow(parent.script_area, 'up')),
            ('↓ Вниз', lambda: insert_send_arrow(parent.script_area, 'down')),
            ('← Влево', lambda: insert_send_arrow(parent.script_area, 'left')),
            ('→ Вправо', lambda: insert_send_arrow(parent.script_area, 'right')),
            # Добавляем кнопки для скролла мышкой
            ('Скролл мышкой вверх', lambda: parent.script_area.insertPlainText('MouseWheel("up",1)\n')),
            ('Скролл мышкой вниз', lambda: parent.script_area.insertPlainText('MouseWheel("down",1)\n')),
            # New button for ESC hotkey
            ('остановить скрипт по нажатию кнопки esc', lambda: insert_esc_hotkey_code(parent.script_area))
        ]
        for label, action in keyboard_actions:
            btn = QPushButton(label)
            btn.clicked.connect(action)
            buttons.append(btn)
        return buttons

    @staticmethod
    def create_delay_buttons(parent):
        # Создание кнопок задержки
        buttons = []
        delays = [50, 100, 200, 300, 500, 1000]
        for delay in delays:
            btn = QPushButton(f'Sleep {delay} ms')
            btn.clicked.connect(lambda checked, d=delay: parent.add_delay(d))
            buttons.append(btn)
        return buttons

    @staticmethod
    def create_comprehensive_keyboard_buttons(parent):
        # Comprehensive list of keyboard buttons with AutoIt code generation
        keyboard_buttons = [
            # Modifier Keys
            ('CTRL', 'Send("{CTRLDOWN}")'),
            ('ALT', 'Send("{ALTDOWN}")'),
            ('SHIFT', 'Send("{SHIFTDOWN}")'),
            ('WIN', 'Send("{WINDOWN}")'),

            # Function Keys
            ('F1', 'Send("{F1}")'),
            ('F2', 'Send("{F2}")'),
            ('F3', 'Send("{F3}")'),
            ('F4', 'Send("{F4}")'),
            ('F5', 'Send("{F5}")'),
            ('F6', 'Send("{F6}")'),
            ('F7', 'Send("{F7}")'),
            ('F8', 'Send("{F8}")'),
            ('F9', 'Send("{F9}")'),
            ('F10', 'Send("{F10}")'),
            ('F11', 'Send("{F11}")'),
            ('F12', 'Send("{F12}")'),

            # Navigation Keys
            ('HOME', 'Send("{HOME}")'),
            ('END', 'Send("{END}")'),
            ('PAGE UP', 'Send("{PGUP}")'),
            ('PAGE DOWN', 'Send("{PGDN}")'),
            ('INSERT', 'Send("{INS}")'),
            ('DELETE', 'Send("{DEL}")'),

            # Arrow Keys
            ('↑ UP', 'Send("{UP}")'),
            ('↓ DOWN', 'Send("{DOWN}")'),
            ('← LEFT', 'Send("{LEFT}")'),
            ('→ RIGHT', 'Send("{RIGHT}")'),

            # Special Keys
            ('ENTER', 'Send("{ENTER}")'),
            ('BACKSPACE', 'Send("{BACKSPACE}")'),
            ('TAB', 'Send("{TAB}")'),
            ('ESC', 'Send("{ESC}")'),
            ('SPACE', 'Send("{SPACE}")'),
            ('CAPS LOCK', 'Send("{CAPSLOCK}")'),
            ('NUM LOCK', 'Send("{NUMLOCK}")'),
            ('SCROLL LOCK', 'Send("{SCROLLLOCK}")'),

            # Numpad Keys
            ('NUMPAD 0', 'Send("{NUMPAD0}")'),
            ('NUMPAD 1', 'Send("{NUMPAD1}")'),
            ('NUMPAD 2', 'Send("{NUMPAD2}")'),
            ('NUMPAD 3', 'Send("{NUMPAD3}")'),
            ('NUMPAD 4', 'Send("{NUMPAD4}")'),
            ('NUMPAD 5', 'Send("{NUMPAD5}")'),
            ('NUMPAD 6', 'Send("{NUMPAD6}")'),
            ('NUMPAD 7', 'Send("{NUMPAD7}")'),
            ('NUMPAD 8', 'Send("{NUMPAD8}")'),
            ('NUMPAD 9', 'Send("{NUMPAD9}")'),
            ('NUMPAD .', 'Send("{NUMPADDOT}")'),
            ('NUMPAD +', 'Send("{NUMPADPLUS}")'),
            ('NUMPAD -', 'Send("{NUMPADMINUS}")'),
            ('NUMPAD *', 'Send("{NUMPADMULT}")'),
            ('NUMPAD /', 'Send("{NUMPADDIV}")'),
        ]

        buttons = []
        for label, code in keyboard_buttons:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, c=code: parent.script_area.insertPlainText(c + '\n'))
            buttons.append(btn)
        return buttons
