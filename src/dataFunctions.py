import json

def create_empty_data():
    """
        Create an empty JSON file, usefull for creating a partial JSON file, as
        every key is already in this file.
    """
    parameters = {}
    material = {
        "name" : None,
        "atomic_symbol" : None,
        "lattice_type" : None,
        "melting_point" : None,
        "atomic_number" : None,
        "mean_lattice_constant" : None,
        "density" : None,
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
            "data" : []
        }
        for _ in range(1)
    ]
    parameters["material"] = material
    parameters["source"] = source
    parameters["equation"] = equations
    parameters["traps"] = traps
    return parameters