import DragAndDrop
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QHBoxLayout, QScrollArea, QScroller, QPushButton, QApplication, QTabWidget, QTreeWidget, QTreeWidgetItem
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
        """
            Here is a little hack: in the QTreeWidget (see below), we will add
            some QTreeWidgetItem. Each one of them will be removable. But each
            time we remove a QTreeWidgetItem, the index of the QTreeWidgetItem
            below it will be reindexed. So, we need to remember how many
            QTreeWidgetItem were deleted to calculate the old index.
        """
        self.nb_created = 0
        self.correspondence_index_position = []

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
        
        tabs.addTab(make_scroll(self.make_vbox_from_data_equation(list_data_equation)), "Coefficients values")
        
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
        self.list_data_source = parameters["source"]
        for prop in parameters["source"]:
            gridSource.layout.addWidget(QLabel(prop), i, 0)
            value = parameters["source"][prop]
            if value is None:
                value = "None"
            elif type(value) is not str:
                if prop == "year":
                    value = str(int(value))
                else:
                    value = "{:.2e}".format(float(value))
            gridSource.layout.addWidget(QLineEditWidthed(value, editable), i, 1)
            i += 1
        tabs.addTab(make_scroll(gridSource), "Source")
        
        tree = QTreeWidget()
        tree.setColumnCount(4)
        tree.setHeaderLabels([
            "Density",
            "Angular frequency",
            "Delete this trap",
            "Add an energy"
        ])
        tree.setObjectName("traps")
        for trap in parameters["traps"]:
            tree_item_for_this_trap = self.create_subtree_for_a_trap(tree, trap)
            for energy in trap["energy"]:
                self.addEnergyToATrap(tree, tree_item_for_this_trap, energy)
        vbox = make_vbox()
        vbox.layout.addWidget(tree)
        if self.editable:
            bt_add_new_trap = QPushButton("Add a trap")
            vbox.layout.addWidget(bt_add_new_trap)
            bt_add_new_trap.clicked.connect(partial(self.create_subtree_for_a_trap, tree, trap))
        tabs.addTab(vbox, "Traps")
        
        self.list_data_equation = list_data_equation
        layout = QVBoxLayout()  # contient les tabs
        layout.addWidget(tabs)
        self.setLayout(layout)
    
    def create_subtree_for_a_trap(self, tree, trap):
        self.correspondence_index_position.append(self.nb_created)
        tree_item_for_this_trap = QTreeWidgetItem(tree)
        tree_item_for_this_trap.setText(0, "{:.2e}".format(float(trap["density"])))
        tree_item_for_this_trap.setText(1, "{:.2e}".format(float(trap["angular_frequency"])))
        tree_item_for_this_trap.correspondence_index_position_energy = []
        tree_item_for_this_trap.nb_energy_created = 0
        
        if self.editable:
            # lets create a button that remove a trap
            remove_bt = QPushButton()
            remove_bt.setIcon(QIcon("ressources/trash-alt-solid.svg"))
            remove_bt.clicked.connect(partial(self.on_click_remove_bt_trap, tree, self.nb_created))
            # add the button to the tree
            tree.setItemWidget(tree_item_for_this_trap, 2, remove_bt)
            # lets create a button that add energy to trap
            add_energy_bt = QPushButton()
            add_energy_bt.setIcon(QIcon("ressources/plus-circle-solid.svg"))
            add_energy_bt.clicked.connect(partial(self.addEnergyToATrap, tree, tree_item_for_this_trap))
            # add the button to the tree
            tree.setItemWidget(tree_item_for_this_trap, 3, add_energy_bt)
        # increment the creation counter
        self.nb_created += 1
        return tree_item_for_this_trap

    def on_click_remove_bt_trap(self, tree, initial_index):
        index_to_delete = self.correspondence_index_position.index(initial_index)
        self.correspondence_index_position.pop(index_to_delete)
        tree.takeTopLevelItem(index_to_delete)
    
    def addEnergyToATrap(self, tree, trap_tree, value=""):
        energy_trap = QTreeWidgetItem(trap_tree)
        tree.setItemWidget(energy_trap, 0, QLineEditWidthed("{:.2e}".format(float(value)), self.editable))

        if self.editable:
            remove_energy_bt = QPushButton()
            remove_energy_bt.setIcon(QIcon("ressources/trash-alt-solid.svg"))
            remove_energy_bt.clicked.connect(partial(self.on_click_remove_energy_bt, trap_tree, trap_tree.nb_energy_created))
            # add the button to the tree
            tree.setItemWidget(energy_trap, 1, remove_energy_bt)
            
        trap_tree.correspondence_index_position_energy.append(trap_tree.nb_energy_created)
        trap_tree.nb_energy_created += 1
        

    def on_click_remove_energy_bt(self, trap_tree, initial_index):
        index_to_delete = trap_tree.correspondence_index_position_energy.index(initial_index)
        trap_tree.correspondence_index_position_energy.pop(index_to_delete)
        trap_tree.removeChild(trap_tree.child(index_to_delete))


    def make_vbox_from_data_equation(self, list_data_equation):
        equations_container = make_vbox()
        equations_container.setObjectName("equation")
        for name, c1, c2 in list_data_equation:
            coef1 = "None" if c1[1] is None else "{:.2e}".format(float(c1[1]))
            coef2 = "None" if c2[1] is None else "{:.2e}".format(float(c2[1]))
            coef2kJmol = "None" if c2[1] is None else "{:.2e}".format(float(c2[1]/0.0104))
            equation_container = QGroupBox()
            if name == "D":
                equation_container.setTitle("for interstitial diffusivity D = D_0 * exp(-E_D/(Kb*T))")
                equation_container.setObjectName("diffusivity")
                grid_data_coef = QGridLayout()
                grid_data_coef.addWidget(QLabel("D_0"), 0, 0)
                grid_data_coef.addWidget(QLineEditWidthed(coef1, self.editable), 0, 1)
                grid_data_coef.addWidget(QLabel("(m²/s)"), 0, 2)
                grid_data_coef.addWidget(QLabel("E_D"), 1, 0)
                grid_data_coef.addWidget(QLineEditWidthed(coef2, self.editable), 1, 1)
                grid_data_coef.addWidget(QLabel("(eV)"), 1, 2)
                grid_data_coef.addWidget(QLineEditWidthed(coef2kJmol, self.editable), 1, 3)
                grid_data_coef.addWidget(QLabel("(kJ/mol)"), 1, 4)
            elif name == "S":
                equation_container.setTitle("for solubility S = S_0 * exp(-E_S/(Kb*T))")
                equation_container.setObjectName("solubility")
                grid_data_coef = QGridLayout()
                grid_data_coef.addWidget(QLabel("S_0"), 0, 0)
                grid_data_coef.addWidget(QLineEditWidthed(coef1, self.editable), 0, 1)
                grid_data_coef.addWidget(QLabel("(m²/s)"), 0, 2)
                grid_data_coef.addWidget(QLabel("E_S"), 1, 0)
                grid_data_coef.addWidget(QLineEditWidthed(coef2, self.editable), 1, 1)
                grid_data_coef.addWidget(QLabel("(eV)"), 1, 2)
                grid_data_coef.addWidget(QLineEditWidthed(coef2kJmol, self.editable), 1, 3)
                grid_data_coef.addWidget(QLabel("(kJ/mol)"), 1, 4)
            elif name == "Kr":
                equation_container.setTitle("for combination Kr = Kr_0 * exp(-E_r/(Kb*T))")  # todo: check translation
                equation_container.setObjectName("combination")
                grid_data_coef = QGridLayout()
                grid_data_coef.addWidget(QLabel("Kr_0"), 0, 0)
                grid_data_coef.addWidget(QLineEditWidthed(coef1, self.editable), 0, 1)
                grid_data_coef.addWidget(QLabel("(m²/s)"), 0, 2)
                grid_data_coef.addWidget(QLabel("E_r"), 1, 0)
                grid_data_coef.addWidget(QLineEditWidthed(coef2, self.editable), 1, 1)
                grid_data_coef.addWidget(QLabel("(eV)"), 1, 2)
                grid_data_coef.addWidget(QLineEditWidthed(coef2kJmol, self.editable), 1, 3)
                grid_data_coef.addWidget(QLabel("(kJ/mol)"), 1, 4)
            else:
                print("WARNING : I cant't show the equation named", name, "because it is not in ['D', 'S', 'Kr'].")
            equation_container.setLayout(grid_data_coef)
            equations_container.layout.addWidget(equation_container)
        return equations_container


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
    return scroll_area