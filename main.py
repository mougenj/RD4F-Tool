import App
from PyQt5.QtWidgets import QApplication
import random as rd
import json
import sip
import sqlite3
import sys
sip.setdestroyonexit(True)


def create_json_example():
    parameters = {}
    material = {
        "name" : "C",
        "atomic_number" : 6,
        "density" : 1.0,
        "net" : None,  # reseaux TODO : traduire
        "lattice_parameter" : 1,
        "melting_point" : 600
    }
    source = {
        "author_name" : "Touchard",
        "year" : 2012,
        "doi" : "45454"
    }
    equation = {
        "D" : {
            "D_0" : 1.0,
            "E_D" : 6545
        },
        "S" : {
            "S_0" : 1.0,
            "E_S" : 6545
        },
        "Kr" : {
            "Kr_0" : 1.0,
            "E_r" : 6545
        }
    }
    traps = [
        {
            "density" : 5,
            "angular_frequency" : 8,
            "energy" : 454
        }
        for _ in range(10)
    ]
    parameters["material"] = material
    parameters["source"] = source
    parameters["equation"] = equation
    parameters["traps"] = traps
    chaine = json.dumps(parameters, indent=4)
    with open("ressources/json.txt", "w") as fichier:
        fichier.write(chaine)

def create_database():
    if not os.path.isfile('database.sqlite'):
        db = sqlite3.connect("test.sqlite")
        cursor = db.cursor()
        cursor.execute("CREATE TABLE MATERIAUX ([id] INTEGER PRIMARY KEY, [nom] text, [flux_hydrogene] text, [retrodif] number, [energie_ions] number, [num_atom_proj] integer, [masse_atomique] integer)")
        #cursor.execute("INSERT INTO TEST VALUES (3, 'blibli')")
        cursor.execute("SELECT * FROM TEST")

        db.commit()


        rows = cursor.fetchall()
        for row in rows:
            print(row)

        db.close()

# todo:
# AVEC LE CLIENT:
# revoir le json et y ajouter des paramètres
# faire une BDD
# lire le matlab founi par le client

# ne plus pouvoir modifer les box dans l'onglet lecture
if __name__ == '__main__':
    # create_json_example()
    #print("création de l'interface")
    #print(sys.argv)
    app = QApplication(sys.argv)
    #print("lancement de l'interface")
    ex = App.App()
    #print("sortie de l'interface")
    rc = app.exec_()
    #print("sortie prog")
    del app
    sys.exit(rc)