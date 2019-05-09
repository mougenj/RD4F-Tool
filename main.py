import sip
sip.setdestroyonexit(True)

#from PyQt5.QtCore import *
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
                             QSpinBox)
from PyQt5.QtGui import QIcon, QPixmap
import random as rd
import sys
import matplotlib.pyplot as plt
import json


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Titre'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

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
        label = QLabel(self)
        pixmap = QPixmap('image.png')
        label.setPixmap(pixmap)
        tab1.layout.addWidget(label)
        #return it
        return tab1
    
    def create_second_tab(self):
        # create the tab
        tab2 = QWidget()
        tab2.layout = QHBoxLayout()
        tab2.setLayout(tab2.layout)
        # fill it
        boutton = QPushButton("PyQt5 button")
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
        data = json.loads(chaine)
        # print("I loaded", data)
        scroll_area = QScrollArea()
        layout = QGridLayout()
        layout.addWidget(scroll_area)

        scroll_widget = QWidget()
        scroll_layout = QFormLayout(scroll_widget)

        for element in data:
            # create a line
            line = QWidget()
            line.layout = QHBoxLayout()
            line.setLayout(line.layout)
            
            #fill the line
            name, values = element
            line.layout.addWidget(QLabel(name))
            for value in values:
                sp = QSpinBox()
                sp.setValue(value)
                line.layout.addWidget(sp)
            scroll_layout.addRow(line)

        scroll_area.setWidget(scroll_widget)

        QScroller.grabGesture(
            scroll_area.viewport(), QScroller.LeftMouseButtonGesture
        )

        return scroll_area


def create_json_example():
    data = []
    alphabet_latin = [chr(x) for x in range(ord('a'), ord('z') + 1)]
    #ecriture de 5 nom au hasard de 9 caractere de long
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
