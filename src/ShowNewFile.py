import DragAndDrop
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout,
                             QGroupBox,
                             QGridLayout,
                             QLabel,
                             QHBoxLayout,
                             QScrollArea,
                             QScroller,
                             QPushButton,
                             QApplication,
                             QTabWidget,
                             QTreeWidget,
                             QTreeWidgetItem,
                             QHeaderView,
                             QCheckBox,
                             QTextEdit)
from QLineEditWidthed import QLineEditWidthed
from PyQt5.QtGui import QColor, QFont, QIcon
import pdb
from PyQt5.QtCore import Qt
import rlcompleter
from functools import partial
import makeWidget
from datetime import datetime

import sys
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PyQt5 import QtGui, QtCore
# Use LaTEX font
try:
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
except:
    print('No latex installation found')
    pass


def mathTex_to_QPixmap(mathTex, fs):
    '''
    Convert matplotlib figure to QPixmap object
    Args:
    - mathTex : str, mathematical expression
    - fs : int, font size
    Returns QPixmap object's label.
    '''
    # ---- set up a mpl figure instance ----

    fig = plt.Figure()
    fig.patch.set_facecolor('none')
    fig.set_canvas(FigureCanvasAgg(fig))
    renderer = fig.canvas.get_renderer()

    # ---- plot the mathTex expression ----

    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.patch.set_facecolor('none')
    t = ax.text(0, 0, mathTex, ha='left', va='bottom', fontsize=fs)

    # ---- fit figure size to text artist ----

    fwidth, fheight = fig.get_size_inches()
    fig_bbox = fig.get_window_extent(renderer)

    text_bbox = t.get_window_extent(renderer)

    tight_fwidth = text_bbox.width * fwidth / fig_bbox.width
    tight_fheight = text_bbox.height * fheight / fig_bbox.height + 0.1

    fig.set_size_inches(tight_fwidth, tight_fheight)
    # ---- convert mpl figure to QPixmap ----

    buf, size = fig.canvas.print_to_buffer()
    qimage = QtGui.QImage.rgbSwapped(QtGui.QImage(buf, size[0], size[1],
                                                  QtGui.QImage.Format_ARGB32))
    qpixmap = QtGui.QPixmap(qimage)

    label = QLabel()
    label.setObjectName('label')
    label.setPixmap(qpixmap)

    return label


def get_today_date():
    year = str(datetime.today().year)
    month = str(datetime.today().month)
    day = str(datetime.today().day)
    hour = str(datetime.today().hour)
    minute = str(datetime.today().minute)
    second = str(datetime.today().second)

    add_0 = lambda s: "0" + s if len(s) == 1 else s
    today = year + "-" + add_0(month) + "-" + add_0(day)
    today += " " + add_0(hour) + ":" + add_0(minute) + ":" + add_0(second)

    return today


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
        print(parameters)
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
        for key in parameters["equation"]:
            if key == "D":
                first_coef_type = "D_0"
                second_coef_type = "E_D"
            elif key == "S":
                first_coef_type = "S_0"
                second_coef_type = "E_S"
            elif key == "Kr":
                first_coef_type = "Kr_0"
                second_coef_type = "E_r"
            

            sorted_coefficients = []
            sorted_coefficients.append(key)
            sorted_coefficients.append((first_coef_type, parameters["equation"][key][first_coef_type]))
            sorted_coefficients.append((second_coef_type, parameters["equation"][key][second_coef_type]))
            comment = parameters["equation"][key].get("comment", "")
            sorted_coefficients.append(("comment", comment))
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
        for key in ["adatome", "adatome_atomic_number", "adatome_atomic_symbol"]:
            value = ""
            try:
                value = str(parameters["material"][key])
            except KeyError:
                print("There is no key named", key, "in the file loaded, thus it is not possible to diplay this information.")
                if self.editable:
                    value = "None"
            if value:
                line = QLineEditWidthed(value, editable, "--------------")
                grid_adatome.addWidget(QLabel(key), adatome_counter, 0)
                grid_adatome.addWidget(line, adatome_counter, 1);
                adatome_counter += 1

        
        material_counter = 0
                # "name" : None,
        # "atomic_symbol" : None,
        # "lattice_type" : None,
        # "melting_point" : None,
        # "atomic_number" : None,
        # "mean_lattice_constant" : None,
        # "density" : None,

        # "adatome" : None,
        # "adatome_atomic_number" : None,
        # "adatome_atomic_symbol" : None

        keys = ("name", "atomic_symbol", "lattice_type", "melting_point", "atomic_number", "mean_lattice_constant", "density")
        units = ("", "", "", "K", "", "m", "atoms/m³")
        for key, unit in zip(keys, units):
            value = ""
            try:
                value = str(parameters["material"][key])
            except KeyError:
                print("There is no key named", key, "in the file loaded, thus it is not possible to diplay this information.")
                if self.editable:
                    value = "None"
            if value:
                line = QLineEditWidthed(value, editable, "--------------")
                grid_material.addWidget(QLabel(key), material_counter, 0)
                grid_material.addWidget(QLabel("     "), material_counter, 1)  # todo: find a better way to align Qlabels inside the grid
                grid_material.addWidget(line, material_counter, 2)

                if unit:
                    grid_material.addWidget(QLabel("("+unit+")"), material_counter, 3)
                    if key == "density":
                        eq_density = makeWidget.make_pixmap("ressources/latex_equation_density_resized.png")
                        grid_material.addWidget(eq_density, material_counter, 4)
                    else:
                        grid_material.addWidget(QLabel(""), material_counter, 4)
                material_counter += 1

        tabs.addTab(makeWidget.make_scroll(material_container), "Material")

        gridSource = QWidget()
        gridSource.layout = QGridLayout()
        gridSource.setLayout(gridSource.layout)
        gridSource.setObjectName("source")
        i = 0

        self.list_data_source = parameters["source"]
        # last edit
        prop = "last_edit"
        gridSource.layout.addWidget(QLabel(prop), i, 0)
        value = parameters["source"].get("last_edit", get_today_date())
        gridSource.layout.addWidget(QLineEditWidthed(value, False, "2019-07-01 10:56:89"), i, 1)
        i += 1

        # author_name
        prop = "author_name"
        gridSource.layout.addWidget(QLabel(prop), i, 0)
        value = parameters["source"][prop]
        if value is None:
            value = "None"
        elif type(value) is not str:
            value = "{:.2e}".format(float(value))
        gridSource.layout.addWidget(QLineEditWidthed(value, editable, "-------------------------------"), i, 1)
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
                    """
                        "decorator of a decorator" that allow the decorator
                        to accept an argument. If the decorated function didn't
                        finish before 'timeout' seconds, then a
                        TimeoutException is raised.
                    """
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
                    return decorate

                @deadline(3)
                def request_doi_api():
                    works = Works()
                    address = parameters["source"][prop]
                    data = works.doi(address)
                    if data:
                        value = data["URL"]
                        to_insert = QLabel("<html><a href=\"" + value + "\">" + value + "</a></html>")
                    else:
                        to_insert = None
                    return to_insert
                
                try:
                    # to_insert = request_doi_api()
                    if to_insert:
                        doi_api_success = True
                except TimeoutException:
                    print("time out")
            except Exception as e:
                print(e)
        if not doi_api_success:
            value = parameters["source"][prop]
            if value is None:
                value = "None"
            elif type(value) is not str:
                value = "{:.2e}".format(float(value))
            to_insert = QLineEditWidthed(value, editable, "https://doi.org/10.1016/j.nme.2018.11.020-------------")
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
        gridSource.layout.addWidget(QLineEditWidthed(value, editable, "------"), i, 1)
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
                "",
                "energy",
                "",
                "frequence",
                "",
                "Delete this trap",
                "Add data to this trap"
            ])
        else:
            tree.setColumnCount(2)
            tree.setHeaderLabels([
                "Density",
                "",
                "energy",
                "",
                "frequence",
                ""
            ])
        tree.header().resizeSection(0, 120)
        tree.header().resizeSection(1, 50)
        tree.header().resizeSection(2, 100)
        tree.header().resizeSection(3, 35)
        tree.header().resizeSection(4, 100)
        tree.header().resizeSection(5, 35)

        tree.header().resizeSection(6, 115)
        tree.header().resizeSection(7, 145)
        tree.header().setStretchLastSection(False)
        tree.setObjectName("traps")
        
        for trap in parameters["traps"]:
            tree_item_for_this_trap = self.create_subtree_for_a_trap(tree, trap)
            for data in trap["data"]:
                self.addEnergyToATrap(tree, tree_item_for_this_trap, data)
        vbox = makeWidget.make_vbox()
        vbox.layout.addWidget(tree)

        if self.editable:
            bt_add_new_trap = QPushButton("Add a trap")
            vbox.layout.addWidget(bt_add_new_trap)
            empty_trap = {"density":None, "angular_frequency":None, "energy":[]}
            bt_add_new_trap.clicked.connect(partial(self.create_subtree_for_a_trap, tree, empty_trap))
        comment = parameters.get("traps-comment", "")
        textedit = QTextEdit(comment)
        textedit.setReadOnly(not self.editable)
        textedit.setObjectName("traps-comment")
        tabs.addTab(makeWidget.make_vbox(vbox, textedit), "Traps")
        
        layout = QVBoxLayout()  # contient les tabs
        layout.addWidget(tabs)
        self.setLayout(layout)
        self.tabs = tabs
    
    def create_subtree_for_a_trap(self, tree, trap):  # todo: done
        """
            Create a node that display informations about a trap. Can have
            subnodes that diplay infos about some (energy, frequency
            of this trap.
        """
        # add it to the list, so it can be deleted later
        self.correspondence_index_position.append(self.nb_created)
        tree_item_for_this_trap = QTreeWidgetItem(tree)

        # get informations from the JSON file

        if trap.get("density") is not None:
            density = "{:.2e}".format(float(trap["density"]))
        else:
            density = "None"
        density_line = QLineEditWidthed(density, self.editable, "--------------")
        tree.setItemWidget(tree_item_for_this_trap, 0, density_line)
        tree.setItemWidget(tree_item_for_this_trap, 1, QLabel("at. fr."))

        """
        if trap.get("angular_frequency") is not None:
            angular_frequency = "{:.2e}".format(float(trap["angular_frequency"]))
        else:
            angular_frequency = "None"
        angular_frequency_line = QLineEditWidthed(angular_frequency, self.editable, "--------------")
        tree.setItemWidget(tree_item_for_this_trap, 1, angular_frequency_line)
        """

        # create a list that store the ids of its subnodes. see a comment in
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
            tree.setItemWidget(tree_item_for_this_trap, 6, remove_bt)
            # lets create a button that add energy to this trap
            add_energy_bt = QPushButton()
            add_energy_bt.setIcon(QIcon("ressources/plus-circle-solid.svg"))
            add_energy_bt.setMaximumSize(50, 50)
            add_energy_bt.clicked.connect(partial(self.addEnergyToATrap, tree, tree_item_for_this_trap, {}))
            # add the button to the tree
            tree.setItemWidget(tree_item_for_this_trap, 7, add_energy_bt)
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


    @pyqtSlot()
    def addEnergyToATrap(self, tree, trap_tree, value):  # todo rename
        """
            Add a subnode to this node that can be filled by the user to
            display informations about energy of this trap.
        """
        energy_trap = QTreeWidgetItem(trap_tree)
        energy = value.get("energy", 0)
        frequence = value.get("frequency", 0)
        tree.setItemWidget(energy_trap, 2, QLineEditWidthed("{:.2e}".format(float(energy)), self.editable, "--------------"))
        tree.setItemWidget(energy_trap, 3, QLabel("eV"))
        tree.setItemWidget(energy_trap, 4, QLineEditWidthed("{:.2e}".format(float(frequence)), self.editable, "--------------"))
        tree.setItemWidget(energy_trap, 5, QLabel("Hz"))
        if self.editable:
            # create a button that remove this subnode
            remove_energy_bt = QPushButton("delete line")
            remove_energy_bt.setIcon(QIcon("ressources/trash-alt-solid.svg"))
            # remove_energy_bt.setMinimumSize(120, 0);
            # remove_energy_bt.setMaximumSize(120, 28);
            remove_energy_bt.clicked.connect(partial(self.on_click_remove_energy_bt, trap_tree, trap_tree.nb_energy_created))
            # add the button to the tree
            tree.setItemWidget(energy_trap, 6, remove_energy_bt)
            
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

        def fillVboxWithAnything(equations_container, name, coef1, coef2, comment_content, is_in_the_file=True):
            """
                Create a QGroupBox, fill it with the informations contained in
                'name', 'coef1' and 'coef2'.
                Then, add this widget to equations_container.
            """
            coef2kJmol = "None" if coef2 == "None" else "{:.2e}".format(float(coef2)/0.0104)
            equation_container = QGroupBox()
            unit2 = ("(eV)", "(kJ/mol)")
            if name == "D":
                unit1 = "(m²/s)"
                # latex_equation = makeWidget.make_pixmap("ressources/latex_equation_diffusivity_resized.png")
                latex_equation_text = \
                    r"$D = D_0 \cdot e^{-\frac{E_D}{k_B \cdot T}}$"
                latex_equation = mathTex_to_QPixmap(latex_equation_text, 16)
                title = "For interstitial diffusivity"
                objectName = "diffusivity"
                coef1_name = "D_0"
                coef2_name = "E_D"
            elif name == "S":
                unit1 = "(adatome/(m³*Pa½))"  # todo: update it (like JS)
                # latex_equation = makeWidget.make_pixmap("ressources/latex_equation_solubility_resized.png")
                latex_equation_text = \
                    r"$S = S_0 \cdot e^{-\frac{E_S}{k_B \cdot T}}$"
                latex_equation = mathTex_to_QPixmap(latex_equation_text, 16)
                title = "For solubility"
                objectName = "solubility"
                coef1_name = "S_0"
                coef2_name = "E_S"
            elif name == "Kr":
                unit1 = "(m⁴/s)"
                # latex_equation = makeWidget.make_pixmap("ressources/latex_equation_combination_resized.png")
                latex_equation_text = \
                    r"$K_r = K_{r_0} \cdot e^{-\frac{E_r}{k_B \cdot T}}$"
                latex_equation = mathTex_to_QPixmap(latex_equation_text, 16)
                title = "For combination"  # todo: check translation
                objectName = "combination"
                coef1_name = "Kr_0"
                coef2_name = "E_r"
            equation_container.setTitle(title)
            equation_container.setObjectName(objectName)

            grid_data_coef = QWidget()
            grid_data_coef.layout = QGridLayout()
            grid_data_coef.setLayout(grid_data_coef.layout)

            grid_data_coef.layout.addWidget(latex_equation, 0, 0)
            grid_data_coef.layout.addWidget(QLabel(coef1_name), 1, 0)
            grid_data_coef.layout.addWidget(QLineEditWidthed(coef1, self.editable, "--------------"), 1, 1)
            grid_data_coef.layout.addWidget(QLabel(unit1), 1, 2)
            if self.editable:
                checkbox = QCheckBox("Take it into account")
                checkbox.setChecked(is_in_the_file)
                grid_data_coef.layout.addWidget(checkbox, 1, 4)
            grid_data_coef.layout.addWidget(QLabel(coef2_name), 2, 0)

            # eV
            coef2_line = QLineEditWidthed(coef2, self.editable, "--------------")
            grid_data_coef.layout.addWidget(coef2_line, 2, 1)
            grid_data_coef.layout.addWidget(QLabel(unit2[0]), 2, 2)

            # kJ/mol
            coef2kJmol_line = QLineEditWidthed(coef2kJmol, self.editable, "--------------")
            grid_data_coef.layout.addWidget(coef2kJmol_line, 2, 3)
            grid_data_coef.layout.addWidget(QLabel(unit2[1]), 2, 4)

            # automatic update
            coef2_line.setAutoUpdate(coef2kJmol_line, 1/0.0104)
            coef2kJmol_line.setAutoUpdate(coef2_line, 0.0104)

            textedit = QTextEdit(comment_content)
            textedit.setReadOnly(not self.editable)
            vbox = makeWidget.make_vbox(grid_data_coef, textedit)
            equation_container.setLayout(vbox.layout)
            equations_container.layout.addWidget(equation_container)

        for name, c1, c2, comment in list_data_equation:
            coef1 = "None" if c1[1] is None else "{:.2e}".format(float(c1[1]))
            coef2 = "None" if c2[1] is None else "{:.2e}".format(float(c2[1]))
            comment_content = comment[1]
            equation_container = QGroupBox()
            if name == "D" or name == "S" or name == "Kr":
                fillVboxWithAnything(equations_container, name, coef1, coef2, comment_content)
                list_equation_already_written.append(name)
            else:
                print("WARNING : I can't show the equation named", name, "because it is not in ['D', 'S', 'Kr'].")
        # if this ShowNewFile is editable and if some informations is lacking,
        # we must display an empty section so that the user will be able to
        # fill it anyway
        # (if we don't, the section will be missing and the user won't be able
        # to add the lacking infos)
        if self.editable:
            for name in ("D", "S", "Kr"):
                if name not in list_equation_already_written:
                    print("WARNING:", name, "not found in the JSON. I'll add it myself.")
                    fillVboxWithAnything(equations_container, name, "None", "None", "", is_in_the_file=False)

        return equations_container
