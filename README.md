# The Elephant Colection Save Deleter
Save deletion automator written in python for The Elephant Collection.

![image](https://github.com/user-attachments/assets/0ba96f6f-5fdd-4c80-8fc5-736352551fe8)


## Features

- GUI interface for simplified use
- Displays current unlocked memory count if a save is found
- Can scan selected directory to find Elecphant Collection save file
- Confirms that you want to delete found .sol files if base save isn't located (technically means this could be used to quickly delete .sol saves for any flash game if you know where it's stored).

## Requirements
- Python 3.x (version 3.11 recommended)
- Py3AMF (can be installed from requirements.txt)

## Installation
### Install Python 3.11
You can download Python 3.11 from the official site: https://www.python.org/downloads/release/python-3110/

Make sure to tick "Add Python to PATH" during installation.

### Install Dependencies
In your terminal or command prompt, navigate to the project directory and run:

    pip install -r requirements.txt

## Usage

Run the script using:

    python EleDelGUI.py

Usage is pretty straightforward

- Browse - Select the folder with the base Elephant Collection save file or the folder to scan.
- Delete Saves - Delete the saves in the save file directory
    - f ELC_SAVE.sol is not found it will scan the directory for .sol files and ask you to confirm before deletion
 - Locate/Check Save - Will scan the current for the base save file, and once located will update the deletion directory to where it was found
     - If the save directory is already set correctly, this will tell you if the save currently exists, and if so, how many memories are currently unlocked.

On Windows, the default directory for The Elephant Collection saves should be:

    ../Users/<User>/AppData/Roaming/ElephantCollection/Local Store/#SharedObjects

*If anybody can confirm the default location on Mac then I'll add it in here too*

## Notes

- If you would like to avoid save loss **back up your save before deleting**. There is no way to recover the deleted files after deletion.
- It is reccomended to close out of the game before deleting saves.
    - Deleting saves while the game is open may cause save files not to be deleted properly or be rewritten with current game data.
- Thank you to jmtb02 and the Wonderful Elephant team for making the gane!
- This program may become obselete after the next major game update :P
