from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QWidget,
                             QHBoxLayout,
                             QFileDialog,
                             QMessageBox,
                             QListWidgetItem,
                             QPushButton,
                             QLabel,
                             QTabWidget,
                             QGroupBox,
                             QVBoxLayout,
                             QCheckBox,
                             QScrollArea,
                             QScroller
                            )
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import json
import numpy as np
from functools import partial
import time

from myListWidget import DoubleThumbListWidget
from makeWidget import make_vbox, make_hbox, make_scroll
from PltWindows import PltWindowProfile
from AddFiles import AddFiles
 
from DataOfAFile import DataOfAFile


class Checkboxes(QGroupBox):
    
    def __init__(self, name):
        super().__init__()

        self.vbox = make_vbox()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.vbox)
        QScroller.grabGesture(scroll_area.viewport(), QScroller.LeftMouseButtonGesture)
        
        self.setTitle(name)
        self.setObjectName(name)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(scroll_area)
        self.checked = []
    
    def addCheckbox(self):
        i = len(self.checked)
        if i == 0:
            cb = QCheckBox("solubility")
        elif i == 1:
            cb = QCheckBox("source")
        else:
            cb = QCheckBox("trap " + str(i - 1))
        cb.setCheckState(True)
        cb.setTristate(False)

        self.checked.append(True)

        trigger = partial(self.state_changed, cb, i)
        cb.stateChanged.connect(trigger)
        self.vbox.layout.addWidget(cb)

    def state_changed(self, cb, i):
        self.checked[i] = cb.isChecked()
        print(self.checked)
    
    def getChecked(self):
        return self.checked


class Profile(QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.data_onglets = []

        self.doublelist = DoubleThumbListWidget()
        trigger_click = partial(self.on_click_open_files, self.doublelist)
        
        def todo(*args):
            pass
        
        bt_draw = QPushButton("Draw")
        bt_draw.clicked.connect(self.draw)

        draw_bts = make_vbox()
        #for _ in range(10):  # todo: find another way to place the widget down
        #    draw_bts.layout.addWidget(QLabel(" "))
        draw_bts.layout.addWidget(QLabel("Draw"))
        draw_bts.layout.addWidget(bt_draw)
        self.checkboxes = Checkboxes("Select your data")
        
        self.layout.addWidget(
            make_hbox(
                make_vbox(
                    self.doublelist,
                    AddFiles(todo, trigger_click)  # todo
                ),
                make_vbox(
                    self.checkboxes,
                    draw_bts
                )
            )
        )

        self.pltwindows = [PltWindowProfile() for _ in range(4)]
        tab_right = QTabWidget()
        tab_right.setFocusPolicy(Qt.NoFocus)
        tab_right.addTab(self.pltwindows[0], "Log - Natural")
        tab_right.addTab(self.pltwindows[1], "Log - 1/T")
        tab_right.addTab(self.pltwindows[2], "Natural - Natural")
        tab_right.addTab(self.pltwindows[3], "Log - Log")
        self.layout.addWidget(tab_right)


        get_name_from_path = lambda path : path.split("/")[-1].split('.', 1)[0]
        filepath = "cas_test/profil000001.txt"
        data = self.getDataFromFilepath(filepath)
        name = get_name_from_path(filepath)
        self.open_new_file(self.doublelist, DataOfAFile(filepath, name, data))
        

    def open_new_file(self, doubleListToAdd, data):
        doubleListToAdd.addItemFromData(data)
    
    def getDataFromFilepath(self, filepath):
        list_numbers = []
        length = -1
        with open(filepath, "r") as fichier:
            for ligne in fichier:
                if not ligne.strip().startswith("%"):
                    numbers = [float(x) for x in ligne.split()]
                    if length == -1:
                        length = len(numbers)
                    else:
                        if length != len(numbers):
                            raise Exception("the file can't be parsed")
                    list_numbers.append(numbers)
        
        # Here, numbers looks like:
        # [[x0, y0, z0, ...], [x1, y1, z1, ...], [x2, y2, z2, ...], ...]
        # It is better to have:
        # [[x0, x1, x2, ...], [y0, y1, y2, ...], [z0, z1, z2, ...]]
        list_numbers = list(zip(*list_numbers))
        list_numbers = np.array(list_numbers)
        maxlen = len(list_numbers)

        checked = self.checkboxes.getChecked()
        
        if (maxlen > len(checked)):
            diff = maxlen - len(checked) - 1
            print("adding ", maxlen, "-", len(checked), "checkboxes")
            for i in range(diff):
                self.checkboxes.addCheckbox()
        
        try:
            master, slaves = self.doublelist.getData()
            if master:
                master_t, master_y, *master_traps = master.data
                maxlen = max(maxlen, len(master_traps))
            if slaves:
                for slave in slaves:
                    _, _, *slave_traps = slave.data
                    maxlen = max(maxlen, len(slave_traps))
        except Exception as e:
            print(e)
        print(maxlen)

        return list_numbers

    @pyqtSlot()
    def on_click_open_files(self, doubleListToAdd):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        sucessfully_loaded = []
        failed = []
        get_name_from_path = lambda path : path.split("/")[-1].split('.', 1)[0]
        for filepath in files:
            try:
                data = self.getDataFromFilepath(filepath)
                name = get_name_from_path(filepath)
                sucessfully_loaded.append(DataOfAFile(filepath, name, data))
            except Exception as e:
                print(e)
                failed.append(filepath)
        if failed:
            if len(failed) > 1:
                title = "Error: Invalid Files"
            else:
                title = "Error: Invalid File"
            error_text = "An error occured when loading :"
            for failure in failed:
                error_text += "\n" + failure
            self.newErrorWindow(title, error_text)
        for success in sucessfully_loaded:
            self.open_new_file(doubleListToAdd, success)
    
    def newErrorWindow(self, title, content):
        dialog = QMessageBox()
        dialog.setWindowTitle(title)
        dialog.setText(content)
        dialog.setIcon(QMessageBox.Warning)
        dialog.exec_()

    @pyqtSlot()
    def draw(self):
        start = time.time()

        # clean graphs
        for indice_figure in range(len(self.pltwindows)):
            self.pltwindows[indice_figure].clear()
        master, slaves = self.doublelist.getData()

        checked = self.checkboxes.checked

        if master:
            # master
            master_t, master_y, *master_traps, master_source = master.data
            xmax = master_t[0]

            if checked[0]:
                self.pltwindows[0].plot((master_t, master_y), master.name + " solubility")
            if checked[1]:
                self.pltwindows[0].plot((master_t, master_source), master.name + " source")
            for index, trap in enumerate(master_traps):
                if checked[index + 2]:
                    self.pltwindows[0].plot((master_t, trap), master.name + " (trap " + str(index + 1) + ")")
            
        if slaves:
            # slaves
            for slave in slaves:
                slave_t, slave_y, *slaves_traps, slave_source = slave.data
                if checked[0]:
                    self.pltwindows[0].plot((slave_t, slave_y), slave.name + " solubility")
                if checked[1]:
                    sous = master_source - slave_source
                    print(sous)
                    score = np.max(np.abs(np.sqrt(sous**2)))
                    self.pltwindows[0].plot((master_t, slave_source), slave.name + " source (score: " + str(score) + ")")
                for index, trap in enumerate(slaves_traps):
                    if checked[index + 2]:
                        self.pltwindows[0].plot((slave_t, trap), slave.name + " (trap " + str(index + 1) + ")")
                
        print("Time taken to plot " + str(time.time() - start))