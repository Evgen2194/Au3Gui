import win32api

class DragHandler:
    def __init__(self, display_scaling, insert_command_callback):
        self.display_scaling = display_scaling
        self.insert_command_callback = insert_command_callback
        self.drag_coordinates = []
        self.is_dragging = False
        self.start_captured = False

    def start_drag(self):
        self.drag_coordinates = []
        self.is_dragging = True
        self.start_captured = False
        print("Start drag initiated.")

    def capture_start_coordinate(self):
        if not self.is_dragging:
            print("Error: Drag not started")
            return
            
        x, y = win32api.GetCursorPos()
        scaled_x = int(x * (100 / self.display_scaling))
        scaled_y = int(y * (100 / self.display_scaling))
        self.drag_coordinates = [scaled_x, scaled_y]
        self.start_captured = True
        print(f"Captured start coordinate: {scaled_x}, {scaled_y}")

    def capture_end_coordinate(self):
        if not self.is_dragging or not self.start_captured:
            print("Error: Start coordinates not captured or drag not started")
            self.is_dragging = False
            self.start_captured = False
            self.drag_coordinates = []
            return
            
        x, y = win32api.GetCursorPos()
        scaled_x = int(x * (100 / self.display_scaling))
        scaled_y = int(y * (100 / self.display_scaling))
        
        start_x, start_y = self.drag_coordinates
        command = f'MouseClickDrag("left", {start_x}, {start_y}, {scaled_x}, {scaled_y})\n'
        self.insert_command_callback(command)
        print(f"Generated drag command: {command}")
        self.is_dragging = False
        self.start_captured = False
        self.drag_coordinates = []
        print("Drag command inserted. Dragging finished.")