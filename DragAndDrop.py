# !/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QMessageBox, QLineEdit
from PyQt5.QtGui import QIcon

import sys
import os


class FileEdit(QLineEdit):
    def __init__(self, title):
        super(FileEdit, self).__init__()
        self.setText(title)
        self.setReadOnly(True)
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            filepath = str(urls[0].path())[1:]
            # any file type here
            if filepath[-4:].upper() == ".txt":
                self.setText(filepath)
            else:
                dialog = QMessageBox()
                dialog.setWindowTitle("Error: Invalid File")
                dialog.setText("Only .txt files are accepted")
                dialog.setIcon(QMessageBox.Warning)
                dialog.exec_()