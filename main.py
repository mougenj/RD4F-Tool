import os
import random as rd
import sqlite3
import sys

# the two import below is just an evil way to frorce cx_freeze to include these parts in the exe. Should br done in the setup.py, but I'm not sure how to do it.
import numpy.core._methods
import numpy.lib.format
from PyQt5.QtWidgets import QApplication

import App
import dataFunctions


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
# choisir l'emplacement des sauvegardes
# faire un paquet debian
# envoyer un mail pour la troisiemen partie
# lire le matlab founi par le client
# pouvoir ajouter des pieges dans l'interface
def main():
    dataFunctions.create_json_example()
    create_database()
    # print("création de l'interface")
    app = QApplication(sys.argv)
    #print("lancement de l'interface")
    ex = App.App()
    #print("sortie de l'interface")
    rc = app.exec_()
    #print("sortie prog")
    del app
    sys.exit(rc)


if __name__ == '__main__':
    main()