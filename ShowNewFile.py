import DragAndDrop
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QHBoxLayout, QScrollArea, QScroller, QPushButton, QApplication, QTabWidget
from QLineEditWidthed import QLineEditWidthed
from PyQt5.QtGui import QColor, QFont, QIcon
import pdb
from PyQt5.QtCore import Qt
import rlcompleter
from functools import partial


class ShowNewFile(QWidget):

    def __init__(self, parameters, color, editable=False):
        super().__init__()
        self.editable = editable

        tabs = QTabWidget()
        tabs.setFocusPolicy(Qt.NoFocus)  # prevent the "horrible orange box effect" on Ubuntu
        tabs.setStyleSheet(tabs.styleSheet() + """
        QTabBar::tab:!selected {
            color: rgb(242, 241, 240);
            background-color: rgb(0, 126, 148);
        }

        QTabBar::tab:selected {
            color: rgb(0, 126, 148);
        }
        """)

        #change color
        p = self.palette()
        red, green, blue, alpha = color
        p.setColor(self.backgroundRole(), QColor(red, green, blue, alpha))
        self.setPalette(p)
        
        

        list_data_equation = []
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

        adatome_name = parameters["material"]["adatome"]
        adatome_name = str(adatome_name) if adatome_name is not None else "None"
        material_name = parameters["material"]["name"]
        material_name = str(material_name) if material_name is not None else "None"
        name_of_area = QLabel("diffusion of " + adatome_name + " in " + material_name)
        myFont=QFont()
        myFont.setBold(True)
        name_of_area.setFont(myFont)
        #tabs.addTab(make_scroll(name_of_area), "1er")
        
        i = 0
        gridEquation = QWidget()
        gridEquation.layout = QGridLayout()
        gridEquation.setLayout(gridEquation.layout)
        gridEquation.setObjectName("equation")
        for name, c1, c2 in list_data_equation:
            j = 0
            gridEquation.layout.addWidget(QLabel(name), i, j)
            for c in c1, c2:
                hbox = make_hbox()
                hbox.layout.addWidget(QLabel(c[0]))
                if c[1] is None:
                    value = "None"
                else:
                    value =  value = "{:.2e}".format(float(c[1]))
                hbox.layout.addWidget(QLineEditWidthed(value, editable))
                gridEquation.layout.addWidget(hbox, i, j+1)
                j += 1
            i += 1
        tabs.addTab(make_scroll(gridEquation), "Equation")
        
        gridMaterial = QWidget()
        gridMaterial.layout = QGridLayout()
        gridMaterial.setLayout(gridMaterial.layout)
        gridMaterial.setObjectName("material")
        i = 0
        for prop in parameters["material"]:
            gridMaterial.layout.addWidget(QLabel(prop), i, 0)
            value = parameters["material"][prop]
            if value is None:
                value = "None"
            elif type(value) is not str:
                value = "{:.2e}".format(float(value))
            gridMaterial.layout.addWidget(QLineEditWidthed(value, editable), i, 1)
            i += 1
        tabs.addTab(make_scroll(gridMaterial), "Material")

        gridSource = QWidget()
        gridSource.layout = QGridLayout()
        gridSource.setLayout(gridSource.layout)
        gridSource.setObjectName("source")
        i = 0
        for prop in parameters["source"]:
            gridSource.layout.addWidget(QLabel(prop), i, 0)
            value = parameters["source"][prop]
            if value is None:
                value = "None"
            elif type(value) is not str:
                value = "{:.2e}".format(float(value))
            gridSource.layout.addWidget(QLineEditWidthed(value, editable), i, 1)
            i += 1
        tabs.addTab(make_scroll(gridSource), "Source")

        gridTraps = QWidget()
        gridTraps.layout = QGridLayout()
        gridTraps.setLayout(gridTraps.layout)
        gridTraps.setObjectName("traps")
        i = 0
        for trap in parameters["traps"]:
            gridTraps.layout.addWidget(QLabel(str(i)), i, 0)
            j = 0
            for prop in trap:
                hbox = make_hbox()
                hbox.layout.addWidget(QLabel(prop))
                value = trap[prop]
                if value is None:
                    value = "None"
                elif type(value) is not str:
                    value = "{:.2e}".format(float(value))
                hbox.layout.addWidget(QLineEditWidthed(value, editable))
                gridTraps.layout.addWidget(hbox, i, j+1)
                j += 1
            if self.editable:
                self.add_remove_bt(gridTraps, i, j+1)
            i += 1
        vbox = make_vbox()
        vbox.layout.addWidget(gridTraps)
        scroll_area = make_scroll(vbox)
        if self.editable:
            bt_add_new_trap = QPushButton("Add a trap")
            vbox.layout.addWidget(bt_add_new_trap)
            i += 1
            bt_add_new_trap.clicked.connect(partial(self.on_clik_bt_add_new_trap, scroll_area, gridTraps, bt_add_new_trap, self))
        tabs.addTab(scroll_area, "Traps")
        # pdb.Pdb.complete=rlcompleter.Completer(locals()).complete; pdb.set_trace()
        
        self.list_data_equation = list_data_equation
        layout = QVBoxLayout()  # contient les tabs
        layout.addWidget(tabs)
        self.setLayout(layout)
    
    def add_remove_bt(self, grid, i, j):
        remove_bt = QPushButton()
        img = QIcon("ressources/trash-alt-solid.svg")
        remove_bt.setIcon(img)
        remove_bt.clicked.connect(partial(self.on_click_remove_bt_trap, grid, i))
        grid.layout.addWidget(remove_bt, i, j)

    def on_clik_bt_add_new_trap(self, qscroll, grid, bt, thing):
        i = grid.layout.rowCount()

        grid.layout.addWidget(QLabel(str(i)), i, 0)
        j = 0
        for prop in ("energy", "density", "angular_frequency"):
            hbox = make_hbox()
            hbox.layout.addWidget(QLabel(prop))
            hbox.layout.addWidget(QLineEditWidthed("None", True))
            grid.layout.addWidget(hbox, i, j+1)
            j += 1
        self.add_remove_bt(grid, i, j+1)
        qscroll.widget().resize(qscroll.widget().sizeHint())
        QApplication.processEvents()
        vbar = qscroll.verticalScrollBar()
        vbar.setValue(vbar.maximum())

    def on_click_remove_bt_trap(self, grid, i):
        for j in range(grid.layout.columnCount()):
            try:
                grid.layout.itemAtPosition(i, j).widget().setParent(None)
            except Exception as e:
                print(e)
    


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


def make_scroll(scrollAreaWidgetContents):
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(scrollAreaWidgetContents)
    QScroller.grabGesture(scroll_area.viewport(), QScroller.LeftMouseButtonGesture)
    print()
    print()
    return scroll_area