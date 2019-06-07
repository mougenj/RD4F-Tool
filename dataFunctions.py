import json


def create_json_example():
    parameters = {}
    material = {
        "name" : "Carbone",
        "atomic_symbol" : "C",
        "atomic_number" : 6,
        "density" : 1.0,
        "net" : None,  # reseaux TODO : traduire
        "lattice_parameter" : 1,
        "melting_point" : 600,
        "adatome" : "hydrogene"
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
    parameters = {}
    material = {
        "name" : None,
        "atomic_symbol" : None,
        "atomic_number" : None,
        "density" : None,
        "net" : None,  # reseaux TODO : traduire
        "lattice_parameter" : None,
        "melting_point" : None,
        "adatome" : None
    }
    source = {
        "author_name" : None,
        "year" : None,
        "doi" : None
    }
    equations = {
        "D" : {
            "D_0" : None,
            "E_D" : None
        },
        "S" : {
            "S_0" : None,
            "E_S" : None
        },
        "Kr" : {
            "Kr_0" : None,
            "E_r" : None
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