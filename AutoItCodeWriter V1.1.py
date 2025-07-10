import os
import sys

# Add script directory to path first
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Add embedded Python directory to path
python_embedded_dir = os.path.join(script_dir, 'python_embedded')
if os.path.exists(python_embedded_dir):
    os.environ['PATH'] = f"{python_embedded_dir};{python_embedded_dir}\\Scripts;{os.environ['PATH']}"
    sys.path.extend([
        python_embedded_dir,
        os.path.join(python_embedded_dir, 'Lib', 'site-packages'),
        os.path.join(python_embedded_dir, 'Lib', 'site-packages', 'win32'),
        os.path.join(python_embedded_dir, 'Lib', 'site-packages', 'win32', 'lib'),
        os.path.join(python_embedded_dir, 'Lib', 'site-packages', 'pywin32_system32')
    ])

import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit,
                            QScrollArea)
from PyQt5.QtCore import Qt, QTimer, QEvent, QMetaType
from PyQt5.QtGui import QTextCursor
import win32gui
from drag_function import DragHandler
from left_click import insert_left_click
from right_click import insert_right_click_command
from click_on_color import click_on_color
from wait_for_pixel_color import wait_for_pixel_color
from move_mouse import insert_move_command
from keyboard_commands import insert_send_c, insert_send_v, insert_send_x, insert_send_z
from delay_commands import insert_sleep_command
from random_click import generate_random_click_code
from random_click_area import generate_random_click_area_code
from ui_components import UIComponents
from event_handlers import EventHandler
from script_generator import ScriptGenerator
from utils import Utils

# Регистрируем QTextCursor для использования в сигналах
QMetaType.type("QTextCursor")

class AutoItScriptGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_variables()
        self.auto_it_path = Utils.load_config()
        self.initUI()
        self.event_handler = EventHandler(self)
        QApplication.instance().installEventFilter(self)
        
        # Устанавливаем таймер для проверки состояния клавиши Ctrl
        self.ctrl_check_timer = QTimer()
        self.ctrl_check_timer.timeout.connect(self.check_ctrl_state)
        self.ctrl_check_timer.start(50)  # Проверка каждые 50мс

    def check_ctrl_state(self):
        # Проверяем состояние клавиши Ctrl через win32api
        import win32api
        ctrl_state = win32api.GetKeyState(0x11) & 0x8000
        print(f"Checking Ctrl state: {ctrl_state}")  # Отладочное сообщение
        
        if ctrl_state and not self.is_ctrl_pressed:
            print("Ctrl key pressed - triggering handler")  # Отладочное сообщение
            if self.click_type:  # Проверяем, есть ли активное действие
                print(f"Active click type: {self.click_type}")  # Отладочное сообщение
                x, y = win32api.GetCursorPos()
                scaled_x = int(x * (100 / self.display_scaling))
                scaled_y = int(y * (100 / self.display_scaling))
                print(f"Mouse position: {scaled_x}, {scaled_y}")  # Отладочное сообщение
                if self.event_handler.handle_global_ctrl_press(None):
                    self.is_ctrl_pressed = True
        elif not ctrl_state and self.is_ctrl_pressed:
            print("Ctrl key released")  # Отладочное сообщение
            self.is_ctrl_pressed = False
            self.event_handler.handle_global_ctrl_release(None)

    def init_variables(self):
        self.click_type = None
        self.drag_coordinates = []
        self.display_scaling = 150
        self.is_ctrl_pressed = False
        self.ctrl_press_count = 0
        self.loop_count = 1
        self.is_collecting_coords = False
        self.coordinates_collected = []
        self.coord_selection_count = 0
        self.area_coordinates = []
        self.is_area_selection_active = False
        self.script_commands = []
        self.num_coordinates = 0
        self.drag_handler = DragHandler(self.display_scaling, self.insert_script_command)
        self.is_always_on_top = False
        self.font_size = 12  # Начальный размер шрифта
        # Add coordinate tracking timer
        self.coord_timer = QTimer()
        self.coord_timer.timeout.connect(self.update_coordinates)
        self.coord_timer.start(100)  # Update every 100ms

    def eventFilter(self, obj, event):
        return self.event_handler.handle_key_event(event)

    def initUI(self):
        self.setWindowTitle('AutoIt Script Generator')
        self.setGeometry(100, 100, 1200, 1200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Store sidebar as an instance attribute
        self.sidebar_widget = QWidget()
        self.sidebar = QVBoxLayout(self.sidebar_widget)
        main_layout.addWidget(self.sidebar_widget, 1)

        # Add always on top button at the very top
        self.always_on_top_btn = QPushButton('Закрепить окно')
        self.always_on_top_btn.clicked.connect(self.toggle_always_on_top)
        self.sidebar.addWidget(self.always_on_top_btn)

        # Add coordinate display label
        self.coord_label = QLabel('X: 0, Y: 0, Color: 0x000000')
        self.coord_label.setStyleSheet('font-family: monospace; padding: 5px; background-color: #f0f0f0; border: 1px solid #ccc;')
        self.sidebar.addWidget(self.coord_label)

        # Font size control buttons
        font_size_layout = QHBoxLayout()
        increase_font_btn = QPushButton('A+')
        increase_font_btn.clicked.connect(lambda: self.change_font_size(True))
        decrease_font_btn = QPushButton('A-')
        decrease_font_btn.clicked.connect(lambda: self.change_font_size(False))
        font_size_layout.addWidget(decrease_font_btn)
        font_size_layout.addWidget(increase_font_btn)
        self.sidebar.addLayout(font_size_layout)

        # Display Scaling Input
        scaling_layout = QHBoxLayout()
        scaling_label = QLabel('Display Scaling (%):')
        self.scaling_input = QLineEdit()
        self.scaling_input.setText('150')
        self.scaling_input.textChanged.connect(self.update_scaling)
        scaling_layout.addWidget(scaling_label)
        scaling_layout.addWidget(self.scaling_input)
        self.sidebar.addLayout(scaling_layout)

        # AutoIt Path Input
        auto_it_path_layout = QHBoxLayout()
        auto_it_path_label = QLabel('AutoIt3.exe Path:')
        self.auto_it_path_input = QLineEdit()
        self.auto_it_path_input.setText(self.auto_it_path)
        self.auto_it_path_input.textChanged.connect(self.update_auto_it_path)
        auto_it_path_layout.addWidget(auto_it_path_label)
        auto_it_path_layout.addWidget(self.auto_it_path_input)
        self.sidebar.addLayout(auto_it_path_layout)

        # Add main buttons
        for btn in UIComponents.create_buttons(self):
            self.sidebar.addWidget(btn)

        # Random Click on Coordinates Button and Input
        random_click_layout = QVBoxLayout()
        random_click_label = QLabel('Random Click on Coordinates:')
        self.random_click_input = QLineEdit()
        self.random_click_input.setPlaceholderText('Enter number of coordinates')
        random_click_button = QPushButton('Start Selection')
        random_click_button.clicked.connect(self.start_random_click_selection)
        random_click_layout.addWidget(random_click_label)
        random_click_layout.addWidget(self.random_click_input)
        random_click_layout.addWidget(random_click_button)
        self.sidebar.addLayout(random_click_layout)

        # Random Click in Area Button
        random_area_layout = QVBoxLayout()
        random_area_label = QLabel('Random Click in Area:')
        random_area_button = QPushButton('Start Area Selection')
        random_area_button.clicked.connect(self.start_area_selection)
        random_area_layout.addWidget(random_area_label)
        random_area_layout.addWidget(random_area_button)
        self.sidebar.addLayout(random_area_layout)

        # Add keyboard buttons
        for btn in UIComponents.create_keyboard_buttons(self):
            self.sidebar.addWidget(btn)

        # Add comprehensive keyboard buttons toggle button
        self.keyboard_list_btn = QPushButton('Показать кнопки клавиатуры')
        self.keyboard_list_btn.clicked.connect(self.toggle_keyboard_buttons)
        self.sidebar.addWidget(self.keyboard_list_btn)

        # Add delay buttons
        for btn in UIComponents.create_delay_buttons(self):
            self.sidebar.addWidget(btn)

        # Run Script Button
        run_script_button = QPushButton('Запустить скрипт')
        run_script_button.clicked.connect(self.run_script)
        self.sidebar.addWidget(run_script_button)

        self.script_area = QTextEdit()
        # Установка начального размера шрифта
        font = self.script_area.font()
        font.setPointSize(self.font_size)
        self.script_area.setFont(font)
        main_layout.addWidget(self.script_area, 3)

        self.status_label = QLabel('Ready')
        self.sidebar.addWidget(self.status_label)

        # Loop creation
        loop_layout = QHBoxLayout()
        loop_label = QLabel('Loop repetition:')
        self.loop_input = QLineEdit()
        self.loop_input.setText(str(self.loop_count))
        loop_button = QPushButton('Create loop')
        loop_button.clicked.connect(self.create_loop)
        loop_layout.addWidget(loop_label)
        loop_layout.addWidget(self.loop_input)
        loop_layout.addWidget(loop_button)
        self.sidebar.addLayout(loop_layout)

    def update_scaling(self):
        try:
            new_scaling = int(self.scaling_input.text() or 150)
            self.display_scaling = new_scaling
            self.drag_handler.display_scaling = new_scaling
        except ValueError:
            self.scaling_input.setText(str(self.display_scaling))

    def update_auto_it_path(self):
        self.auto_it_path = self.auto_it_path_input.text()
        Utils.save_config(self.auto_it_path)

    def prepare_action(self, action_type):
        print(f"Setting click_type to: {action_type}")  # Отладочное сообщение
        print(f"Type of action_type: {type(action_type)}")  # Новое отладочное сообщение
        self.click_type = action_type
        if action_type == 'drag':
            self.drag_handler.start_drag()
            self.status_label.setText('Наведите курсор на начальную точку и нажмите Ctrl')
        elif action_type in ['click_color', 'wait_color']:
            self.status_label.setText('Hover over the pixel and press Ctrl to get color')
        elif action_type == 'move':
            self.status_label.setText('Move the mouse and press Ctrl to record movement coordinates')
        elif action_type == 'random_area':
            try:
                num_points = int(self.random_click_input.text())
                if num_points <= 0:
                    self.status_label.setText('Please enter a valid number of points')
                    return
                self.num_coordinates = num_points
                self.status_label.setText('Select first corner of the area')
            except ValueError:
                self.status_label.setText('Please enter a valid number')
                return
        else:
            self.status_label.setText(f'Move the mouse and press Ctrl for {action_type} action')
        print(f"Current click_type after setting: {self.click_type}")  # Отладочное сообщение
        print(f"Type of click_type after setting: {type(self.click_type)}")  # Новое отладочное сообщение

    def create_loop(self):
        try:
            self.loop_count = int(self.loop_input.text() or 1)
        except ValueError:
            self.loop_count = 1
            self.loop_input.setText('1')

        cursor = self.script_area.textCursor()
        selected_text = cursor.selectedText()
        
        if selected_text:
            loop_text = ScriptGenerator.generate_loop(selected_text, self.loop_count)
            cursor.insertText(loop_text)
        else:
            self.status_label.setText('Please select text to loop')

    def start_random_click_selection(self):
        """Start the random click selection process"""
        try:
            num_points = int(self.random_click_input.text())
            if num_points <= 0:
                self.statusBar().showMessage('Please enter a valid number of points')
                return
                
            # Set click type to random
            self.click_type = 'random'
            self.event_handler.click_type = 'random'
            
            self.random_points = []
            self.remaining_points = num_points
            self.statusBar().showMessage(f'Select {num_points} points')
            
        except ValueError:
            self.statusBar().showMessage('Please enter a valid number')

    def start_area_selection(self):
        """Start the random area selection process"""
        # Set click type to random_area
        self.click_type = 'random_area'
        self.event_handler.click_type = 'random_area'
        
        self.statusBar().showMessage('Select first corner of the area')

    def run_script(self):
        script_content = self.script_area.toPlainText()
        if not script_content:
            self.status_label.setText('No script to run')
            return

        with open('script.au3', 'w') as f:
            f.write(script_content)

        try:
            subprocess.run([self.auto_it_path, 'script.au3'])
            self.status_label.setText('Script executed successfully')
        except Exception as e:
            self.status_label.setText(f'Error running script: {str(e)}')

    def insert_script_command(self, command):
        cursor = self.script_area.textCursor()
        cursor.movePosition(QTextCursor.End)
        if cursor.position() > 0 and not self.script_area.toPlainText().endswith('\n'):
            cursor.insertText('\n')
        cursor.insertText(command + '\n')
        self.script_area.setTextCursor(cursor)

    def add_delay(self, ms):
        insert_sleep_command(self.script_area, ms)

    def change_font_size(self, increase=True):
        if increase:
            self.font_size = min(self.font_size + 2, 32)  # Максимальный размер 32
        else:
            self.font_size = max(self.font_size - 2, 8)   # Минимальный размер 8
        
        font = self.script_area.font()
        font.setPointSize(self.font_size)
        self.script_area.setFont(font)

    # Отслеживание координат
    def update_coordinates(self):
        x, y = self.event_handler.get_precise_cursor_pos()
        color = self.event_handler.get_pixel_color(x, y)
        self.coord_label.setText(f'X: {x}, Y: {y}, Color: {color}')

    # Поверх других окон
    def toggle_always_on_top(self):
        self.is_always_on_top = not self.is_always_on_top
        if self.is_always_on_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.always_on_top_btn.setText('Открепить окно')
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.always_on_top_btn.setText('Закрепить окно')
        self.show()  # Необходимо для применения изменений флагов окна

    def toggle_keyboard_buttons(self):
        # Toggle visibility of comprehensive keyboard buttons
        if not hasattr(self, 'comprehensive_keyboard_buttons_widget'):
            # Create a widget to hold the comprehensive keyboard buttons
            self.comprehensive_keyboard_buttons_widget = QWidget()
            comprehensive_keyboard_buttons_layout = QVBoxLayout(self.comprehensive_keyboard_buttons_widget)
            
            # Create a scroll area for the buttons
            self.comprehensive_keyboard_buttons_scroll = QScrollArea()
            self.comprehensive_keyboard_buttons_scroll.setWidgetResizable(True)
            self.comprehensive_keyboard_buttons_scroll.setWidget(self.comprehensive_keyboard_buttons_widget)
            
            # Create buttons
            self.comprehensive_keyboard_buttons = UIComponents.create_comprehensive_keyboard_buttons(self)
            
            # Add buttons to the layout
            for btn in self.comprehensive_keyboard_buttons:
                comprehensive_keyboard_buttons_layout.addWidget(btn)
            
            # Add the scroll area to the sidebar
            self.sidebar.addWidget(self.comprehensive_keyboard_buttons_scroll)
            
            # Initially hide the scroll area
            self.comprehensive_keyboard_buttons_scroll.hide()
        
        # Toggle visibility of buttons scroll area
        if self.comprehensive_keyboard_buttons_scroll.isVisible():
            self.comprehensive_keyboard_buttons_scroll.hide()
            self.keyboard_list_btn.setText('Показать кнопки клавиатуры')
        else:
            self.comprehensive_keyboard_buttons_scroll.show()
            self.keyboard_list_btn.setText('Hide Keyboard Buttons')

    def closeEvent(self, event):
        # Cleanup resources
        self.event_handler.cleanup()
        self.coord_timer.stop()
        super().closeEvent(event)

def main():
    app = QApplication(sys.argv)
    ex = AutoItScriptGenerator()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
