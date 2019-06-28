from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout, 
                             QTabWidget
                            )
import matplotlib.pyplot as plt
from ReadingPart import ReadingPart
from WritingPart import WritingPart
from Profile import Profile
from Totaux import Totaux
import os
from PyQt5.QtCore import Qt



class MainWidget(QWidget):
    """
        The main widget of this app. It contains the matplotlib's subplots and
        the three tabs (read, write and post-traitements).
    """
    def __init__(self):
        super().__init__()
        self.onglets = []
        self.plots = [plt.subplots() for _ in range(3)]  # 3 subplots
        self.initUI()

    def initUI(self):
        """
            Init the UI (ie: set the stylesheet and create the tabs).
        """
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

        tabs.addTab(ReadingPart(), "Read")
        tabs.addTab(WritingPart(), "Write")
        tabs.addTab(Profile(), "Profile")
        tabs.addTab(Totaux(), "Totaux")
        tabs.setCurrentIndex(0)

        layout = QVBoxLayout()  # contient les tabs
        layout.addWidget(tabs)
        self.setLayout(layout)