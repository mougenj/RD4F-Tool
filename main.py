import os
import random as rd
import sqlite3
import sys
from PyQt5.QtWidgets import QApplication
import signal

# the two import below is just an evil way to force cx_freeze to include these parts in the exe. Should be done in the setup.py, but I'm not sure how to do it.
import numpy.core._methods  # todo: check if it is safe to remove them
import numpy.lib.format

import App
import dataFunctions


# import pdb; import rlcompleter; pdb.Pdb.complete=rlcompleter.Completer(locals()).complete; pdb.set_trace()

def create_database():
    dbname = 'database.sqlite'
    # remove the database if it already exists
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
            "[melting_point] number,"
            "[difusion_coefficient] number,"
            "[noccupied_site] number,"
            "[diffusion_energy], number,"
            "[traps_energy] number,"
            "[frequence_attaque] number,"  # todo: traduire
            "[distance_interdtitielle] number"  # todo: traduire
            ")"
        )
        db.commit()
        cursor.execute(
            "INSERT INTO MATERIAL"
            "(id, name, lattice_parameter, density, net, atomic_number, melting_point)"
            "VALUES"
            "(1, \"Carbone\", 0.3, 0.5, \"CFC\", 6,  3553.85);")
        db.commit()
        cursor.execute(
            "INSERT INTO MATERIAL"
            "(id, name, lattice_parameter, density, net, atomic_number, melting_point)"
            "VALUES"
            "(2, \"Acier\", 0.3, 0.5, \"changeme\", 6,  3553.85);")
        db.commit()
        cursor.execute(
            "INSERT INTO MATERIAL"
            "(id, name, lattice_parameter, density, net, atomic_number, melting_point)"
            "VALUES"
            "(3, \"AAA\", 0.3, 0.5, \"AAA\", 6,  3553.85);")
        db.commit()
        cursor.execute(
            "INSERT INTO MATERIAL"
            "(id, name, lattice_parameter, density, net, atomic_number, melting_point)"
            "VALUES"
            "(4, \"Carbone\", 0.3, 0.5, \"CFC\", 6,  3553.85);")
        db.commit()
        cursor.execute(
            "INSERT INTO MATERIAL"
            "(id, name, lattice_parameter, density, net, atomic_number, melting_point)"
            "VALUES"
            "(5, \"Carbone\", 0.3, 0.5, \"CFC\", 6,  3553.85);")
        db.commit()
        cursor.execute(
            "INSERT INTO MATERIAL"
            "(id, name, lattice_parameter, density, net, atomic_number, melting_point)"
            "VALUES"
            "(6, \"Carbone\", 0.3, 0.5, \"CFC\", 6,  3553.85);")
        db.commit()
        cursor.execute(
            "INSERT INTO MATERIAL"
            "(id, name, lattice_parameter, density, net, atomic_number, melting_point)"
            "VALUES"
            "(7, \"Carbone\", 0.3, 0.5, \"CFC\", 6,  3553.85);")
        db.commit()

        cursor.execute("SELECT * FROM MATERIAL")

        """
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        """

        db.close()

# todo:
# troisieme partie
# lire le matlab founi par le client
# export des valeur brutes

# optionel:
# afficher le doi même si on a pas de reponse de l'api et l'afficher par la suite
# faire un paquet debian
# "resserrer" les champs du premier onglet
# ecrire l'aide (ecriture)
def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
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