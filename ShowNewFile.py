import DragAndDrop
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QHBoxLayout, QScrollArea, QScroller
from QLineEditWidthed import QLineEditWidthed



class ShowNewFile(QWidget):

    def __init__(self, parameters, editable=False):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

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
                hbox.layout.addWidget(QLineEditWidthed(value, editable))  # "{:.2e}".format(value)
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
            grid.layout.addWidget(QLineEditWidthed(value, editable), i, 1)
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
            grid.layout.addWidget(QLineEditWidthed(value, editable), i, 1)
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
                hbox.layout.addWidget(QLineEditWidthed(value, editable))
                grid.layout.addWidget(hbox, i, j+1)
                j += 1
            i += 1
        scrollAreaWidgetContents.layout.addWidget(grid)


        scroll_area = QScrollArea()
        scroll_area.setWidget(scrollAreaWidgetContents)
        QScroller.grabGesture(scroll_area.viewport(), QScroller.LeftMouseButtonGesture)

        self.layout.addWidget(scroll_area)
        self.list_data_equation = list_data_equation


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