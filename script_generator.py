class ScriptGenerator:
    @staticmethod
    def generate_loop(text, count):
        return f"\nFor $i = 1 To {count}\n{text}\nNext\n"

    @staticmethod
    def generate_click_command(x, y, click_type="left"):
        return f"MouseClick(\"{click_type}\", {x}, {y})"

    @staticmethod
    def generate_move_command(x, y):
        return f"MouseMove({x}, {y})"

    @staticmethod
    def generate_drag_command(start_x, start_y, end_x, end_y):
        return f"MouseClickDrag(\"left\", {start_x}, {start_y}, {end_x}, {end_y})"
