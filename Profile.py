from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QWidget,
                             QHBoxLayout,
                             QFileDialog,
                             QMessageBox,
                             QListWidgetItem,
                             QPushButton,
                             QLabel
                            )
from PyQt5.QtGui import QIcon, QPixmap
import matplotlib.pyplot as plt
import json
import numpy as np
from functools import partial

from myListWidget import DoubleThumbListWidget
from makeWidget import make_vbox, make_hbox, make_scroll
from PltWindows import PltWindowProfile
from AddFiles import AddFiles


class DataOfAFile:
    def __init__(self, name, data):
        self.name = name
        self.data = data


class Profile(QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.data_onglets = []

        doublelist = DoubleThumbListWidget()
        trigger_click = partial(self.on_click_open_files, doublelist)
        
        def todo(*args):
            pass
        
        bt_d = QPushButton("Diffusion")
        bt_d.clicked.connect(todo)
        bt_s = QPushButton("Solubility")
        bt_s.clicked.connect(todo)
        bt_kr = QPushButton("Combination coefficients")  # todo: demander pour la traduction
        bt_kr.clicked.connect(todo)

        draw_bts = make_vbox()
        for _ in range(10):  # todo: find another way to place the widget down
            draw_bts.layout.addWidget(QLabel(" "))
        draw_bts.layout.addWidget(QLabel("Coefficients"))
        draw_bts.layout.addWidget(bt_d)
        draw_bts.layout.addWidget(bt_s)
        draw_bts.layout.addWidget(bt_kr)
        

        
        self.layout.addWidget(
            make_hbox(
                make_vbox(
                    doublelist,
                    AddFiles(todo, trigger_click)  # todo
                ),
                draw_bts
            )
        )

    def open_new_file(self, doubleListToAdd, data):
        doubleListToAdd.addItemFromName(data.name)

    @pyqtSlot()
    def on_click_open_files(self, doubleListToAdd):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        sucessfully_loaded = []
        failed = []
        get_name_from_path = lambda path : path.split("/")[-1].split('.', 1)[0]
        for filepath in files:
            try:
                with open(filepath, "r") as fichier: 
                    data = fichier.read()
                name = get_name_from_path(filepath)
                sucessfully_loaded.append(DataOfAFile(name, data))
            except Exception as e:
                print(e)
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
            self.open_new_file(doubleListToAdd, success)








    # def __init__(self):
    #     """
    #         Init the ReadingPart.Create the UI (the three part) and init the
    #         validity range.
    #     """




    #     # LEFT
    #     tab_left = QTabWidget(tabsClosable=True)
    #     def CloseTab(i):
    #         tab_left.removeTab(i)
    #         self.data_onglets.pop(i)
    #         self.data_sources.pop(i)
    #         self.end_validity_ranges.pop(i)
    #         self.majValidityRange()
            

    #     tab_left.tabCloseRequested.connect(CloseTab)
    #     tab_left.setTabPosition(QTabWidget.West)
    #     tab_left.setFocusPolicy(Qt.NoFocus)

    #     add_files = QWidget()
    #     add_files.layout = QHBoxLayout()
    #     add_files.setLayout(add_files.layout)

    #     add_files.layout.addWidget(DragAndDrop.FileEdit("Drop your files here", partial(self.open_new_file, tab_left)))
    #     boutton_ajout_fichiers = QPushButton("Add file(s)")
    #     boutton_ajout_fichiers.clicked.connect(partial(self.on_click_open_files, tab_left))
    #     add_files.layout.addWidget(boutton_ajout_fichiers)        

    #     # TODO: commenter
    #     """
    #     with open("Touchard-2012.txt") as fichier:
    #         self.open_new_file(tab_left, "Touchard-2012.txt", json.loads(fichier.read()))
    #     """
    #     with open("json.txt") as fichier:
    #         self.open_new_file(tab_left, "json.txt", json.loads(fichier.read()))
    #     files_vbox = QWidget()
    #     files_vbox.layout = QVBoxLayout()
    #     files_vbox.setLayout(files_vbox.layout)
    #     files_vbox.layout.addWidget(tab_left)
    #     files_vbox.layout.addWidget(add_files)

    #     self.layout.addWidget(files_vbox)
    #     bt_d = QPushButton("Diffusion")
    #     bt_d.clicked.connect(partial(self.on_click_tracer, "D"))
    #     bt_s = QPushButton("Solubility")
    #     bt_s.clicked.connect(partial(self.on_click_tracer, "S"))
    #     bt_kr = QPushButton("Combination coefficients")  # todo: demander pour la traduction
    #     bt_kr.clicked.connect(partial(self.on_click_tracer, "Kr"))

    #     hbox = make_vbox()
    #     for _ in range(10):  # todo: find another way to place the widget down
    #         hbox.layout.addWidget(QLabel(" "))
    #         self.majValidityRange()
    #     self.qlabel_validity_range.setText(self.validity_range)
    #     hbox.layout.addWidget(self.qlabel_validity_range)
    #     hbox.layout.addWidget(QLabel("Coefficients"))
    #     hbox.layout.addWidget(bt_d)
    #     hbox.layout.addWidget(bt_s)
    #     hbox.layout.addWidget(bt_kr)
    #     self.layout.addWidget(hbox)


    #     # RIGHT

    #     # let's add tabs on the right
    #     self.pltwindows = [PltWindowReading() for _ in range(4)]
    #     tab_right = QTabWidget()
    #     tab_right.setFocusPolicy(Qt.NoFocus)
    #     tab_right.addTab(self.pltwindows[0], "Log - Natural")
    #     tab_right.addTab(self.pltwindows[1], "Log - 1/T")
    #     tab_right.addTab(self.pltwindows[2], "Natural - Natural")
    #     tab_right.addTab(self.pltwindows[3], "Log - Log")
    #     self.layout.addWidget(tab_right)
    
    # def majValidityRange(self):
    #     """
    #         Update the validity range. Should be called each time a new file is
    #         opened or close. Can also be called to get the maximal validity
    #         range (which is the minimal of all the fusion temperatures).
    #     """
    #     if self.end_validity_ranges:
    #         mini = min(self.end_validity_ranges)
    #         self.validity_range = self.template_validity_range.format(mini)
    #         self.qlabel_validity_range.setText(self.validity_range)
    #         return mini
    #     else:
    #         self.validity_range = ""
    #         self.qlabel_validity_range.setText(self.validity_range)
    #         return None

    # def make_tab(self):
    #     return make_vbox()

    # def make_pixmap(self, picture_name, label_name):
    #     """
    #         Create a QLabel with the name picture_name, containing a QPixmap
    #         made from the image picture_name. 
    #     """
    #     label = QLabel()
    #     label.setObjectName(label_name)
    #     pixmap = QPixmap(picture_name)
    #     label.setPixmap(pixmap)
    #     return label

    # def open_new_file(self, tab, name, parameters):
    #     """
    #         Create a new tab that shows informations about a file. Extract and
    #         add those informations to a list, so that they can be re-used later
    #         (for plotting, for instance).
    #     """
    #     decoupe = lambda chaine : "..." + chaine[-10:] if len(chaine) > 10 else chaine
    #     snf = ShowNewFile(parameters, self.background)
    #     tab.setCurrentIndex(tab.addTab(snf, decoupe(name)))
    #     self.data_onglets.append(snf.list_data_equation)
    #     self.data_sources.append(snf.list_data_source)
    #     self.end_validity_ranges.append(parameters["material"]["melting_point"])
    #     self.majValidityRange()
    #     self.qlabel_validity_range.setText(self.validity_range)


    # @pyqtSlot()
    # def on_click_tracer(self, name):
    #     """
    #         Plot every graph on every tab : for every equation from
    #         every file, plot it if the equation name is equal to the parameter
    #         'name'. The name can be 'D' (for diffusion), 'S' (for solubility)
    #         or 'Kr' (for combination).
    #     """
    #     start = time.time()
    #     print('Tracons la courbe des lignes ' + name)

    #     # clean graphs
    #     for indice_figure in range(len(self.pltwindows)):
    #         self.pltwindows[indice_figure].clear()
        
    #     # temperature
    #     debut, fin, pas = 300, 2500, 0.1
    #     les_temperatures = np.arange(debut, fin, pas)

    #     # Boltzmann constant
    #     k_b = 1.38064852 * 10**(-23) * 8.617e+18

    #     value_x_max = self.majValidityRange()
    #     xlim=300

    #     for onglet, source in zip(self.data_onglets, self.data_sources):
    #         for equation in onglet:
    #             if equation[0] == name:
    #                 try:
    #                     y_values = equation[1][1] * np.exp(-equation[2][1]/(k_b * les_temperatures))
    #                     legend = source["author_name"] + " - " + str(source["year"])
    #                     data = les_temperatures, y_values
    #                     self.pltwindows[0].plot(data, legend, ylog=True, x_label="Temperature (K)", y_label="" + " (logscale)", xlim=xlim, xlimmax=(value_x_max, value_x_max))

    #                     data = 1 / les_temperatures, y_values
    #                     if xlim != 0:
    #                         xlim_divided = 1 / xlim
    #                     else:
    #                         xlim_divided = 0

    #                     if value_x_max != 0:
    #                         value_x_max_divided = 1 / value_x_max
    #                     else:
    #                         value_x_max_divided = 0

    #                     self.pltwindows[1].plot(data, legend, ylog=True, x_label="1/Temperature ($K^{-1}$)", y_label="" + " (logscale)", xlim=xlim_divided, xlimmax=(value_x_max_divided, value_x_max))

    #                     data = les_temperatures, y_values
    #                     self.pltwindows[2].plot(data, legend, x_label="Temperature (K)", y_label="", xlim=xlim, xlimmax=(value_x_max, value_x_max))

    #                     data = les_temperatures, y_values
    #                     self.pltwindows[3].plot(data, legend, xlog=True, ylog=True, x_label="Temperature (K)" + " (logscale)",y_label=""  + " (logscale)", xlim=xlim, xlimmax=(value_x_max, value_x_max))
    #                     # since the curves was plot, we need to stop plotting
    #                     # the xilm and the xlimmax
    #                     xlim, value_x_max = 0, 0
    #                 except TypeError:  # there is a None in the data
    #                     print("I cant't draw", name)

    #     print("Time taken to plot " + str(time.time() - start))

    # @pyqtSlot()
    # def on_click_open_files(self, tab_to_add):
    #     """
    #         Open a dialog which let the user choose some files that he can open
    #         in the app.
    #     """
    #     options = QFileDialog.Options()
    #     options |= QFileDialog.DontUseNativeDialog
    #     files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
    #     sucessfully_loaded = []
    #     failed = []
    #     for filepath in files:
    #         try:
    #             with open(filepath, "r") as fichier: 
    #                 liste = json.loads(fichier.read())
    #             sucessfully_loaded.append((filepath, liste))
    #         except Exception as e:
    #             failed.append(filepath)
    #     if failed:
    #         dialog = QMessageBox()
    #         if len(failed) > 1:
    #             dialog.setWindowTitle("Error: Invalid Files")
    #         else:
    #             dialog.setWindowTitle("Error: Invalid File")
    #         error_text = "An error occured when loading :"
    #         for failure in failed:
    #             error_text += "\n" + failure
    #         dialog.setText(error_text)
    #         dialog.setIcon(QMessageBox.Warning)
    #         dialog.exec_()
    #     for success in sucessfully_loaded:
    #         get_name_from_path = lambda path : path.split("/")[-1].split('.', 1)[0]
    #         filepath, liste = success
    #         self.open_new_file(tab_to_add, get_name_from_path(filepath), liste)