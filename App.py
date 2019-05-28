from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout, 
                             QTabWidget,
                             QDesktopWidget
                            )
from PyQt5.QtGui import QIcon, QColor, QPalette, QBrush
import matplotlib.pyplot as plt
from FirstTab import FirstTab
from SecondTab import SecondTab
from ThirdTab import ThirdTab
import os
from PyQt5.QtCore import Qt
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'RDRP Database Tools'
        self.left = 10
        self.top = 10
        self.width = 1600  # 640
        self.height = 640
        self.onglets = []
        self.plots = [plt.subplots() for _ in range(3)]  # 3 subplots
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + "ressources" +  os.path.sep + "logo.png"))
        self.initUI()
        self.center()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        tabs = QTabWidget()
        tabs.setFocusPolicy(Qt.NoFocus)  # prevent the "horrible orange box effect" on Ubuntu
        tabs.setStyleSheet(tabs.styleSheet() + """
        QTabBar::tab:!selected {
            color: rgb(242, 241, 240);
            background-color: rgb(0, 126, 148);
        }

        QTabBar::tab:selected {
            color: rgb(0, 126, 148);
        }
        """)


        tabs.resize(self.width, self.height)
        tabs.addTab(FirstTab(), "Lecture")
        tabs.addTab(SecondTab(), "Ecriture")
        tabs.addTab(ThirdTab(), "Post-traitement")
        tabs.setCurrentIndex(0) #  todo: commenter

        layout = QVBoxLayout()  # contient les tabs
        layout.addWidget(tabs)
        self.setLayout(layout)
        #set background color
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(0, 113, 134))
        self.setPalette(p)
        self.show()
    
    def center(self):
        # see answer of BPL on https://stackoverflow.com/questions/39046059/pyqt-location-of-the-window
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        maxX = ag.width() - widget.width()
        maxY = 2 * ag.height() - sg.height() - widget.height()
        self.move(maxX/2, maxY/2)