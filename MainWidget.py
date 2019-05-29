# todo: remove them
from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout, 
                             QTabWidget,
                             QDesktopWidget,
                             QMainWindow,
                             QAction,
                             QMenuBar,
                             QDialog,
                             QMessageBox
                            )
from PyQt5.QtGui import QIcon, QColor, QPalette, QBrush
import matplotlib.pyplot as plt
from FirstTab import FirstTab
from SecondTab import SecondTab
from ThirdTab import ThirdTab
import os
from PyQt5.QtCore import Qt
from HelpWindow import HelpWindow

class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.onglets = []
        self.plots = [plt.subplots() for _ in range(3)]  # 3 subplots
        self.initUI()

    def initUI(self):

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

        tabs.addTab(FirstTab(), "Lecture")
        tabs.addTab(SecondTab(), "Ecriture")
        tabs.addTab(ThirdTab(), "Post-traitement")
        tabs.setCurrentIndex(0)  # todo: commenter

        layout = QVBoxLayout()  # contient les tabs
        layout.addWidget(tabs)
        self.setLayout(layout)