## How to use the Help System
Help topics are detailed below in White Header Text and explanation text for the highlighted topic is shown in Yellow Text.

Up Arrow, BackSpace Key: Go up one Help topic.
Down Arrow, Space Bar: Go down one topic.
Home Key, - Key: Go to first topic.
End Key, + Key: Go to last topic.
Letter & Number Keys: Go directly to topic.
PgUp/PgDn: Go up/down topics screen.
F1 Key: Go to first Help screen.
F3 Key: Exit Help, return to TERMINAL.
Escape Key: Exit Help, return to HDM.

## MOUSE:
Left Button = Click, Right Button = Esc.
Click on the topic in the left window to display it in the right window. Click on the up & down arrow heads at the bottom to move the cursor. Click on the keys listed at the bottom to perform that action.

## Keys active while in the User Menu
LETTER KEYS (A-Z): Go directly to page of entries.
NUMERIC KEYS (0-9): Run entry on the current page.
UP ARROW or BACKSPACE: Go to previous menu entry.
DOWN ARROW or SPACE BAR: Go to next menu entry.
PGUP or LEFT ARROW: Go to prior page of entries.
PGDN or RIGHT ARROW: Go to next page of entries.
CTRL-PGUP: Go up one screen of pages (about 8).
CTRL-PGDN: Go down one screen of pages (about 8).
HOME KEY: Go to the first existing menu entry.
END KEY: Go to the last existing menu entry.
ENTER KEY: Run the highlighted User Menu entry.
INS KEY: Add a new User Menu entry.
DEL KEY: Delete a User Menu entry.
ALT-F1 KEY: Add, Change, Delete entry's security.
F2 KEY: Change a User Menu entry.
F4 KEY: Copy a User Menu entry.
F6 KEY: Move a User Menu entry.
F8 KEY: Switch two User Menu entries.
F9 KEY: Open Terminal
F10 KEY: Activates and displays the Top Menu.

## How to use the Top Menu... F10/Alt-F10
You cannot activate the Top Menu from Help or Logo. Press F10 at any other time to go to the Top Menu, then highlight your choice and press ENTER to pull down a window. The Top Menu choices are:

MENU:      Add, change, delete, copy, move, & switch
           User Menu entries. Save menu to disk.

PAGE:      Compress, erase, copy, or name a page of
           entries. Switch all entries in two pages.

SECURITY:  Add, change, or delete passwords for all
           security levels. Put security on one or
           all User Menu entries or pull-down menus;
           hide the Top Menu, and set up user IDs.

LOCAL:     Set border type, colors, macros, titles,
           background, date & time. Display actions
           and Date/Top Menu, switch the Page Index
           and User Menu. (Current menu file only).

GLOBAL:    Set cursor, mouse, phone, screen blanker,
           projects, timed & delayed executions.

EXIT:      Quit HDM, TERMINAL Window, Log Off, Reports.

## Keys active in the Top Menu
To pull down a window from the Top Menu: press F10 to get to the Top Menu, then press the highlighted letter. Another way is to press Alt and the highlighted letter: Alt-M for Menu, Alt-P for Page, Alt-S for Security, Alt-L for Local, Alt-G for Global, or Alt-X for eXit. Press Alt-F10 from the User Menu to go to the last Pull Down menu entry. To start a Pull Down menu entry, move the cursor and press ENTER or just press the highlighted key.

LEFT ARROW: Go to previous Top or Pull Down menu.
RIGHT ARROW: Go to the next Top or Pull Down menu.
UP ARROW: Move up or open a pull down window.
DOWN ARROW: Move down or open a pull down window.
HOME: Go to first entry in the current menu.
END: Go to last entry in the current menu.
F1: Get help.
ALT-F1: Set security for Pull Down menu entry.
ESC or F10: Return to the previous menu/screen.

## MENU Maintenance Pull Down Window... Alt-M
ADD         (Ins)    Add a new entry to the User Menu.
CHANGE      (F2)     Edit an entry in the User Menu.
DUPLICATE   (F4)     Copy an entry in the User Menu.
ERASE       (Del)    Delete an entry from the User Menu.
MOVE        (F6)     Move an entry in the User Menu.
SWITCH      (F8)     Swap two menu entries.
WRITE FILE  (Ctrl-F10) Save menu data to disk.

(Key) is a short cut to the pull down menu entries. If an entry has a security level, you may have to enter a password first. Alt-F1 is used to set it. A User Menu entry consists of a Menu Description and a Menu Action. The description can be up to 48 characters long. It is what the user sees in the HDM User Menu as menu entries. The action is what the menu does when the user chooses one of the User Menu entries. It consists of TERMINAL commands, macros batch files, programs, and special HDM {functions} seperated by the tilde ~ character.

## PAGE Maintenance Pull Down Window... Alt-P
COMPRESS    (Ctrl-F1) moves entries to top of a page.
ERASE       (Ctrl-F2) non-protected entries in a page.
IMPORT      (Ctrl-F3) entries from another page/file.
NAME        (Ctrl-F4) change name in the Page Index.
SWITCH      (Ctrl-F5) swap two pages in current file.

This menu lets you make changes to the names in the page index and lets you erase all the non-password protected entries in one page at once. Page import lets you copy a page of User Menu entries from any menu file (including the current one) to a page in the current menu file. Entries are only copied to matching ones in the current file that are empty. Any existing entries will not be overwritten, so if you want to copy all ten entries in a page, make sure you copy them to a completely empty page. Compress moves all entries in a page to the top of that page and leaves all the empty entries at the bottom. You can switch the contents of two pages.

## SECURITY Password Pull Down Window... Alt-S
SET SECURITY (Alt-F1): protect one User Menu entry.
PAGE SECURITY (Alt-F2): security level for a page.
ALL ENTRIES (Alt-F3): security level for menu file.
FILE CHANGE (Alt-F4): prevent changes to menu file.
TOP MENU ENTRIES (Alt-F5): security for Top Menu.
HIDE TOP MENU (Alt-F6): (use /UNHIDE to unhide it)
LOGOFF AUTOMATICALLY (Alt-F7): auto Log Off & Exec.
MASTER PASSWORD TABLE (Alt-F8): security passwords.
USER ID TABLE (Alt-F9): set user names & passwords.

The security administrator should set the highest levels in the security table as master passwords. This allows you to over-ride other passwords that were forgotten or not known. You can protect the User Menu entries individually or as a group, you can also put security on each pull down menu entry or on the whole group. To remove security, use the same procedure that set it, enter zero as the security level and the old password if needed.

## LOCAL Variables Pull Down Window... Alt-L
ACTION DISPLAY (Shift-F1) Show Actions in Top Box.
BORDER LINES   (Shift-F2) Single/Double/Bold/None.
CHANGE COLORS  (Shift-F3) User Menu & all Windows.
DATE/TOP MENU  (Shift-F4) Date, Top Menu, or Both.
LINES IN MENU  (Shift-F5) Change User Menu Lines.
MENU MACROS    (Shift-F6) Set Menu Action Macros.
SWITCH SCREENS (Shift-F7) Alternate User Menus.
TOP BOX TITLES (Shift-F8) Change Titles in Top Box.
WALLPAPER      (Shift-F9) Set Background Character.

Changes to any of the above variables affect only the current menu file. There are a total of 1000 menu files all together, each can have a different set of local variables. The menu files are named HDM.000 through HDM.999. You create or access them using the {MENU ###} action function in any of the User Menu entries. You can give each of your menu files a completely different look by using unique colors, borders, lines, titles, background, etc.

## GLOBAL Variables Pull Down Window... Alt-G
BLINKING CURSOR (Alt-1) Set Cursor Blink Speed.
CHANGE PROJECT  (Alt-2) Change Project Number.
DATE AND TIME   (Alt-3) Set US/European/Military.
GLOBAL SETTINGS (Alt-4) Configuration Switches.
INACTIVE EXECUTE (Alt-5) Run at Inactive Timeout.
MOUSE SPEED     (Alt-6) Horizontal/Vertical Speed.
PHONE PARAMETERS (Alt-7) COM Port, IRQ, Dial Type.
SCREEN BLANKER  (Alt-8) Blank at Inactive Timeout.
TIMED EXECUTION (Alt-9) Auto Running of Entries.

Global variables affect all menu files. Changes can can be made to the rate of blinking of the cursor, the speed of the horizontal and vertical motion of the mouse, and the date and time format. You can exclude blank pages and entries, keep the cursor on the current page, set tone/pulse, IRQ #, and port # for the {DIAL} function. Set the screen blank time and user message. Run any entry unattended at any time, day, week, month, or after an inactive time.

## EXIT Pull Down Window... Alt-X
TERMINAL WINDOW (F9): TERMINAL Prompt with Command Recall.
LOGOFF     (F7): Logoff User. Optionally Run Entry.
PRIOR MENU (Esc): Go to Previous Menu File screen.
REPORTS    (F5): Go to HDM Usage Log report module.
EXIT HDM   (F3): To TERMINAL prompt. Enter X to return.

The TERMINAL window can be used to run anything that can be used in a normal User Menu entry, including TERMINAL commands, batch files, programs, action functions, and macros. It also retains the last nine entries run from it. You can scroll through them with the arrow keys and change them or just run them as they are. If a user is logged on, LOGOFF logs them off. Prior Menu returns to calling {MENU ###} menu file. Return goes back to the User Menu no matter where you are in the Hard Disk Menu. Exit takes HDM out of memory and gives you the TERMINAL prompt. Key in "X" at the TERMINAL prompt to return to HDM. The "X" can be renamed with the "Set X=" environment variable.

## COMMON HDM KEYS and MOUSE USAGE
F1: Get Help from anywhere except the Logo screen.
F2: Save entries keyed into data entry fields.
F3: Exit HDM and go to the TERMINAL prompt at any time.
F10: Get the Top Menu any time execpt Logo or Help.
Alt-F10: Go to the last active pull down menu.
Esc: Cancel and go to the previous window or menu.
Ctrl-B: will force the Screen Blanker to activate.
Ctrl-F: will Freeze HDM so that no screen writing will be done and all automatic executions will be suspended until a key is pressed. This is useful when in the background on a multitasking computer.
Ctrl-U: will Undo menu changes if * is displayed.

MOUSE: Click Right Button to cancel (same as Esc). Click Left Button on the following spots:
Any menu entry... Starts appropriate action
Key assignments.. Same as pressing that key
Up/down arrows... Move cursor up or down
Outside window... Close window

## Useful keys in EDIT mode
--> or <-- : Arrows move the cursor one position.
-->| or |<--: Tab moves the cursor 8 positions.
UP↑ or DOWN↓: Moves to the previous or next field.
PGUP or PGDN: Moves to the first or last field.
HOME or END: Moves to the start or end of a field.
CTRL-HOME: Deletes from cursor to start of field
CTRL-END: Deletes from cursor to end of field.
CTRL-BACK-SP: Deletes entire field.
DELETE KEY: Deletes the character at the cursor.
BACK SPACE: Deletes the character left of cursor.
INSERT KEY: Switches between insert & overwrite.
CTRL-U: (Undo) Restores field to original.
ENTER KEY: Accepts changes & goes to next field.
F2 KEY: Saves changes and ends editing.
ESCAPE KEY: Cancels changes and ends editing.

MOUSE: Click on field to move cursor to it. Click outside of edit window to cancel it.

## Setting up Entries
For python programs in virtual environments complete Python venv field, Directory field for working directory and Program field to run in the 
program located in the working directory.

For non python programs leave blank Python venv and Directory fields.

See sample entries of how to setup python and non python programs are included.
