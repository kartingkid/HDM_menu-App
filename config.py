import json
import os
import string

# Get the directory where config.py actually lives
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(CONFIG_DIR, "hdm_config.json")


# Fallback default colors in case the JSON gets corrupted or deleted
DEFAULT_COLORS = {
    "DOS_BLUE": "#0000AA",
    "DOS_CYAN": "#00FFFF",
    "DOS_TIFFANY_BLUE": "#00AAAA",
    "DOS_WHITE": "#FFFFFF",
    "DOS_YELLOW": "#FFFF55",
    "DOS_BLACK": "#000000",
    "DOS_GRAY": "#AAAAAA",
    "DOS_GREEN": "#00AA00",
    "DOS_RED": "#AA0000",
    "DOS_DARK_BLUE": "#000055",
    "DOS_AQUAMARINE": "#3D3DE7",
    "DOS_ULTRA_GREEN": "#55FF55",
    "DOS_SUNSET_ORANGE": "#FF5555",
}

def load_config():
    """Loads configuration from JSON, injecting default colors if missing."""
    if not os.path.exists(CONFIG_FILE):
        return create_default_config()
    
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            
        # Ensure the colors block exists; if missing, restore defaults
        if "colors" not in config:
            config["colors"] = DEFAULT_COLORS.copy()
            save_config(config)
            
        return config
    except (json.JSONDecodeError, IOError):
        # Fallback if JSON syntax gets broken by manual edits
        print("Warning: Config file corrupted. Loading defaults.")
        return create_default_config()

def save_config(config_data):
    """Saves the current configuration state to disk."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=2)

def create_default_config():
    default_config = {}
    
    # 1. Put colors at the very top
    default_config["colors"] = DEFAULT_COLORS.copy()
    
    # 2. Then add your A-Z pages
    for letter in string.ascii_uppercase:
        default_config[letter] = {
            "title": "Sample Menu Entries" if letter in ["A", "B"] else "",
            "items": [{"label": f"{i if i < 10 else 0} ", "action": ""} for i in range(1, 11)]
        }
        
    save_config(default_config)
    return default_config

def restore_default_colors(config_data):
    """Resets just the color scheme back to factory defaults."""
    config_data["colors"] = DEFAULT_COLORS.copy()
    save_config(config_data)
    return config_data["colors"]
