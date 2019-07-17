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
from Checkboxes import ProfileCheckboxes


class Profile(QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.data_onglets = []
        self.names_of_curves = ["solubility", "source", "trap"]

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
        self.checkboxes = ProfileCheckboxes("Select your data", self.names_of_curves)
        
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
        tab_right.setCurrentIndex(3)
        self.layout.addWidget(tab_right)

        # get_name_from_path = lambda path : path.split("/")[-1].split('.', 1)[0]
        # filepath = "cas_test/profil000400.txt"
        # data, codename = self.getDataFromFilepath(filepath)
        # name = get_name_from_path(filepath)
        # self.open_new_file(self.doublelist, DataOfAFile(filepath, name, data, codename))
        
        

    def open_new_file(self, doubleListToAdd, data):
        doubleListToAdd.addItemFromData(data)
    
    def getDataFromFilepath(self, filepath):
        list_numbers = []
        length = -1
        with open(filepath, "r") as fichier:
            codename = ""
            for ligne in fichier:
                if not ligne.strip().startswith("%"):
                    numbers = [float(x) for x in ligne.split()]
                    if length == -1:
                        length = len(numbers)
                    else:
                        if length != len(numbers):
                            raise Exception("the file can't be parsed")
                    list_numbers.append(numbers)
                else:
                    # thus this line is a comment
                    # if is starts like "% Code: XXX", then the codename is XXX
                    if ligne.split(":")[0].replace(" ", "") == "%Code":
                        codename = ligne.split(":")[1].strip(" ")

        
        # Here, numbers looks like:
        # [[x0, y0, z0, ...], [x1, y1, z1, ...], [x2, y2, z2, ...], ...]
        # It is better to have:
        # [[x0, x1, x2, ...], [y0, y1, y2, ...], [z0, z1, z2, ...]]
        list_numbers = list(zip(*list_numbers))
        list_numbers = np.array(list_numbers)
        maxlen = len(list_numbers)

        checked = self.checkboxes.getChecked()
        
        if (maxlen > len(checked)):
            diff = maxlen - len(checked) - 1  # -1 because of the abscissa
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

        return list_numbers, codename

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
                data, codename = self.getDataFromFilepath(filepath)
                name = get_name_from_path(filepath)
                sucessfully_loaded.append(DataOfAFile(filepath, name, data, codename))
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

        def plot_every_window(x, y, name):
            if self.checkboxes.isSourceOnly():
                linestyle = ".--"
            else:
                linestyle = ""
            data = x, y
            self.pltwindows[0].plot(data, name, ylog=True, x_label="TODO", y_label="" + " (logscale)", linestyle=linestyle)
            
            data = 1 / x, y
            self.pltwindows[1].plot(data, name, ylog=True, x_label="TODO", y_label="" + " (logscale)", linestyle=linestyle)

            data = x, y
            self.pltwindows[2].plot(data, name, x_label="TODOs", y_label="", linestyle=linestyle)

            data = x, y
            self.pltwindows[3].plot(data, name, xlog=True, ylog=True, x_label="Temperature (K)" + " (logscale)",y_label=""  + " (logscale)", linestyle=linestyle)
        """
                i = len(self.checked)
                if i < len(self.names_of_buttons) - 1:
                    cb = QCheckBox(self.names_of_buttons[i])
                else:
                    cb = QCheckBox(self.names_of_buttons[-1] + str(i + 1 - len(self.names_of_buttons)))
        """
        if master:
            # master
            master_t, master_y, *master_traps, master_source = master.data
            xmax = master_t[0]

            if checked[0]:
                curve_name =  master.name + " " + self.names_of_curves[0]
                plot_every_window(master_t, master_y, curve_name)
            if checked[1]:
                curve_name = master.name + " " + self.names_of_curves[1]
                plot_every_window(master_t, master_source, curve_name)
            for index, trap in enumerate(master_traps):
                if checked[index + 2]:
                    curve_name = master.name + " (" + self.names_of_curves[2] + " " + str(index + 1) + ")"
                    plot_every_window(master_t, trap, curve_name)
            
        if slaves:
            # slaves
            for slave in slaves:
                slave_t, slave_y, *slaves_traps, slave_source = slave.data
                if checked[0]:
                    curve_name =  slave.name + " " + self.names_of_curves[0]
                    plot_every_window(slave_t, slave_y, curve_name)
                if checked[1]:
                    score = np.max(np.abs(np.sqrt((master_source - slave_source)**2)))
                    curve_name = slave.name + " " + self.names_of_curves[1] + " (score: " + str(score) + ")"
                    plot_every_window(slave_t, slave_source, curve_name)
                for index, trap in enumerate(slaves_traps):
                    if checked[index + 2]:
                        curve_name = slave.name + " (" + self.names_of_curves[2] + " " + str(index + 1) + ")"
                        plot_every_window(slave_t, trap, curve_name)
                
        print("Time taken to plot " + str(time.time() - start))