from PyQt5.QtCore import pyqtSlot, Qt, QObject
from PyQt5.QtWidgets import (QWidget,
                             QPushButton,
                             QLabel,
                             QHBoxLayout, 
                             QTabWidget,
                             QFileDialog,
                             QMessageBox,
                             QGroupBox,
                             QTextEdit,
                             QGridLayout
                            )
from PyQt5.QtGui import QPixmap, QPalette
import json
import numpy as np
from functools import partial
import time
# matplotlib stufffs
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# my classes
import ShowNewFile
from PltWindows import PltWindowReading
from makeWidget import make_vbox
from AddFiles import AddFiles
from datetime import datetime







class ReadingPart(QWidget):
    """
        The first tab of this app (ie: the reading part).
        It contains three main parts:
         - Some tabs, in which the user can read informations about a file
           (a file per tab)
         - Three button, used for plotting the graph
         - A graph, which is in a Canva, which is in a PltWindowReading
           (see this class for more inforamtions)
    """

    def __init__(self):
        """
            Init the ReadingPart.Create the UI (the three part) and init the
            validity range.
        """
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.data_onglets = []
        self.data_sources = []
        self.start_validity_range = 300  # K
        self.end_validity_ranges = []  # K
        self.template_validity_range = "validity range : [300; {}]"
        self.validity_range = ""
        self.qlabel_validity_range = QLabel()
        # sauvegarde de la couleur du fond
        color = self.palette().color(QPalette.Background)
        rgba = color.red(), color.green(), color.blue(), color.alpha()
        self.background = rgba


        # LEFT
        tab_left = QTabWidget(tabsClosable=True)
        def CloseTab(i):
            tab_left.removeTab(i)
            self.data_onglets.pop(i)
            self.data_sources.pop(i)
            self.end_validity_ranges.pop(i)
            self.majValidityRange()
            

        tab_left.tabCloseRequested.connect(CloseTab)
        tab_left.setTabPosition(QTabWidget.West)
        tab_left.setFocusPolicy(Qt.NoFocus)
        tab_left.setObjectName("tab_left")

        trigger_drag = partial(self.open_new_file, tab_left)
        trigger_click = partial(self.on_click_open_files, tab_left)


        # with open("json.txt") as fichier:
        #     self.open_new_file(tab_left, "json.txt", json.loads(fichier.read()))

        self.layout.addWidget(
            make_vbox(
                tab_left,
                AddFiles(trigger_drag, trigger_click)
            )
        )

        bt_d = QPushButton("Diffusion")
        bt_d.clicked.connect(partial(self.on_click_tracer, "D"))
        bt_s = QPushButton("Solubility")
        bt_s.clicked.connect(partial(self.on_click_tracer, "S"))
        bt_kr = QPushButton("Combination coefficients")  # todo: demander pour la traduction
        bt_kr.clicked.connect(partial(self.on_click_tracer, "Kr"))

        hbox = make_vbox()
        for _ in range(10):  # todo: find another way to place the widget down
            hbox.layout.addWidget(QLabel(" "))
            self.majValidityRange()
        
        button_save = QPushButton("Convert the file")
        button_save.clicked.connect(partial(self.convert_to_other_format, tab_left.currentIndex))
        hbox.layout.addWidget(button_save)
        self.qlabel_validity_range.setText(self.validity_range)
        hbox.layout.addWidget(self.qlabel_validity_range)
        hbox.layout.addWidget(QLabel("Coefficients"))
        hbox.layout.addWidget(bt_d)
        hbox.layout.addWidget(bt_s)
        hbox.layout.addWidget(bt_kr)
        self.layout.addWidget(hbox)


        # RIGHT

        # let's add tabs on the right
        self.pltwindows = [PltWindowReading() for _ in range(4)]
        tab_right = QTabWidget()
        tab_right.setFocusPolicy(Qt.NoFocus)
        tab_right.addTab(self.pltwindows[0], "Log - Natural")
        tab_right.addTab(self.pltwindows[1], "Log - 1/T")
        tab_right.addTab(self.pltwindows[2], "Natural - Natural")
        tab_right.addTab(self.pltwindows[3], "Log - Log")
        tab_right.setCurrentIndex(3)
        self.layout.addWidget(tab_right)
    
    def majValidityRange(self):
        """
            Update the validity range. Should be called each time a new file is
            opened or close. Can also be called to get the maximal validity
            range (which is the minimal of all the fusion temperatures).
        """
        if self.end_validity_ranges:
            mini = min(self.end_validity_ranges)
            self.validity_range = self.template_validity_range.format(mini)
            self.qlabel_validity_range.setText(self.validity_range)
            return mini
        else:
            self.validity_range = ""
            self.qlabel_validity_range.setText(self.validity_range)
            return None

    def make_tab(self):
        return make_vbox()

    def make_pixmap(self, picture_name, label_name):
        """
            Create a QLabel with the name picture_name, containing a QPixmap
            made from the image picture_name. 
        """
        label = QLabel()
        label.setObjectName(label_name)
        pixmap = QPixmap(picture_name)
        label.setPixmap(pixmap)
        return label

    def open_new_file(self, tab, name, parameters):
        print(parameters)
        """
            Create a new tab that shows informations about a file. Extract and
            add those informations to a list, so that they can be re-used later
            (for plotting, for instance).
        """
        decoupe = lambda chaine : "..." + chaine[-10:] if len(chaine) > 10 else chaine
        snf = ShowNewFile.ShowNewFile(parameters, self.background)
        tab.setCurrentIndex(tab.addTab(snf, decoupe(name)))
        self.data_onglets.append(snf.list_data_equation)
        self.data_sources.append(snf.list_data_source)
        self.end_validity_ranges.append(parameters["material"]["melting_point"])
        self.majValidityRange()
        self.qlabel_validity_range.setText(self.validity_range)


    @pyqtSlot()
    def on_click_tracer(self, name):
        """
            Plot every graph on every tab : for every equation from
            every file, plot it if the equation name is equal to the parameter
            'name'. The name can be 'D' (for diffusion), 'S' (for solubility)
            or 'Kr' (for combination).
        """
        start = time.time()
        print('Tracons la courbe des lignes ' + name)

        # clean graphs
        for indice_figure in range(len(self.pltwindows)):
            self.pltwindows[indice_figure].clear()
        
        # temperature
        debut, fin, pas = 300, 2500, 0.1
        les_temperatures = np.arange(debut, fin, pas)

        # Boltzmann constant
        k_b = 1.38064852 * 10**(-23) * 8.617e+18

        # value_x_max = self.majValidityRange()
        # xlim=300

        for onglet, source in zip(self.data_onglets, self.data_sources):
            for equation in onglet:
                if equation[0] == name:
                    try:
                        if name == "D":
                            y_unit = "Diffusivity (m²/s)"
                        elif name == "Kr":
                            y_unit = "Recombinaison coefficient (m⁴/s)"
                        elif name == "S":
                            y_unit = "Solubility (adatome/(m³*Pa½)"
                        else:
                            y_unit = ""
                        y_values = equation[1][1] * np.exp(-equation[2][1]/(k_b * les_temperatures))
                        legend = source["author_name"] + " - " + str(source["year"])
                        data = les_temperatures, y_values
                        self.pltwindows[0].plot(data, legend, ylog=True, x_label="Temperature (K)", y_label=y_unit + " (logscale)")

                        data = 1 / les_temperatures, y_values
                        # if xlim != 0:
                        #     xlim_divided = 1 / xlim
                        # else:
                        #     xlim_divided = 0

                        # if value_x_max != 0:
                        #     value_x_max_divided = 1 / value_x_max
                        # else:
                        #     value_x_max_divided = 0

                        self.pltwindows[1].plot(data, legend, ylog=True, x_label="1/Temperature ($K^{-1}$)", y_label=y_unit + " (logscale)")

                        data = les_temperatures, y_values
                        self.pltwindows[2].plot(data, legend, x_label="Temperature (K)", y_label=y_unit)

                        data = les_temperatures, y_values
                        self.pltwindows[3].plot(data, legend, xlog=True, ylog=True, x_label="Temperature (K)" + " (logscale)",y_label=y_unit  + " (logscale)")
                        # since the curves was plot, we need to stop plotting
                        # the xilm and the xlimmax
                        # xlim, value_x_max = 0, 0
                    except TypeError as e:  # there is a None in the data
                        print("I cant't draw", name)
                        print(e)

        print("Time taken to plot " + str(time.time() - start))

    @pyqtSlot()
    def on_click_open_files(self, tab_to_add):
        """
            Open a dialog which let the user choose some files that he can open
            in the app.
        """
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
            except Exception:
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

    def correctTypes(self, data):
        def to_float_secure(x):
            try:
                floated = float(x)
                return floated
            except Exception as e:
                print("to_float_secure:", e)
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
        
        def to_sci_notation(x):
            try: 
                scied = "{:.2e}".format(to_float_secure(x))
                return scied
            except:
                return None


        for i in range(len(data["traps"])):
            try:
                data["traps"][i]["density"] = to_sci_notation(data["traps"][i]["density"])
            except KeyError as e:  # attrape le bouton d'ajout
                print(e)
            # data part
            data_trap_dict_list = data["traps"][i]["data"]
            data_trap_dict_list_corrected = []
            for dictionnary in data_trap_dict_list:
                dictionnary_corrected = {}
                dictionnary_corrected["energy"] = to_sci_notation(dictionnary["energy"])
                dictionnary_corrected["frequency"] = to_sci_notation(dictionnary["frequency"])
                data_trap_dict_list_corrected.append(dictionnary_corrected)
            data["traps"][i]["data"] = data_trap_dict_list_corrected

        for key in data["equation"]:
            for subkey in data["equation"][key]:
                if subkey != "comment":
                    data["equation"][key][subkey] = to_float_secure(data["equation"][key][subkey])
        
        data["source"]["year"] = to_int_secure(data["source"]["year"])
        data["source"]["last_edit"] = ShowNewFile.get_today_date()

        for key in ("melting_point", "lattice_parameter", "density"):
            data["material"][key] = to_float_secure(data["material"][key])

        #atomic number and adatom atomic number to float
        data["material"]["atomic_number"] = to_int_secure(data["material"].get("atomic_number", None))
        data["material"]["adatome_atomic_symbol"] = to_int_secure(data["material"].get("adatome_atomic_symbol", None))
        data["material"]["adatome_atomic_number"] = to_int_secure(data["material"].get("adatome_atomic_number", None))

        return data

    def getDataInFile(self, functionToCallToGetIndex):
        def searchForChild(parent, filtre):
            children = [x for x in parent.findChildren(QObject) if x.objectName() in filtre]
            return children
        index = functionToCallToGetIndex()
        data_to_save = {
            "material" :{},
            "source" :{},
            "traps" : [],
            "equation" : {}
        }
        tabs = searchForChild(self, ["tab_left"])[0]
        snf = tabs.widget(index)
        tabs_to_save = snf.findChild(QTabWidget)

        for tab_data_container in searchForChild(tabs_to_save, ["traps", "material", "source", "equation"]):
            print(tab_data_container.objectName())
            if tab_data_container.objectName() == "equation":
                vbox = tab_data_container
                print("vbox", vbox)
                groupboxes = vbox.findChildren(QGroupBox)
                print("groupboxes", groupboxes)
                for groupbox in groupboxes:
                    print("groupbox", groupbox)
                    grid_layout = groupbox.findChild(QGridLayout)
                    coef1 = grid_layout.itemAtPosition(1, 0).widget().text()
                    val1 = grid_layout.itemAtPosition(1, 1).widget().text()
                    coef2 = grid_layout.itemAtPosition(2, 0).widget().text()
                    val2 = grid_layout.itemAtPosition(2, 1).widget().text()
                    # checkbox = grid_layout.itemAtPosition(1, 4).widget()

                    comment_content = groupbox.findChild(QTextEdit).toPlainText()
                    # if checkbox.isChecked():
                    if True:  # todo: ask if it is ok
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
                        "data": []
                    }
                    for j in range(trap_tree.childCount()):
                        energy_tree = trap_tree.child(j)
                        energy = tab_data_container.itemWidget(energy_tree, 2)
                        frequence = tab_data_container.itemWidget(energy_tree, 4)
                        if energy:
                            energy = energy.text()
                        else:
                            energy = None
                        if frequence:
                            frequence = frequence.text()
                        else:
                            frequence = None
                        dictionnary_of_this_trap["data"].append({"energy":energy, "frequency":frequence})

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
            error_text = "An error occured while saving your file. It is likely that your file is filled with wrong datas (or maybe you don't have any file opened yet).\n"
            error_text += "Error text: " + str(e)
            dialog.setText(error_text)
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()

    def convert_to_other_format(self, functionToCallToGetIndex):
        try:
            data_to_convert = self.getDataInFile(functionToCallToGetIndex)
            adatome = data_to_convert["material"]["adatome"]
            material_name = data_to_convert["material"]["name"]

            # write the converted data into a string
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
            with open(filename, "w", encoding='utf-8') as fichier:
                fichier.write(data_converted)
        except Exception as e:
            print("Une erreur est survenue lors de la conversion", e)