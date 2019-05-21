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

class tooManyValues(Exception):

    def __init__(self):
        super().__init__()


class SecondTab(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        tab_left = QTabWidget(tabsClosable=True)
        def CloseTab(i):
            tab_left.removeTab(i)
        tab_left.tabCloseRequested.connect(CloseTab)
        tab_left.setTabPosition(QTabWidget.West)

        button_load_files = QPushButton("Selectionner un squelette de fichier depuis la base de données")
        button_add_files = QPushButton("Ajout de fichier(s)")
        button_add_files.clicked.connect(partial(self.on_click_open_files, tab_left))
        button_save = QPushButton("Enregistrer le fichier")
        button_save.clicked.connect(partial(self.save, tab_left.currentIndex))
        add_files = make_vbox()
        add_files.layout.addWidget(button_load_files)
        add_files.layout.addWidget(button_save)
        add_files.layout.addWidget(DragAndDrop.FileEdit("Glisser vos fichiers ici", partial(self.open_new_file, tab_left)))
        add_files.layout.addWidget(button_add_files)

        # TODO: commenter
        with open("/home/tcarre/LSPM-Gui/ressources/json.txt") as fichier:
            self.open_new_file(tab_left, "nom", json.loads(fichier.read()))
        files_vbox = make_vbox()
        #files_vbox.layout.addWidget(tab_left)
        files_vbox.layout.addWidget(add_files)

        self.layout.addWidget(tab_left)
        self.layout.addWidget(files_vbox)
        self.save(tab_left.currentIndex)

    def open_new_file(self, tab, name, parameters):
        decoupe = lambda chaine : "..." + chaine[-5:] if len(chaine) > 10 else chaine
        snf = ShowNewFile(parameters, editable=True)
        tab.addTab(snf, decoupe(name))

    def save(self, functionToCallToGetIndex):
        index = functionToCallToGetIndex()
        data_to_save = {
            "material" :{},
            "source" :{},
            "traps" : [],
            "equation" : {}
        }
        tabs = self.findChild(QTabWidget)
        snf = tabs.widget(index)
        scroll_area = snf.findChild(QScrollArea)

        for gb in scroll_area.findChildren(QGroupBox):
            if gb.objectName() == "material":
                for row in range(gb.layout.rowCount()):
                    label = gb.layout.itemAtPosition(row, 0).widget().text()
                    value = gb.layout.itemAtPosition(row, 1).widget().text()
                    data_to_save["material"][label] = value
            elif gb.objectName() == "source":
                for row in range(gb.layout.rowCount()):
                    label = gb.layout.itemAtPosition(row, 0).widget().text()
                    value = gb.layout.itemAtPosition(row, 1).widget().text()
                    data_to_save["source"][label] = value
            elif gb.objectName() == "traps":
                for row in range(gb.layout.rowCount()):
                    gb.layout.itemAtPosition(row, 0).widget().text()  # inutile
                    dictionnary_of_this_trap = {}
                    for column in range(1, 4):
                        hb = gb.layout.itemAtPosition(row, column).widget()
                        if hb.layout.count() > 2:
                            raise tooManyValues(
                                "Trop de valeur dans le champs des pieges pour"
                                " pouvoir lire correctement le fichier. Il "
                                "faut compléter la fonction de lecture du"
                                " formulaire."
                            )
                        label = hb.layout.itemAt(0).widget().text()
                        value = hb.layout.itemAt(1).widget().text()
                        dictionnary_of_this_trap[label] = value
                    data_to_save["traps"].append(dictionnary_of_this_trap)
            elif gb.objectName() == "equation":
                for row in range(gb.layout.rowCount()):
                    equation_type = gb.layout.itemAtPosition(row, 0).widget().text()
                    data_to_save["equation"][equation_type] = {}
                    for column in range(1, 3):
                        hb = gb.layout.itemAtPosition(row, column).widget()
                        if hb.layout.count() > 2:
                            raise tooManyValues(
                                "Trop de valeur dans le champs des equation"
                                " pour pouvoir lire correctement le fichier."
                                " Il faut compléter la fonction de lecture"
                                " du formulaire."
                            )
                        label = hb.layout.itemAt(0).widget().text()
                        value = hb.layout.itemAt(1).widget().text()
                        data_to_save["equation"][equation_type][label] = value
            else:
                raise tooManyValues(
                    "Trop de type de champs dans l'interface pour pouvoir "
                    "les écrire dans le fichier."
                )
        #pdb.Pdb.complete=rlcompleter.Completer(locals()).complete; pdb.set_trace()
        with open("/home/tcarre/sav.txt", "w") as fichier:
            fichier.write(json.dumps(data_to_save, indent=4))

        

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