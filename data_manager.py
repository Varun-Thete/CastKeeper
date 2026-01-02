import json
import os

CHARACTER_FILE = "characters.json"
PROFILE_PICS_FOLDER = "profile_pics"
# You might want to make this configurable or pass it in
BASE_IMAGE_SEARCH_PATH = r"D:\Apps\New Moodel"

def load_characters():
    try:
        with open(CHARACTER_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_characters_to_file(characters):
    with open(CHARACTER_FILE, 'w') as file:
        json.dump(characters, file, indent=4)

def ensure_profile_pics_folder():
    os.makedirs(PROFILE_PICS_FOLDER, exist_ok=True)

def collect_character_images(character_name):
    """Collect all images for a character including from children folders"""
    image_list = []
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    
    # Get the first word of the character name for matching
    name_start = character_name.split()[0].lower()
    
    try:
        # Walk through all directories and subdirectories
        for root, dirs, files in os.walk(BASE_IMAGE_SEARCH_PATH):
            current_folder = os.path.basename(root).lower()
            
            # If the current folder starts with the character name
            if current_folder.startswith(name_start):
                # Check all files in this folder
                for file in files:
                    if file.lower().endswith(image_extensions):
                        full_path = os.path.join(root, file)
                        image_list.append(full_path)
        
    except Exception as e:
        print(f"Error collecting images for {character_name}: {str(e)}")
    
    return image_list

def get_all_images_recursive(base_path):
    """Get all images recursively from a base path"""
    image_files = []
    try:
        for root, _, files in os.walk(base_path):
            image_files.extend([
                os.path.join(root, f) for f in files
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
            ])
    except Exception as e:
        print(f"Error reading images from {base_path}: {e}")
    return image_files
