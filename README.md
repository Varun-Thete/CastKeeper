# CastKeeper

A powerful local character management desktop application built with Python and PyQt5. **CastKeeper** allows you to organize character profiles, manage descriptions, and view associated image collections in a feature-rich slideshow interface.

## 🚀 Features

- **Character Management**: Create, edit, delete, and organize character profiles with ease.
- **Rich Media**: Associate profile photos with characters and automatically collect related images from your local library.
- **Smart Search & Filtering**: Quickly find characters by name or description.
- **Slideshow Mode**:
    - View character image collections with adjustable duration.
    - **Fullscreen Mode**: Immersive image viewing experience.
    - **Global Slideshow**: Cycle through all character images recursively.
- **Modern UI**:
    - Built-in Dark Mode theme.
    - Responsive layout with resizable viewing areas.
- **Data Persistence**: All data is stored locally in JSON format for easy backup and portability.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/cast-keeper.git
    cd cast-keeper
    ```

2.  **Install Dependencies:**
    This project requires Python 3.x and PyQt5.
    ```bash
    pip install PyQt5
    ```

3.  **Run the Application:**
    ```bash
    python CastKeeper.py
    ```

## 📂 Project Structure

The project is structured for modularity and maintainability:

- **`CastKeeper.py`**: The main entry point and application controller.
- **`data_manager.py`**: Handles all file operations, JSON data storage, and image directory searching.
- **`styles.py`**: Contains the application's visual styling, color palettes, and dark mode configuration.
- **`fullscreen_window.py`**: Dedicated module for the immersive fullscreen image viewer.
- **`characters.json`**: (Generated) Stores your character database.
- **`profile_pics/`**: (Generated) Directory where profile images are saved.

## 💡 Usage

- **Adding a Character**: Enter a name and description on the left panel and click "Save".
- **Adding Images**: The app searches for images in your configured base directory (`D:\Apps\New Moodel` by default - *you may want to change this in `data_manager.py`*) that match the character's name.
- **Slideshow**: Select a character to start a slideshow of their images. Use the slider to adjust speed or the "Fullscreen" button for a better view.

## 📝 License

This project is open source.
