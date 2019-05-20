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
                             QTabBar,
                             QFileDialog,
                             QMessageBox,
                             QLineEdit,
                             QGroupBox
                            )
from PyQt5.QtGui import QPixmap, QFontMetrics
import json
import numpy as np
from functools import partial
import pdb
import rlcompleter
import time
from QLineEditWidthed import QLineEditWidthed

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

        # TODO: commenter
        with open("/home/tcarre/LSPM-Gui/ressources/json.txt") as fichier:
            self.show_new_file(tab_left, "nom", json.loads(fichier.read()))
        files_vbox = QWidget()
        files_vbox.layout = QVBoxLayout()
        files_vbox.setLayout(files_vbox.layout)
        files_vbox.layout.addWidget(tab_left)
        files_vbox.layout.addWidget(add_files)

        self.layout.addWidget(files_vbox)
        bt_d = QPushButton("Tracer les D")
        bt_d.clicked.connect(partial(self.on_click_tracer, "D"))
        bt_s = QPushButton("Tracer les S")
        bt_s.clicked.connect(partial(self.on_click_tracer, "S"))
        bt_kr = QPushButton("Tracer les Kr") 
        bt_kr.clicked.connect(partial(self.on_click_tracer, "Kr"))
        tab_center = self.make_tab()
        tab_center.layout.addWidget(QLabel("Dessiner les courbes :"))
        tab_center.layout.addWidget(bt_d)
        tab_center.layout.addWidget(bt_s)
        tab_center.layout.addWidget(bt_kr)
        self.layout.addWidget(tab_center)


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
        return make_vbox()

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

    def create_scroll(self, parameters):
        list_data_equation = []
        self.data_onglets.append(list_data_equation)
        for equation_type in parameters["equation"]:
            coefs_type = parameters["equation"][equation_type]
            l_coef_type = list(coefs_type)
            first_coef_type = equation_type + "_0"
            l_coef_type.remove(equation_type + "_0")
            second_coef_type = l_coef_type[0]
            sorted_coefficients = []
            sorted_coefficients.append(equation_type)
            sorted_coefficients.append((first_coef_type, parameters["equation"][equation_type][first_coef_type]))
            sorted_coefficients.append((second_coef_type, parameters["equation"][equation_type][second_coef_type]))
            list_data_equation.append(sorted_coefficients)

        scrollAreaWidgetContents = make_vbox()
        i = 0            
        grid = QGroupBox("equation")
        grid.layout = QGridLayout()
        grid.setLayout(grid.layout)
        #grid.setFlat(False)
        for name, c1, c2 in list_data_equation:
            j = 0
            grid.layout.addWidget(QLabel(name), i, j)
            for c in c1, c2:
                hbox = make_hbox()
                hbox.layout.addWidget(QLabel(c[0]))
                value = "{:.2e}".format(c[1])
                hbox.layout.addWidget(QLabel(value))  # "{:.2e}".format(value)
                grid.layout.addWidget(hbox, i, j+1)
                j += 1
            i += 1
        scrollAreaWidgetContents.layout.addWidget(grid)
        grid = QGroupBox("material")
        grid.layout = QGridLayout()
        grid.setLayout(grid.layout)
        i = 0
        for prop in parameters["material"]:
            grid.layout.addWidget(QLabel(prop), i, 0)
            value = parameters["material"][prop]
            if value is None:
                value = "None"
            elif type(value) is not str:
                value = "{:.2e}".format(value)
            grid.layout.addWidget(QLabel(value), i, 1)
            i += 1
        scrollAreaWidgetContents.layout.addWidget(grid)

        grid = QGroupBox("source")
        grid.layout = QGridLayout()
        grid.setLayout(grid.layout)
        i = 0
        for prop in parameters["source"]:
            grid.layout.addWidget(QLabel(prop), i, 0)
            value = parameters["source"][prop]
            if value is None:
                value = "None"
            elif type(value) is not str:
                value = "{:.2e}".format(value)
            grid.layout.addWidget(QLabel(value), i, 1)
            i += 1
        scrollAreaWidgetContents.layout.addWidget(grid)

        grid = QGroupBox("traps")
        grid.layout = QGridLayout()
        grid.setLayout(grid.layout)
        i = 0
        for trap in parameters["traps"]:
            grid.layout.addWidget(QLabel(str(i)), i, 0)
            j = 0
            for prop in trap:
                hbox = make_hbox()
                hbox.layout.addWidget(QLabel(prop))
                value = trap[prop]
                if value is None:
                    value = "None"
                elif type(value) is not str:
                    value = "{:.2e}".format(value)
                hbox.layout.addWidget(QLabel(value))
                grid.layout.addWidget(hbox, i, j+1)
                j += 1
            i += 1
        scrollAreaWidgetContents.layout.addWidget(grid)


        scroll_area = QScrollArea()
        scroll_area.setWidget(scrollAreaWidgetContents)
        QScroller.grabGesture(scroll_area.viewport(), QScroller.LeftMouseButtonGesture)
        return scroll_area

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
        debut, fin, pas = 300, 2500, 0.1
        les_temperatures = np.arange(debut, fin, pas)
        k_b = 1.38064852 * 10**(-23) * 8.617e+18
        for onglet in self.data_onglets:
            print("un nouvel onglet")
            for equation in onglet:
                if equation[0] == name:
                    print("trouvé")
                    print(equation[1][1], equation[2][1])
                    les_d = equation[1][1] * np.exp(equation[2][1]/(k_b * les_temperatures))
                    for indice in range(len(self.plots)):
                        fig, ax = self.plots[indice]
                        if indice == 0:
                            ax.plot(les_temperatures, les_d)
                        elif indice == 1:
                            ax.plot(np.log(les_temperatures, np.log(les_d)))
                        elif indice == 2:
                            ax.plot(1000/les_temperatures, les_d)
        for indice in range(len(self.plots)):
            fig, ax = self.plots[indice]
            if indice == 0:
                fig.savefig("ressources/tab_right_1.png")
            elif indice == 1:
                fig.savefig("ressources/tab_right_2.png")
            elif indice == 2:
                fig.savefig("ressources/tab_right_3.png")

        self.update_first_tab_image()
        print("Temps de tracé: " + str(time.time() - start))

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


def make_vbox():
    vbox = QWidget()
    vbox.layout = QVBoxLayout()
    vbox.setLayout(vbox.layout)
    return vbox

def make_hbox():
    hbox = QWidget()
    hbox.layout = QHBoxLayout()
    hbox.setLayout(hbox.layout)
    return hbox