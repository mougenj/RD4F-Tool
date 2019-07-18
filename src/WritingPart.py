import DragAndDrop
from PyQt5.QtCore import pyqtSlot, Qt, QObject
from PyQt5.QtWidgets import (QWidget,
                             QPushButton,
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout, 
                             QTabWidget,
                             QGridLayout,
                             QFileDialog,
                             QMessageBox,
                             QGroupBox,
                             QTextEdit,
                             QShortcut
                            )
from PyQt5.QtGui import QPalette, QKeySequence
from PyQt5.QtCore import QStringListModel
import ShowNewFile
import json
from functools import partial
import pdb
import rlcompleter
import os
import sqlite3
import dataFunctions
from ReadingAndWritingPart import ReadingAndWritingPart

class tooManyValues(Exception):

    def __init__(self, msg):
        super().__init__(msg)


class BDDNonTrouvee(Exception):

    def __init__(self, msg):
        super().__init__()


class WritingPart(QWidget, ReadingAndWritingPart):

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        # save background color
        color = self.palette().color(QPalette.Background)
        rgba = color.red(), color.green(), color.blue(), color.alpha()
        self.background = rgba
        
        tab_left = QTabWidget(tabsClosable=True)
        def CloseTab(i):
            tab_left.removeTab(i)
        tab_left.tabCloseRequested.connect(CloseTab)
        tab_left.setTabPosition(QTabWidget.West)
        tab_left.setFocusPolicy(Qt.NoFocus)
        tab_left.setObjectName("tab_left")
        self.tab_left = tab_left

        search_bar = make_vbox()
        search_bar.layout.addWidget(QLabel("<html><center>Choose a name of a material to load it from the database :</center></html>"))
        search_bar.layout.addWidget(SearchButtons("database.sqlite", self, tab_left))

        button_add_files = QPushButton("Add file(s)")
        button_add_files.clicked.connect(partial(self.on_click_open_files, tab_left))
        button_save = QPushButton("Save the file")
        button_save.clicked.connect(partial(self.save, tab_left.currentIndex))
        add_files = make_vbox()
        add_files.layout.addWidget(search_bar)
        add_files.layout.addWidget(button_save)
        add_files.layout.addWidget(DragAndDrop.FileEdit("Drop your files here", partial(self.open_new_file, tab_left)))
        add_files.layout.addWidget(button_add_files)

        files_vbox = make_vbox()
        files_vbox.layout.addWidget(add_files)

        self.layout.addWidget(tab_left)
        self.layout.addWidget(files_vbox)
        self.shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut.activated.connect(partial(self.save, tab_left.currentIndex))


    def open_new_file(self, tab, name, parameters):
        decoupe = lambda chaine : "..." + chaine[-10:] if len(chaine) > 10 else chaine
        #get background color
        snf = ShowNewFile.ShowNewFile(parameters, self.background, editable=True)
        tab.setCurrentIndex(tab.addTab(snf, decoupe(name)))

    def save(self, functionToCallToGetIndex):
        """
            Save a file (ie: a tab) to a json file. Each file is represented by 4 sub tabs.)
        """
        try:
            data_to_save = self.getDataInFile(functionToCallToGetIndex)
            filename = QFileDialog.getSaveFileName(None, "Save File")[0]
            if filename[-4::] != ".txt":
                filename += ".txt"
            #pdb.Pdb.complete=rlcompleter.Completer(locals()).complete; pdb.set_trace()
            with open(filename, "w") as fichier:
                fichier.write(json.dumps(data_to_save, indent=4))
        except Exception as e:
            dialog = QMessageBox()
            dialog.setWindowTitle("Error")
            error_text = "An error occured while saving your file. It is likely that your file is filled with wrong datas (or maybe you don't have any file opened yet).\n"
            error_text += "Error text: " + str(e)
            dialog.setText(error_text)
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()

    @pyqtSlot()
    def on_click_open_files(self, tab_to_add):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
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


class SearchButtons(QWidget):

    def __init__(self, dbname, parent, tabs):
        super().__init__()
        self.dbname = dbname
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.parent = parent
        if not os.path.isfile(self.dbname):
            raise BDDNonTrouvee("base de donnes non trouvée")
        col_index = 0
        lin_index = 0
        for name in self.getMaterialNameFromDatabase():
            bt = QPushButton(name)
            bt.clicked.connect(partial(self.loadDataFromDataBase, bt, tabs))
            self.layout.addWidget(bt, lin_index, col_index)
            col_index += 1
            if col_index == 3:
                col_index = 0
                lin_index += 1

    def loadDataFromDataBase(self, bt, tabs):
        material_name = bt.text()
        if not material_name in self.getMaterialNameFromDatabase():
            print(material_name, "not found in the database")
            return
        print("Let's load", material_name, "from the database.")
        materialData = self.getDataFromMaterialName(material_name)
        parameters = self.createPartialJSONFromDataMaterial(materialData)
        self.parent.open_new_file(tabs, "Default", parameters)
        # show the new contant
        self.parent.tab_left.currentWidget().tabs.setCurrentIndex(1)
    
    def createPartialJSONFromDataMaterial(self, materialData):
        parameters = dataFunctions.create_empty_data()
        for key, value in materialData:
            parameters["material"][key] = value
        return parameters

    def getMaterialNameFromDatabase(self):
        db = sqlite3.connect(self.dbname)
        cursor = db.cursor()
        cursor.execute("SELECT LOWER(NAME) FROM MATERIAL;")
        db.commit()
        # première colonne uniquement
        rows = [result[0] for result in cursor.fetchall()]
        db.close()
        return rows


    def getDataFromMaterialName(self, material_name):
        db = sqlite3.connect(self.dbname)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM MATERIAL WHERE LOWER(NAME) = \"" + material_name + "\";")
        db.commit()
        #print(cursor.description)
        # première colonne uniquement, en minuscule s'il vous plait
        column_name = [description[0] for description in cursor.description]
        rows = cursor.fetchall()[0]
        db.close()
        return list(zip(column_name, rows))


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