import DragAndDrop
from PyQt5.QtCore import pyqtSlot, Qt
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
                             QGroupBox,
                             QCompleter
                            )
from PyQt5.QtGui import QPixmap, QFontMetrics, QPalette
from PyQt5.QtCore import QStringListModel
from ShowNewFile import ShowNewFile
from QLineEditWidthed import QLineEditWidthed
import json
import numpy as np
from functools import partial
import pdb
import rlcompleter
import time
import os
import sqlite3
import dataFunctions


class tooManyValues(Exception):

    def __init__(self, msg):
        super().__init__(msg)


class BDDNonTrouvee(Exception):

    def __init__(self):
        super().__init__()


class SecondTab(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        # sauvegarde de la couleur du fond
        color = self.palette().color(QPalette.Background)
        rgba = color.red(), color.green(), color.blue(), color.alpha()
        self.background = rgba
        
        tab_left = QTabWidget(tabsClosable=True)
        def CloseTab(i):
            tab_left.removeTab(i)
        tab_left.tabCloseRequested.connect(CloseTab)
        tab_left.setTabPosition(QTabWidget.West)
        tab_left.setFocusPolicy(Qt.NoFocus)

        search_bar = make_hbox()
        search_bar.layout.addWidget(QLineEditWidthed("Choose a name of a material to load it from the database :"))
        search_bar.layout.addWidget(SearchBar("database.sqlite", self, tab_left))

        button_add_files = QPushButton("Add file(s)")
        button_add_files.clicked.connect(partial(self.on_click_open_files, tab_left))
        button_save = QPushButton("Save the file")
        button_save.clicked.connect(partial(self.save, tab_left.currentIndex))
        add_files = make_vbox()
        add_files.layout.addWidget(search_bar)
        add_files.layout.addWidget(button_save)
        add_files.layout.addWidget(DragAndDrop.FileEdit("Drop your files here", partial(self.open_new_file, tab_left)))
        add_files.layout.addWidget(button_add_files)

        # TODO: commenter
        with open("json.txt") as fichier:
            self.open_new_file(tab_left, "Exemple", json.loads(fichier.read()))
        files_vbox = make_vbox()
        #files_vbox.layout.addWidget(tab_left)
        files_vbox.layout.addWidget(add_files)

        self.layout.addWidget(tab_left)
        self.layout.addWidget(files_vbox)
        self.save(tab_left.currentIndex)

    def open_new_file(self, tab, name, parameters):
        decoupe = lambda chaine : "..." + chaine[-10:] if len(chaine) > 10 else chaine
        #get background color
        snf = ShowNewFile(parameters, self.background, editable=True)
        tab.setCurrentIndex(tab.addTab(snf, decoupe(name)))

    def save(self, functionToCallToGetIndex):
        """
            Save a file (ie: a tab) to a json file. Each file is represented by 4 sub tabs.)
        """
        index = functionToCallToGetIndex()
        data_to_save = {
            "material" :{},
            "source" :{},
            "traps" : [],
            "equation" : {}
        }
        tabs = self.findChild(QTabWidget)
        snf = tabs.widget(index)
        tabs_to_save = snf.findChild(QTabWidget)

        for scroller in tabs_to_save.findChildren(QScrollArea):
            filtre = ["traps", "material", "source", "equation"]
            vbox_or_grid = [x for x in scroller.findChildren(QWidget) if x.objectName() in filtre]
            if len(vbox_or_grid) != 1:
                print("WARNING :", len(vbox_or_grid), "widget are named", filtre, "in a tab.")
            vbox_or_grid = vbox_or_grid[0]  # we extract the only element in it
            
            if vbox_or_grid.objectName() == "equation":
                vbox = vbox_or_grid
                groupboxes = vbox.findChildren(QGroupBox)
                for groupbox in groupboxes:
                    grid_layout = groupbox.findChild(QGridLayout)
                    coef1 = grid_layout.itemAtPosition(0, 0).widget().text()
                    val1 = grid_layout.itemAtPosition(0, 1).widget().text()
                    coef2 = grid_layout.itemAtPosition(1, 0).widget().text()
                    val2 = grid_layout.itemAtPosition(1, 1).widget().text()
                    if groupbox.objectName() == "diffusivity":
                        equation_type = "D"
                    elif groupbox.objectName() == "solubility":
                        equation_type = "S"
                    elif groupbox.objectName() == "combination":
                        equation_type = "Kr"
                    else:
                        print("WARNING : I don't know how to save", groupbox.objectName())

                    data_to_save["equation"][equation_type] = {}
                    data_to_save["equation"][equation_type][coef1] = val1
                    data_to_save["equation"][equation_type][coef2] = val2
            else:
                grid = vbox_or_grid
                if grid.objectName() == "material":
                    for row in range(grid.layout.rowCount()):
                        label = grid.layout.itemAtPosition(row, 0).widget().text()
                        value = grid.layout.itemAtPosition(row, 1).widget().text()
                        data_to_save["material"][label] = value
                elif grid.objectName() == "source":
                    for row in range(grid.layout.rowCount()):
                        label = grid.layout.itemAtPosition(row, 0).widget().text()
                        value = grid.layout.itemAtPosition(row, 1).widget().text()
                        data_to_save["source"][label] = value
                elif grid.objectName() == "traps":
                    for row in range(grid.layout.rowCount()):
                        dictionnary_of_this_trap = {}
                        for column in range(1, 4):
                            try:
                                hb = grid.layout.itemAtPosition(row, column).widget()
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
                            except AttributeError as e:  # attrape le bouton d'ajout
                                print(e)
                        # when a row is deleted from the grid, the number of
                        # the total row don't decrease, and thus the next row
                        # is added below a row that don't exists.
                        # that is why it is mandatory to check if the dictionnnary
                        # is empty (to remove the deleted rows)
                        if not dictionnary_of_this_trap == {}:
                            data_to_save["traps"].append(dictionnary_of_this_trap)
                else:
                    print("WARNING: I don't know how to save the grid named", grid.objectName())

        data_to_save = self.correctTypes(data_to_save)
        #pdb.Pdb.complete=rlcompleter.Completer(locals()).complete; pdb.set_trace()
        with open("sav.txt", "w") as fichier:
            fichier.write(json.dumps(data_to_save, indent=4))

    def correctTypes(self, data):
        for i in range(len(data["traps"])):
            for key in ("density", "energy", "angular_frequency"):
                try:
                    value = data["traps"][i][key]
                    if value == "None":
                        value = None
                    value = float(value) if value is not None else None
                    data["traps"][i][key] = value
                except KeyError as e:  # attrape le bouton d'ajout
                    print(e)
        for key in data["equation"]:
            for subkey in data["equation"][key]:
                value = data["equation"][key][subkey]
                value = float(value) if value is not None else None
                data["equation"][key][subkey] = float(value)
        year = data["source"]["year"]
        year = int(float(year)) if year is not None else None
        data["source"]["year"] = year
        for key in ("melting_point", "lattice_parameter", "density"):
            value = data["material"][key]
            value = float(value) if value is not None else None
            data["material"][key] = value
        value = data["material"]["atomic_number"]
        value = int(float(value)) if value is not None else None
        data["material"]["atomic_number"] = value
        return data

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


class SearchBar(QLineEdit):

    def __init__(self, dbname, parent, tabs):
        super().__init__()
        self.dbname = dbname
        self.parent = parent
        if not os.path.isfile(self.dbname):
            raise BDDNonTrouvee("base de donnes non trouvée")
        model = QStringListModel()
        model.setStringList(self.getMaterialNameFromDatabase())
        completer = QCompleter()
        completer.setModel(model)
        self.setCompleter(completer)
        self.returnPressed.connect(partial(self.loadDataFromDataBase, tabs))

    def loadDataFromDataBase(self, tabs):
        material_name = self.text()
        if not material_name in self.getMaterialNameFromDatabase():
            print(material_name, "not found in the database")
            return
        print("Let's load", material_name, "from the database.")
        materialData = self.getDataFromMaterialName(material_name)
        parameters = self.createPartialJSONFromDataMaterial(materialData)
        self.parent.open_new_file(tabs, "Default", parameters)
    
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