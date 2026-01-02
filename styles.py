from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

def apply_dark_mode(app_or_widget):
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)

    app_or_widget.setPalette(dark_palette)
    if hasattr(app_or_widget, 'setAutoFillBackground'):
        app_or_widget.setAutoFillBackground(True)

# Stylesheets
HEADER_LABEL_STYLE = """
    font-size: 24px; 
    font-weight: bold; 
    color: #4CAF50;
    padding: 10px;
"""

INPUT_STYLE = """
    padding: 8px; 
    font-size: 14px; 
    border: 1px solid #444; 
    border-radius: 4px;
    background-color: #2c2c2c;
    color: white;
"""

BUTTON_BASE_STYLE = """
    color: white; 
    padding: 10px; 
    font-size: 14px; 
    border-radius: 5px;
"""

PHOTO_BUTTON_STYLE = BUTTON_BASE_STYLE + "background-color: #FF5722;"
SORT_BUTTON_STYLE = BUTTON_BASE_STYLE + "background-color: #2196F3;"
SAVE_BUTTON_STYLE = BUTTON_BASE_STYLE + "background-color: #4CAF50;"
EDIT_BUTTON_STYLE = """
    background-color: #FFC107; 
    color: black; 
    padding: 10px; 
    font-size: 14px; 
    border-radius: 5px;
"""
DELETE_BUTTON_STYLE = BUTTON_BASE_STYLE + "background-color: #f44336;"
DEFAULT_PIC_BUTTON_STYLE = BUTTON_BASE_STYLE + "background-color: #f44336;" # Same as delete?
EXIT_BUTTON_STYLE = BUTTON_BASE_STYLE + "background-color: #555555;"
GLOBAL_SLIDESHOW_BUTTON_STYLE = BUTTON_BASE_STYLE + "background-color: #9C27B0;"

LIST_WIDGET_STYLE = """
    padding: 8px; 
    font-size: 14px; 
    border: 1px solid #444; 
    border-radius: 4px;
    background-color: #2c2c2c;
    color: white;
    selection-background-color: #4CAF50;
"""

DISPLAY_LABEL_STYLE = """
    padding: 10px; 
    background-color: #1e1e1e; 
    border: 1px solid #444; 
    font-size: 14px; 
    border-radius: 4px;
    color: white;
"""

DISPLAY_IMAGE_STYLE = "background-color: #2c2c2c; border: 1px solid #444;"

SLIDER_BUTTON_STYLE = """
    background-color: #2196F3; 
    color: white; 
    font-size: 16px; 
    font-weight: bold;
    border-radius: 15px;
"""

SLIDER_STYLE = """
    background-color: #2c2c2c;
    height: 20px;
"""

PAUSE_BUTTON_PAUSED_STYLE = BUTTON_BASE_STYLE + "background-color: #4CAF50;"
PAUSE_BUTTON_RESUMED_STYLE = BUTTON_BASE_STYLE + "background-color: #673AB7;"

FULLSCREEN_BUTTON_STYLE = BUTTON_BASE_STYLE + "background-color: #E91E63;"
COPY_BUTTON_STYLE = BUTTON_BASE_STYLE + "background-color: #008CBA;"
