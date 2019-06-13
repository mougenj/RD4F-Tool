# LSPM-Gui
A GUI made by the LSPM
## how to install it
To install it you must have Python 3 installed on your machine, as well as the following modules: matplotlib, PyQt5, numpy, pdb, sqlite3, rlcompleter, functools, json and re. For displaying additional information about DOIs, you may want to install the crossref module.  
To install them, you should install Python3 first, then install pip (the package installer for Python). Finally, install every modules by using "pip install module_name".  
On Linux:
```
sudo apt-get install python3 python3-pip git # (some of them should be already on your machine)
sudo python3 -m pip install matplotlib PyQt5 numpy pdb sqlite3 rlcompleter functools json re crossref
git clone https://github.com/Ribodou/LSPM-Gui
cd LSPM-Gui
python3 main.py
```
This way, you can execute the program via command-line interface, via "python main.py" on Windows, or "python3 main.py" on Linux.  

However, you may want to build an executable (ie: double-click on it to execute it). In this case, you should install another module: pyinstaller. Then, type "pyinstaller main.py --exclude-module PyQt4 --onedir --noconsole" in a console while being in the LSPM-Gui folder.
```
sudo python3 -m pip install pyinstaller
pyinstaller main.py --exclude-module PyQt4 --onedir --noconsole
```
This sould create a folder, named "dist", with a folder inside, named "main". Inside this "main" folder, there is an executable named "main". You cand double-click to lauch it, and create a shortcut and place it wherever you want.  

You can also compress the "dist" folder and then unzip it on another machine runnig the same OS. You will still be able to launch it even if this machine don't have python installed.
