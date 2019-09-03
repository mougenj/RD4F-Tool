# RD4F-Tool

## Basic purpose of the tool
This tool allows to manage (read and create) JSON files of the Reaction-Diffusion 4 Fusion database, compare easly data of those files and convert data for inputs of Raction-Diffusion codes (e.g. TMAP). The Reaction-Diffusion 4 Fusion is composed by JSON files which contain main diffusion and trapping parameters of adatom (e.g. hydrogen or helium) in material (e.g. tunsgten, aliminium, beryllium, carbon or stainless steel). The parameters (diffusion & recombinaison coefficients, solubility, trap energies & densities) are extracted from the scientific litterature which can provide different sets of parameters for one adatom/material couple. There is so one file per ad-atom/material couple and per source of data (e.g. a file for hydrogen in tungsten from Frauenfelder et al. publication and another file for hydrogen in tunsgten from Fernandez et al. publication) . The basic purpose of the Reaction-Diffusion 4 Fusion Database and Tool is to make it easier to use diffusion and trapping parameters for numerical codes (avoiding entry and converting errors into different codes) and their dissemination.

## How to install it?
In the release section you can download compiled versions of the tool for Windows (x64) and Linux (x64) systems. Just extract the archive and execute the main.exe (Windows) or main (Linux) file. No python library is requiered.

## How to compile it?
To compile the tool from source, you must have Python 3 installed on your machine, as well as the following modules: matplotlib, PyQt5, numpy, pdb, sqlite3, rlcompleter, functools, json and re. For displaying additional information about DOIs, you may want to install the crossref module.  
To install them, you should install Python3 first, then install pip (the package installer for Python). Finally, install every modules by using "pip install module_name".  
On Linux:
```
sudo apt-get install python3 python3-pip git # (some of them should be already on your machine)
sudo python3 -m pip install matplotlib PyQt5 numpy pdb sqlite3 rlcompleter functools json re crossrefapi
git clone https://github.com/Ribodou/LSPM-Gui
cd LSPM-Gui
python3 main.py
```
On Windows:
After having installing git (https://git-scm.com/download/win), go to https://www.python.org/downloads/windows/ and click on "Latest Python 3 Release". Execute the Python installer. At the end of the installation, the installer will let you add Python to your PATH. Be sure to add Python in your PATH, otherwise you won't have access to pip (wich is required to install modules). Then, use pip to install every modules. Depending on your version of Windows, you might already have some of them on your machine. In such case, if you try to install them, you might get an error. You should just ignore them and re-enter the command without the troublesome modules.
```
python -m pip install matplotlib PyQt5 numpy functools crossrefapi
git clone https://github.com/Ribodou/LSPM-Gui
cd LSPM-Gui
python main.py
```
This way, you can execute the program via command-line interface, via "python main.py" on Windows, or "python3 main.py" on Linux.  

However, you may want to build an executable (ie: double-click on it to execute it). In this case, you will have to "compile" the python program. In this case, the crossref module is mandatory. To compile python scripts, you should install another module: pyinstaller. Then, type "pyinstaller main.py --exclude-module PyQt4 --onedir --noconsole" in a console while being in the LSPM-Gui folder.
```
sudo python3 -m pip install pyinstaller
pyinstaller main.py --exclude-module PyQt4 --onedir --noconsole
```
This sould create a folder, named "dist", with a folder inside, named "main". Inside this "main" folder, there is an executable named "main". You cand double-click to lauch it, and create a shortcut and place it wherever you want.  

You can also compress the "dist" folder and then unzip it on another machine runnig the same OS. You will still be able to launch it even if this machine don't have python installed.

## Credits
The project and programmation began during the interships of Lucas Robidou and Thibaud Carré (april-july 2019); both engineering students of the Sup'Galilée Engineering School (Université Paris 13). Interships were financed by the LSPM laboratory (CNRS UPR 3407 - France) and supervised by Jonathan Mougenot. We thank the ITER Scientist Fellowship "Fuel Retention Management" lead by Greg De Temmerman for the discussions and recommendations. The tool is licensed under the GNU General Public License v3.0.

