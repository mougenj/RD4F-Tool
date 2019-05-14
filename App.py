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
import matplotlib.pyplot as plt
import json
import numpy as np
from functools import partial
from FirstTab import FirstTab
from SecondTab import SecondTab
from ThirdTab import ThirdTab

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Titre'
        self.left = 10
        self.top = 10
        self.width = 1500  # 640
        self.height = 480
        fileName = "json.txt"
        self.onglets = []
        self.plots = [plt.subplots() for _ in range(3)]  # 3 subplots

        with open(fileName, "r") as fichier:
            chaine = fichier.read()
            self.data = json.loads(chaine)

        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        tabs = QTabWidget()#tabsClosable=True
        #tabs.setTabPosition(QTabWidget.West)
        tabs.resize(self.width, self.height)
        tabs.addTab(self.create_fisrt_tab(), "Lecture")
        tabs.addTab(self.create_second_tab(), "Ecriture")
        tabs.addTab(self.create_third_tab(), "Post-traitement")

        layout = QVBoxLayout()  # contient les tabs
        layout.addWidget(tabs)
        self.setLayout(layout)
        self.show()
    
    def create_fisrt_tab(self):
        return FirstTab(self.data, self.plots)
    
    def create_second_tab(self):
        return SecondTab()

    def create_third_tab(self):
        return ThirdTab()