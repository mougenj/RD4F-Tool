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
        print('gogogo')
        db = sqlite3.connect(dbname)
        cursor = db.cursor()
        cursor.execute(
            "CREATE TABLE MATERIAL ("
            "[id] INTEGER PRIMARY KEY,"
            "[name] text NOT NULL,"
            "[atomic_symbol] text,"
            "[lattice_type] text,"
            "[melting_point] number,"
            "[atomic_number] INTEGER,"
            "[mean_lattice_constant] number,"
            "[density] number"
            ")"
        )
        #     "[difusion_coefficient] number,"
        #     "[noccupied_site] number,"
        #     "[diffusion_energy], number,"
        #     "[traps_energy] number,"
        #     "[frequence_attaque] number,"  # todo: traduire
        #     "[distance_interdtitielle] number"  # todo: traduire
            
        # )
        db.commit()
        # cursor.execute(
        #     "INSERT INTO MATERIAL"
        #     "(id, name, lattice_parameter, density, net, atomic_number, melting_point)"
        #     "VALUES"
        #     "(1, \"Carbone\", 0.3, 0.5, \"CFC\", 6,  3553.85);")
        # db.commit()
        # cursor.execute(
        #     "INSERT INTO MATERIAL"
        #     "(id, name, lattice_parameter, density, net, atomic_number, melting_point)"
        #     "VALUES"
        #     "(2, \"Acier\", 0.3, 0.5, \"changeme\", 6,  3553.85);")
        # db.commit()


        def insert(id, name, atomic_symbol, lattice_type, melting_point, atomic_number, mean_lattice_constant, density):
            id = str(id)
            mean_lattice_constant = str(mean_lattice_constant)
            density = str(density)
            requete = ("INSERT INTO MATERIAL"
                "(id, name, atomic_symbol, lattice_type, melting_point, atomic_number, mean_lattice_constant, density)"
                "VALUES"
                "({0}, \"{1}\", \"{2}\", \"{3}\", {4}, {5}, {6}, {7});").format(id, name, atomic_symbol, lattice_type, melting_point, atomic_number, mean_lattice_constant, density)
            cursor.execute(requete)
            db.commit()
        
        insert(1, "Tungsten",  "W",  "cc",  3695, 74, 3.156*10**-10, 6.322*10**28)
        insert(2, "Aluminium", "Al", "cfc", 933,  13, 4.06*10**-10,  6.026*10**28)
        insert(3, "Beryllium", "Be", "hcp", 1590, 4,  2.72*10**-10,  1.235*10**29)
        insert(4, "Carbon",    "C",  "hcp", 3823, 6,  3.88*10**-10,  1.133*10**29)
        insert(5, "Cupper",    "Cu", "cfc", 1358, 29, 3.615*10**-10, 8.491*10**28)
        cursor.execute("SELECT * FROM MATERIAL")

        """
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        """

        db.close()

# todo:
# export des valeur brutes
# changer taille comment trap
# decouper en classes
# drag and drop post traitement
# tout passer en anglis (nom du post traitement)
# voir pour le DOI

# optionel:
# afficher le doi même si on a pas de reponse de l'api et l'afficher par la suite
# faire un paquet debian
# "resserrer" les champs du premier onglet
# ecrire l'aide (ecriture)
def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
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