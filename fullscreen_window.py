from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class FullscreenImageDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.showFullScreen()
        
        # Create layout with zero margins to use full screen space
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        
        # Create image label with size policy to maintain aspect ratio
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image_label.setMinimumSize(1, 1)  # Prevent zero-size scenarios
        layout.addWidget(self.image_label)
        
        # Set black background
        self.setStyleSheet("background-color: black;")
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
            
    def mousePressEvent(self, event):
        self.close()
        
    def update_image(self, pixmap):
        if pixmap.isNull():
            return
            
        # Get the screen size
        available_size = self.size()
        
        # Scale the image to fit the available space
        scaled_pixmap = pixmap.scaled(
            available_size.width(),
            available_size.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        # Clear any existing pixmap before setting new one
        self.image_label.clear()
        self.image_label.setPixmap(scaled_pixmap)
