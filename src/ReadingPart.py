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
from ReadingAndWritingPart import ReadingAndWritingPart



class ReadingPart(QWidget, ReadingAndWritingPart):
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
                            y_unit = r"Diffusivity (m$^2$/s)"
                        elif name == "Kr":
                            y_unit = r"Recombinaison coefficient (m$^4$/s)"
                        elif name == "S":
                            y_unit = r"Solubility (adatome/(m$^3$ Pa$^{0.5}$)"
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