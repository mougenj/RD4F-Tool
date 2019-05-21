from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout, 
                             QTabWidget
                            )
from PyQt5.QtGui import QIcon
import matplotlib.pyplot as plt
from FirstTab import FirstTab
from SecondTab import SecondTab
from ThirdTab import ThirdTab
import os

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Titre'
        self.left = 10
        self.top = 10
        self.width = 1500  # 640
        self.height = 480
        fileName = "ressources/json.txt"
        self.onglets = []
        self.plots = [plt.subplots() for _ in range(3)]  # 3 subplots
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + "ressources" + os.path.sep + "logo.png"))
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        tabs = QTabWidget()#tabsClosable=True
        #tabs.setTabPosition(QTabWidget.West)
        tabs.resize(self.width, self.height)
        tabs.addTab(FirstTab(self.plots), "Lecture")
        tabs.addTab(SecondTab(), "Ecriture")
        tabs.addTab(ThirdTab(), "Post-traitement")

        # todo: commenter
        tabs.setCurrentIndex(1) 

        layout = QVBoxLayout()  # contient les tabs
        layout.addWidget(tabs)
        self.setLayout(layout)
        self.show()