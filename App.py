from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout, 
                             QTabWidget,
                             QStyle
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
        self.title = 'Titre'
        self.left = 10
        self.top = 10
        self.width = 1500  # 640
        self.height = 480
        fileName = "json.txt"
        self.onglets = []
        self.plots = [plt.subplots() for _ in range(3)]  # 3 subplots
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + os.path.sep + "logo.png"))
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        tabs = QTabWidget()#tabsClosable=True
        #tabs.tabBar().setTabTextColor(1, QColor(0, 0, 0))
        #self.setStyle(Style_tweaks())
        tabs.setFocusPolicy(Qt.NoFocus)
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

        # todo: commenter
        tabs.setCurrentIndex(0) 

        layout = QVBoxLayout()  # contient les tabs
        layout.addWidget(tabs)
        self.setLayout(layout)
        #set background color
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(0, 113, 134))
        self.setPalette(p)
        #set haeder
        self.show()



class Style_tweaks(QStyle):

    def __init__(self):
        super().__init__()

    def drawPrimitive(self, element, option, painter, widget):
        print(element)
        if element == QStyle.PE_FrameFocusRect:
            return
        super().drawPrimitive(element, option, painter, widget)