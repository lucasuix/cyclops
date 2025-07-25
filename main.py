from validator import Cyclops
import os, json
from datetime import datetime, timedelta

def evaluate(reference, target):
    """
    Verifica o target com a referência
    """
    v = Cyclops(reference)
    v.docs = target
    return (v.validate(target), v.errors)

file_path = f"{os.getcwd()}\\Modelagem\\rules.json"

# Buscar o arquivo de rules no banco de dados
with open(file_path, "r") as file:
    schemas = json.load(file)

# O que cada TCU retorna
payload = {
    "serialnumber": "0225030209999",
    "target": 55,
    "last-seen": datetime.now(),
    "last-angle": 54.8
}


print(evaluate(schemas, payload))