from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor
import win32clipboard

def copy_pixel_color_to_clipboard(color):
    """Copy the pixel color to clipboard in hex format."""
    # Remove the extra "0x" prefix if it exists
    if color.startswith("0x"):
        color = color[2:]
    
    # Add single "0x" prefix
    color_with_prefix = "0x" + color
    
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(color_with_prefix)
    win32clipboard.CloseClipboard()
