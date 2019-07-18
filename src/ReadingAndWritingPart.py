from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import (QTabWidget,
                             QGroupBox,
                             QTextEdit,
                             QGridLayout
                            )
from ShowNewFile import get_today_date




class ReadingAndWritingPart():
    def __init__(self):
        pass

    def correctTypes(self, data):
        def to_float_secure(x):
            try:
                floated = float(x)
                return floated
            except Exception as e:
                print("to_float_secure:", e)
                return None

        def to_int_secure(x):
            try:
                # here, I use int(float(x)) instead of int(x):
                # that's because int(float("2.5e2")) return 250
                # while int("2.5e2") raise a ValueError.
                inted = int(float(x))
                return inted
            except Exception as e:
                print(e)
                return None
        
        def to_sci_notation(x):
            try: 
                scied = "{:.2e}".format(to_float_secure(x))
                return scied
            except:
                return None


        for i in range(len(data["traps"])):
            try:
                data["traps"][i]["density"] = to_sci_notation(data["traps"][i]["density"])
            except KeyError as e:  # attrape le bouton d'ajout
                print(e)
            # data part
            data_trap_dict_list = data["traps"][i]["data"]
            data_trap_dict_list_corrected = []
            for dictionnary in data_trap_dict_list:
                dictionnary_corrected = {}
                dictionnary_corrected["energy"] = to_sci_notation(dictionnary["energy"])
                dictionnary_corrected["frequency"] = to_sci_notation(dictionnary["frequency"])
                data_trap_dict_list_corrected.append(dictionnary_corrected)
            data["traps"][i]["data"] = data_trap_dict_list_corrected

        for key in data["equation"]:
            for subkey in data["equation"][key]:
                if subkey != "comment":
                    data["equation"][key][subkey] = to_float_secure(data["equation"][key][subkey])
        
        data["source"]["year"] = to_int_secure(data["source"]["year"])
        data["source"]["last_edit"] = get_today_date()

        for key in ("melting_point", "lattice_parameter", "density"):
            data["material"][key] = to_float_secure(data["material"][key])

        #atomic number and adatom atomic number to float
        data["material"]["atomic_number"] = to_int_secure(data["material"].get("atomic_number", None))
        data["material"]["adatome_atomic_symbol"] = to_int_secure(data["material"].get("adatome_atomic_symbol", None))
        data["material"]["adatome_atomic_number"] = to_int_secure(data["material"].get("adatome_atomic_number", None))

        return data

    def getDataInFile(self, functionToCallToGetIndex):
        def searchForChild(parent, filtre):
            children = [x for x in parent.findChildren(QObject) if x.objectName() in filtre]
            return children

        index = functionToCallToGetIndex()
        data_to_save = {
            "material" :{},
            "source" :{},
            "traps" : [],
            "equation" : {},
            "traps-comment" : ""
        }

        tabs = searchForChild(self, ["tab_left"])[0]
        snf = tabs.widget(index)
        tabs_to_save = snf.findChild(QTabWidget)

        for tab_data_container in searchForChild(tabs_to_save, ["traps", "material", "source", "equation", "traps-comment"]):
            print(tab_data_container.objectName())
            if tab_data_container.objectName() == "equation":
                vbox = tab_data_container
                groupboxes = vbox.findChildren(QGroupBox)
                for groupbox in groupboxes:
                    grid_layout = groupbox.findChild(QGridLayout)
                    coef1 = grid_layout.itemAtPosition(1, 0).widget().text()
                    val1 = grid_layout.itemAtPosition(1, 1).widget().text()
                    coef2 = grid_layout.itemAtPosition(2, 0).widget().text()
                    val2 = grid_layout.itemAtPosition(2, 1).widget().text()

                    comment_content = groupbox.findChild(QTextEdit).toPlainText()
                    display_groupbox = True
                    if grid_layout.itemAtPosition(1, 4):
                        checkbox = grid_layout.itemAtPosition(1, 4).widget()
                        display_groupbox = checkbox.isChecked()

                    if display_groupbox:  # todo: ask if it is ok
                        if groupbox.objectName() == "diffusivity":
                            equation_type = "D"
                        elif groupbox.objectName() == "solubility":
                            equation_type = "S"
                        elif groupbox.objectName() == "combination":
                            equation_type = "Kr"
                        else:
                            print("WARNING : I don't know how to save the coefficient named", groupbox.objectName())
                        data_to_save["equation"][equation_type] = {}
                        data_to_save["equation"][equation_type][coef1] = val1
                        data_to_save["equation"][equation_type][coef2] = val2
                        data_to_save["equation"][equation_type]["comment"] = comment_content
            elif tab_data_container.objectName() == "traps":

                for i in range(tab_data_container.topLevelItemCount()):
                    trap_tree = tab_data_container.topLevelItem(i)
                    dictionnary_of_this_trap = {
                        "density" : tab_data_container.itemWidget(trap_tree, 0).text(),
                        "data": []
                    }
                    for j in range(trap_tree.childCount()):
                        energy_tree = trap_tree.child(j)
                        energy = tab_data_container.itemWidget(energy_tree, 2)
                        frequence = tab_data_container.itemWidget(energy_tree, 4)
                        if energy:
                            energy = energy.text()
                        else:
                            energy = None
                        if frequence:
                            frequence = frequence.text()
                        else:
                            frequence = None
                        dictionnary_of_this_trap["data"].append({"energy":energy, "frequency":frequence})

                    if not dictionnary_of_this_trap == {}:
                        data_to_save["traps"].append(dictionnary_of_this_trap)
            
            elif tab_data_container.objectName() == "traps-comment":
                data_to_save["traps-comment"] = tab_data_container.toPlainText()
            elif tab_data_container.objectName() == "material":
                vbox = tab_data_container 
                for groupbox in searchForChild(vbox, ["gb_material"]):
                    for row in range(groupbox.layout.rowCount()):
                        label = groupbox.layout.itemAtPosition(row, 0).widget().text()
                        value = groupbox.layout.itemAtPosition(row, 2).widget().text()
                        data_to_save["material"][label] = value
                for groupbox in searchForChild(vbox, ["gb_adatome"]):
                    for row in range(groupbox.layout.rowCount()):
                        label = groupbox.layout.itemAtPosition(row, 0).widget().text()
                        value = groupbox.layout.itemAtPosition(row, 1).widget().text()
                        data_to_save["material"][label] = value
                        
            elif tab_data_container.objectName() == "source":
                grid = tab_data_container
                for row in range(grid.layout.rowCount()):
                    label = grid.layout.itemAtPosition(row, 0).widget().text()
                    value = grid.layout.itemAtPosition(row, 1).widget().text()
                    data_to_save["source"][label] = value

            else:
                print("WARNING: I don't know how to save the grid named", grid.objectName())

        data_to_save = self.correctTypes(data_to_save)
        return data_to_save