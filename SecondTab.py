from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QWidget,
                             QPushButton,
                             QHBoxLayout
                            )
from PyQt5.QtGui import QIcon, QPixmap
import matplotlib.pyplot as plt
import json
import numpy as np
from functools import partial

class SecondTab(QWidget):

    def __init__(self):
        super().__init__()
        # create the tab
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        # fill it
        boutton = QPushButton("PyQt5 button")
        boutton.clicked.connect(self.on_click)
        self.layout.addWidget(boutton)
        # return it
        #return tab2

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')