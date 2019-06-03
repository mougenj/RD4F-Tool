#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout, 
                             QTabWidget,
                             QDesktopWidget,
                             QMainWindow,
                             QAction,
                             QMenuBar,
                             QDialog,
                             QMessageBox,
                             QPushButton,
                             QApplication
                            )
from PyQt5.QtGui import QIcon, QColor, QPalette, QBrush
import matplotlib.pyplot as plt
from FirstTab import FirstTab
from SecondTab import SecondTab
from ThirdTab import ThirdTab
import os
from PyQt5.QtCore import Qt
import sys

class Second(QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)


class First(QMainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)
        self.pushButton = QPushButton("click me")

        self.setCentralWidget(self.pushButton)

        self.pushButton.clicked.connect(self.on_pushButton_clicked)

    def on_pushButton_clicked(self):
        dialog = Second(self)
        dialog.show()


def main():
    app = QApplication(sys.argv)
    main = First()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()