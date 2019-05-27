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
                             QGroupBox
                            )
from PyQt5.QtGui import QPixmap, QFontMetrics, QPalette
import json
import numpy as np
from functools import partial
import pdb
import rlcompleter
import time
from QLineEditWidthed import QLineEditWidthed
from ShowNewFile import ShowNewFile
import matplotlib.pyplot as plt


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import sys
import random as rd

class PltWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.plot()

    def plot(self, data=None):
        if data is None:
            data = [rd.random() for _ in range(20)]
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(data, "o--")
        else:
            ax = self.figure.add_subplot(111)
            x, y = data
            ax.plot(x, y)
        self.canvas.draw()

    def clear(self):
        self.figure.clear()



class FirstTab(QWidget):

    def __init__(self, background):
        super().__init__()
        #todo: use lists

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.data_onglets = []
        self.bakground = background


        # LEFT
        tab_left = QTabWidget(tabsClosable=True)
        def CloseTab(i):
            tab_left.removeTab(i)
            self.data_onglets.pop(i)
        tab_left.tabCloseRequested.connect(CloseTab)
        tab_left.setTabPosition(QTabWidget.West)
        tab_left.setFocusPolicy(Qt.NoFocus)
        #pdb.Pdb.complete=rlcompleter.Completer(locals()).complete
        #pdb.set_trace()

        add_files = QWidget()
        add_files.layout = QHBoxLayout()
        add_files.setLayout(add_files.layout)

        add_files.layout.addWidget(DragAndDrop.FileEdit("Glisser vos fichiers ici", partial(self.open_new_file, tab_left)))
        boutton_ajout_fichiers = QPushButton("Ajout de fichier(s)")
        boutton_ajout_fichiers.clicked.connect(partial(self.on_click_open_files, tab_left))
        add_files.layout.addWidget(boutton_ajout_fichiers)        

        # TODO: commenter
        with open("json.txt") as fichier:
            self.open_new_file(tab_left, "nom", json.loads(fichier.read()))
        files_vbox = QWidget()
        files_vbox.layout = QVBoxLayout()
        files_vbox.setLayout(files_vbox.layout)
        files_vbox.layout.addWidget(tab_left)
        files_vbox.layout.addWidget(add_files)

        self.layout.addWidget(files_vbox)
        bt_d = QPushButton("Tracer les D")
        bt_d.clicked.connect(partial(self.on_click_tracer, "D"))
        bt_s = QPushButton("Tracer les S")
        bt_s.clicked.connect(partial(self.on_click_tracer, "S"))
        bt_kr = QPushButton("Tracer les Kr") 
        bt_kr.clicked.connect(partial(self.on_click_tracer, "Kr"))
        tab_center = self.make_tab()
        tab_center.layout.addWidget(QLabel("Dessiner les courbes :"))
        tab_center.layout.addWidget(bt_d)
        tab_center.layout.addWidget(bt_s)
        tab_center.layout.addWidget(bt_kr)
        self.layout.addWidget(tab_center)


        # RIGHT

        # let's add tabs on the right
        self.pltwindows = [PltWindow() for _ in range(3)]
        tab_right = QTabWidget()
        tab_right.setFocusPolicy(Qt.NoFocus)
        tab_right.addTab(self.pltwindows[0], "Non log")
        tab_right.addTab(self.pltwindows[1], "log-log")
        tab_right.addTab(self.pltwindows[2], "log-1/T")
        self.layout.addWidget(tab_right)

        self.draw_first_pictures()

    def draw_first_pictures(self):
        for indice in range(len(self.pltwindows)):
            data = [], []
            self.pltwindows[indice].plot(data)

    def make_tab(self):
        return make_vbox()

    def make_pixmap(self, picture_name, label_name):
        label = QLabel()
        label.setObjectName(label_name)
        pixmap = QPixmap(picture_name)
        label.setPixmap(pixmap)
        return label

    def open_new_file(self, tab, name, parameters):
        decoupe = lambda chaine : "..." + chaine[-5:] if len(chaine) > 10 else chaine
        #get background color
        snf = ShowNewFile(parameters, self.bakground)
        tab.addTab(snf, decoupe(name))
        self.data_onglets.append(snf.list_data_equation)

    @pyqtSlot()
    def on_click_tracer(self, name):
        start = time.time()  # 4*2 onglets utiles + 1 inutile : Temps: 4.524548768997192 (1.1296305656433105 en mutualisant les ecritures)
        print('Tracons la courbe des lignes ' + name)
        # effaçons les graphes pécédents
        for indice_figure in range(len(self.pltwindows)):
            self.pltwindows[indice_figure].clear()
        debut, fin, pas = 300, 2500, 0.1
        les_temperatures = np.arange(debut, fin, pas)
        k_b = 1.38064852 * 10**(-23) * 8.617e+18

        for onglet in self.data_onglets:
            print("un nouvel onglet")
            for equation in onglet:
                if equation[0] == name:
                    les_d = equation[1][1] * np.exp(equation[2][1]/(k_b * les_temperatures))

                    data = les_temperatures, les_d
                    self.pltwindows[0].plot(data)

                    data = np.log(les_temperatures), np.log(les_d)
                    self.pltwindows[1].plot(data)

                    data = 1000/les_temperatures, les_d
                    self.pltwindows[2].plot(data)

        print("Temps de tracé: " + str(time.time() - start))

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