import json


def create_json_example():
    """
        Create a fake JSON file, usefull for test.
    """
    parameters = {}
    material = {
        "name" : "Carbone",
        "atomic_symbol" : "C",
        "atomic_number" : 6,
        "density" : 1.0,
        "net" : None,  # reseaux TODO : traduire
        "lattice_parameter" : 1,
        "melting_point" : 600,
        "adatome" : "hydrogene",
        "adatome_atomic_number" : 1,
        "adatome_atomic_symbol" : "H"
    }
    source = {
        "author_name" : "Touchard",
        "year" : 2012,
        "doi" : "45454"
    }
    equations = {
        "D" : {
            "D_0" : 6e-4,
            "E_D" : 1.04,
            "comment" : "Add a comment"
        },
        "S" : {
            "S_0" : 1.0,
            "E_S" : 6545,
            "comment" : "Add a comment"
        },
        "Kr" : {
            "Kr_0" : 1.0,
            "E_r" : 6545,
            "comment" : "Add a comment"
        }
    }
    traps = [
        {
            "density" : 5,
            "angular_frequency" : 8,
            "energy" : [454, 48, 98]
        }
        for _ in range(1)
    ]
    parameters["material"] = material
    parameters["source"] = source
    parameters["equation"] = equations
    parameters["traps"] = traps
    chaine = json.dumps(parameters, indent=4)
    with open("json.txt", "w") as fichier:
        fichier.write(chaine)

def create_empty_data():
    """
        Create an empty JSON file, usefull for creating a partial JSON file, as
        every key is already in this file.
    """
    parameters = {}
    material = {
        "name" : None,
        "atomic_symbol" : None,
        "atomic_number" : None,
        "density" : None,
        "net" : None,  # reseaux TODO : traduire
        "lattice_parameter" : None,
        "melting_point" : None,
        "adatome" : None,
        "adatome_atomic_number" : None,
        "adatome_atomic_symbol" : None
    }
    source = {
        "author_name" : None,
        "year" : None,
        "doi" : None
    }
    equations = {
        "D" : {
            "D_0" : None,
            "E_D" : None,
            "comment" : ""
        },
        "S" : {
            "S_0" : None,
            "E_S" : None,
            "comment" : ""
        },
        "Kr" : {
            "Kr_0" : None,
            "E_r" : None,
            "comment" : ""
        }
    }
    traps = [
        {
            "density" : None,
            "angular_frequency" : None,
            "energy" : []
        }
        for _ in range(1)
    ]
    parameters["material"] = material
    parameters["source"] = source
    parameters["equation"] = equations
    parameters["traps"] = traps
    return parameters