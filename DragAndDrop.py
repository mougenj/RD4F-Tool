# !/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QMessageBox, QLineEdit
import json
from re import search

class FileEdit(QLineEdit):
    """
        A modified QLineEdit that execute a function when some files are
        dropped on it.
    """
    def __init__(self, title, trigger):
        """
            Init the FileEdit.
        """
        super(FileEdit, self).__init__()
        self.setText(title)
        self.setReadOnly(True)
        self.setDragEnabled(True)
        self.trigger = trigger

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
        """
            Execute the trigger when files are dropped on it.
            Add two parameters to the trigger: the name of the file
            (without extension) and a list of data included in the JSON file.
            If some files are dropped while one of them is not a valid JSON
            file, a pop-up will display an warning, and the programm will only
            load the correct JSON files, if there is any in the dropped files.
        """
        data = event.mimeData()
        urls = data.urls()
        sucessfully_loaded = []
        failed = []
        for url in urls:
            filepath = str(url.path())
            if search(r"/[\w]+:/", filepath) is not None:
                filepath = filepath[1::]
            try:
                with open(filepath, "r") as fichier: 
                    liste = json.loads(fichier.read())
                sucessfully_loaded.append((filepath, liste))
            except Exception as e:
                failed.append(filepath)
                print("Error when laoding a file:", e)
        if failed:  # if failed is not empty
            dialog = QMessageBox()
            # handle plural
            if len(failed) > 1:
                dialog.setWindowTitle("Error: Invalid Files")
            else:
                dialog.setWindowTitle("Error: Invalid File")
            error_text = "An error occured when loading :\n"
            error_text += "\n".join(failed)
            dialog.setText(error_text)

            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()
        for success in sucessfully_loaded:
            get_name_from_path = lambda path : path.split("/")[-1].split('.', 1)[0]
            filepath, liste = success
            self.trigger(get_name_from_path(filepath), liste)