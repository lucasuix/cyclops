
# Regras para a TCU
{
    "serialnumber": {},
    "target": {"min": -58, "max": 58}, # Quais targets a TCU pode mandar
    "last-seen": {"type": "datetime", "recent": 5}, # Quantos minutos atrás a TCU tem que ter mandado o último UPLINK
    "last-angle": {"tolerance": 0.5}, # Tolerância de 2° grus fora do target
}

# Filtro -> Procura por número de série
"0225030209898" : {
    "type_join": "u+",
    "rules": {
        "target": {"type": "float", "min": -53, "max": 53}
    }
}

{
    "serialnumber": {
        "0225030209898": {
            "type_join": "u+",
            "target": {"type": "float", "min": -53, "max": 53}
        },
        "0225030209595": {
            "type_join": "u+",
            "target": {"type": "float", "min": -52, "max": 52}
        }
    },

    "timestamp": {
        "night": {
            "type_join": "u+",
            "target": {"type": "float", "min": -25, "max": 25}
        }
    }
}