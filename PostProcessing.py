from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout, 
                             QTabWidget
                            )
import matplotlib.pyplot as plt
from Profile import Profile
from Totaux import Totaux
import os
from PyQt5.QtCore import Qt



class PostProcessing(QWidget):
    """
        The main widget of this app. It contains the matplotlib's subplots and
        the three tabs (read, write and post-traitements).
    """
    def __init__(self):
        super().__init__()
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
        tabs.addTab(Profile(), "Profile")
        tabs.addTab(Totaux(), "Totaux")
        tabs.setCurrentIndex(0)

        layout = QVBoxLayout()  # contient les tabs
        layout.addWidget(tabs)
        self.setLayout(layout)