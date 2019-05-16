import App
from PyQt5.QtWidgets import QApplication
import random as rd
import json
import sip
import sqlite3
import sys
sip.setdestroyonexit(True)


def create_json_example():
    data = []
    # ajout de données "sensées"
    data.append(["D", [1, 6]])
    data.append(["S", [1, 6]])
    alphabet_latin = [chr(x) for x in range(ord('a'), ord('z') + 1)]
    # ecriture de 5 nom au hasard de 9 caractere de long
    liste_nom_equation = []
    for _ in range(5):
        nom = "".join([rd.choice(alphabet_latin) for _ in range(9)])
        liste_nom_equation.append(nom)
    for nom in liste_nom_equation:
        data.append((nom, [rd.randint(0, 50) for _ in range(rd.randint(1, 5))]))
    chaine = json.dumps(data, indent=4)
    with open("ressources/json.txt", "w") as fichier:
        fichier.write(chaine)

def create_database():
    if not os.path.isfile('database.sqlite'):
        db = sqlite3.connect("test.sqlite")
        cursor = db.cursor()
        cursor.execute("CREATE TABLE MATERIAUX ([id] INTEGER PRIMARY KEY, [nom] text, [flux_hydrogene] text, [retrodif] number, [energie_ions] number, [num_atom_proj] integer, [masse_atomique] integer)")
        cursor.execute("INSERT INTO TEST VALUES (3, 'blibli')")
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

# ajouter un champs de recherche des valeurs sur le graphes en fonction de l'abscisse (qu'en est-il de s'il y a plusieurs courbes?)
# pouvoir ouvrir la fenetre plt (rend caduque le point au dessus)
# ne plus pouvoir modifer les box dans l'onglet lecture
if __name__ == '__main__':
    create_json_example()
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
