import sip
sip.setdestroyonexit(True)

#from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QPushButton,
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout, 
                             QTabWidget,
                             QScrollArea,
                             QGridLayout,
                             QScroller,
                             QFormLayout,
                             QDoubleSpinBox,
                             QGroupBox)
from PyQt5.QtGui import QIcon, QPixmap
import random as rd
import sys
import matplotlib.pyplot as plt
import json
import numpy as np
from functools import partial

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Titre'
        self.left = 10
        self.top = 10
        self.width = 1800  # 640
        self.height = 480
        self.initUI()
        self.plots = [plt.subplots() for _ in range(3)]  # 3 subplots

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        tabs = QTabWidget()
        tabs.resize(self.width, self.height)
        tabs.addTab(self.create_fisrt_tab(), "Lecture")
        tabs.addTab(self.create_second_tab(), "Ecriture")
        tabs.addTab(self.create_third_tab(), "Post-traitement")

        layout = QVBoxLayout()  # contient les tabs
        layout.addWidget(tabs)
        self.setLayout(layout)

        #self.resize(pixmap.width()+self.width,pixmap.height()+self.height)
        self.show()
    
    def create_fisrt_tab(self):
        # create the tab
        tab1 = QWidget()
        tab1.layout = QHBoxLayout()
        tab1.setLayout(tab1.layout)
        # fill it
        tab1.layout.addWidget(self.create_scroll())

        # let's add tabs in the 1st tab
        tabs = QTabWidget()

        def make_tab():
            tab = QWidget()
            tab.layout = QHBoxLayout()
            tab.setLayout(tab.layout)
            return tab

        def make_pixmap(name):
            label = QLabel()
            pixmap = QPixmap(name)
            label.setPixmap(pixmap)
            return label

        # 1st image
        tab1_1 = make_tab()
        tab1_1.layout.addWidget(make_pixmap("tab1_1.png"))
        tabs.addTab(tab1_1, "Non log")


        tab1_2 = make_tab()
        tab1_2.layout.addWidget(make_pixmap("tab1_2.png"))
        tabs.addTab(tab1_2, "log-log")

        tab1_3 = make_tab()
        tab1_3.layout.addWidget(make_pixmap("tab1_3.png"))
        tabs.addTab(tab1_3, "log-1/T")

        tab1.layout.addWidget(tabs)

        #return it
        return tab1

    def update_first_tab_image(self, name):
        tabWidget = self.findChildren(QTabWidget)[0]
        labels = tabWidget.findChildren(QLabel)

        for label in labels:
            if label.pixmap() is not None:
                pixmap = QPixmap(name)
                label.setPixmap(pixmap)
    
    def create_second_tab(self):
        # create the tab
        tab2 = QWidget()
        tab2.layout = QHBoxLayout()
        tab2.setLayout(tab2.layout)
        # fill it
        boutton = QPushButton("PyQt5 button")
        boutton.clicked.connect(self.on_click)
        tab2.layout.addWidget(boutton)
        # return it
        return tab2

    def create_third_tab(self):
        # create the tab
        tab3 = QWidget()
        tab3.layout = QVBoxLayout()
        tab3.setLayout(tab3.layout)
        # fill it
        # return it
        return tab3
    
    def create_scroll(self):
        with open("json.txt", "r") as fichier:
            chaine = fichier.read()
        self.data = json.loads(chaine)

        # element[1] is the data, so we get all the len() of the data
        number_of_column = max([len(element[1]) for element in self.data])
        number_of_lines = len(self.data)
        
        scroll_area = QScrollArea()
        #scroll_area.setWidgetResizable(True)
        scrollAreaWidgetContents = QWidget()
        grid_layout = QGridLayout(scrollAreaWidgetContents)
        for i, element in enumerate(self.data):
            name, values = element
            # first of all, place the name at the beginning of the line
            grid_layout.addWidget(QLabel(name), i, 0)
            for j, value in enumerate(values):
                # add a spinbox at the right place with the right value
                sp = QDoubleSpinBox()
                sp.setObjectName(json.dumps([i, j]))
                sp.setValue(value)
                sp.valueChanged.connect(self.on_update_spin_box)
                grid_layout.addWidget(sp, i, j+1)
            # last but not least, let's create a button at the end of the line
            bt = QPushButton("Tracer") 
            bt.clicked.connect(partial(self.on_click_tracer, self.data[i]))
            grid_layout.addWidget(bt, i, len(self.data) + 1)

        QScroller.grabGesture(
            scroll_area.viewport(), QScroller.LeftMouseButtonGesture
        )

        scroll_area.setWidget(scrollAreaWidgetContents)
        return scroll_area

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        # self.update_first_tab_image("image.png")

    def on_update_spin_box(self):
        spinbox = self.sender()
        i, j = json.loads(spinbox.objectName())
        self.data[i][1][j] = spinbox.value()


    @pyqtSlot()
    def on_click_tracer(self, line):
        print('Tracons la courbe de la ligne ' + str(line))
        name, values = line
        if name == "S" or name == "D":
            debut, fin, pas = 300, 2500, 0.1
            les_temperatures = np.arange(debut, fin, pas)
            d_0 = values[0]  # 6*10**-4
            e_d = values[1]  # 1.04
            k_b = 1.38064852 * 10**(-23) * 8.617e+18
            les_d = d_0 * np.exp(-e_d/(k_b * les_temperatures))
            for plot in self.plots:
                fig, ax = plot
            plt.figure(0)  # 1st
            plt.plot(1000/les_temperatures, les_d)
            plt.savefig("name.png")
            self.update_first_tab_image("name.png")
        else:
            print("Fonction non reconnue.")


def create_json_example():
    data = []
    # ajout de données "sensées"
    data.append(["D", [1, 6]])
    data.append(["S", [1, 6]])
    alphabet_latin = [chr(x) for x in range(ord('a'), ord('z') + 1)]
    # ecriture de 5 nom au hasard de 9 caractere de long
    liste_nom_equation = []
    for _ in range(5):
        nom = "".join([rd.choice(alphabet_latin) for _ in range(9)])
        liste_nom_equation.append(nom)
    for nom in liste_nom_equation:
        data.append((nom, [rd.randint(0, 50) for _ in range(rd.randint(1, 5))]))
    chaine = json.dumps(data, indent=4)
    with open("json.txt", "w") as fichier:
        fichier.write(chaine)
    # print(chaine)


if __name__ == '__main__':
    create_json_example()
    #print("création de l'interface")
    #print(sys.argv)
    app = QApplication(sys.argv)
    #print("lancement de l'interface")
    ex = App()
    #print("sortie de l'interface")
    rc = app.exec_()
    #print("sortie prog")
    del app
    sys.exit(rc)
