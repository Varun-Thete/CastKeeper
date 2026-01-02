import sys
import os
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, 
    QPushButton, QListWidget, QWidget, QMessageBox, QFileDialog, QSlider
)
from PyQt5.QtGui import QPixmap 
from PyQt5.QtCore import Qt, QTimer

# Custom Modules
import styles
import data_manager
from fullscreen_window import FullscreenImageDisplay

class CharacterManager(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("CastKeeper")
        self.setGeometry(100, 100, 1920, 1080)

        self.characters = data_manager.load_characters()
        self.icon_list = ['❤️','😍','😘','💕','💖','🥰','😍','💘','💝','💗','💓','💞','❣️','❤️‍🔥','❤️‍🩹','❤️','🩷','🫶']
        self.current_editing_name = None
        self.sort_ascending = True
        
        # Slideshow State
        self.slideshow_timer = QTimer(self)
        self.slideshow_timer.timeout.connect(self.change_slideshow_image)
        self.current_image_list = []
        self.current_image_index = 0
        self.is_slideshow_active = False
        self.image_size = 980
        self.slideshow_duration = 1000
        self.is_slideshow_paused = False
        self.fullscreen_window = None
        self.is_fullscreen = False
        self.duration_step = 100

        # Global Slideshow State
        self.global_slideshow_timer = QTimer(self)
        self.global_slideshow_timer.timeout.connect(self.change_global_slideshow)
        self.current_character_index = 0
        self.is_global_slideshow_active = False

        data_manager.ensure_profile_pics_folder()
        styles.apply_dark_mode(self)
        self.init_ui()
        self.display_default_photo()
        self.showMaximized()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Header Section
        header_label = QLabel("CastKeeper")
        header_label.setStyleSheet(styles.HEADER_LABEL_STYLE)
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        # Content Layout
        content_layout = QHBoxLayout()
        input_layout = QVBoxLayout()

        # Search Section
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search characters...")
        self.search_input.setStyleSheet(styles.INPUT_STYLE)
        self.search_input.textChanged.connect(self.filter_characters)
        input_layout.addWidget(self.search_input)

        # Left Side - Input Section
        input_layout.setContentsMargins(0, 0, 20, 0)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter character name")
        self.name_input.setStyleSheet(styles.INPUT_STYLE)
        input_layout.addWidget(QLabel("Character Name:"))
        input_layout.addWidget(self.name_input)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter character description")
        self.description_input.setStyleSheet(styles.INPUT_STYLE)
        input_layout.addWidget(QLabel("Character Description:"))
        input_layout.addWidget(self.description_input)

        self.photo_button = QPushButton("Set Profile Photo")
        self.photo_button.setStyleSheet(styles.PHOTO_BUTTON_STYLE)
        self.photo_button.clicked.connect(self.set_profile_photo)
        input_layout.addWidget(self.photo_button)

        # Button Layout
        button_layout = QHBoxLayout()

        self.sort_button = QPushButton("Sort A-Z")
        self.sort_button.setStyleSheet(styles.SORT_BUTTON_STYLE)
        self.sort_button.clicked.connect(self.sort_characters)
        button_layout.addWidget(self.sort_button)

        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(styles.SAVE_BUTTON_STYLE)
        self.save_button.clicked.connect(self.save_character)
        button_layout.addWidget(self.save_button)

        self.edit_button = QPushButton("Edit")
        self.edit_button.setStyleSheet(styles.EDIT_BUTTON_STYLE)
        self.edit_button.clicked.connect(self.edit_character)
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.setStyleSheet(styles.DELETE_BUTTON_STYLE)
        self.delete_button.clicked.connect(self.delete_character)
        button_layout.addWidget(self.delete_button)

        self.default_pic_button = QPushButton("Default Photo")
        self.default_pic_button.setStyleSheet(styles.DEFAULT_PIC_BUTTON_STYLE)
        self.default_pic_button.clicked.connect(self.set_default_photo)
        button_layout.addWidget(self.default_pic_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.setStyleSheet(styles.EXIT_BUTTON_STYLE)
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.exit_button)

        self.global_slideshow_button = QPushButton("Global Slideshow")
        self.global_slideshow_button.setStyleSheet(styles.GLOBAL_SLIDESHOW_BUTTON_STYLE)
        self.global_slideshow_button.clicked.connect(self.toggle_global_slideshow)
        button_layout.addWidget(self.global_slideshow_button)

        input_layout.addLayout(button_layout)

        # Right Side - List and Display Section
        list_layout = QVBoxLayout()

        self.character_list = QListWidget()
        self.character_list.setStyleSheet(styles.LIST_WIDGET_STYLE)
        self.character_list.itemSelectionChanged.connect(self.display_character)
        list_layout.addWidget(QLabel("Select Character:"))
        list_layout.addWidget(self.character_list)

        self.display_label = QLabel("")
        self.display_label.setStyleSheet(styles.DISPLAY_LABEL_STYLE)
        self.display_label.setAlignment(Qt.AlignTop)
        self.display_label.setWordWrap(True)
        self.display_label.setMaximumSize(300, 100)
        self.display_label.hide()
        list_layout.addWidget(self.display_label)

        image_layout = QVBoxLayout()

        self.display_image = QLabel()
        self.display_image.setMinimumSize(self.image_size,self.image_size)
        self.display_image.setStyleSheet(styles.DISPLAY_IMAGE_STYLE)
        self.display_image.setAlignment(Qt.AlignCenter)
        self.display_image.clear()
        image_layout.addWidget(self.display_image)

        # Slideshow Controls
        slider_layout = QVBoxLayout()
        slider_label = QLabel("Slideshow Duration:")
        slider_label.setStyleSheet("color: white; font-size: 14px;")
        slider_layout.addWidget(slider_label)

        slider_controls_layout = QHBoxLayout()

        self.minus_button = QPushButton("-")
        self.minus_button.setFixedSize(30, 30)
        self.minus_button.setStyleSheet(styles.SLIDER_BUTTON_STYLE)
        self.minus_button.clicked.connect(self.decrease_duration)
        slider_controls_layout.addWidget(self.minus_button)

        self.duration_slider = QSlider(Qt.Horizontal)
        self.duration_slider.setMinimum(100)
        self.duration_slider.setMaximum(3000)
        self.duration_slider.setValue(self.slideshow_duration)
        self.duration_slider.setTickInterval(100)
        self.duration_slider.setTickPosition(QSlider.TicksBelow)
        self.duration_slider.valueChanged.connect(self.update_slideshow_duration)
        self.duration_slider.setStyleSheet(styles.SLIDER_STYLE)
        slider_controls_layout.addWidget(self.duration_slider, 1)

        self.plus_button = QPushButton("+")
        self.plus_button.setFixedSize(30, 30)
        self.plus_button.setStyleSheet(styles.SLIDER_BUTTON_STYLE)
        self.plus_button.clicked.connect(self.increase_duration)
        slider_controls_layout.addWidget(self.plus_button)

        slider_layout.addLayout(slider_controls_layout)

        self.duration_value_label = QLabel(f"Duration: {self.slideshow_duration/1000:.1f} seconds")
        self.duration_value_label.setStyleSheet("color: white; font-size: 12px;")
        self.duration_value_label.setAlignment(Qt.AlignCenter)
        slider_layout.addWidget(self.duration_value_label)

        self.pause_button = QPushButton("Pause")
        self.pause_button.setStyleSheet(styles.PAUSE_BUTTON_RESUMED_STYLE)
        self.pause_button.clicked.connect(self.toggle_pause)

        self.fullscreen_button = QPushButton("Fullscreen")
        self.fullscreen_button.setStyleSheet(styles.FULLSCREEN_BUTTON_STYLE)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)

        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.setStyleSheet(styles.COPY_BUTTON_STYLE)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        
        list_layout.addWidget(self.copy_button)
        list_layout.addWidget(self.pause_button)
        list_layout.addWidget(self.fullscreen_button)
        list_layout.addLayout(slider_layout)

        content_layout.addLayout(input_layout, 40)
        content_layout.addLayout(list_layout, 60)
        content_layout.addLayout(image_layout, 60)

        main_layout.addLayout(content_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.populate_character_list()

    def toggle_global_slideshow(self):
        if self.is_global_slideshow_active:
            self.stop_global_slideshow()
            self.global_slideshow_button.setText("Global Slideshow")
        else:
            self.start_global_slideshow()
            self.global_slideshow_button.setText("Stop Global Slideshow")

    def start_global_slideshow(self):
        self.stop_slideshow()
        self.search_input.clear()
        self.display_label.clear()
        self.character_list.clearSelection()

        # Get images from data manager
        self.current_image_list = data_manager.get_all_images_recursive(data_manager.BASE_IMAGE_SEARCH_PATH)
        
        if len(self.current_image_list) > 1:
            self.is_global_slideshow_active = True
            self.current_image_index = 0
            self.start_slideshow()
        elif len(self.current_image_list) == 1:
            self.display_single_image(self.current_image_list[0])
            self.is_global_slideshow_active = True
        else:
            self.display_default_photo()
            QMessageBox.warning(self, "Warning", "No images found in the specified directory!")
            self.is_global_slideshow_active = False
            self.global_slideshow_button.setText("Global Slideshow")

    def stop_global_slideshow(self):
        self.global_slideshow_timer.stop()
        self.slideshow_timer.stop()
        self.is_global_slideshow_active = False
        self.display_default_photo()
        self.display_label.clear()
        self.current_image_list = []

    def change_global_slideshow(self):
        if not self.characters:
            self.stop_global_slideshow()
            return

        self.current_character_index = (self.current_character_index + 1) % len(self.characters)
        self.display_character_in_slideshow()

    def display_character_in_slideshow(self):
        if not self.characters:
            return

        character = self.characters[self.current_character_index]
        self.display_label.setText(f"<b>Name:</b> {character['name']}<br><b>Description:</b> {character['description']}")
        
        self.character_list.setCurrentRow(self.current_character_index)
        
        self.current_image_list = data_manager.collect_character_images(character["name"])
        
        if self.current_image_list:
            self.current_image_index = 0
            self.start_slideshow()
        else:
            self.display_default_photo()

    def increase_duration(self):
        new_value = min(self.duration_slider.value() + self.duration_step, self.duration_slider.maximum())
        self.duration_slider.setValue(new_value)

    def decrease_duration(self):
        new_value = max(self.duration_slider.value() - self.duration_step, self.duration_slider.minimum())
        self.duration_slider.setValue(new_value)

    def update_slideshow_duration(self, value):
        self.slideshow_duration = value
        self.duration_value_label.setText(f"Duration: {value/1000:.1f} seconds")
        
        if self.slideshow_timer.isActive():
            self.slideshow_timer.stop()
            self.slideshow_timer.start(self.slideshow_duration)

    def toggle_pause(self):
        if self.slideshow_timer.isActive() or self.is_slideshow_paused:
            self.is_slideshow_paused = not self.is_slideshow_paused
            
            if self.is_slideshow_paused:
                self.slideshow_timer.stop()
                self.pause_button.setText("Resume")
                self.pause_button.setStyleSheet(styles.PAUSE_BUTTON_PAUSED_STYLE)
            else:
                self.slideshow_timer.start(self.slideshow_duration)
                self.pause_button.setText("Pause")
                self.pause_button.setStyleSheet(styles.PAUSE_BUTTON_RESUMED_STYLE)

    def toggle_fullscreen(self):
        if not self.is_fullscreen:
            if self.fullscreen_window is None:
                self.fullscreen_window = FullscreenImageDisplay()
            
            current_pixmap = self.display_image.pixmap()
            if current_pixmap:
                self.fullscreen_window.update_image(current_pixmap)
                self.fullscreen_window.show()
                self.is_fullscreen = True
                self.fullscreen_button.setText("Exit Fullscreen")
                
                if self.slideshow_timer.isActive():
                    self.connect_fullscreen_slideshow()
        else:
            self.exit_fullscreen()

    def exit_fullscreen(self):
        if self.fullscreen_window:
            self.fullscreen_window.close()
            self.fullscreen_window = None
            self.is_fullscreen = False
            self.fullscreen_button.setText("Fullscreen")

    def connect_fullscreen_slideshow(self):
        if self.fullscreen_window and self.slideshow_timer.isActive():
            try:
                self.slideshow_timer.timeout.disconnect()
            except:
                pass
            self.slideshow_timer.timeout.connect(self.update_fullscreen_slideshow)

    def update_fullscreen_slideshow(self):
        if not self.current_image_list:
            return
            
        try:
            photo_path = self.current_image_list[self.current_image_index]
            pixmap = QPixmap(photo_path)
            if pixmap.isNull():
                self.display_default_photo()
                return
                
            label_size = self.display_image.size()
            main_pixmap = pixmap.scaled(
                label_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.display_image.setPixmap(main_pixmap)
            
            if self.fullscreen_window and self.is_fullscreen:
                self.fullscreen_window.update_image(pixmap)
            
            self.current_image_index = (self.current_image_index + 1) % len(self.current_image_list)
            
        except Exception as e:
            print(f"Error updating slideshow: {e}")
            self.display_default_photo()

    def set_profile_photo(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter a character name before setting a profile photo!")
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Profile Photo", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)

        if file_path:
            new_file_name = os.path.join(data_manager.PROFILE_PICS_FOLDER, f"{name.replace(' ', '_')}.png")
            try:
                with open(file_path, "rb") as source_file, open(new_file_name, "wb") as target_file:
                    target_file.write(source_file.read())
                QMessageBox.information(self, "Success", "Profile photo set successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to set profile photo: {str(e)}")

    def set_default_photo(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Default Photo", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)

        if file_path:
            new_file_name = os.path.join(data_manager.PROFILE_PICS_FOLDER, "default.png")
            try:
                with open(file_path, "rb") as source_file, open(new_file_name, "wb") as target_file:
                    target_file.write(source_file.read())
                self.display_default_photo()
                QMessageBox.information(self, "Success", "Default photo set successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to set profile photo: {str(e)}")

    def display_character(self):
        if self.is_global_slideshow_active:
            return
        
        selected_items = self.character_list.selectedItems()
        if selected_items:
            self.display_image.show()
            self.display_label.show()
            selected_name = selected_items[0].text()
            
            for character in self.characters:
                if character["name"] == selected_name:
                    self.display_label.setText(f"<b>Name:</b> {character['name']}<br><b>Description:</b> {character['description']}")
                    
                    self.current_image_list = data_manager.collect_character_images(character["name"])
                    
                    if len(self.current_image_list) > 1:
                        self.current_image_index = 0
                        self.start_slideshow()
                    elif len(self.current_image_list) == 1:
                        self.display_single_image(self.current_image_list[0])
                    else:
                        self.display_default_photo()
                    break

    def start_slideshow(self):
        if self.current_image_list:
            self.is_slideshow_paused = False
            self.pause_button.setText("Pause")
            self.pause_button.setStyleSheet(styles.PAUSE_BUTTON_RESUMED_STYLE)
            self.change_slideshow_image()
            
            if self.is_fullscreen:
                self.connect_fullscreen_slideshow()
            else:
                try:
                    self.slideshow_timer.timeout.disconnect()
                except:
                    pass
                self.slideshow_timer.timeout.connect(self.change_slideshow_image)
                
            self.slideshow_timer.start(self.slideshow_duration)
            self.is_slideshow_active = True 

    def stop_slideshow(self):
        self.slideshow_timer.stop()
        self.is_slideshow_active = False
        self.is_slideshow_paused = False
        self.pause_button.setText("Pause")
        self.pause_button.setStyleSheet(styles.PAUSE_BUTTON_RESUMED_STYLE)
        if self.is_fullscreen:
            self.exit_fullscreen()

    def change_slideshow_image(self):
        if not self.current_image_list:
            return

        try:
            photo_path = self.current_image_list[self.current_image_index]
            
            label_size = self.display_image.size()
            pixmap = QPixmap(photo_path).scaled(
                label_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.display_image.setPixmap(pixmap)

            self.current_image_index = (self.current_image_index + 1) % len(self.current_image_list)
            
        except Exception as e:
            self.display_default_photo()

    def display_single_image(self, photo_path):
        label_size = self.display_image.size()
        pixmap = QPixmap(photo_path).scaled(
            label_size, 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        self.display_image.setPixmap(pixmap)

    def display_default_photo(self):
        photo_path = os.path.join(data_manager.PROFILE_PICS_FOLDER, "default.png")
        if os.path.exists(photo_path):
            label_size = self.display_image.size()
            pixmap = QPixmap(photo_path).scaled(
                label_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.display_image.setPixmap(pixmap)
        else:
            self.display_image.clear()
            self.display_image.setText("No Photo")

    def populate_character_list(self):
        self.character_list.clear()
        for character in self.characters:
            self.character_list.addItem(character["name"])

    def filter_characters(self):
        search_term = self.search_input.text().strip().lower()
        
        self.character_list.clear()
        for character in self.characters:
            if (search_term in character["name"].lower() or 
                search_term in character["description"].lower()):
                self.character_list.addItem(character["name"])
    
    def save_character(self):
        name = self.name_input.text().strip()
        description = self.description_input.toPlainText().strip()

        if name and description:
            if self.current_editing_name:
                for character in self.characters:
                    if character["name"] == self.current_editing_name:
                        character["name"] = name
                        character["description"] = description
                        break
                self.current_editing_name = None
            else:
                new_character = {
                    "name": name,
                    "description": description
                }
                self.characters.append(new_character)

            data_manager.save_characters_to_file(self.characters)

            self.filter_characters()
            
            self.name_input.clear()
            self.description_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Name and description cannot be empty!")

    def edit_character(self):
        selected_items = self.character_list.selectedItems()
        if selected_items:
            selected_name = selected_items[0].text()
            for character in self.characters:
                if character["name"] == selected_name:
                    self.name_input.setText(character["name"])
                    self.description_input.setText(character["description"])
                    self.current_editing_name = selected_name
                    break
        else:
            QMessageBox.warning(self, "Warning", "No character selected to edit!")

    def copy_to_clipboard(self):
        self.stop_slideshow()
        text = self.display_label.text()
        if text:
            name_start = text.find("Name:</b> ") + len("Name:</b> ")
            name_end = text.find("<br>")
            description_start = text.find("Description:</b> ") + len("Description:</b> ")

            name = text[name_start:name_end].strip()
            description = text[description_start:].strip()
            description = description.replace('\n', ' ')
            
            clipboard = QApplication.clipboard()
            clipboard.setText(f"{name}{random.choice(self.icon_list)}{random.choice(self.icon_list)}\n\n{description}")
            
            self.search_input.clear()
            self.display_label.clear()
            self.display_image.clear()
            self.display_default_photo() 
            self.character_list.clearSelection()
        else:
            QMessageBox.warning(self, "Warning", "No character details to copy!")
        self.display_default_photo() 

    def delete_character(self):
        selected_items = self.character_list.selectedItems()
        if selected_items:
            selected_name = selected_items[0].text()
            
            self.characters = [char for char in self.characters if char["name"] != selected_name]
            data_manager.save_characters_to_file(self.characters)
            
            self.filter_characters()
            self.display_label.clear()
        else:
            QMessageBox.warning(self, "Warning", "No character selected to delete!")
    
    def sort_characters(self):
        self.characters.sort(
            key=lambda x: x['name'], 
            reverse=not self.sort_ascending
        )
        self.sort_ascending = not self.sort_ascending
        self.sort_button.setText("Sort A-Z" if self.sort_ascending else "Sort Z-A")
        self.filter_characters()
        data_manager.save_characters_to_file(self.characters)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = CharacterManager()
    window.show()
    sys.exit(app.exec_())