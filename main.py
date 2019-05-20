import App
from PyQt5.QtWidgets import QApplication
import random as rd
import json
import sip
import sqlite3
import os
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
    equations = {
        "D" : {
            "D_0" : 6e-4,
            "E_D" : 1.04
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
    parameters["equation"] = equations
    parameters["traps"] = traps
    chaine = json.dumps(parameters, indent=4)
    with open("ressources/json.txt", "w") as fichier:
        fichier.write(chaine)

def create_database():
    dbname = 'database.sqlite'
    if os.path.isfile(dbname):
        os.remove(dbname)
    if not os.path.isfile(dbname):
        db = sqlite3.connect(dbname)
        cursor = db.cursor()
        cursor.execute(
            "CREATE TABLE MATERIAL ("
            "[id] INTEGER PRIMARY KEY,"
            "[name] text NOT NULL,"
            "[lattice_parameter] number,"
            "[density] number,"
            "[net] text,"
            "[atomic_number] INTEGER,"
            "[melting_point] number)"
        )
        """
        cursor.execute(
            "CREATE TABLE SOURCE ("
            "[doi] text PRIMARY KEY,"
            "[year] text,"
            "[author_name] number)"
        )
        cursot.execute(
            "CREATE TABLE EQUATION"
            "[id] INTEGER PRIMARY KEY,"
            "[type] text,"
            "[coef1] number,"
            "[coef2] number,"
            "CHECK(type IN ('Kr', 'D', 'S'))"

        )
        """
        cursor.execute(
            "INSERT INTO MATERIAL"
            "(id, name, lattice_parameter, density, net, atomic_number, melting_point)"
            "VALUES"
            "(1, \"Carbone\", 0.3, 0.5, \"CFC\", 6,  3553.85);")
        db.commit()

        cursor.execute("SELECT * FROM MATERIAL")


        rows = cursor.fetchall()
        for row in rows:
            print(row)

        db.close()

# todo:
# "resserrer" les champs du premier onglet
# faire une BDD
# lire le matlab founi par le client

if __name__ == '__main__':
    create_json_example()
    print("création de l'interface")
    app = QApplication(sys.argv)
    #print("lancement de l'interface")
    ex = App.App()
    #print("sortie de l'interface")
    rc = app.exec_()
    #print("sortie prog")
    del app
    sys.exit(rc)
