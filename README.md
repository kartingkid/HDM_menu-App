# HDM Launcher (hdm_launcher.py)

HDM Launcher is a DOS retro-styled desktop application built with Python and Tkinter. It features a top-level drop-down menu navigation system, status bar indicators, and global/local keyboard shortcuts reminiscent of classic Norton Commander or DOS utility interfaces.

---

## Features

* **Interactive Top-Level Menu:** Categorized navigation (Security, Local, Global, etc.) accessible via mouse or keyboard mnemonic hotkeys.
* **Global & Local Keyboard Shortcuts:** Fast execution of common utility tasks using function keys combined with `Alt`, `Shift`, or `Ctrl`.
* **Dynamic Status Bar:** Real-time feedback and state indicators at the bottom of the interface.
* **Modal Window & Guard Support:** Safeguards built into menu actions to prevent overlapping triggers when active modals or dropdown menus are open.

---

## Selection of Keyboard Shortcuts

Their is a detailed help file to explain the all the key functions.

| Shortcut | Action | Category / Description |
| :--- | :--- | :--- |
| **Alt-F1** | Set Security (1 Entry) | Security |
| **Alt-F5** | Top Menu Entries (All) | Security |
| **Ctrl-F5** | Switch Pages | Navigation / View |
| **Shift-F3** | Change Colors | Local Customization |
| **Shift-F9** | Wallpaper | Local Customization |
| **Alt-4** | Global Settings | Global Configuration |
| **Alt-8** | Screen Blanker | Global Utility |

---

## Requirements

* **Python 3.x**
* **Tkinter** (Standard GUI library, usually included with standard Python installations on Windows/Linux/macOS).

---

## Installation & Running

1. Clone or download the repository containing `hdm_launcher.py`.
2. Open your terminal or command prompt in the project directory.
3. Run the application using Python:

```bash
python hdm_launcher.py
