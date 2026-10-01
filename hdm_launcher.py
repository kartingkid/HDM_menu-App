import json
import os
import platform
import string
import subprocess
import shutil
import sys
import datetime
import tkinter as tk
from tkinter import filedialog, colorchooser, Toplevel, Label, Button, Frame, font as tkfont
from pathlib import Path
import config

# --- DOS Color Palette ---
DOS_BLUE = "#0000AA"
DOS_CYAN = "#00FFFF"
DOS_TIFFANY_BLUE = "#00AAAA"
DOS_WHITE = "#FFFFFF"
DOS_YELLOW = "#FFFF55"
DOS_BLACK = "#000000"
DOS_GRAY = "#AAAAAA"
DOS_GREEN = "#00AA00"
DOS_RED = "#AA0000"
DOS_DARK_BLUE = "#000055"
DOS_AQUAMARINE = "#3D3DE7"
DOS_ULTRA_GREEN = "#55FF55"
DOS_SUNSET_ORANGE = "#FF5555"

# Version
version = "1.0"

# Define the absolute directory where this script lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Always use this absolute path for your config file
CONFIG_FILE = os.path.join(SCRIPT_DIR, "hdm_config.json")

# Build the absolute path to help.md
HELP_FILE_PATH = os.path.join(SCRIPT_DIR, "help.md")


def load_or_create_config():
    """Loads menu data from JSON or creates a default A-Z structure."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    default_data = {}
    for letter in string.ascii_uppercase:
        default_data[letter] = {
            "title": "" if letter in ["A", "B"] else "",
            "items": [
                {
                    "label": (
                        f"{i if i < 10 else 0} Application or Script {i}"
                        if letter in ["A", "B"]
                        else f"{i if i < 10 else 0} "
                    ),
                    "action": "",
                }
                for i in range(1, 11)
            ],
        }
    save_config(default_data)
    return default_data


def save_config(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


class HardDiskMenuApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Hard Disk Menu - Python Edition")
        self.root.geometry("850x450")
        config_data = config.load_config()
        self.dos_colors = config_data.get("colors", config.DEFAULT_COLORS.copy())
        self.root.configure(bg=self.dos_colors["DOS_BLUE"])
        self.root.resizable(True, True)

        # --- Scalable Font Objects ---
        self.dos_font = tkfont.Font(family="Courier New", size=12, weight="bold")
        self.small_dos_font = tkfont.Font(family="Courier New", size=10, weight="bold")
        self.tiny_dos_font = tkfont.Font(family="Courier New", size=8, weight="bold")
        


        self._last_w = 840
        self._last_h = 620
        
        self.menu_data = load_or_create_config()
        self.pages = list(string.ascii_uppercase)
        self.current_page_idx = 0

        self.top_menu_active = False
        self.active_menu_idx = 0
        self.modal_win = None
        self.build_win = None

        self.TOP_MENU_STRUCTURE = [
            {
                "heading": "Menu",
                "key": "m",
                "items": [
                    ("Add Entry", "Ins", lambda: self.start_add_workflow()),
                    ("Change Entry", "F2", lambda: self.start_change_workflow()),
                    (
                        "Duplicate Entry",
                        "F4",
                        lambda: self.start_duplicate_workflow(),
                    ),
                    ("Erase Entry", "Del", lambda: self.erase_selected_entry()),
                    ("Move Entry", "F6", lambda: self.start_move_workflow()),
                    ("Switch Entries", "F8", lambda: self.start_switch_workflow()),
                    ("Write File", "Ctrl-F10", lambda: print("Write File")),
                ],
            },
            {
                "heading": "Page",
                "key": "p",
                "items": [
                    (
                        "Compress Page",
                        "Ctrl-F1",
                        lambda: self.start_compress_page_workflow(),
                    ),
                    (
                        "Erase Page",
                        "Ctrl-F2",
                        lambda: self.start_erase_page_workflow(),
                    ),
                    (
                        "Import Page",
                        "Ctrl-F3",
                        lambda: self.start_import_page_workflow(),
                    ),
                    (
                        "Name Page",
                        "Ctrl-F4",
                        lambda: self.start_name_page_workflow(),
                    ),
                    (
                        "Switch Pages", 
                        "Ctrl-F5", 
                        lambda: self.action_switch_pages()),
                ],
            },
            {
                "heading": "Security",
                "key": "s",
                "items": [
                    ("Set Security (1 Entry)", "Alt-F1", lambda: self.action_set_security()),
                    ("Top Menu Entries (All)", "Alt-F5", lambda: self.action_top_menu_all()),
                ],
            },
            {
                "heading": "Local",
                "key": "l",
                "items": [
                    ("Change Colors", "Shift-F3", lambda: self.action_change_colors()),
                    ("Wallpaper", "Shift-F9", lambda: self.action_wallpaper()),
                ],
            },
            {
                "heading": "Global",
                "key": "g",
                "items": [
                    ("Global Settings", "Alt-4", lambda: self.action_global_settings()),
                    ("Screen Blanker", "Alt-8", lambda: self.action_screen_blanker()),
                ],
            },
            {
                "heading": "eXit",
                "key": "x",
                "items": [
                    ("Terminal Window", "F9", lambda: self.open_terminal_shortcut()),
                    ("eXit HDM", "F3", lambda: sys.exit(0)),
                ],
            },
        ]

        self.create_widgets()
        self.bind_keys()
        self.update_display()
        self.right_listbox.focus_set()
        self.update_clock()
    
    def action_change_colors(self):
        """Opens the color palette customizer modal window with descriptive labels."""
        if getattr(self, "top_menu_active", False) or getattr(self, "modal_win", None):
            return

        # Load current configuration data using config.py
        self.current_config = config.load_config()
        self.active_colors = self.current_config.get("colors", config.DEFAULT_COLORS.copy())

        # Create the modal window
        self.modal_win = tk.Toplevel(self.root)
        self.modal_win.title("DOS Color Palette Customizer")
        self.modal_win.geometry("450x620")
        self.modal_win.configure(bg=self.active_colors.get("DOS_DARK_BLUE", "#000055"))
        self.modal_win.transient(self.root)
        
        # Ensure it's rendered before setting grab (resolves the TclError)
        self.modal_win.update_idletasks()
        self.modal_win.wait_visibility()
        self.modal_win.grab_set()

        # Title label inside modal
        title_lbl = tk.Label(
            self.modal_win, 
            text="Customize DOS Color Palette", 
            fg=self.active_colors.get("DOS_YELLOW", "#FFFF55"), 
            bg=self.active_colors.get("DOS_DARK_BLUE", "#000055"), 
            font=("Courier", 12, "bold")
        )
        title_lbl.pack(pady=10)

        # Container frame for the list of color options
        container = tk.Frame(self.modal_win, bg=self.active_colors.get("DOS_BLUE", "#0000AA"))
        container.pack(fill="both", expand=True, padx=15, pady=10)

        # Mapping of Descriptive Display Names to internal config keys
        color_settings = [
            ("Main Panel Dashboard", "DOS_BLUE"),
            ("1st Popup Window", "DOS_CYAN"),
            ("2nd Popup Window", "DOS_TIFFANY_BLUE"),
            ("Menu Text", "DOS_WHITE"),
            ("Status Bar Text", "DOS_YELLOW"),
            ("Selection Text", "DOS_BLACK"),
            ("Selection Cursor", "DOS_GRAY"),
            ("Dropdown Window", "DOS_GREEN"),
            ("Add/Move Window", "DOS_RED"),
            ("Banner", "DOS_DARK_BLUE"),
            ("Boarder Line 1", "DOS_AQUAMARINE"),
            ("Boarder Line 2", "DOS_ULTRA_GREEN"),
            ("Boarder Line 3", "DOS_SUNSET_ORANGE"),
        ]

        self.color_preview_boxes = {}

        # Build each row dynamically
        for index, (display_name, config_key) in enumerate(color_settings):
            row_frame = tk.Frame(container, bg=self.active_colors.get("DOS_BLUE", "#0000AA"))
            row_frame.pack(fill="x", padx=5, pady=3)

            # 3. Change Button (Pack FIRST on the right so it stays fixed)
            btn = tk.Button(
                row_frame, 
                text="Change...", 
                font=("Courier", 9),
                command=lambda k=config_key: self.open_color_picker(k)
            )
            btn.pack(side="right", padx=2)

            # 2. Color Preview Swatch (Pack SECOND on the right)
            current_color = self.active_colors.get(config_key, "#0000AA")
            swatch = tk.Label(
                row_frame, 
                text="    ", 
                width=6, 
                relief="solid",
                bg=current_color
            )
            swatch.pack(side="right", padx=10)
            self.color_preview_boxes[config_key] = swatch

            # 1. Descriptive Label (Takes up the remaining space on the left)
            lbl = tk.Label(
                row_frame, 
                text=display_name, 
                anchor="w", 
                bg=self.active_colors.get("DOS_BLUE", "#0000AA"), 
                fg=self.active_colors.get("DOS_WHITE", "#FFFFFF"),
                font=("Courier", 10, "bold")
            )
            lbl.pack(side="left", fill="x", expand=True)

        # Button Frame for Save & Close / Restore Defaults
        btn_frame = tk.Frame(self.modal_win, bg=self.active_colors.get("DOS_DARK_BLUE", "#000055"))
        btn_frame.pack(pady=10)

        save_btn = tk.Button(
            btn_frame, 
            text="Save & Close", 
            font=("Courier", 10, "bold"),
            command=self.close_color_modal
        )
        save_btn.pack(side="left", padx=5)
        
        restore_btn = tk.Button(
            btn_frame, 
            text="Restore Defaults", 
            font=("Courier", 10, "bold"),
            command=self.restore_color_defaults
        )
        restore_btn.pack(side="left", padx=5)

        return "break"

    def open_color_picker(self, config_key):
        """Helper triggered when clicking 'Change...' for a specific setting."""
        from tkinter import colorchooser
        current_color = self.active_colors.get(config_key, "#0000AA")
        color_code = colorchooser.askcolor(title=f"Choose color for {config_key}", initialcolor=current_color, parent=self.modal_win)
        if color_code[1]:  # If a hex color string was selected
            hex_val = color_code[1]
            self.active_colors[config_key] = hex_val
            if config_key in self.color_preview_boxes:
                self.color_preview_boxes[config_key].configure(bg=hex_val)

    def restore_color_defaults(self):
        """Resets the active colors back to factory defaults using config module."""
        self.active_colors = config.restore_default_colors(self.current_config)
        for key, swatch in self.color_preview_boxes.items():
            if key in self.active_colors:
                swatch.configure(bg=self.active_colors[key])

    def close_color_modal(self):
        """Saves configuration changes, updates theme live, destroys modal, updates UI status."""
        if hasattr(self, "modal_win") and self.modal_win:
            # Save back to JSON via config module
            self.current_config["colors"] = self.active_colors
            config.save_config(self.current_config)

            # Make the new colors active on the current app instance
            self.dos_colors = self.active_colors.copy()
            
            self.modal_win.grab_release()
            self.modal_win.destroy()
            self.modal_win = None
            
            # Update status label with success, then reset to Ready after 3 seconds
            self.lbl_ready.configure(text="Palette updated successfully.")
            self.root.after(3000, lambda: self.lbl_ready.configure(text="Ready"))
    
    def on_window_resize(self, event):
        if event.widget == self.root:
            w, h = event.width, event.height
            if w == self._last_w and h == self._last_h:
                return
            self._last_w = w
            self._last_h = h

            scale_w = w / 840.0
            scale_h = h / 620.0
            scale = min(scale_w, scale_h)

            new_main_size = max(10, int(12 * scale))
            new_small_size = max(8, int(9 * scale))
            new_tiny_size = max(7, int(8 * scale))

            self.dos_font.configure(size=new_main_size)
            self.small_dos_font.configure(size=new_small_size)
            self.tiny_dos_font.configure(size=new_tiny_size)

    def create_widgets(self):
        self.menu_bar_frame = tk.Frame(self.root, bg=DOS_DARK_BLUE)
        self.menu_bar_frame.pack(fill=tk.X, side=tk.TOP)

        self.menu_buttons = []
        for idx, menu_data in enumerate(self.TOP_MENU_STRUCTURE):
            btn = tk.Label(
                self.menu_bar_frame,
                text=f" {menu_data['heading']} ",
                bg=DOS_DARK_BLUE,
                fg=self.dos_colors["DOS_WHITE"],
                font=self.dos_font,
            )
            btn.pack(side=tk.LEFT, padx=2)
            btn.bind("<Button-1>", lambda e, i=idx: self.open_top_menu(i))
            self.menu_buttons.append(btn)

        lbl_top_help = tk.Label(
            self.menu_bar_frame,
            text="F1=Help",
            bg=DOS_DARK_BLUE,
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        )
        lbl_top_help.pack(side=tk.RIGHT, padx=10)

        self.main_container = tk.Frame(self.root, bg=self.dos_colors["DOS_BLUE"])
        self.main_container.pack(fill=tk.BOTH, expand=True)

        top_bar_frame = tk.Frame(self.main_container, bg=self.dos_colors["DOS_BLUE"])
        top_bar_frame.pack(fill=tk.X, padx=32, pady=8)

        self.lbl_datetime = tk.Label(
            top_bar_frame,
            text="",
            bg=self.dos_colors["DOS_BLUE"],
            fg=self.dos_colors["DOS_YELLOW"],
            font=self.dos_font,
            anchor="w",
        )
        self.lbl_datetime.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.lbl_ready = tk.Label(
            top_bar_frame,
            text="Ready",
            bg=self.dos_colors["DOS_BLUE"],
            fg=self.dos_colors["DOS_YELLOW"],
            font=self.dos_font,
            anchor="e",
        )
        self.lbl_ready.pack(side=tk.RIGHT)

        title_wrapper = tk.Frame(self.main_container, bg=self.dos_colors["DOS_BLUE"])
        title_wrapper.pack(fill=tk.X, padx=32, pady=8)

        title_shadow = tk.Frame(title_wrapper, bg="black")
        title_shadow.place(x=16, y=16, relwidth=1.0, relheight=1.0, width=-16, height=-16)

        title_frame = tk.Frame(
            title_wrapper,
            bg=self.dos_colors["DOS_BLUE"],
            highlightbackground=self.dos_colors["DOS_AQUAMARINE"],
            highlightthickness=2,
        )
        title_frame.pack(fill=tk.X, padx=(0, 16), pady=(0, 16))

        lbl_banner = tk.Label(
            title_frame,
            text="My Python Projects.",
            bg=self.dos_colors["DOS_BLUE"],
            fg=self.dos_colors["DOS_CYAN"],
            font=self.dos_font,
        )
        lbl_banner.pack(pady=2)

        python_exe = sys.executable
        env_path = os.environ.get("PATH", "")
        max_len = 75
        display_path = env_path if len(env_path) <= max_len else env_path[:max_len] + "..."

        self.lbl_path = tk.Label(
            title_frame,
            text=f"Python: {python_exe}",
            bg=self.dos_colors["DOS_BLUE"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        )
        self.lbl_path.pack(pady=1)

        self.lbl_env_path = tk.Label(
            title_frame,
            text=f"PATH: {display_path}",
            bg=self.dos_colors["DOS_BLUE"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        )
        self.lbl_env_path.pack(pady=1)

        split_frame = tk.Frame(self.main_container, bg=self.dos_colors["DOS_BLUE"])
        split_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=(8, 16))
        
        split_frame.columnconfigure(0, weight=3)
        split_frame.columnconfigure(1, weight=7)
        split_frame.rowconfigure(0, weight=1)

        left_wrapper = tk.Frame(split_frame, bg=self.dos_colors["DOS_BLUE"])
        left_wrapper.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=4)

        left_shadow = tk.Frame(left_wrapper, bg="black")
        left_shadow.place(x=16, y=16, relwidth=1.0, relheight=1.0, width=-16, height=-16)

        self.left_panel = tk.Frame(
            left_wrapper,
            bg=self.dos_colors["DOS_BLUE"],
            highlightbackground=self.dos_colors["DOS_AQUAMARINE"],
            highlightthickness=2,
        )
        self.left_panel.place(x=0, y=0, relwidth=1.0, relheight=1.0, width=-16, height=-16)

        self.left_listbox = tk.Listbox(
            self.left_panel,
            bg=self.dos_colors["DOS_BLUE"],
            fg=self.dos_colors["DOS_WHITE"],
            selectbackground=self.dos_colors["DOS_GRAY"],
            selectforeground=self.dos_colors["DOS_BLACK"],
            font=self.dos_font,
            bd=0,
            highlightthickness=0,
            exportselection=False,
        )
        self.left_listbox.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        for page_letter in self.pages:
            p_title = self.menu_data.get(page_letter, {}).get("title", "")
            self.left_listbox.insert(
                tk.END, f" {page_letter}  {p_title[:22]:<22}"
            )

        lbl_index_footer = tk.Label(
            self.left_panel,
            text="▲ HDM INDEX ▼",
            bg=self.dos_colors["DOS_BLUE"],
            fg=self.dos_colors["DOS_YELLOW"],
            font=self.dos_font,
        )
        lbl_index_footer.pack(side=tk.BOTTOM, pady=6)

        right_wrapper = tk.Frame(split_frame,bg=self.dos_colors["DOS_BLUE"])
        right_wrapper.grid(row=0, column=1, sticky="nsew", padx=(12, 0), pady=4)

        right_shadow = tk.Frame(right_wrapper, bg="black")
        right_shadow.place(x=16, y=16, relwidth=1.0, relheight=1.0, width=-16, height=-16)

        self.right_panel = tk.Frame(
            right_wrapper,
            bg=self.dos_colors["DOS_BLUE"],
            highlightbackground=self.dos_colors["DOS_AQUAMARINE"],
            highlightthickness=2,
        )
        self.right_panel.place(x=0, y=0, relwidth=1.0, relheight=1.0, width=-16, height=-16)

        self.right_listbox = tk.Listbox(
            self.right_panel,
            bg=self.dos_colors["DOS_BLUE"],
            fg=self.dos_colors["DOS_WHITE"],
            selectbackground=self.dos_colors["DOS_GRAY"],
            selectforeground=self.dos_colors["DOS_BLACK"],
            font=self.dos_font,
            bd=0,
            highlightthickness=0,
            exportselection=False,
        )
        self.right_listbox.pack(fill=tk.BOTH, expand=True, padx=6, pady=(6, 0))
        self.right_listbox.bind("<Double-Button-1>", lambda e: self.launch_selected_entry())

        choice_frame = tk.Frame(self.right_panel, bg=self.dos_colors["DOS_BLUE"])
        choice_frame.pack(fill=tk.X, padx=6, pady=6)

        self.lbl_choice = tk.Label(
            choice_frame,
            text=(
                "[1] ◄═ Choice?    Enter=A1   «   ▲   ▼   »   version"
            ),
            bg=self.dos_colors["DOS_BLUE"],
            fg=self.dos_colors["DOS_YELLOW"],
            font=self.dos_font,
        )
        self.lbl_choice.pack(side=tk.LEFT)

        footer_frame = tk.Frame(self.root, bg=self.dos_colors["DOS_DARK_BLUE"])
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.lbl_footer = tk.Label(
            footer_frame,
            text="F2=Change   F3=Exit   F4=Duplicate   F6=Move   Del=Erase   Ins=Insert   F9=Terminal   F10=Menu",
            bg=self.dos_colors["DOS_DARK_BLUE"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        )
        self.lbl_footer.pack(side=tk.LEFT, padx=10, pady=4)
        
    def bind_keys(self):
        self.root.bind("<Left>", self.prev_page)
        self.root.bind("<Right>", self.next_page)
        self.root.bind("<Insert>", lambda e: self.start_add_workflow())
        self.root.bind("<F1>", self.open_help_dialog)
        self.root.bind("<F2>", lambda e: self.start_change_workflow())
        self.root.bind("<F4>", self.handle_f4)
        self.root.bind("<Delete>", lambda e: self.erase_selected_entry())
        self.root.bind("<F6>", lambda e: self.start_move_workflow())
        self.root.bind("<F8>", lambda e: self.start_switch_workflow())
        self.root.bind("<F9>", lambda event: self.open_terminal_shortcut())
        
        self.root.bind("<F3>", self.handle_f3)
        self.root.bind("<Control-F1>", lambda e: self.start_compress_page_workflow())
        self.root.bind("<Control-F2>", lambda e: self.start_erase_page_workflow())
        self.root.bind("<Control-F5>", lambda e: self.action_switch_pages())
        
        self.root.bind("<Alt-F1>", lambda e: self.action_set_security())
        self.root.bind("<Alt-F5>", lambda e: self.action_top_menu_all())
        self.root.bind("<Alt-4>", lambda e: self.action_global_settings())
        self.root.bind("<Alt-8>", lambda e: self.action_screen_blanker())
        
        self.root.bind("<Shift-F3>", lambda e: self.action_change_colors())
        self.root.bind("<Shift-F9>", lambda e: self.action_wallpaper())
        
        for letter in string.ascii_lowercase:
            self.root.bind(f"<Key-{letter}>", lambda e, l=letter: self.jump_to_page_by_key(l))
        for letter in string.ascii_uppercase:
            self.root.bind(f"<Key-{letter}>", lambda e, l=letter: self.jump_to_page_by_key(l))
          
        for digit in "1234567890":
            self.root.bind(f"<Key-{digit}>", lambda e, d=digit: self.jump_to_entry_by_key(d))

        self.right_listbox.bind("<Return>", self.on_enter)
        self.right_listbox.bind("<<ListboxSelect>>", self.update_footer)
        self.left_listbox.bind(
            "<<ListboxSelect>>", self.on_left_click_selection
        )

        self.root.bind("<F10>", lambda e: self.toggle_top_menu())
        self.root.bind("<Configure>", self.on_window_resize)

        for menu_def in self.TOP_MENU_STRUCTURE:
            k = menu_def["key"]
            idx = self.TOP_MENU_STRUCTURE.index(menu_def)
            self.root.bind(f"<Alt-{k}>", lambda e, i=idx: self.open_top_menu(i))
            self.root.bind(f"<Alt-{k.upper()}>", lambda e, i=idx: self.open_top_menu(i))

    def handle_f3(self, event):
        if event.state & 0x4 or (event.state & 0x0004):
            self.start_import_page_workflow()
            return "break"
        else:
            self.root.destroy()
        return "break"

    def handle_f4(self, event):
        if self.top_menu_active or self.modal_win:
            return "break"
        if event.state & 0x4:
            self.start_name_page_workflow()
        else:
            self.start_duplicate_workflow()
        return "break"

    def prev_page(self, event=None):
        if not self.top_menu_active:
            if not self.modal_win or getattr(self, "is_move_workflow", False):
                self.current_page_idx = (self.current_page_idx - 1) % len(self.pages)
                self.update_display()
        return "break"

    def next_page(self, event=None):
        if not self.top_menu_active:
            if not self.modal_win or getattr(self, "is_move_workflow", False):
                self.current_page_idx = (self.current_page_idx + 1) % len(self.pages)
                self.update_display()
        return "break"
    
    def jump_to_page_by_key(self, letter):
        if self.top_menu_active or self.modal_win:
            return
        letter = letter.upper()
        if letter in self.pages:
            self.current_page_idx = self.pages.index(letter)
            self.update_display()
        return "break"
    
    def jump_to_entry_by_key(self, char):
        if self.top_menu_active or self.modal_win:
            return
        
        if char in "123456789":
            idx = int(char) - 1
        elif char == "0":
            idx = 9
        else:
            return

        if idx < self.right_listbox.size():
            self.right_listbox.selection_clear(0, tk.END)
            self.right_listbox.selection_set(idx)
            self.right_listbox.activate(idx)
            self.right_listbox.see(idx)
            self.right_listbox.focus_set()
            self.update_footer()
          
        return "break"

    def update_footer(self, event=None):
        current_letter = self.pages[self.current_page_idx]
        sel = self.right_listbox.curselection()
        row_idx = sel[0] if sel else 0
        slot_num = row_idx + 1 if row_idx < 9 else 0
        self.lbl_choice.configure(
            text=f"[{slot_num}] ◄═ Choice?   Enter={current_letter}{slot_num}   «  ▲  ▼  »    {version}"
        )
  
    def update_display(self):
        self.left_listbox.selection_clear(0, tk.END)
        self.left_listbox.selection_set(self.current_page_idx)
        self.left_listbox.see(self.current_page_idx)

        current_letter = self.pages[self.current_page_idx]
        page_data = self.menu_data.get(
            current_letter,
            {
                "title": "",
                "items": [
                    {"label": f"{i if i < 10 else 0} ", "action": ""}
                    for i in range(1, 11)
                ],
            },
        )

        self.right_listbox.delete(0, tk.END)
        for item in page_data.get("items", []):
            self.right_listbox.insert(tk.END, f"  {item['label']}")

        if self.right_listbox.size() > 0:
            self.right_listbox.selection_set(0)
          
        self.update_footer()

    def on_left_click_selection(self, event):
        if not self.modal_win or getattr(self, "is_move_workflow", False):
            sel = self.left_listbox.curselection()
            if sel:
                self.current_page_idx = sel[0]
                self.update_display()
        
    def check_click_outside(self, event):
        if hasattr(self, "dropdown_win") and self.dropdown_win and self.dropdown_win.winfo_exists():
            x = self.dropdown_win.winfo_rootx()
            y = self.dropdown_win.winfo_rooty()
            w = self.dropdown_win.winfo_width()
            h = self.dropdown_win.winfo_height()

            if not (x <= event.x_root <= x + w and y <= event.y_root <= y + h):
                clicked_on_menu_btn = any(btn.winfo_rootx() <= event.x_root <= btn.winfo_rootx() + btn.winfo_width() and
                                          btn.winfo_rooty() <= event.y_root <= btn.winfo_rooty() + btn.winfo_height()
                                          for btn in self.menu_buttons)
                if not clicked_on_menu_btn:
                    self.close_top_menu()

    def toggle_top_menu(self):
        if self.top_menu_active:
            self.close_top_menu()
        else:
            self.open_top_menu(0)

    def open_top_menu(self, index):
        if self.modal_win:
            return
        self.top_menu_active = True
        self.active_menu_idx = index
        if hasattr(self, "dropdown_win") and self.dropdown_win:
            self.dropdown_win.destroy()

        for i, btn in enumerate(self.menu_buttons):
            if i == index:
                btn.configure(bg=self.dos_colors["DOS_WHITE"], fg=DOS_BLUE)
            else:
                btn.configure(bg=self.dos_colors["DOS_DARK_BLUE"], fg=self.dos_colors["DOS_WHITE"])

        x_pos = self.menu_buttons[index].winfo_x() + 10

        self.dropdown_win = tk.Frame(
            self.root,
            bg=self.dos_colors["DOS_GREEN"],
            highlightbackground=self.dos_colors["DOS_WHITE"],
            highlightthickness=2,
        )
        self.dropdown_win.place(x=x_pos, y=30)
        
        self._click_binding = self.root.bind("<Button-1>", self.check_click_outside, add=True)

        menu_items = self.TOP_MENU_STRUCTURE[index]["items"]

        max_text_len = max((len(t) for t, _, _ in menu_items), default=15)
        max_shortcut_len = max((len(s) for _, s, _ in menu_items), default=5)
        total_cols = max_text_len + max_shortcut_len + 8

        self.drop_listbox = tk.Listbox(
            self.dropdown_win,
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_WHITE"],
            selectbackground=DOS_BLUE,
            selectforeground=self.dos_colors["DOS_YELLOW"],
            font=self.dos_font,
            bd=0,
            highlightthickness=0,
            width=total_cols,
            height=len(menu_items) + 1,
            activestyle="none",
        )
        self.drop_listbox.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        for item_text, shortcut, _ in menu_items:
            space_count = (max_text_len - len(item_text)) + 4
            self.drop_listbox.insert(
                tk.END, f" {item_text}{' ' * space_count}{shortcut}"
            )

        separator_line = "─" * (total_cols + 2)
        lbl_cancel = tk.Label(
            self.dropdown_win,
            text=f" {separator_line}\n Esc=Cancel",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.small_dos_font,
            justify=tk.LEFT,
        )
        lbl_cancel.pack(fill=tk.X, padx=4, pady=2)

        self.drop_listbox.selection_set(0)
        self.drop_listbox.focus_set()

        self.drop_listbox.bind("<Return>", self.execute_dropdown_action)
        self.drop_listbox.bind(
            "<Double-Button-1>", lambda e: self.execute_dropdown_action()
        )
        self.drop_listbox.bind("<Escape>", lambda e: self.close_top_menu())
        self.drop_listbox.bind("<Left>", self.prev_top_tab)
        self.drop_listbox.bind("<Right>", self.next_top_tab)

        for menu_def in self.TOP_MENU_STRUCTURE:
            k = menu_def["key"]
            idx = self.TOP_MENU_STRUCTURE.index(menu_def)
            self.drop_listbox.bind(
                f"<Key-{k}>", lambda e, i=idx: self.open_top_menu(i)
            )
            self.drop_listbox.bind(
                f"<Key-{k.upper()}>", lambda e, i=idx: self.open_top_menu(i)
            )

    def prev_top_tab(self, event):
        new_idx = (self.active_menu_idx - 1) % len(self.TOP_MENU_STRUCTURE)
        self.open_top_menu(new_idx)
        return "break"

    def next_top_tab(self, event):
        new_idx = (self.active_menu_idx + 1) % len(self.TOP_MENU_STRUCTURE)
        self.open_top_menu(new_idx)
        return "break"

    def close_top_menu(self):
        if hasattr(self, "dropdown_win") and self.dropdown_win:
            self.dropdown_win.destroy()
            self.dropdown_win = None

        if hasattr(self, "_click_binding") and self._click_binding:
            try:
                self.root.unbind("<Button-1>", self._click_binding)
            except Exception:
                pass
            self._click_binding = None

        self.top_menu_active = False

        for btn in self.menu_buttons:
            btn.configure(bg=self.dos_colors["DOS_DARK_BLUE"], fg=self.dos_colors["DOS_WHITE"])

        self.right_listbox.focus_set()

    def execute_dropdown_action(self, event=None):
        sel = self.drop_listbox.curselection()
        if sel:
            idx = sel[0]
            action_func = self.TOP_MENU_STRUCTURE[self.active_menu_idx]["items"][idx][2]
            self.close_top_menu()
            if callable(action_func):
                action_func()
  
    def launch_selected_entry(self, event=None):
        self.on_enter(event)

    def on_enter(self, event=None):
        if self.modal_win:
            return
        sel = self.right_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        current_letter = self.pages[self.current_page_idx]
        page_items = self.menu_data.get(current_letter, {}).get("items", [])

        if idx < len(page_items):
            action = page_items[idx]["action"]
            if action.strip():
                try:
                    cwd_path = None
                    parts = action.split()
                    for part in parts:
                        if part.endswith(".py"):
                            p = Path(part)
                            if p.is_absolute() and p.parent.exists():
                                cwd_path = str(p.parent)
                                break
                    
                    subprocess.Popen(action, shell=True, cwd=cwd_path)
                except Exception as e:
                    print(f"Error launching command: {e}")

    def start_add_workflow(self):
        if self.top_menu_active:
            self.close_top_menu()
        if self.modal_win or (hasattr(self, "outer_modal_container") and self.outer_modal_container):
            return

        # Step 1: Outer shadow/border container
        self.outer_modal_container = tk.Frame(
            self.root,
            bg=self.dos_colors["DOS_RED"],
        )
        self.outer_modal_container.place(relx=0.35, rely=0.08, relwidth=0.30, relheight=0.08)
        

        # Step 2: Middle background fill frame (creates the outer line width)
        modal_bg_frame = tk.Frame(
            self.outer_modal_container,
            bg=self.dos_colors["DOS_SUNSET_ORANGE"],
        )
        modal_bg_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Step 3: Inner content frame with the stepped-in border line
        self.modal_win = tk.Frame(
            modal_bg_frame,
            bg=self.dos_colors["DOS_RED"],
        )
        self.modal_win.pack(fill="both", expand=True, padx=2, pady=2)

        lbl_msg = tk.Label(
            self.modal_win,
            text="Select menu entry to Add",
            bg=self.dos_colors["DOS_RED"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        )
        lbl_msg.pack(expand=True)

        self.right_listbox.bind("<Return>", self.confirm_slot_selection)

    def confirm_slot_selection(self, event=None):
        if not self.modal_win:
            return
        self.modal_win.destroy()
        self.modal_win = None

        self.right_listbox.bind("<Return>", self.on_enter)

        sel = self.right_listbox.curselection()
        slot_idx = sel[0] if sel else 0
        slot_num = slot_idx + 1 if slot_idx < 9 else 0
        current_letter = self.pages[self.current_page_idx]
        target_code = f"{current_letter}{slot_num}"

        self.show_description_dialog(target_code, slot_idx)

    def start_change_workflow(self):
        if self.top_menu_active:
            self.close_top_menu()
        if self.modal_win:
            return
        sel = self.right_listbox.curselection()
        if not sel:
            return
        slot_idx = sel[0]
        slot_num = slot_idx + 1 if slot_idx < 9 else 0
        current_letter = self.pages[self.current_page_idx]
        target_code = f"{current_letter}{slot_num}"

        page_items = self.menu_data.get(current_letter, {}).get("items", [])
        current_label = ""
        if slot_idx < len(page_items):
            # Fix: Use .get() method to safely fetch the label with a default fallback
            full_label = page_items[slot_idx].get("label", "")
            parts = full_label.split(" ", 1)
            current_label = parts[1] if len(parts) > 1 else full_label

        self.show_description_dialog(
            target_code, slot_idx, existing_desc=current_label
        )

    def start_duplicate_workflow(self):
        if self.top_menu_active or self.modal_win:
            return
        sel = self.right_listbox.curselection()
        if not sel:
            return
        src_idx = sel[0]
        
        # Step 1: Outer shadow/border container
        self.outer_modal_container = tk.Frame(
            self.root,
            bg=self.dos_colors["DOS_RED"],
        )
        self.outer_modal_container.place(relx=0.22, rely=0.15, relwidth=0.56, relheight=0.08)
        
        # Step 2: Middle background fill frame (creates the outer line width)
        modal_bg_frame = tk.Frame(
            self.outer_modal_container,
            bg=self.dos_colors["DOS_SUNSET_ORANGE"],
        )
        modal_bg_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Step 3: Inner content frame with the stepped-in border line
        self.modal_win = tk.Frame(
            modal_bg_frame,
            bg=self.dos_colors["DOS_RED"],
        )
        self.modal_win.pack(fill="both", expand=True, padx=2, pady=2)

        tk.Label(
            self.modal_win,
            text="Select target slot to Copy to, then Enter",
            bg=self.dos_colors["DOS_RED"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        ).pack(expand=True)

        self.right_listbox.bind(
            "<Return>", lambda e: self.confirm_duplicate(src_idx)
        )

    def confirm_duplicate(self, src_idx):
        if not self.modal_win:
            return
            
        # --- Fix: Destroy outer container and modal win properly ---
        if hasattr(self, "outer_modal_container") and self.outer_modal_container:
            self.outer_modal_container.destroy()
            self.outer_modal_container = None
            
        self.modal_win.destroy()
        self.modal_win = None
        self.right_listbox.bind("<Return>", self.on_enter)

        sel = self.right_listbox.curselection()
        if not sel:
            return
        target_idx = sel[0]

        current_letter = self.pages[self.current_page_idx]
        items = self.menu_data[current_letter]["items"]

        if src_idx < len(items) and target_idx < len(items):
            src_item = items[src_idx]
            slot_num = target_idx + 1 if target_idx < 9 else 0
            
            parts = src_item["label"].split(" ", 1)
            desc = parts[1] if len(parts) > 1 else ""

            items[target_idx] = {
                "label": f"{slot_num if slot_num != 0 else 0} {desc}",
                "action": src_item["action"],
            }

            save_config(self.menu_data)
            self.update_display()
            
            # --- Fix for double selection on duplicate ---
            self.right_listbox.focus_set()
            self.right_listbox.selection_clear(0, tk.END)
            self.right_listbox.selection_set(target_idx)
            self.right_listbox.activate(target_idx)
            self.right_listbox.see(target_idx)

    def erase_selected_entry(self):
        if self.top_menu_active or self.modal_win:
            return
        sel = self.right_listbox.curselection()
        if not sel:
            return
        slot_idx = sel[0]
        slot_num = slot_idx + 1 if slot_idx < 9 else 0
        current_letter = self.pages[self.current_page_idx]

        if current_letter in self.menu_data and slot_idx < len(
            self.menu_data[current_letter]["items"]
        ):
            self.menu_data[current_letter]["items"][slot_idx] = {
                "label": f"{slot_num if slot_num != 0 else 0} ",
                "action": "",
            }
            save_config(self.menu_data)
            self.update_display()
            
            # --- Fix for double selection on erase ---
            self.right_listbox.focus_set()
            self.right_listbox.selection_clear(0, tk.END)
            self.right_listbox.selection_set(slot_idx)
            self.right_listbox.activate(slot_idx)
            self.right_listbox.see(slot_idx)

    def start_move_workflow(self):
        if self.top_menu_active or self.modal_win:
            return
        sel = self.right_listbox.curselection()
        if not sel:
            return

        self.src_page_idx = self.current_page_idx
        self.src_idx = sel[0]
        self.is_move_workflow = True
       
        # Step 1: Outer shadow/border container
        self.outer_modal_container = tk.Frame(
            self.root,
            bg=self.dos_colors["DOS_RED"],
        )
        self.outer_modal_container.place(relx=0.15, rely=0.15, relwidth=0.60, relheight=0.08)
        
        # Step 2: Middle background fill frame (creates the outer line width)
        modal_bg_frame = tk.Frame(
            self.outer_modal_container,
            bg=self.dos_colors["DOS_SUNSET_ORANGE"],
        )
        modal_bg_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Step 3: Inner content frame with the stepped-in border line
        self.modal_win = tk.Frame(
            modal_bg_frame,
            bg=self.dos_colors["DOS_RED"],
        )
        self.modal_win.pack(fill="both", expand=True, padx=2, pady=2)

        tk.Label(
            self.modal_win,
            text="Navigate pages, select target slot, then Enter",
            bg=self.dos_colors["DOS_RED"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        ).pack(expand=True)

        self.root.bind("<Escape>", lambda e: self.cancel_move())
        self.right_listbox.bind("<Return>", lambda e: self.confirm_move())

    def cancel_move(self):
        self.is_move_workflow = False
        self.close_modal()

    def confirm_move(self):
        if not self.modal_win:
            return

        sel = self.right_listbox.curselection()
        if not sel:
            return
        target_idx = sel[0]
        target_page_idx = self.current_page_idx

        src_letter = self.pages[self.src_page_idx]
        target_letter = self.pages[target_page_idx]

        if self.src_page_idx == target_page_idx and self.src_idx == target_idx:
            self.cancel_move()
            return

        if src_letter not in self.menu_data:
            self.menu_data[src_letter] = {"title": src_letter, "items": []}
        if target_letter not in self.menu_data:
            self.menu_data[target_letter] = {"title": target_letter, "items": []}

        src_items = self.menu_data[src_letter]["items"]
        target_items = self.menu_data[target_letter]["items"]

        while len(src_items) < 10:
            src_items.append({"label": "", "action": ""})
        while len(target_items) < 10:
            target_items.append({"label": "", "action": ""})

        item_to_move = src_items[self.src_idx].copy()

        target_slot_num = target_idx + 1 if target_idx < 9 else 0
        parts = item_to_move["label"].split(" ", 1)
        desc = parts[1] if len(parts) > 1 else item_to_move["label"]
        item_to_move["label"] = f"{target_slot_num} {desc.strip()}" if desc.strip() else f"{target_slot_num} "

        target_items[target_idx] = item_to_move

        src_slot_num = self.src_idx + 1 if self.src_idx < 9 else 0
        src_items[self.src_idx] = {"label": f"{src_slot_num} ", "action": ""}
        
        save_config(self.menu_data)
        self.is_move_workflow = False
        self.close_modal()
        
        self.current_page_idx = target_page_idx
        self.update_display()
        
        self.right_listbox.focus_set()
        self.right_listbox.selection_clear(0, tk.END)
        self.right_listbox.selection_set(target_idx)
        self.right_listbox.activate(target_idx)
        self.right_listbox.see(target_idx)

    def start_switch_workflow(self):
        if self.top_menu_active or self.modal_win:
            return
        sel = self.right_listbox.curselection()
        if not sel:
            return
        src_idx = sel[0]
        
        # Step 1: Outer shadow/border container
        self.outer_modal_container = tk.Frame(
            self.root,
            bg=self.dos_colors["DOS_RED"],
        )
        self.outer_modal_container.place(relx=0.22, rely=0.15, relwidth=0.56, relheight=0.08)
        
        # Step 2: Middle background fill frame (creates the outer line width)
        modal_bg_frame = tk.Frame(
            self.outer_modal_container,
            bg=self.dos_colors["DOS_SUNSET_ORANGE"],
        )
        modal_bg_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Step 3: Inner content frame with the stepped-in border line
        self.modal_win = tk.Frame(
            modal_bg_frame,
            bg=self.dos_colors["DOS_RED"],
        )
        self.modal_win.pack(fill="both", expand=True, padx=2, pady=2)

        tk.Label(
            self.modal_win,
            text="Select second entry to Switch with, then Enter",
            bg=self.dos_colors["DOS_RED"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        ).pack(expand=True)

        self.right_listbox.bind(
            "<Return>", lambda e: self.confirm_switch(src_idx)
        )

    def confirm_switch(self, src_idx):
        if not self.modal_win:
            return
            
        # --- Fix: Destroy outer container and modal win properly ---
        if hasattr(self, "outer_modal_container") and self.outer_modal_container:
            self.outer_modal_container.destroy()
            self.outer_modal_container = None
            
        self.modal_win.destroy()
        self.modal_win = None
        self.right_listbox.bind("<Return>", self.on_enter)

        sel = self.right_listbox.curselection()
        if not sel:
            return
        target_idx = sel[0]
        if src_idx == target_idx:
            return

        current_letter = self.pages[self.current_page_idx]
        items = self.menu_data[current_letter]["items"]

        items[src_idx], items[target_idx] = items[target_idx], items[src_idx]

        for i, itm in enumerate(items):
            slot_num = i + 1 if i < 9 else 0
            parts = itm["label"].split(" ", 1)
            desc = parts[1] if len(parts) > 1 else ""
            itm["label"] = (
                f"{slot_num if slot_num != 0 else 0} {desc}"
                if desc
                else f"{slot_num if slot_num != 0 else 0} "
            )

        save_config(self.menu_data)
        self.update_display()
        
        # --- Fix for double selection on switch ---
        self.right_listbox.focus_set()
        self.right_listbox.selection_clear(0, tk.END)
        self.right_listbox.selection_set(target_idx)
        self.right_listbox.activate(target_idx)
        self.right_listbox.see(target_idx)

    def start_compress_page_workflow(self):
        if self.top_menu_active:
            self.close_top_menu()
        if self.modal_win:
            return

        self.lbl_ready.configure(text="Page Compress")
        
        # Step 1: Outer shadow/border container
        self.outer_modal_container = tk.Frame(
            self.root,
            bg=self.dos_colors["DOS_RED"],
        )
        self.outer_modal_container.place(relx=0.20, rely=0.15, relwidth=0.60, relheight=0.08)
        
        # Step 2: Middle background fill frame (creates the outer line width)
        modal_bg_frame = tk.Frame(
            self.outer_modal_container,
            bg=self.dos_colors["DOS_SUNSET_ORANGE"],
        )
        modal_bg_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Step 3: Inner content frame with the stepped-in border line
        self.modal_win = tk.Frame(
            modal_bg_frame,
            bg=self.dos_colors["DOS_RED"],
        )
        self.modal_win.pack(fill="both", expand=True, padx=2, pady=2)

        tk.Label(
            self.modal_win,
            text="Select page to Compress, then press ENTER",
            bg=self.dos_colors["DOS_RED"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        ).pack(expand=True)

        self.left_listbox.focus_set()
        self.root.bind("<Escape>", lambda e: self.close_modal())
        self.left_listbox.bind("<Return>", lambda e: self.execute_compress_page())

    def execute_compress_page(self):
        if not self.modal_win:
            return
        self.modal_win.destroy()
        self.modal_win = None

        sel = self.left_listbox.curselection()
        if sel:
            self.current_page_idx = sel[0]
        target_letter = self.pages[self.current_page_idx]

        if target_letter in self.menu_data:
            items = self.menu_data[target_letter].get("items", [])
            
            active_items = []
            for itm in items:
                action = itm.get("action", "").strip()
                label_full = itm.get("label", "")
                parts = label_full.split(" ", 1)
                desc = parts[1].strip() if len(parts) > 1 else ""
                
                if action or desc:
                    active_items.append({"label": desc, "action": action})

            new_items = []
            for i in range(10):
                slot_num = i + 1 if i < 9 else 0
                if i < len(active_items):
                    desc = active_items[i]["label"]
                    action = active_items[i]["action"]
                    new_items.append({
                        "label": f"{slot_num if slot_num != 0 else 0} {desc}",
                        "action": action
                    })
                else:
                    new_items.append({
                        "label": f"{slot_num if slot_num != 0 else 0} ",
                        "action": ""
                    })

            self.menu_data[target_letter]["items"] = new_items
            save_config(self.menu_data)

        self.lbl_ready.configure(text="Ready")
        self.close_modal()
        self.update_display()
        self.right_listbox.focus_set()

    def start_erase_page_workflow(self):
        if self.top_menu_active:
            self.close_top_menu()
        if self.modal_win:
            return

        self.lbl_ready.configure(text="Page Erase")

        '''self.modal_win = tk.Frame(
            self.root,
            bg=self.dos_colors["DOS_RED"],
            highlightbackground=self.dos_colors["DOS_WHITE"],
            highlightthickness=2,
        )
        self.modal_win.place(relx=0.20, rely=0.15, relwidth=0.60, relheight=0.08)'''
        
        # Step 1: Outer shadow/border container
        self.outer_modal_container = tk.Frame(
            self.root,
            bg=self.dos_colors["DOS_RED"],
        )
        self.outer_modal_container.place(relx=0.20, rely=0.15, relwidth=0.56, relheight=0.08)
        
        # Step 2: Middle background fill frame (creates the outer line width)
        modal_bg_frame = tk.Frame(
            self.outer_modal_container,
            bg=self.dos_colors["DOS_SUNSET_ORANGE"],
        )
        modal_bg_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Step 3: Inner content frame with the stepped-in border line
        self.modal_win = tk.Frame(
            modal_bg_frame,
            bg=self.dos_colors["DOS_RED"],
        )
        self.modal_win.pack(fill="both", expand=True, padx=2, pady=2)

        tk.Label(
            self.modal_win,
            text="Select page to Erase, then press ENTER",
            bg=self.dos_colors["DOS_RED"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        ).pack(expand=True)

        self.left_listbox.focus_set()
        self.root.bind("<Escape>", lambda e: self.close_modal())
        self.left_listbox.bind(
            "<Return>", lambda e: self.show_erase_page_confirm()
        )

    def show_erase_page_confirm(self):
        if not self.modal_win:
            return
        self.modal_win.destroy()
        self.modal_win = None

        sel = self.left_listbox.curselection()
        if sel:
            self.current_page_idx = sel[0]
        target_letter = self.pages[self.current_page_idx]

        self.modal_win = tk.Frame(
            self.root,
            bg=self.dos_colors["DOS_GREEN"],
            highlightbackground=self.dos_colors["DOS_WHITE"],
            highlightthickness=2,
        )
        self.modal_win.place(relx=0.32, rely=0.18, relwidth=0.36, relheight=0.32)

        tk.Label(
            self.modal_win,
            text="CONFIRM (Y/N)",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_YELLOW"],
            font=self.dos_font,
        ).pack(pady=10)

        tk.Frame(self.modal_win, bg=self.dos_colors["DOS_WHITE"], height=2).pack(fill=tk.X, padx=10)

        tk.Label(
            self.modal_win,
            text=f"Erase Page: {target_letter}",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        ).pack(pady=15)

        tk.Frame(self.modal_win, bg=self.dos_colors["DOS_WHITE"], height=2).pack(fill=tk.X, padx=10)

        tk.Label(
            self.modal_win,
            text="Enter=Yes    Esc=No",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        ).pack(pady=12)

        self.root.bind("<Escape>", lambda e: self.close_modal())
        self.root.bind("<Return>", lambda e: self.execute_erase_page(target_letter))
        self.root.bind("y", lambda e: self.execute_erase_page(target_letter))
        self.root.bind("Y", lambda e: self.execute_erase_page(target_letter))

    def execute_erase_page(self, target_letter):
        if not self.modal_win:
            return

        self.menu_data[target_letter] = {
            "title": "",
            "items": [{"label": f"{i if i < 10 else 0} ", "action": ""} for i in range(1, 11)],
        }
        save_config(self.menu_data)

        self.lbl_ready.configure(text="Ready")
        self.close_modal()
        self.update_display()
        self.right_listbox.focus_set()

    def start_import_page_workflow(self):
        if self.top_menu_active:
            self.close_top_menu()
        if self.modal_win:
            return

        current_letter = self.pages[self.current_page_idx]
        self.lbl_ready.configure(text="Import Page")

        '''self.modal_win = tk.Frame(
            self.root,
            bg=self.dos_colors["DOS_GREEN"],
            highlightbackground=self.dos_colors["DOS_WHITE"],
            highlightthickness=2,
        )
        self.modal_win.place(relx=0.15, rely=0.15, relwidth=0.70, relheight=0.40)'''
        
        # Step 1: Outer shadow/border container
        self.outer_modal_container = tk.Frame(
            self.root,
            bg=self.dos_colors["DOS_GREEN"],
        )
        self.outer_modal_container.place(relx=0.15, rely=0.15, relwidth=0.70, relheight=0.40)
        
        # Step 2: Middle background fill frame (creates the outer line width)
        modal_bg_frame = tk.Frame(
            self.outer_modal_container,
            bg=self.dos_colors["DOS_WHITE"],
        )
        modal_bg_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Step 3: Inner content frame with the stepped-in border line
        self.modal_win = tk.Frame(
            modal_bg_frame,
            bg=self.dos_colors["DOS_GREEN"],
        )
        self.modal_win.pack(fill="both", expand=True, padx=2, pady=2)

        tk.Label(
            self.modal_win,
            text=" Import Any Page to Current Menu File ",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_YELLOW"],
            font=self.dos_font,
        ).pack(pady=12)

        form_frame = tk.Frame(self.modal_win, bg=self.dos_colors["DOS_GREEN"])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

        form_frame.columnconfigure(0, weight=0)
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(2, weight=0)

        tk.Label(
            form_frame,
            text="Copy from Menu File number   [",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        ).grid(row=0, column=0, sticky="w", pady=10)

        self.import_file_num_entry = tk.Entry(
            form_frame,
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_WHITE"],
            insertbackground=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
            bd=0,
        )
        self.import_file_num_entry.grid(row=0, column=1, sticky="ew", pady=10, padx=2)
        self.import_file_num_entry.insert(0, "0")

        tk.Label(
            form_frame,
            text="]  (0-999)",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        ).grid(row=0, column=2, sticky="w", pady=10)

        tk.Label(
            form_frame,
            text="Copy from Page letter         [",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        ).grid(row=1, column=0, sticky="w", pady=10)

        self.import_page_letter_entry = tk.Entry(
            form_frame,
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_WHITE"],
            insertbackground=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
            bd=0,
        )
        self.import_page_letter_entry.grid(
            row=1, column=1, sticky="ew", pady=10, padx=2
        )
        self.import_page_letter_entry.insert(0, current_letter)

        tk.Label(
            form_frame,
            text="]  (A through Z)",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        ).grid(row=1, column=2, sticky="w", pady=10)

        modal_footer = tk.Label(
            self.modal_win,
            text="Esc=Cancel    F2=Import",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        )
        modal_footer.pack(side=tk.BOTTOM, pady=15)

        self.import_page_letter_entry.focus_set()
        self.root.bind("<Escape>", lambda e: self.close_modal())
        self.root.bind("<F2>", lambda e: self.execute_import_page(current_letter))
        self.root.bind(
            "<Return>", lambda e: self.execute_import_page(current_letter)
        )

    def execute_import_page(self, current_letter):
        if not self.modal_win:
            return
        
        src_page = self.import_page_letter_entry.get().strip().upper()
        if not src_page or src_page not in string.ascii_uppercase:
            src_page = current_letter

        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as f:
                    imported_data = json.load(f)
                    if src_page in imported_data:
                        self.menu_data[current_letter] = imported_data[src_page]
                        save_config(self.menu_data)
        except Exception as e:
            print(f"Error importing page: {e}")

        self.lbl_ready.configure(text="Ready")
        self.close_modal()
        self.update_display()

    def start_name_page_workflow(self):
        if self.top_menu_active:
            self.close_top_menu()
        if self.modal_win:
            return

        current_letter = self.pages[self.current_page_idx]
        current_title = self.menu_data.get(current_letter, {}).get("title", "")
        self.lbl_ready.configure(text="Name Page")

        '''self.modal_win = tk.Frame(
            self.root,
            bg=self.dos_colors["DOS_GREEN"],
            highlightbackground=self.dos_colors["DOS_WHITE"],
            highlightthickness=2,
        )
        self.modal_win.place(relx=0.15, rely=0.15, relwidth=0.70, relheight=0.35)'''
        
        # Step 1: Outer shadow/border container
        self.outer_modal_container = tk.Frame(
            self.root,
            bg=self.dos_colors["DOS_GREEN"],
        )
        self.outer_modal_container.place(relx=0.15, rely=0.15, relwidth=0.70, relheight=0.35)
        
        # Step 2: Middle background fill frame (creates the outer line width)
        modal_bg_frame = tk.Frame(
            self.outer_modal_container,
            bg=self.dos_colors["DOS_WHITE"],
        )
        modal_bg_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Step 3: Inner content frame with the stepped-in border line
        self.modal_win = tk.Frame(
            modal_bg_frame,
            bg=self.dos_colors["DOS_GREEN"],
        )
        self.modal_win.pack(fill="both", expand=True, padx=2, pady=2)

        tk.Label(
            self.modal_win,
            text=f" Name Page {current_letter} ",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_YELLOW"],
            font=self.dos_font,
        ).pack(pady=12)

        form_frame = tk.Frame(self.modal_win, bg=self.dos_colors["DOS_GREEN"])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

        form_frame.columnconfigure(0, weight=0)
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(2, weight=0)

        tk.Label(
            form_frame,
            text="Page Title [",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        ).grid(row=0, column=0, sticky="w", pady=10)

        self.page_title_entry = tk.Entry(
            form_frame,
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_WHITE"],
            insertbackground=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
            bd=0,
        )
        self.page_title_entry.grid(row=0, column=1, sticky="ew", pady=10, padx=2)
        self.page_title_entry.insert(0, current_title)

        tk.Label(
            form_frame, text="]", bg=self.dos_colors["DOS_GREEN"], fg=self.dos_colors["DOS_WHITE"], font=self.dos_font
        ).grid(row=0, column=2, sticky="w", pady=10)

        modal_footer = tk.Label(
            self.modal_win,
            text="Esc=Cancel    F2=Save",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        )
        modal_footer.pack(side=tk.BOTTOM, pady=15)

        self.page_title_entry.focus_set()
        self.root.bind("<Escape>", lambda e: self.close_modal())
        self.root.bind("<F2>", lambda e: self.save_page_name(current_letter))
        self.root.bind("<Return>", lambda e: self.save_page_name(current_letter))

    def save_page_name(self, current_letter):
        if not self.modal_win:
            return
        new_title = self.page_title_entry.get().strip()

        if current_letter not in self.menu_data:
            # Initialize with 10 default empty item slots (1-9, then 0)
            default_items = [{"label": f"{i+1 if i < 9 else 0} ", "action": ""} for i in range(10)]
            self.menu_data[current_letter] = {"title": new_title, "items": default_items}
        else:
            self.menu_data[current_letter]["title"] = new_title
            # Ensure existing pages that somehow ended up with empty items get their slots back
            if not self.menu_data[current_letter].get("items"):
                self.menu_data[current_letter]["items"] = [{"label": f"{i+1 if i < 9 else 0} ", "action": ""} for i in range(10)]

        save_config(self.menu_data)
        self.lbl_ready.configure(text="Ready")
        self.close_modal()

        self.left_listbox.delete(0, tk.END)
        for page_letter in self.pages:
            p_title = self.menu_data.get(page_letter, {}).get("title", "")
            self.left_listbox.insert(
                tk.END, f" {page_letter}  {p_title[:22]:<22}"
            )
        self.update_display()
    
    def action_switch_pages(self):
        if self.top_menu_active or self.modal_win:
            return
        self.lbl_ready.configure(text="Switch Pages")
        print("Switch Pages triggered via Ctrl-F5")
        return "break"
    
    def action_set_security(self):
        if self.top_menu_active or self.modal_win:
            return
        self.lbl_ready.configure(text="Security (1 Entry)")
        print("Security workflow triggered via Alt-F1")
        return "break"

    def action_top_menu_all(self):
        if self.top_menu_active or self.modal_win:
            return
        self.lbl_ready.configure(text="Top Menu Entries (All)")
        print("Top Menu workflow triggered via Alt-F5")
        return "break"

    def action_global_settings(self):
        if self.top_menu_active or self.modal_win:
            return
        self.lbl_ready.configure(text="Global Settings")
        print("Global Settings triggered via Alt-4")
        return "break"

    def action_screen_blanker(self):
        if self.top_menu_active or self.modal_win:
            return
        self.lbl_ready.configure(text="Screen Blanker")
        print("Screen Blanker triggered via Alt-8")
        return "break"

    def action_wallpaper(self):
        if self.top_menu_active or self.modal_win:
            return
        self.lbl_ready.configure(text="Wallpaper")
        print("Wallpaper triggered via Shift-F9")
        return "break"

    def show_description_dialog(self, target_code, slot_idx, existing_desc=""):
        if hasattr(self, "outer_modal_container") and self.outer_modal_container:
            self.outer_modal_container.destroy()

        # 1. Outer container handles the screen positioning and creates the outer gap/margin
        self.outer_modal_container = tk.Frame(
            self.root,
            bg=self.dos_colors["DOS_GREEN"],
        )
        self.outer_modal_container.place(relx=0.08, rely=0.15, relwidth=0.84, relheight=0.68)

        # 2. modal_win acts as your ULTRA_GREEN border thickness
        self.modal_win = tk.Frame(
            self.outer_modal_container,
            bg=self.dos_colors["DOS_ULTRA_GREEN"],
        )
        # Adjust padx and pady here to change how thick your ULTRA_GREEN border is!
        self.modal_win.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # 3. Inner frame steps it inside to show the green background content
        inner_modal = tk.Frame(
            self.modal_win,
            bg=self.dos_colors["DOS_GREEN"],
        )
        inner_modal.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.desc_title_lbl = tk.Label(
            inner_modal,
            text=f" Edit menu entry {target_code} in HDM.000 "
            if existing_desc
            else f" Add menu entry {target_code} in HDM.000 ",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_YELLOW"],
            font=self.dos_font,
        )
        self.desc_title_lbl.pack(pady=15)

        form_frame = tk.Frame(inner_modal, bg=self.dos_colors["DOS_GREEN"])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        form_frame.columnconfigure(0, weight=0)
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(2, weight=0)
        form_frame.columnconfigure(3, weight=0)

        tk.Label(
            form_frame,
            text="Description to Show      [",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_BLUE"],
            font=self.dos_font,
        ).grid(row=0, column=0, sticky="w", pady=15)

        self.desc_entry = tk.Entry(
            form_frame,
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_WHITE"],
            insertbackground=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
            relief="flat",
        )
        self.desc_entry.grid(row=0, column=1, sticky="ew", pady=15)
        if existing_desc:
            self.desc_entry.insert(0, existing_desc)

        tk.Label(
            form_frame, text="]", bg=self.dos_colors["DOS_GREEN"], fg=self.dos_colors["DOS_BLUE"], font=self.dos_font
        ).grid(row=0, column=2, sticky="w", pady=15, padx=(5, 0))

        tk.Label(
            form_frame,
            text="Help File Name (optional) [",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_BLUE"],
            font=self.dos_font,
        ).grid(row=1, column=0, sticky="w", pady=15)

        self.help_entry = tk.Entry(
            form_frame,
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_WHITE"],
            insertbackground=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
            relief="flat",
        )
        self.help_entry.grid(row=1, column=1, sticky="ew", pady=15)

        tk.Label(
            form_frame,
            text="]",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_BLUE"],
            font=self.dos_font,
        ).grid(row=1, column=2, sticky="w", pady=15, padx=(5, 0))
        
        tk.Label(
            form_frame,
            text=f"  ({target_code}.000)",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_YELLOW"],
            font=self.dos_font,
        ).grid(row=1, column=3, sticky="w", pady=15, padx=(5, 0))

        self.modal_footer = tk.Label(
            inner_modal,
            text="Esc=Cancel    F2=Save    F4=Build    Ctrl-U=Undo",
            bg=self.dos_colors["DOS_GREEN"],
            fg=self.dos_colors["DOS_YELLOW"],
            font=self.dos_font,
        )
        self.modal_footer.pack(side=tk.BOTTOM, pady=20)

        self.desc_entry.focus_set()

        self.desc_entry.bind(
            "<KeyRelease>",
            lambda e: self.check_description_state(target_code, slot_idx),
        )
        self.root.bind("<Escape>", lambda e: self.close_modal())
        self.root.bind(
            "<F2>",
            lambda e: self.save_entry_data(target_code, slot_idx, "", "", ""),
        )
        self.root.bind(
            "<F4>", lambda e: self.show_build_action_dialog(target_code, slot_idx)
        )

    def check_description_state(self, target_code, slot_idx):
        val = self.desc_entry.get()
        if len(val.strip()) > 0:
            self.desc_title_lbl.configure(
                text=" Add the menu entry's Action or press F4 to get help building it "
            )
            self.modal_footer.configure(
                text="Esc=Cancel   F2=Save   F4=Build   Ctrl-U=Undo                    Ins 1"
            )
            self.root.bind(
                "<F4>", lambda e: self.show_build_action_dialog(target_code, slot_idx)
            )

    def show_build_action_dialog(self, target_code, slot_idx):
        if hasattr(self, "build_outer_container") and self.build_outer_container:
            self.build_outer_container.destroy()

        # 1. Outer container handles screen placement and margin
        self.build_outer_container = tk.Frame(
            self.root,
            bg=self.dos_colors["DOS_TIFFANY_BLUE"],
        )
        self.build_outer_container.place(relx=0.08, rely=0.15, relwidth=0.84, relheight=0.70)

        # 2. build_win acts as your ULTRA_GREEN border thickness
        self.build_win = tk.Frame(
            self.build_outer_container,
            bg=self.dos_colors["DOS_CYAN"],
        )
        self.build_win.pack(fill=tk.BOTH, expand=True, padx=8, pady=8) # Adjust padx/pady to change border width

        # 3. inner_build steps inside to hold your actual cyan dialog content
        inner_build = tk.Frame(
            self.build_win,
            bg=self.dos_colors["DOS_TIFFANY_BLUE"],
        )
        inner_build.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        tk.Label(
            inner_build,
            text=" Build the Action String ",
            bg=self.dos_colors["DOS_TIFFANY_BLUE"],
            fg=self.dos_colors["DOS_YELLOW"],
            font=self.dos_font,
        ).pack(pady=10)

        b_form = tk.Frame(inner_build, bg=self.dos_colors["DOS_TIFFANY_BLUE"])
        b_form.pack(fill=tk.BOTH, expand=True, padx=25, pady=5)

        b_form.columnconfigure(0, weight=0)
        b_form.columnconfigure(1, weight=1)
        b_form.columnconfigure(2, weight=0)
        b_form.columnconfigure(3, weight=0)

        tk.Label(
            b_form,
            text="Python venv.. [",
            bg=self.dos_colors["DOS_TIFFANY_BLUE"],
            fg=self.dos_colors["DOS_BLUE"],
            font=self.dos_font,
        ).grid(row=0, column=0, sticky="w", pady=8)

        self.venv_ent = tk.Entry(
            b_form,
            bg=self.dos_colors["DOS_TIFFANY_BLUE"],
            fg=self.dos_colors["DOS_WHITE"],
            insertbackground=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
            bd=0,
        )
        self.venv_ent.grid(row=0, column=1, sticky="ew", pady=8, padx=2)

        tk.Label(
            b_form, text="]", bg=self.dos_colors["DOS_TIFFANY_BLUE"], fg=self.dos_colors["DOS_BLUE"], font=self.dos_font
        ).grid(row=0, column=2, sticky="w", pady=8)

        btn_browse_py = tk.Button(
            b_form,
            text="Browse...",
            font=self.small_dos_font,
            command=lambda: self.browse_python_executable(),
        )
        btn_browse_py.grid(row=0, column=3, padx=(10, 0), pady=8)

        tk.Label(
            b_form,
            text="Directory..   [",
            bg=self.dos_colors["DOS_TIFFANY_BLUE"],
            fg=self.dos_colors["DOS_BLUE"],
            font=self.dos_font,
        ).grid(row=1, column=0, sticky="w", pady=8)

        self.dir_ent = tk.Entry(
            b_form,
            bg=self.dos_colors["DOS_TIFFANY_BLUE"],
            fg=self.dos_colors["DOS_WHITE"],
            insertbackground=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
            bd=0,
        )
        self.dir_ent.grid(row=1, column=1, sticky="ew", pady=8, padx=2)

        tk.Label(
            b_form, text="]", bg=self.dos_colors["DOS_TIFFANY_BLUE"], fg=self.dos_colors["DOS_BLUE"], font=self.dos_font
        ).grid(row=1, column=2, sticky="w", pady=8)

        btn_browse_dir = tk.Button(
            b_form,
            text="Browse...",
            font=self.small_dos_font,
            command=lambda: self.browse_directory(),
        )
        btn_browse_dir.grid(row=1, column=3, padx=(10, 0), pady=8)

        tk.Label(
            b_form,
            text="Program....   [",
            bg=self.dos_colors["DOS_TIFFANY_BLUE"],
            fg=self.dos_colors["DOS_BLUE"],
            font=self.dos_font,
        ).grid(row=2, column=0, sticky="w", pady=8)

        self.prog_ent = tk.Entry(
            b_form,
            bg=self.dos_colors["DOS_TIFFANY_BLUE"],
            fg=self.dos_colors["DOS_WHITE"],
            insertbackground=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
            bd=0,
        )
        self.prog_ent.grid(row=2, column=1, sticky="ew", pady=8, padx=2)

        tk.Label(
            b_form,
            text="]",
            bg=self.dos_colors["DOS_TIFFANY_BLUE"],
            fg=self.dos_colors["DOS_BLUE"],
            font=self.dos_font,
        ).grid(row=2, column=2, sticky="w", pady=8)
        
        tk.Label(
            b_form,
            text="  (.py/sh)",
            bg=self.dos_colors["DOS_TIFFANY_BLUE"],
            fg=self.dos_colors["DOS_YELLOW"],
            font=self.dos_font,
        ).grid(row=2, column=3, sticky="w", pady=8)

        tk.Label(
            b_form,
            text="Parameters.   [",
            bg=self.dos_colors["DOS_TIFFANY_BLUE"],
            fg=self.dos_colors["DOS_BLUE"],
            font=self.dos_font,
        ).grid(row=3, column=0, sticky="w", pady=8)

        self.param_ent = tk.Entry(
            b_form,
            bg=self.dos_colors["DOS_TIFFANY_BLUE"],
            fg=self.dos_colors["DOS_WHITE"],
            insertbackground=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
            bd=0,
        )
        self.param_ent.grid(row=3, column=1, sticky="ew", pady=8, padx=2)

        tk.Label(
            b_form, text="]", bg=self.dos_colors["DOS_TIFFANY_BLUE"], fg=self.dos_colors["DOS_BLUE"], font=self.dos_font
        ).grid(row=3, column=2, sticky="w", pady=8)

        current_letter = self.pages[self.current_page_idx]
        page_items = self.menu_data.get(current_letter, {}).get("items", [])
        existing_action = (
            page_items[slot_idx].get("action", "")
            if slot_idx < len(page_items)
            else ""
        )

        default_venv = "Select Your Virtual Environment"
        default_dir = "Select Your Working Directory"
        program_val = ""
        param_val = ""

        if existing_action.strip():
            parts = existing_action.split()
            if len(parts) > 1 and ("bin/python" in parts[0] or "python" in parts[0]):
                default_venv = parts[0]
                script_path = Path(parts[1])
                default_dir = str(script_path.parent) + "/"
                program_val = script_path.name
                if len(parts) > 2:
                    param_val = " ".join(parts[2:])
            else:
                script_path = Path(parts[0])
                default_dir = str(script_path.parent) + "/"
                program_val = script_path.name
                if len(parts) > 1:
                    param_val = " ".join(parts[1:])
        else:
            program_val = "main.py"

        self.prog_ent.insert(0, program_val)
        self.param_ent.insert(0, param_val)
        self.venv_ent.insert(0, default_venv)
        self.dir_ent.insert(0, default_dir)

        b_footer = tk.Label(
            inner_build,
            text="Esc=Cancel    F2=Save    F4=Search",
            bg=self.dos_colors["DOS_TIFFANY_BLUE"],
            fg=self.dos_colors["DOS_YELLOW"],
            font=self.dos_font,
        )
        b_footer.pack(side=tk.BOTTOM, pady=15)

        self.prog_ent.focus_set()

        self.root.bind("<Escape>", lambda e: self.close_build_dialog())
        self.root.bind(
            "<F2>",
            lambda e: self.save_entry_data(
                target_code,
                slot_idx,
                self.prog_ent.get(),
                self.dir_ent.get(),
                "",
                self.param_ent.get(),
                self.venv_ent.get(),
            ),
        )
  
    def set_status(self, text):
        if hasattr(self, "lbl_ready"):
            self.lbl_ready.configure(text=text)
  
    def browse_python_executable(self):
        pyenv_dir = Path.home() / ".pyenv" / "versions"
        initial_dir = str(pyenv_dir) if pyenv_dir.exists() else str(Path.home())

        filename = filedialog.askopenfilename(
            title="Select Python/Venv Executable",
            initialdir=initial_dir
        )
        if filename:
            self.venv_ent.delete(0, tk.END)
            self.venv_ent.insert(0, filename)

    def browse_directory(self):
        default_dir = Path.home() / "my_projects"
        initial_dir = str(default_dir) if default_dir.exists() else str(Path.home())

        dirname = filedialog.askdirectory(
            title="Select Working Directory",
            initialdir=initial_dir
        )
        if dirname:
            if not dirname.endswith("/"):
                dirname += "/"
            self.dir_ent.delete(0, tk.END)
            self.dir_ent.insert(0, dirname)

    def close_build_dialog(self):
        if self.build_win:
            self.build_win.destroy()
            self.build_win = None
        self.root.bind("<Escape>", lambda e: self.close_modal())
        if hasattr(self, "desc_entry") and self.desc_entry:
            self.desc_entry.focus_set()
        if hasattr(self, "build_outer_container") and self.build_outer_container:
            self.build_outer_container.destroy()
            self.build_outer_container = None
            self.build_win = None

    def save_entry_data(
        self, target_code, slot_idx, prog="", directory="", drive="", params="", venv_path=""
    ):
        desc = self.desc_entry.get().strip()

        slot_num = target_code[1:]
        label_str = (
            f"{slot_num if slot_num != '0' else '0'} {desc}"
            if desc
            else f"{slot_num if slot_num != '0' else '0'} "
        )

        current_letter = self.pages[self.current_page_idx]
        page_items = self.menu_data.get(current_letter, {}).get("items", [])

        action_str = (
            page_items[slot_idx]["action"]
            if slot_idx < len(page_items)
            else ""
        )

        if prog:
            clean_dir = directory.strip()
            clean_prog = prog.strip()
            clean_params = params.strip()
            clean_venv = venv_path.strip()

            if "Select" in clean_dir or clean_dir == "./":
                clean_dir = ""
            if "Select" in clean_venv:
                clean_venv = ""

            if platform.system() == "Linux":
                if clean_dir:
                    if clean_dir.endswith("/"):
                        full_path = f"{clean_dir}{clean_prog}"
                    else:
                        full_path = f"{clean_dir}/{clean_prog}"
                else:
                    full_path = clean_prog

                if clean_venv:
                    if "python" in Path(clean_venv).name or clean_venv.endswith(("python", "python3", "python3.13")):
                        python_exec = clean_venv
                    else:
                        python_exec = f"{clean_venv.rstrip('/')}/bin/python"
                    action_str = f"{python_exec} {full_path}"
                else:
                    action_str = f"{full_path}"

                if clean_params:
                    action_str += f" {clean_params}"
            else:
                if clean_dir:
                    action_str = f"cd {drive}:{clean_dir} && {clean_prog}"
                else:
                    action_str = clean_prog
                if clean_params:
                    action_str += f" {clean_params}"

        if current_letter not in self.menu_data:
            self.menu_data[current_letter] = {
                "title": f"Page {current_letter} Entries",
                "items": [
                    {"label": f"{i if i < 10 else 0} ", "action": ""}
                    for i in range(1, 11)
                ],
            }

        while len(self.menu_data[current_letter]["items"]) <= slot_idx:
            self.menu_data[current_letter]["items"].append(
                {"label": "", "action": ""}
            )

        self.menu_data[current_letter]["items"][slot_idx] = {
            "label": label_str,
            "action": action_str,
        }

        save_config(self.menu_data)
        if self.build_win:
            self.build_win.destroy()
            self.build_win = None
        self.close_modal()
        self.update_display()

    def close_modal(self):
        # Destroy all possible outer containers and windows
        if hasattr(self, "build_outer_container") and self.build_outer_container:
            self.build_outer_container.destroy()
            self.build_outer_container = None
            
        if hasattr(self, "outer_modal_container") and self.outer_modal_container:
            self.outer_modal_container.destroy()
            self.outer_modal_container = None

        if hasattr(self, "build_win") and self.build_win:
            self.build_win.destroy()
            self.build_win = None

        if hasattr(self, "modal_win") and self.modal_win:
            try:
                self.modal_win.destroy()
            except Exception:
                pass
            self.modal_win = None

        self.lbl_ready.configure(text="Ready")
        self.root.unbind("<F4>")
        self.root.unbind("<F2>")
        self.root.unbind("<Return>")
        self.root.unbind("y")
        self.root.unbind("Y")
        self.bind_keys()
        self.right_listbox.focus_set()
    
    def open_help_dialog(self, event=None):
        if self.top_menu_active or self.modal_win:
            return

        sections = self.load_markdown_help()

        self.modal_win = tk.Frame(
            self.root,
            bg=self.dos_colors["DOS_TIFFANY_BLUE"],
            highlightbackground=self.dos_colors["DOS_WHITE"],
            highlightthickness=2,
        )
        self.modal_win.place(relx=0.08, rely=0.08, relwidth=0.84, relheight=0.84)

        tk.Label(
            self.modal_win,
            text="HDM Help System (Press ESC to Close)",
            bg=self.dos_colors["DOS_RED"],
            fg=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        ).pack(fill=tk.X, pady=5)

        text_area = tk.Text(
            self.modal_win,
            bg=self.dos_colors["DOS_TIFFANY_BLUE"],
            fg=self.dos_colors["DOS_YELLOW"],
            font=self.small_dos_font,
            wrap=tk.WORD,
            bd=0,
            highlightthickness=0,
        )
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(self.modal_win, command=text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        text_area.config(yscrollcommand=scrollbar.set)
    
        text_area.tag_config(
            "heading", 
            foreground=self.dos_colors["DOS_WHITE"],
            font=self.dos_font,
        )

        for heading, content in sections:
            if heading:
                text_area.insert(tk.END, f"\n{heading}\n", "heading")
            text_area.insert(tk.END, f"{content}\n")

        text_area.config(state=tk.DISABLED)

        self.root.bind("<Escape>", self.close_help_dialog)

    def close_help_dialog(self, event=None):
        if not self.modal_win:
            return
        self.modal_win.destroy()
        self.modal_win = None
        self.root.unbind("<Escape>")
    
    def load_markdown_help(self, filepath=HELP_FILE_PATH):
        sections = []
        current_heading = ""
        current_content = []

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.rstrip()
                    if line.startswith("##"):
                        if current_heading or current_content:
                            sections.append((current_heading, "\n".join(current_content)))
                            current_content = []
                        current_heading = line.replace("##", "").strip()
                    else:
                        current_content.append(line)
                
                if current_heading or current_content:
                    sections.append((current_heading, "\n".join(current_content)))
        except FileNotFoundError:
            sections.append(("Error", "Help file (help.md) not found."))

        return sections
  
    def update_clock(self):
        now = datetime.datetime.now()

        date_part = now.strftime("%A, %B %d, %Y")
        hour = str(int(now.strftime("%I")))
        minute = now.strftime("%M")
        am_pm = now.strftime("%p").lower()

        time_str = f"{hour}:{minute}{am_pm}"
        full_text = f"{date_part}   {time_str}"

        self.lbl_datetime.configure(text=full_text)
        self.root.after(1000, self.update_clock)
    
    def open_terminal_shortcut(self):
        try:
            terminals = ["gnome-terminal", "konsole", "xfce4-terminal", "lxterminal", "xterm"]
            selected_term = None
            
            for term in terminals:
                if shutil.which(term):
                    selected_term = term
                    break
                    
            if selected_term:
                subprocess.Popen([selected_term])
            else:
                subprocess.Popen("x-terminal-emulator", shell=True)
                
            self.lbl_ready.config(text="Terminal opened via F9")
            self.root.after(3000, lambda: self.lbl_ready.config(text="Ready"))
            
        except Exception as e:
            self.lbl_ready.config(text=f"Error opening terminal: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = HardDiskMenuApp(root)
    root.mainloop()
