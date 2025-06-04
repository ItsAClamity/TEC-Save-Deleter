import configparser
import os
import tkinter as tk
from pyamf import sol
from tkinter import scrolledtext, filedialog, messagebox
import time
import threading

# Read config file
config = configparser.ConfigParser()
config.read("config.ini")
settings = config['Settings']

# Define file criteria
file_criteria = lambda name: name.endswith('.sol')

# Create UI
window = tk.Tk()
window.title("The Elephant Collection - Save File Deleter")
window.geometry("800x400")

# String to display
status_string = tk.StringVar(window, value="Ready")
first_press = tk.BooleanVar(window, value=True)

#Global variables
is_scanning = False
is_deleting = False
cancel_event = threading.Event()


# Check save on open
def check_save():
    directory = dir_var.get()
    sol_path = directory + "/ELC_SAVE.sol"
    try:
        os.path.getmtime(sol_path)
        save_found = True
    except OSError:
        memories = get_total_mems(directory)
        if memories == 0:
            save_found = False
            status_string.set("No save file found.")
        else:
            save_found = True
            output_box.insert(tk.END, "ELC_SAVE.sol not found, but elephantrave4k.sol was... If you didn't manually delete ELC_SAVE.sol yourself let the developer know you're seeing this message.")
    if save_found == True:
        memories = get_total_mems(directory)
        if memories == 1:
            status_string.set(f"Save file found. {memories} memory unlocked.")
        else:
            status_string.set(f"Save file found. {memories} memories unlocked.")
    return save_found

def get_total_mems(directory):
    ER_path = directory + "/elephantrave4k.sol"
    try:
        with open(ER_path, "rb") as f:
            game_dict_full = sol.load(f)
            game_dict = game_dict_full["saveObject"]
            game_dict.setdefault('metagameScore',0)
            total = game_dict["metagameScore"]
            return total
    except OSError:
        return 0


# Function to delete files and return the names of deleted files
def delete_files(directory, criteria):
    deleted_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if criteria(filename):
                full_path = os.path.join(root, filename)
                os.remove(full_path)
                deleted_files.append(f"Deleted: {full_path}")
    return deleted_files


def list_and_confirm_deletion():
    directory = dir_var.get()
    sol_files = []
    output_box.insert(tk.END, "\nNo ELC-SAVE.sol found in top level, scanning directory for all .sol files...")
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if file_criteria(filename):
                sol_files.append(os.path.join(root, filename))
                output_box.insert(tk.END, f"\nFound {filename} in {root}.")

    if not sol_files:
        output_box.insert(tk.END, "\nNo save files (.sol) found in chosen directory or subfolders. If there is an active save, check the directory is correct.")
        return False

    file_list = "\n".join(sol_files)
    confirm = messagebox.askyesno("Confirm Deletion", f"No ELC-SAVE.sol found in top level, but the following .sol files were detected:\n\n{file_list}\n\nDo you want to delete them?")
    if confirm:
        return True
    else:
        sol_amount = len(sol_files)
        output_box.insert(tk.END, f"\n{sol_amount} .sol files found, but deletion operation was aborted by user.")
        return False

#Scan for File
def scan_and_set_directory_thread():
    global is_scanning

    fp = first_press.get()
    if fp == False:
        output_box.insert(tk.END, "\n\n")
    first_press.set(False)

    output_box.insert(tk.END, f"Scanning for The Elephant Collection save file...")
    base_dir = dir_var.get()
    found = False

    for root, dirs, files in os.walk(base_dir):
        if cancel_event.is_set():
            output_box.insert(tk.END, "\nScan cancelled by user.")
            break

        status_string.set(f"\nChecking:\xa0{root}")
        output_box.yview_moveto(1.0)
        output_box.update_idletasks()

        if "ELC_SAVE.sol" in files:
            if base_dir == root:
                output_box.insert(tk.END, f"\nBase save file found in current directory.")
            else:
                dir_var.set(root)
                settings['saves_directory'] = root
                with open("config.ini", "w") as configfile:
                    config.write(configfile)
                output_box.insert(tk.END, f"\nBase save file found in: {root}\nUpdated directory to saves ")
            found = True
            break

    if not found and not cancel_event.is_set():
        output_box.insert(tk.END, "\nBase save file not found in selected directory or subdirectories.")

    if not cancel_event.is_set():
        check_save()

    # Reset state after scan
    is_scanning = False
    cancel_event.clear()
    confirm_button.config(text="Locate/Check Save", command=start_scan)

def start_scan():
    global is_scanning
    if is_scanning:
        return  # Prevent double start

    is_scanning = True
    cancel_event.clear()
    confirm_button.config(text="Cancel Scan", command=cancel_scan)
    threading.Thread(target=scan_and_set_directory_thread, daemon=True).start()

def start_delete():
    global is_deleting
    if is_deleting:
        return  # Prevent double start

    is_deleting = True
    cancel_event.clear()
    confirm_button.config(text="Cancel Scan", command=cancel_scan)
    threading.Thread(target=on_delete_click, daemon=True).start()

def cancel_scan():
    cancel_event.set()

# Delete Saves Button Click
def on_delete_click():
    global is_deleting

    fp = first_press.get()
    if fp == False:
        output_box.insert(tk.END, "\n\n")
    first_press.set(False)    
    output_box.insert(tk.END, "Deleting saves... ")
    save_found = check_save()
    #output_box.delete(1.0, tk.END)
    directory = dir_var.get()
    if save_found == False:
        save_found = list_and_confirm_deletion()
    if save_found == True:
        deleted_files = delete_files(directory, file_criteria)
        if deleted_files:
            output_box.insert(tk.END, "\n".join(deleted_files))
            status_string.set(f"Deleted {len(deleted_files)} file(s)")
        else:
            output_box.insert(tk.END, "\n Save file detected, but no saves deleted. Huh? You shouldn't be seeing this message.")   
    output_box.see(tk.END) 

    # Reset state after scan
    is_deleting = False
    cancel_event.clear()
    confirm_button.config(text="Locate/Check Save", command=start_scan)

# Function to choose folder and update config file
def choose_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        dir_var.set(folder_selected)
        settings['saves_directory'] = folder_selected
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        status_string.set(f"Directory set to: {folder_selected}")
    check_save()

# Folder selection row
folder_frame = tk.Frame(window)
folder_frame.pack(pady=10, fill=tk.X, padx=10)

dir_var = tk.StringVar(value=settings.get('saves_directory', ''))
dir_entry = tk.Entry(folder_frame, textvariable=dir_var, width=60)
dir_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
select_button = tk.Button(folder_frame, text="Browse", command=choose_folder)
select_button.pack(side=tk.RIGHT)

button_frame = tk.Frame(window)
button_frame.pack(pady=10)

# Delete button
delete_button = tk.Button(button_frame, text="Delete Saves", command=start_delete, font=("Arial", 14))
delete_button.pack(side=tk.LEFT, pady=10, padx=30)

# New button to list and confirm delete
confirm_button = tk.Button(button_frame, text="Locate/Check Save", command=start_scan, font=("Arial", 14))
confirm_button.pack(side=tk.RIGHT, pady=10, padx=10)

class WrappingLabel(tk.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))

# Status label
status_label = WrappingLabel(window, textvariable=status_string, anchor='nw', justify='left', font=("Arial", 12))
status_label.pack(expand=True, fill=tk.X, padx=10, pady=(0, 10))

# Output text box
output_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=200, height=100, font=("Courier", 10))
output_box.pack(expand=True, fill=tk.X, padx=10, pady=10)

check_save()

# Run the UI loop
window.mainloop()
