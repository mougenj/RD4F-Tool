import DragAndDrop
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QWidget,
                             QPushButton,
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout, 
                             QTabWidget,
                             QScrollArea,
                             QGridLayout,
                             QScroller,
                             QTabBar,
                             QFileDialog,
                             QMessageBox,
                             QLineEdit,
                             QGroupBox
                            )
from PyQt5.QtGui import QPixmap, QFontMetrics
from ShowNewFile import ShowNewFile
import json
import numpy as np
from functools import partial
import pdb
import rlcompleter
import time

class SecondTab(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        tab_left = QTabWidget(tabsClosable=True)
        def CloseTab(i):
            tab_left.removeTab(i)
            self.data_onglets.pop(i)
        tab_left.tabCloseRequested.connect(CloseTab)
        tab_left.setTabPosition(QTabWidget.West)

        boutton_ajout_fichiers = QPushButton("Ajout de fichier(s)")
        boutton_ajout_fichiers.clicked.connect(partial(self.on_click_open_files, tab_left))

        add_files = make_vbox()
        add_files.layout.addWidget(QPushButton("Selectionnez un squelette de fichier depuis la base de données"))
        add_files.layout.addWidget(QPushButton("Enregistrez le fichier"))
        add_files.layout.addWidget(DragAndDrop.FileEdit("Glisser vos fichiers ici", partial(self.open_new_file, tab_left)))
        add_files.layout.addWidget(boutton_ajout_fichiers)

        # TODO: commenter
        with open("/home/tcarre/LSPM-Gui/ressources/json.txt") as fichier:
            self.open_new_file(tab_left, "nom", json.loads(fichier.read()))
        files_vbox = make_vbox()
        #files_vbox.layout.addWidget(tab_left)
        files_vbox.layout.addWidget(add_files)

        self.layout.addWidget(tab_left)
        self.layout.addWidget(files_vbox)

    def open_new_file(self, tab, name, parameters):
        decoupe = lambda chaine : "..." + chaine[-5:] if len(chaine) > 10 else chaine
        tab.addTab(ShowNewFile(parameters, editable=True), decoupe(name))

    @pyqtSlot()
    def on_click_open_files(self, tab_to_add):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        sucessfully_loaded = []
        failed = []
        for filepath in files:
            try:
                with open(filepath, "r") as fichier: 
                    liste = json.loads(fichier.read())
                sucessfully_loaded.append((filepath, liste))
            except Exception as e:
                failed.append(filepath)
        if failed:
            dialog = QMessageBox()
            if len(failed) > 1:
                dialog.setWindowTitle("Error: Invalid Files")
            else:
                dialog.setWindowTitle("Error: Invalid File")
            error_text = "An error occured when loading :"
            for failure in failed:
                error_text += "\n" + failure
            dialog.setText(error_text)
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()
        for success in sucessfully_loaded:
            get_name_from_path = lambda path : path.split("/")[-1].split('.', 1)[0]
            filepath, liste = success
            self.open_new_file(tab_to_add, get_name_from_path(filepath), liste)


def make_vbox():
    vbox = QWidget()
    vbox.layout = QVBoxLayout()
    vbox.setLayout(vbox.layout)
    return vbox

def make_hbox():
    hbox = QWidget()
    hbox.layout = QHBoxLayout()
    hbox.setLayout(hbox.layout)
    return hbox