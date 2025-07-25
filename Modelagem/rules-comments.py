
# Regras para a TCU
{
    "serialnumber": {},
    "target": {"min": -58, "max": 58}, # Quais targets a TCU pode mandar
    "last-seen": {"type": "datetime", "recent": 5}, # Quantos minutos atrás a TCU tem que ter mandado o último UPLINK
    "last-angle": {"tolerance": 0.5}, # Tolerância de 2° grus fora do target
}

# Regras para a usina
# Aqui pode-se adicionar valores específicos para cada TCU (ponteiro para arquivos de configuração)

# Primeiro carregamos o arquivo de configuração padrão,
# e aí percorremos cada TCU por esse validator da Usina, os que forem passando
# direto caem na configuração normal

# Vantagens -> Mudança no BD
# Com vários arquivos de configuração prontos,
# a construção dessas regras fica estruturada ao usuário
# como se o BD fosse seu framework

# Também posso transformar isso tudo em um Objeto só, assim fica carregado
# na memória enquanto vou usando e evita acesso
# exagerado ao banco de dados

{
    "$serialnumber": {
        "0225030209999": "id_abcsroaiyxt.json",
        "0225030209998": "id_sadadjioyxt.json",
        "discard": []
    },
    "$datetime": {
        "2025-04-01_2025-08-01": "id_asdaasdiu.json",
        "discard": [
            "0225030209999",
            "0225030209898"
        ]
    },
    "$commission": {}
}