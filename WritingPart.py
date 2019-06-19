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
from ShowNewFile import ShowNewFile
import json
from functools import partial
import pdb
import rlcompleter
import os
import sqlite3
import dataFunctions


class tooManyValues(Exception):

    def __init__(self, msg):
        super().__init__(msg)


class BDDNonTrouvee(Exception):

    def __init__(self, msg):
        super().__init__()


class WritingPart(QWidget):

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
        self.tab_left = tab_left

        search_bar = make_vbox()
        search_bar.layout.addWidget(QLabel("<html><center>Choose a name of a material to load it from the database :</center></html>"))
        search_bar.layout.addWidget(SearchButtons("database.sqlite", self, tab_left))

        button_add_files = QPushButton("Add file(s)")
        button_add_files.clicked.connect(partial(self.on_click_open_files, tab_left))
        button_save = QPushButton("Save the file")
        button_save.clicked.connect(partial(self.save, tab_left.currentIndex))
        button_convertion = QPushButton("Convert the file")
        button_convertion.clicked.connect(partial(self.convert_to_other_format, tab_left.currentIndex))
        add_files = make_vbox()
        add_files.layout.addWidget(search_bar)
        add_files.layout.addWidget(button_save)
        add_files.layout.addWidget(button_convertion)
        add_files.layout.addWidget(DragAndDrop.FileEdit("Drop your files here", partial(self.open_new_file, tab_left)))
        add_files.layout.addWidget(button_add_files)

        # TODO: commenter
        with open("json.txt") as fichier:
            self.open_new_file(tab_left, "Exemple", json.loads(fichier.read()))
        files_vbox = make_vbox()
        files_vbox.layout.addWidget(add_files)

        self.layout.addWidget(tab_left)
        self.layout.addWidget(files_vbox)
        self.shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut.activated.connect(partial(self.save, tab_left.currentIndex))
        # self.save(tab_left.currentIndex)
        # self.convert_to_other_format(tab_left.currentIndex)

    def open_new_file(self, tab, name, parameters):
        decoupe = lambda chaine : "..." + chaine[-10:] if len(chaine) > 10 else chaine
        #get background color
        snf = ShowNewFile(parameters, self.background, editable=True)
        tab.setCurrentIndex(tab.addTab(snf, decoupe(name)))

    def getDataInFile(self, functionToCallToGetIndex):
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

        def searchForChild(parent, filtre):
            children = [x for x in parent.findChildren(QObject) if x.objectName() in filtre]
            return children

        for tab_data_container in searchForChild(tabs_to_save, ["traps", "material", "source", "equation"]):
            if tab_data_container.objectName() == "equation":
                vbox = tab_data_container
                groupboxes = vbox.findChildren(QGroupBox)
                for groupbox in groupboxes:
                    grid_layout = groupbox.findChild(QGridLayout)
                    coef1 = grid_layout.itemAtPosition(1, 0).widget().text()
                    val1 = grid_layout.itemAtPosition(1, 1).widget().text()
                    coef2 = grid_layout.itemAtPosition(2, 0).widget().text()
                    val2 = grid_layout.itemAtPosition(2, 1).widget().text()
                    checkbox = grid_layout.itemAtPosition(1, 4).widget()

                    comment_content = groupbox.findChild(QTextEdit).toPlainText()
                    if checkbox.isChecked():
                        if groupbox.objectName() == "diffusivity":
                            equation_type = "D"
                        elif groupbox.objectName() == "solubility":
                            equation_type = "S"
                        elif groupbox.objectName() == "combination":
                            equation_type = "Kr"
                        else:
                            print("WARNING : I don't know how to save the coefficient named", groupbox.objectName())
                        data_to_save["equation"][equation_type] = {}
                        data_to_save["equation"][equation_type][coef1] = val1
                        data_to_save["equation"][equation_type][coef2] = val2
                        data_to_save["equation"][equation_type]["comment"] = comment_content
            elif tab_data_container.objectName() == "traps":
                for i in range(tab_data_container.topLevelItemCount()):
                    trap_tree = tab_data_container.topLevelItem(i)
                    dictionnary_of_this_trap = {
                        "density" : tab_data_container.itemWidget(trap_tree, 0).text(),
                        "angular_frequency": tab_data_container.itemWidget(trap_tree, 1).text(),
                        "energy" : []
                    }
                    for j in range(trap_tree.childCount()):
                        energy_tree = trap_tree.child(j)
                        line = tab_data_container.itemWidget(energy_tree, 0)
                        if line:
                            dictionnary_of_this_trap["energy"].append(line.text())
                    if not dictionnary_of_this_trap == {}:
                        data_to_save["traps"].append(dictionnary_of_this_trap)
                
            elif tab_data_container.objectName() == "material":
                vbox = tab_data_container 
                for groupbox in searchForChild(vbox, ["gb_material"]):
                    for row in range(groupbox.layout.rowCount()):
                        label = groupbox.layout.itemAtPosition(row, 0).widget().text()
                        value = groupbox.layout.itemAtPosition(row, 2).widget().text()
                        data_to_save["material"][label] = value
                for groupbox in searchForChild(vbox, ["gb_adatome"]):
                    for row in range(groupbox.layout.rowCount()):
                        label = groupbox.layout.itemAtPosition(row, 0).widget().text()
                        value = groupbox.layout.itemAtPosition(row, 1).widget().text()
                        data_to_save["material"][label] = value
                        
            elif tab_data_container.objectName() == "source":
                grid = tab_data_container
                for row in range(grid.layout.rowCount()):
                    label = grid.layout.itemAtPosition(row, 0).widget().text()
                    value = grid.layout.itemAtPosition(row, 1).widget().text()
                    data_to_save["source"][label] = value

            else:
                print("WARNING: I don't know how to save the grid named", grid.objectName())

        data_to_save = self.correctTypes(data_to_save)
        return data_to_save

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
            error_text = "An error occured while saving your file. It is likely that your file is filled with wrong datas (or maybe you don't have any file opened yet)." 
            dialog.setText(error_text)
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()
        
    def convert_to_other_format(self, functionToCallToGetIndex):
        data_to_convert = self.getDataInFile(functionToCallToGetIndex)
        adatome = data_to_convert["material"]["adatome"]
        material_name = data_to_convert["material"]["name"]

        # write the converte data into a string
        data_converted = ""
        data_converted += "$" + adatome + " in " + material_name + "\n"
        i = 0

        # solubility
        try:
            es = "{:.2e}".format(data_to_convert["equation"]["S"]["E_S"])
            s0 = "{:.2e}".format(data_to_convert["equation"]["S"]["S_0"])
            header = "Solubility of " +  adatome + " in " + material_name + "(" + adatome + "/(m³*Pa½))"
            exp = "exp(" + es + "/8.625e-5/temp)"
            data_converted += "$  (" + str(i) + ")  " + header + "\n"
            data_converted += "y=" + s0 + "*" + exp + ",end" + "\n"
            i += 1
        except Exception as e:
            print(e)
        
        # diffusivity
        try:
            es = "{:.2e}".format(data_to_convert["equation"]["D"]["E_D"])
            s0 = "{:.2e}".format(data_to_convert["equation"]["D"]["D_0"])
            header = "Diffusivity of " +  adatome + " in " + material_name + "(m²/s)"
            exp = "exp(" + es + "/8.625e-5/temp)"
            data_converted += "$  (" + str(i) + ")  " + header + "\n"
            data_converted += "y=" + s0 + "*" + exp + ",end" + "\n"
            i += 1
        except Exception as e:
            print(e)
        
        # recombination
        try:
            es = "{:.2e}".format(data_to_convert["equation"]["Kr"]["E_r"])
            s0 = "{:.2e}".format(data_to_convert["equation"]["Kr"]["Kr_0"])
            header = "Recombination of " +  adatome + " in " + material_name + "(m⁴/s)"
            exp = "exp(" + es + "/8.625e-5/temp)"
            data_converted += "$  (" + str(i) + ")  " + header + "\n"
            data_converted += "y=" + s0 + "*" + exp + ",end" + "\n"
            i += 1
        except Exception as e:
            print(e)

        # save the string
        filename = QFileDialog.getSaveFileName(None, "Save File")[0]
        if filename[-4::] != ".txt":
            filename += ".txt"

        #pdb.Pdb.complete=rlcompleter.Completer(locals()).complete; pdb.set_trace()
        with open(filename, "w") as fichier:
            fichier.write(data_converted)

    def correctTypes(self, data):
        def to_float_secure(x):
            try:
                floated = float(x)
                return floated
            except Exception as e:
                print(e)
                return None

        def to_int_secure(x):
            try:
                # here, I use int(float(x)) instead of int(x):
                # that's because int(float("2.5e2")) return 250
                # while int("2.5e2") raise a ValueError.
                inted = int(float(x))
                return inted
            except Exception as e:
                print(e)
                return None

        for i in range(len(data["traps"])):
            for key in ("density", "angular_frequency"):
                try:
                    data["traps"][i][key] = to_float_secure(data["traps"][i][key])
                except KeyError as e:  # attrape le bouton d'ajout
                    print(e)
            # energy part
            energy_list = data["traps"][i]["energy"]
            corrected_energy_list = [to_float_secure(x) for x in energy_list]
            data["traps"][i]["energy"] = corrected_energy_list

        for key in data["equation"]:
            for subkey in data["equation"][key]:
                if subkey != "comment":
                    data["equation"][key][subkey] = to_float_secure(data["equation"][key][subkey])
        
        data["source"]["year"] = to_int_secure(data["source"]["year"])

        for key in ("melting_point", "lattice_parameter", "density"):
            data["material"][key] = to_float_secure(data["material"][key])

        #atomic number and adatom atomic number to float
        data["material"]["atomic_number"] = to_int_secure(data["material"]["atomic_number"])
        data["material"]["adatome_atomic_number"] = to_int_secure(data["material"]["adatome_atomic_number"])

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