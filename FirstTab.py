import DragAndDrop
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
                             QGroupBox,
                             QPlainTextEdit,
                             QLineEdit)
from PyQt5.QtGui import QIcon, QPixmap
import matplotlib.pyplot as plt
import json
import numpy as np
from functools import partial
import DragAndDrop

class FirstTab(QWidget):

    def __init__(self, data, plots):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.data = data
        self.plots = plots

        # LEFT
        tab_left = QTabWidget(tabsClosable=True)
        tab_left.setTabPosition(QTabWidget.West)

        add_files = QWidget()
        add_files.layout = QHBoxLayout()
        add_files.setLayout(add_files.layout)

        add_files.layout.addWidget(DragAndDrop.FileEdit("Glisser vos fichiers ici", partial(self.show_new_file, tab_left)))
        add_files.layout.addWidget(QPushButton("Ajout de fichier(s)"))        

        files_vbox = QWidget()
        files_vbox.layout = QVBoxLayout()
        files_vbox.setLayout(files_vbox.layout)
        files_vbox.layout.addWidget(tab_left)
        files_vbox.layout.addWidget(add_files)

        self.layout.addWidget(files_vbox)


        # RIGHT

        # let's add tabs in the 1st tab, on the right
        tab_right = QTabWidget()
        # 1st image
        tab_right_1 = self.make_tab()
        tab_right_1.layout.addWidget(self.make_pixmap("ressources/tab_right_1.png", "ressources/tab_right_1.png"))
        tab_right.addTab(tab_right_1, "Non log")

        tab_right_2 = self.make_tab()
        tab_right_2.layout.addWidget(self.make_pixmap("ressources/tab_right_2.png", "ressources/tab_right_2.png"))
        tab_right.addTab(tab_right_2, "log-log")

        tab_right_3 = self.make_tab()
        tab_right_3.layout.addWidget(self.make_pixmap("ressources/tab_right_3.png", "ressources/tab_right_3.png"))
        tab_right.addTab(tab_right_3, "log-1/T")

        self.layout.addWidget(tab_right)

    def make_tab(self):
        tab = QWidget()
        tab.layout = QHBoxLayout()
        tab.setLayout(tab.layout)
        return tab

    def make_pixmap(self, picture_name, label_name):
        label = QLabel()
        label.setObjectName(label_name)
        pixmap = QPixmap(picture_name)
        label.setPixmap(pixmap)
        return label

    def make_show_files(self, data):
        show = QWidget()
        show.layout = QVBoxLayout()
        show.setLayout(show.layout)
        show.layout.addWidget(self.create_scroll(data))
        return show

    def show_new_file(self, tab, name, data):
        decoupe = lambda chaine : "..." + chaine[-5:] if len(chaine) > 10 else chaine
        tab.addTab(self.make_show_files(data), decoupe(name))


    def create_scroll(self, data):
        scroll_area = QScrollArea()
        #scroll_area.setWidgetResizable(True)
        scrollAreaWidgetContents = QWidget()
        grid_layout = QGridLayout(scrollAreaWidgetContents)
        for i, element in enumerate(data):
            name, values = element
            # first of all, place the name at the beginning of the line
            grid_layout.addWidget(QLabel(name), i, 0)
            for j, value in enumerate(values):
                # add a spinbox at the right place with the right value
                sp = QDoubleSpinBox()
                sp.setObjectName(json.dumps([i, j]))
                sp.setValue(value)
                sp.valueChanged.connect(partial(self.on_update_spin_box, data))
                grid_layout.addWidget(sp, i, j+1)
            # last but not least, let's create a button at the end of the line
            bt = QPushButton("Tracer") 
            bt.clicked.connect(partial(self.on_click_tracer, data[i]))
            grid_layout.addWidget(bt, i, len(data) + 1)

        QScroller.grabGesture(
            scroll_area.viewport(), QScroller.LeftMouseButtonGesture
        )

        scroll_area.setWidget(scrollAreaWidgetContents)
        return scroll_area

    def on_update_spin_box(self, data):
        spinbox = self.sender()
        i, j = json.loads(spinbox.objectName())
        data[i][1][j] = spinbox.value()

    def update_first_tab_image(self):
        tabWidget = self.findChildren(QTabWidget)[1]
        labels = tabWidget.findChildren(QLabel)

        for label in labels:
            if label.pixmap() is not None:
                name_label = label.objectName()
                pixmap = QPixmap(name_label)
                label.setPixmap(pixmap)

    @pyqtSlot()
    def on_click_tracer(self, line):
        print('Tracons la courbe de la ligne ' + str(line))
        name, values = line
        if name == "S" or name == "D":
            debut, fin, pas = 300, 2500, 0.1
            les_temperatures = np.arange(debut, fin, pas)
            d_0 = values[0]  # 6*10**-4
            e_d = values[1]  # 1.04
            k_b = 1.38064852 * 10**(-23) * 8.617e+18
            les_d = d_0 * np.exp(-e_d/(k_b * les_temperatures))
            for indice in range(len(self.plots)):
                fig, ax = self.plots[indice]
                if indice == 0:
                    ax.plot(les_temperatures, les_d)
                    fig.savefig("ressources/tab_right_1.png")
                elif indice == 1:
                    ax.plot(np.log(les_temperatures, np.log(les_d)))
                    fig.savefig("ressources/tab_right_2.png")
                elif indice == 2:
                    ax.plot(1000/les_temperatures, les_d)
                    fig.savefig("ressources/tab_right_3.png")
                else:
                    print("trop de figure a tracer")
                    print(indice, len(self.plots))

            self.update_first_tab_image()
        else:
            print("Fonction non reconnue lors du dessin.")