import win32api
import win32gui
from PyQt5.QtCore import QEvent, Qt
from left_click import insert_left_click
from right_click import insert_right_click_command
from click_on_color import click_on_color
from click_on_color_area import click_on_color_area
from wait_for_pixel_color import wait_for_pixel_color
from wait_for_pixel_color_area import wait_for_pixel_color_area
from move_mouse import insert_move_command
from random_click import generate_random_click_code
from random_click_area import generate_random_click_area_code
from copy_pixel_color import copy_pixel_color_to_clipboard

class EventHandler:
    def __init__(self, parent):
        self.parent = parent

    def scale_coordinates(self, x, y):
        """Scale coordinates based on display scaling"""
        scaled_x = int(x * (100 / self.parent.display_scaling))
        scaled_y = int(y * (100 / self.parent.display_scaling))
        return scaled_x, scaled_y

    def handle_global_ctrl_press(self, e=None):
        """Handle global Ctrl key press"""
        try:
            print(f"[DEBUG] Ctrl pressed. Current click type: {self.parent.click_type}")
            
            if self.parent.click_type == 'random':
                print("[DEBUG] Processing random click")
                x, y = win32api.GetCursorPos()
                scaled_x, scaled_y = self.scale_coordinates(x, y)
                print(f"[DEBUG] Captured random click coordinates: ({scaled_x}, {scaled_y})")
                
                if hasattr(self.parent, 'random_points'):
                    self.parent.random_points.append([scaled_x, scaled_y])
                    self.parent.remaining_points -= 1
                    
                    if self.parent.remaining_points <= 0:
                        # Generate random click command using the proper function
                        from random_click import generate_random_click_code
                        code = generate_random_click_code(self.parent.random_points)
                        self.parent.insert_script_command(code)
                        self.parent.random_points = []
                        self.parent.status_label.setText('Random click points collected')
                        self.parent.click_type = None
                    else:
                        self.parent.status_label.setText(f'Select {self.parent.remaining_points} more points')
                return True
                
            if self.parent.click_type == 'random_area':
                print("[DEBUG] Processing random area click")
                x, y = win32api.GetCursorPos()
                scaled_x, scaled_y = self.scale_coordinates(x, y)
                print(f"[DEBUG] Captured random area coordinates: ({scaled_x}, {scaled_y})")
                
                if not hasattr(self.parent, 'area_start_coords'):
                    # Первое нажатие Ctrl - сохраняем начальные координаты
                    self.parent.area_start_coords = (scaled_x, scaled_y)
                    self.parent.status_label.setText('Наведите курсор на конечную точку области и нажмите Ctrl')
                else:
                    # Второе нажатие Ctrl - используем конечные координаты
                    start_x, start_y = self.parent.area_start_coords
                    # Генерируем код для случайных кликов в области
                    from random_click_area import generate_random_click_area_code
                    # Определяем минимальные и максимальные значения координат
                    x_min = min(start_x, scaled_x)
                    x_max = max(start_x, scaled_x)
                    y_min = min(start_y, scaled_y)
                    y_max = max(start_y, scaled_y)
                    code = generate_random_click_area_code(x_min, x_max, y_min, y_max)
                    self.parent.insert_script_command(code)
                    self.parent.status_label.setText('Random click area code generated')
                    # Очищаем сохраненные координаты
                    delattr(self.parent, 'area_start_coords')
                    self.parent.click_type = None
                return True
                
            if not self.parent.is_ctrl_pressed:
                print("Ctrl was not pressed before - processing")
                self.parent.is_ctrl_pressed = True
                self.parent.ctrl_press_count += 1
                
                # Обработка различных типов действий
                x, y = self.get_precise_cursor_pos()
                print(f"Mouse position: x={x}, y={y}")
                print(f"Checking click_type. Current value: {self.parent.click_type}")
                print(f"Type of click_type: {type(self.parent.click_type)}")
                
                try:
                    # Проверяем, собираем ли мы координаты для случайного клика
                    if hasattr(self.parent, 'is_collecting_coords') and self.parent.is_collecting_coords:
                        print(f"Collecting coordinates for random click. Count: {self.parent.coord_selection_count + 1}/{self.parent.num_coordinates}")
                        self.parent.coordinates_collected.append([x, y])
                        self.parent.coord_selection_count += 1
                        
                        if self.parent.coord_selection_count < self.parent.num_coordinates:
                            self.parent.status_label.setText(f'Select point {self.parent.coord_selection_count + 1} of {self.parent.num_coordinates}')
                        else:
                            # Все координаты собраны, генерируем код
                            from random_click import generate_random_click_code
                            code = generate_random_click_code(self.parent.coordinates_collected)
                            self.parent.insert_script_command(code)
                            self.parent.status_label.setText(f'Random click code generated with {self.parent.num_coordinates} points')
                            # Сбрасываем флаги
                            self.parent.is_collecting_coords = False
                            self.parent.coordinates_collected = []
                            self.parent.coord_selection_count = 0
                            self.parent.click_type = None
                        return True
                    
                    if self.parent.click_type == 'left':
                        print("Processing left click - before insert")
                        print(f"Script area type: {type(self.parent.script_area)}")
                        print(f"Script area exists: {hasattr(self.parent, 'script_area')}")
                        print(f"Script area content: {self.parent.script_area.toPlainText() if hasattr(self.parent, 'script_area') else 'No script area'}")
                        insert_left_click(self.parent.script_area, x, y)
                        print("Left click insert completed successfully")
                        self.parent.status_label.setText(f'Left click at: {x}, {y}')
                        self.parent.click_type = None
                    elif self.parent.click_type == 'right':
                        print("Processing right click - before insert")
                        insert_right_click_command(self.parent.script_area, x, y)
                        print("Right click insert completed successfully")
                        self.parent.status_label.setText(f'Right click at: {x}, {y}')
                        self.parent.click_type = None
                    elif self.parent.click_type == 'move':
                        print("Processing move - before insert")
                        insert_move_command(self.parent.script_area, x, y)
                        print("Move insert completed successfully")
                        self.parent.status_label.setText(f'Move to: {x}, {y}')
                        self.parent.click_type = None
                    elif self.parent.click_type == 'click_color':
                        print("Processing click on color - before insert")
                        color = self.get_pixel_color(x, y)
                        click_on_color(self.parent.script_area, x, y, color, "left", self.parent.display_scaling)
                        print("Click on color insert completed successfully")
                        self.parent.status_label.setText(f'Click on color {color} at: {x}, {y}')
                        self.parent.click_type = None
                    elif self.parent.click_type == 'click_color_area':
                        print("Processing click on color area - before insert")
                        if not hasattr(self.parent, 'area_start_coords'):
                            # Первое нажатие Ctrl - сохраняем начальные координаты и цвет
                            self.parent.area_start_coords = (x, y)
                            color = self.get_pixel_color(x, y)
                            self.parent.area_color = color
                            self.parent.status_label.setText('Наведите курсор на конечную точку области и нажмите Ctrl')
                        else:
                            # Второе нажатие Ctrl - используем конечные координаты
                            start_x, start_y = self.parent.area_start_coords
                            color = self.parent.area_color
                            click_on_color_area(self.parent.script_area, start_x, start_y, x, y, color, "left", self.parent.display_scaling)
                            print("Click on color area insert completed successfully")
                            self.parent.status_label.setText(f'Click on color area {color} completed')
                            # Очищаем сохраненные координаты
                            delattr(self.parent, 'area_start_coords')
                            delattr(self.parent, 'area_color')
                            self.parent.click_type = None
                    elif self.parent.click_type == 'wait_color':
                        print("Processing wait for color - before insert")
                        color = self.get_pixel_color(x, y)
                        wait_for_pixel_color(self.parent.script_area, x, y, color)
                        print("Wait for color insert completed successfully")
                        self.parent.status_label.setText(f'Wait for color {color} at: {x}, {y}')
                        self.parent.click_type = None
                    elif self.parent.click_type == 'wait_color_area':
                        print("Processing wait for color area - before insert")
                        if not hasattr(self.parent, 'wait_area_start_coords'):
                            # Первое нажатие Ctrl - сохраняем начальные координаты и цвет
                            self.parent.wait_area_start_coords = (x, y)
                            color = self.get_pixel_color(x, y)
                            self.parent.wait_area_color = color
                            self.parent.status_label.setText('Наведите курсор на конечную точку области и нажмите Ctrl')
                        else:
                            # Второе нажатие Ctrl - используем конечные координаты
                            start_x, start_y = self.parent.wait_area_start_coords
                            color = self.parent.wait_area_color
                            wait_for_pixel_color_area(self.parent.script_area, start_x, start_y, x, y, color, self.parent.display_scaling)
                            print("Wait for color area insert completed successfully")
                            self.parent.status_label.setText(f'Wait for color area {color} completed')
                            # Очищаем сохраненные координаты
                            delattr(self.parent, 'wait_area_start_coords')
                            delattr(self.parent, 'wait_area_color')
                            self.parent.click_type = None
                    elif self.parent.click_type == 'copy_color':
                        print("Processing copy color - before insert")
                        color = self.get_pixel_color(x, y)
                        copy_pixel_color_to_clipboard(color)
                        print("Copy color insert completed successfully")
                        self.parent.status_label.setText(f'Copied color {color} at: {x}, {y}')
                        self.parent.click_type = None
                    elif self.parent.click_type == 'drag':
                        print("Processing drag - before insert")
                        if not self.parent.drag_handler.is_dragging:
                            self.parent.drag_handler.start_drag()
                            self.parent.drag_handler.capture_start_coordinate()
                            self.parent.status_label.setText('Наведите курсор на конечную точку и нажмите Ctrl')
                        elif not self.parent.drag_handler.start_captured:
                            self.parent.drag_handler.capture_start_coordinate()
                            self.parent.status_label.setText('Наведите курсор на конечную точку и нажмите Ctrl')
                        else:
                            self.parent.drag_handler.capture_end_coordinate()
                            self.parent.status_label.setText('Операция перетаскивания завершена')
                            self.parent.click_type = None  # Сбрасываем click_type только после завершения перетаскивания
                        print("Drag insert completed successfully")
                    else:
                        print(f"Unknown click type: {self.parent.click_type}")
                        return False
                    
                    return True
                except Exception as e:
                    print(f"Error processing {self.parent.click_type} action: {str(e)}")
                    print(f"Error type: {type(e)}")
                    import traceback
                    print(f"Traceback: {traceback.format_exc()}")
                    return False

            return False
        except Exception as e:
            print(f"Error in handle_global_ctrl_press: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return False

    def handle_global_ctrl_release(self, e):
        print("Ctrl key released - resetting flags")
        self.parent.is_ctrl_pressed = False
        self.parent.ctrl_press_count = 0

    def handle_key_event(self, event):
        # Этот метод теперь используется только для других клавиш
        return False

    def get_precise_cursor_pos(self):
        raw_x, raw_y = win32api.GetCursorPos()
        scaled_x = int(raw_x * (100 / self.parent.display_scaling))
        scaled_y = int(raw_y * (100 / self.parent.display_scaling))
        return (scaled_x, scaled_y)

    def get_pixel_color(self, x, y):
        # Convert scaled coordinates back to screen coordinates for color detection
        screen_x = int(x * (self.parent.display_scaling / 100))
        screen_y = int(y * (self.parent.display_scaling / 100))
        hdc = win32gui.GetDC(0)
        try:
            color = win32gui.GetPixel(hdc, screen_x, screen_y)
            return f'0x{color & 0xFF:02X}{(color >> 8) & 0xFF:02X}{(color >> 16) & 0xFF:02X}'
        finally:
            win32gui.ReleaseDC(0, hdc)
