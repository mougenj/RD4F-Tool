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


class ThirdTab(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)