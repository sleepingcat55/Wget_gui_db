![Wget_gui_db_r](https://github.com/user-attachments/assets/d2d20ad0-18f5-4fc3-a15e-f950428ea75f)

# Wget_gui_db
Adding a GUI and a database to linux wget command
# Notes :
I make this project to answer fastly a personnal need, it remember which website has been mirrored by wget,
the time does it takes to mirror the website and the final size of the mirror folder.
Before you create a website mirror, you have to write the futur path folder.

As regards the code quality, I know it is ugly, I don't have time to refactoring it yet but surely one day in the future.
Furthermore, I don't understand all of aspects of the GUI Toolkit Dearpygui. So I found a "hack" to make my project works :
I used a bash script to kill the python script and then re-launch it.
It's my stuff to refresh the GUI

# How to install on linux (surely same procedure if you have a Mac. But for Windows, I'm sorry, I don't know how to do) :
- Make sure Python is installed.
- The script works on python3.12, if you don't have this version : download it. Else change the version name of python script : it's the 1st line (the shebang) you have to change the python version with yours.
- Install the GUI Toolkit with this command : pip install dearpygui.
- Make sure about permissions : sudo chmod 755 Wget_gui_db.py
 and :  sudo chmod 755 delete_and_restart.sh

# How to launch the script
Open a terminal and just write : ./Wget_gui_db.py
