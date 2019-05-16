import DragAndDrop
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QWidget,
                             QPushButton,
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout, 
                             QTabWidget,
                             QScrollArea,
                             QGridLayout,
                             QScroller,
                             QDoubleSpinBox,
                             QTabBar,
                             QFileDialog,
                             QMessageBox
                            )
from PyQt5.QtGui import QPixmap
import json
import numpy as np
from functools import partial
import pdb
import rlcompleter
import time

class FirstTab(QWidget):

    def __init__(self, plots):
        super().__init__()
        self.plots = plots
        self.draw_first_pictures()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.data_onglets = []


        # LEFT
        tab_left = QTabWidget(tabsClosable=True)
        def CloseTab(i):
            tab_left.removeTab(i)
            self.data_onglets.pop(i)
        tab_left.tabCloseRequested.connect(CloseTab)
        tab_left.setTabPosition(QTabWidget.West)
        #pdb.Pdb.complete=rlcompleter.Completer(locals()).complete
        #pdb.set_trace()

        add_files = QWidget()
        add_files.layout = QHBoxLayout()
        add_files.setLayout(add_files.layout)

        add_files.layout.addWidget(DragAndDrop.FileEdit("Glisser vos fichiers ici", partial(self.show_new_file, tab_left)))
        boutton_ajout_fichiers = QPushButton("Ajout de fichier(s)")
        boutton_ajout_fichiers.clicked.connect(partial(self.on_click_open_files, tab_left))
        add_files.layout.addWidget(boutton_ajout_fichiers)        

        files_vbox = QWidget()
        files_vbox.layout = QVBoxLayout()
        files_vbox.setLayout(files_vbox.layout)
        files_vbox.layout.addWidget(tab_left)
        files_vbox.layout.addWidget(add_files)

        self.layout.addWidget(files_vbox)


        # RIGHT

        # let's add tabs in the 1st tab, on the right, with a button to show the image in a matplotlib window
        bt1 = QPushButton("Voir l'image")
        bt1.clicked.connect(partial(self.show_picture, 0))
        bt2 = QPushButton("Voir l'image")
        bt2.clicked.connect(partial(self.show_picture, 1))
        bt3 = QPushButton("Voir l'image")
        bt3.clicked.connect(partial(self.show_picture, 2))

        tab_right = QTabWidget()
        # 1st image
        tab_right_1 = self.make_tab()

        tab_right_1.layout.addWidget(self.make_pixmap("ressources/tab_right_1.png", "ressources/tab_right_1.png"))
        tab_right_1.layout.addWidget(bt1)
        tab_right.addTab(tab_right_1, "Non log")

        tab_right_2 = self.make_tab()
        tab_right_2.layout.addWidget(self.make_pixmap("ressources/tab_right_2.png", "ressources/tab_right_2.png"))
        tab_right_2.layout.addWidget(bt2)
        tab_right.addTab(tab_right_2, "log-log")

        tab_right_3 = self.make_tab()
        tab_right_3.layout.addWidget(self.make_pixmap("ressources/tab_right_3.png", "ressources/tab_right_3.png"))
        tab_right_3.layout.addWidget(bt3)
        tab_right.addTab(tab_right_3, "log-1/T")

        self.layout.addWidget(tab_right)

    def draw_first_pictures(self):
        for indice in range(len(self.plots)):
            fig, ax = self.plots[indice]
            if indice == 0:
                ax.plot([], [])
                fig.savefig("ressources/tab_right_1.png")
            elif indice == 1:
                ax.plot([], [])
                fig.savefig("ressources/tab_right_2.png")
            elif indice == 2:
                ax.plot([], [])
                fig.savefig("ressources/tab_right_3.png")

    def make_tab(self):
        tab = QWidget()
        tab.layout = QVBoxLayout()
        tab.setLayout(tab.layout)
        return tab

    def make_pixmap(self, picture_name, label_name):
        label = QLabel()
        label.setObjectName(label_name)
        pixmap = QPixmap(picture_name)
        label.setPixmap(pixmap)
        return label

    def make_show_files(self, data):
        onglet = {}
        for element in data:
            name, value = element
            onglet[name] = value
        self.data_onglets.append(onglet)
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
            bt.clicked.connect(partial(self.on_click_tracer, data[i][0]))
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

    def show_picture(self, i):
        fig, ax = self.plots[i]
        fig.show()

    @pyqtSlot()
    def on_click_tracer(self, name):
        start = time.time()  # 4*2 onglets utiles + 1 inutile : Temps: 4.524548768997192 (1.1296305656433105 en mutualisant les ecritures)
        print('Tracons la courbe des lignes ' + name)
        # effaçons les graphes pécédents
        for indice in range(len(self.plots)):
            fig, ax = self.plots[indice]
            ax.cla()
        if name == "S" or name == "D":
            debut, fin, pas = 300, 2500, 0.1
            les_temperatures = np.arange(debut, fin, pas)
            k_b = 1.38064852 * 10**(-23) * 8.617e+18
            for onglet in self.data_onglets:
                try:
                    values = onglet[name]
                    d_0 = values[0]  # 6*10**-4
                    e_d = values[1]  # 1.04
                    les_d = d_0 * np.exp(-e_d/(k_b * les_temperatures))
                    for indice in range(len(self.plots)):
                        fig, ax = self.plots[indice]
                        if indice == 0:
                            ax.plot(les_temperatures, les_d)
                        elif indice == 1:
                            ax.plot(np.log(les_temperatures, np.log(les_d)))
                        elif indice == 2:
                            ax.plot(1000/les_temperatures, les_d)
                except KeyError:
                    pass
            for indice in range(len(self.plots)):
                fig, ax = self.plots[indice]
                if indice == 0:
                    fig.savefig("ressources/tab_right_1.png")
                elif indice == 1:
                    fig.savefig("ressources/tab_right_2.png")
                elif indice == 2:
                    fig.savefig("ressources/tab_right_3.png")

            self.update_first_tab_image()
            print("Temps: " + str(time.time() - start))
        else:
            print("Fonction non reconnue lors du dessin.")

    @pyqtSlot()
    def on_click_open_files(self, tab_to_add):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        sucessfully_loaded = []
        failed = []
        for filepath in files:
            try:
                with open(filepath, "r") as fichier: 
                    liste = json.loads(fichier.read())
                sucessfully_loaded.append((filepath, liste))
            except Exception as e:
                failed.append(filepath)
        if failed:
            dialog = QMessageBox()
            if len(failed) > 1:
                dialog.setWindowTitle("Error: Invalid Files")
            else:
                dialog.setWindowTitle("Error: Invalid File")
            error_text = "An error occured when loading :"
            for failure in failed:
                error_text += "\n" + failure
            dialog.setText(error_text)
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()
        for success in sucessfully_loaded:
            get_name_from_path = lambda path : path.split("/")[-1].split('.', 1)[0]
            filepath, liste = success
            self.show_new_file(tab_to_add, get_name_from_path(filepath), liste)