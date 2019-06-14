import DragAndDrop
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QHBoxLayout, QScrollArea, QScroller, QPushButton, QApplication, QTabWidget, QTreeWidget, QTreeWidgetItem, QHeaderView, QCheckBox
from QLineEditWidthed import QLineEditWidthed
from PyQt5.QtGui import QColor, QFont, QIcon
import pdb
from PyQt5.QtCore import Qt
import rlcompleter
from functools import partial
import makeWidget


class ShowNewFile(QWidget):
    """
        A QWidget that display a new file. Can be editable or not.
        Contains tabs, that split the informations in the JSON into parts.
    """
    def __init__(self, parameters, color, editable=False):
        """
            Init the ShowNewFile.
        """
        super().__init__()
        self.editable = editable
        """
            Here is a little hack: in the QTreeWidget (see below), we will add
            some QTreeWidgetItem. Each one of them will be removable. But each
            time we remove a QTreeWidgetItem, the index of the QTreeWidgetItem
            below it will be reindexed. So, we need to remember how many
            QTreeWidgetItem were deleted to calculate the old index.
            This is done throught a list. Each time we add a node, we add its
            id to the list. This way, when we delete the node, we search the
            position of its id in the list, and we delete the node at this
            position.
            The same process is used later for the node of other nodes.
        """
        self.nb_created = 0
        self.correspondence_index_position = []

        self.setMinimumSize(690, 500)
        tabs = QTabWidget()
        tabs.setFocusPolicy(Qt.NoFocus)  # prevent the "horrible orange box effect" on Ubuntu
        # set the style
        tabs.setStyleSheet(tabs.styleSheet() + """
        QTabBar::tab:!selected {
            color: rgb(242, 241, 240);
            background-color: rgb(0, 126, 148);
        }

        QTabBar::tab:selected {
            color: rgb(0, 126, 148);
        }
        """)

        # change the background color
        p = self.palette()
        red, green, blue, alpha = color
        p.setColor(self.backgroundRole(), QColor(red, green, blue, alpha))
        self.setPalette(p)

        # get the equation from the file
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
        self.list_data_equation = list_data_equation
        # create a tab based on this informations
        tabs.addTab(makeWidget.make_scroll(self.make_vbox_from_data_equation(list_data_equation)), "Coefficients values")

        """
        # display a nice name for the area
        adatome_name = parameters["material"]["adatome"]
        adatome_name = str(adatome_name) if adatome_name is not None else "None"
        material_name = parameters["material"]["name"]
        material_name = str(material_name) if material_name is not None else "None"
        name_of_area = QLabel("diffusion of " + adatome_name + " in " + material_name)
        myFont=QFont()
        myFont.setBold(True)
        name_of_area.setFont(myFont)
        """

        material_container = makeWidget.make_vbox()
        material_container.setObjectName("material")
        gb_material = QGroupBox()
        gb_material.setTitle("material")
        gb_material.setObjectName("gb_material")
        grid_material = QGridLayout()
        grid_material.setObjectName("grid_material")
        gb_material.layout = grid_material
        gb_material.setLayout(gb_material.layout)

        gb_adatome = QGroupBox()
        gb_adatome.setTitle("adatome")
        gb_adatome.setObjectName("gb_adatome")
        grid_adatome = QGridLayout()
        grid_adatome.setObjectName("grid_adatome")
        gb_adatome.layout = grid_adatome
        gb_adatome.setLayout(gb_adatome.layout)

        material_container.layout.addWidget(gb_adatome)
        material_container.layout.addWidget(gb_material)

        adatome_counter = 0
        for key in ["adatome"]:
            try:
                value = parameters["material"][key]
                value = str(value)
                line = QLineEditWidthed(value, editable)
                grid_adatome.addWidget(QLabel(key), adatome_counter, 0)
                grid_adatome.addWidget(line, adatome_counter, 1);
                adatome_counter += 1
            except KeyError:
                print("There is no key named", key, "in the file loaded, thus it is not possible to diplay this information.")
        
        material_counter = 0
        for key in ("lattice_parameter", "atomic_number", "density", "atomic_symbol", "melting_point", "name", "net"):
            try:
                value = parameters["material"][key]
                value = str(value)
                line = QLineEditWidthed(value, editable)
                grid_material.addWidget(QLabel(key), material_counter, 0)
                grid_material.addWidget(line, material_counter, 1);
                material_counter += 1
            except KeyError:
                print("There is no key named", key, "in the file loaded, thus it is not possible to diplay this information.")

        tabs.addTab(makeWidget.make_scroll(material_container), "Material")

        gridSource = QWidget()
        gridSource.layout = QGridLayout()
        gridSource.setLayout(gridSource.layout)
        gridSource.setObjectName("source")
        i = 0
        self.list_data_source = parameters["source"]
        # author_name
        prop = "author_name"
        gridSource.layout.addWidget(QLabel(prop), i, 0)
        value = parameters["source"][prop]
        if value is None:
            value = "None"
        elif type(value) is not str:
            value = "{:.2e}".format(float(value))
        gridSource.layout.addWidget(QLineEditWidthed(value, editable), i, 1)
        i += 1
        # DOI
        prop = "doi"
        gridSource.layout.addWidget(QLabel(prop), i, 0)
        doi_api_success = False
        to_insert = None
        if not self.editable:
            try:
                import signal
                from crossref.restful import Works

                class TimeoutException(Exception):
                    pass

                def deadline(timeout, *args):
                    def decorate(f):
                        """ the decorator creation """
                        def handler(signum, frame):
                            """ the handler for the timeout """
                            raise TimeoutException()
                
                        def new_f(*args):
                            """ the initiation of the handler, 
                            the lauch of the function and the end of it"""
                            signal.signal(signal.SIGALRM, handler)
                            signal.alarm(timeout)
                            res = f(*args)
                            signal.alarm(0)
                            return res
                    
                        new_f.__name__ = f.__name__
                        return new_f
                @deadline(1)
                def request_doi_api():
                    works = Works()
                    value = works.doi(parameters["source"][prop])["link"][0]["URL"]
                    to_insert = QLabel("<html><a href=\"" + value + "\">" + value + "</a></html>")
                    return to_insert
                
                try:
                    to_insert = request_doi_api()
                except TimeoutException:
                    pass
                doi_api_success = True
            except:
                pass
        if not doi_api_success:
            value = parameters["source"][prop]
            if value is None:
                value = "None"
            elif type(value) is not str:
                value = "{:.2e}".format(float(value))
            to_insert = QLineEditWidthed(value, editable)
        gridSource.layout.addWidget(to_insert, i, 1)
        i += 1
        # YEAR
        prop = "year"
        gridSource.layout.addWidget(QLabel(prop), i, 0)
        value = parameters["source"][prop]
        if value is None:
            value = "None"
        elif type(value) is not str:
            value = str(int(value))
        gridSource.layout.addWidget(QLineEditWidthed(value, editable), i, 1)
        i += 1

        tabs.addTab(makeWidget.make_scroll(gridSource), "Source")
        
        tree = QTreeWidget()
        tree.setItemsExpandable(False)
        tabs.setStyleSheet(tabs.styleSheet() + """
        QTreeWidget::item {
            margin: 3px 0;
        }
        """)
        if self.editable:
            tree.setColumnCount(4)
            tree.setHeaderLabels([
                "Density",
                "Angular frequency",
                "Delete this trap",
                "Add an energy to this trap"
            ])
        else:
            tree.setColumnCount(2)
            tree.setHeaderLabels([
                "Density",
                "Angular frequency"
            ])
        tree.header().resizeSection(0, 150)
        tree.header().resizeSection(1, 150)
        tree.header().resizeSection(2, 150)
        tree.header().resizeSection(3, 200)
        tree.header().setStretchLastSection(False)
        tree.setObjectName("traps")
        for trap in parameters["traps"]:
            tree_item_for_this_trap = self.create_subtree_for_a_trap(tree, trap)
            for energy in trap["energy"]:
                self.addEnergyToATrap(tree, tree_item_for_this_trap, energy)
        vbox = makeWidget.make_vbox()
        vbox.layout.addWidget(tree)
        if self.editable:
            bt_add_new_trap = QPushButton("Add a trap")
            vbox.layout.addWidget(bt_add_new_trap)
            empy_trap = {"density":None, "angular_frequency":None, "energy":[]}
            bt_add_new_trap.clicked.connect(partial(self.create_subtree_for_a_trap, tree, empy_trap))
        tabs.addTab(vbox, "Traps")
        
        layout = QVBoxLayout()  # contient les tabs
        layout.addWidget(tabs)
        self.setLayout(layout)
        self.tabs = tabs
    
    def create_subtree_for_a_trap(self, tree, trap):
        """
            Creat a node that disply onformations about a trap. Can have
            subnodes that diplay infos about some energy of this trap.
        """
        # add it to the list, so it can be deleted later
        self.correspondence_index_position.append(self.nb_created)
        tree_item_for_this_trap = QTreeWidgetItem(tree)

        # get informations from the JSON file
        if trap["density"]:
            density = "{:.2e}".format(float(trap["density"]))
        else:
            density = "None"
        density_line = QLineEditWidthed(density, self.editable)
        tree.setItemWidget(tree_item_for_this_trap, 0, density_line)

        if trap["angular_frequency"]:
            angular_frequency = "{:.2e}".format(float(trap["angular_frequency"]))
        else:
            angular_frequency = "None"
        angular_frequency_line = QLineEditWidthed(angular_frequency, self.editable)
        tree.setItemWidget(tree_item_for_this_trap, 1, angular_frequency_line)

        # creat a list that store the ids of its subnodes. see a comment in
        # ShowNewFile.__init() to see how it works.
        tree_item_for_this_trap.correspondence_index_position_energy = []
        tree_item_for_this_trap.nb_energy_created = 0
        
        if self.editable:
            # lets create a button that remove this trap
            remove_bt = QPushButton()
            remove_bt.setIcon(QIcon("ressources/trash-alt-solid.svg"))
            remove_bt.setMaximumSize(50, 50)
            remove_bt.clicked.connect(partial(self.on_click_remove_bt_trap, tree, self.nb_created))
            # add the button to the tree
            tree.setItemWidget(tree_item_for_this_trap, 2, remove_bt)
            # lets create a button that add energy to this trap
            add_energy_bt = QPushButton()
            add_energy_bt.setIcon(QIcon("ressources/plus-circle-solid.svg"))
            add_energy_bt.setMaximumSize(50, 50)
            add_energy_bt.clicked.connect(partial(self.addEnergyToATrap, tree, tree_item_for_this_trap))
            # add the button to the tree
            tree.setItemWidget(tree_item_for_this_trap, 3, add_energy_bt)
        # increment the creation counter
        tree_item_for_this_trap.setExpanded(True)
        self.nb_created += 1

        return tree_item_for_this_trap

    def on_click_remove_bt_trap(self, tree, initial_index):
        """
            Remove the trap with the id initial_index.
        """
        # get the index
        index_to_delete = self.correspondence_index_position.index(initial_index)
        # remove it from the list, so that the other id will be reindexed
        self.correspondence_index_position.pop(index_to_delete)
        # remove the node
        tree.takeTopLevelItem(index_to_delete)
    
    def addEnergyToATrap(self, tree, trap_tree, value=""):
        """
            Add a subnode to this node that can be filled by the user to
            display informations about energy of this trp.
        """
        energy_trap = QTreeWidgetItem(trap_tree)
        tree.setItemWidget(energy_trap, 0, QLineEditWidthed("{:.2e}".format(float(value)), self.editable))

        if self.editable:
            # create a button that remove this subnode
            remove_energy_bt = QPushButton("delete energy")
            remove_energy_bt.setIcon(QIcon("ressources/trash-alt-solid.svg"))
            # remove_energy_bt.setMinimumSize(120, 0);
            # remove_energy_bt.setMaximumSize(120, 28);
            remove_energy_bt.clicked.connect(partial(self.on_click_remove_energy_bt, trap_tree, trap_tree.nb_energy_created))
            # add the button to the tree
            tree.setItemWidget(energy_trap, 1, remove_energy_bt)
            
        trap_tree.correspondence_index_position_energy.append(trap_tree.nb_energy_created)
        trap_tree.nb_energy_created += 1
        
    def on_click_remove_energy_bt(self, trap_tree, initial_index):
        """
            Remove a subnode (that display energy info) from a node
            (that display trap info).
        """
        index_to_delete = trap_tree.correspondence_index_position_energy.index(initial_index)
        trap_tree.correspondence_index_position_energy.pop(index_to_delete)
        trap_tree.removeChild(trap_tree.child(index_to_delete))

    def make_vbox_from_data_equation(self, list_data_equation):
        """
            Display equation in a widget.
        """
        equations_container = makeWidget.make_vbox()
        equations_container.setObjectName("equation")
        list_equation_already_written = []

        def fillVboxWithAnything(equations_container, name, coef1, coef2):
            """
                Create a QGroupBox, fill it with the informations contained in
                'name', 'coef1' and 'coef2'.
                Then, add this widget to equations_container.
            """
            equation_container = QGroupBox()
            unit1 = "(m²/s)"
            unit2 = ("(eV)", "(kJ/mol)")
            if name == "D":
                title = "For interstitial diffusivity D = D_0 * exp(-E_D/(Kb*T))"
                objectName = "diffusivity"
                coef1_name = "D_0"
                coef2_name = "E_D"
            elif name == "S":
                title = "For solubility S = S_0 * exp(-E_S/(Kb*T))"
                objectName = "solubility"
                coef1_name = "S_0"
                coef2_name = "E_S"
            elif name == "Kr":
                title = "For combination Kr = Kr_0 * exp(-E_r/(Kb*T))"  # todo: check translation
                objectName = "combination"
                coef1_name = "Kr_0"
                coef2_name = "E_r"
            equation_container.setTitle(title)
            equation_container.setObjectName(objectName)
            grid_data_coef = QGridLayout()
            grid_data_coef.addWidget(QLabel(coef1_name), 0, 0)
            grid_data_coef.addWidget(QLineEditWidthed(coef1, self.editable), 0, 1)
            grid_data_coef.addWidget(QLabel(unit1), 0, 2)
            if self.editable:
                checkbox = QCheckBox("Take it into account")
                checkbox.setChecked(True)
                grid_data_coef.addWidget(checkbox, 0, 4)
            grid_data_coef.addWidget(QLabel(coef2_name), 1, 0)
            grid_data_coef.addWidget(QLineEditWidthed(coef2, self.editable), 1, 1)
            grid_data_coef.addWidget(QLabel(unit2[0]), 1, 2)
            grid_data_coef.addWidget(QLineEditWidthed(coef2kJmol, self.editable), 1, 3)
            grid_data_coef.addWidget(QLabel(unit2[1]), 1, 4)
            equation_container.setLayout(grid_data_coef)
            equations_container.layout.addWidget(equation_container)

        for name, c1, c2 in list_data_equation:
            coef1 = "None" if c1[1] is None else "{:.2e}".format(float(c1[1]))
            coef2 = "None" if c2[1] is None else "{:.2e}".format(float(c2[1]))
            coef2kJmol = "None" if c2[1] is None else "{:.2e}".format(float(c2[1]/0.0104))
            equation_container = QGroupBox()
            if name == "D" or name == "S" or name == "Kr":
                fillVboxWithAnything(equations_container, name, coef1, coef2)
                list_equation_already_written.append(name)
            else:
                print("WARNING : I cant't show the equation named", name, "because it is not in ['D', 'S', 'Kr'].")
        # if this ShowNewFile is editable and if some informations is lacking,
        # we must display an empty section so that the user will be able to
        # fill it anyway
        # (if we don't, the section will be missing and the user won't be able
        # to add the lacking infos)
        if self.editable:
            for name in ("D", "S", "Kr"):
                if name not in list_equation_already_written:
                    print("WARNING:", name, "not found in the JSON. I'll add it myself.")
                    fillVboxWithAnything(equations_container, name, "None", "None")

        return equations_container



