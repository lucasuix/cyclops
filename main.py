from harpia.harpia import Harpia
from harpia.model import Model
from datetime import datetime, date

from astral import LocationInfo
from astral.sun import sun

# Uso uma class personalizada para definir os métodos personalizados
class tcu_Harpia(Harpia):

	def _HARPIA_GEOTIME(self):
		# Obter o valor do horário baseado na latitude e longitude do model
		return datetime.now()

m = Model(
		{
			"serialnumber": "0225030209898",
			"anemometro": 48,
			"last-seen": datetime.now(),
			"last-angle": 42.0,
			"target": 55
		},
		{	# Ruleset geral
			"serialnumber": {},
			"target": {"type": "float", "min": -58, "max": 58},
			"last-seen": {"type": "datetime", "recent": 5},
			"last-angle": {"type": "float", "angletolerance": 0.5 },
			"anemometro": {}
		}
	)
f = tcu_Harpia(
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

		"$posicao-seguranca": {
			"SORT_anyof": {
				"HARPIA_GEOTIME": {"type": "datetime", "min": datetime(2025, 7, 27, 16), "max": datetime(2025, 7, 28, 6)},
				"MODEL_anemometro": {"type": "float", "min": 38}
			},
			"rule": {
				"type_join": "u+",
				"last-angle": {"type": "float", "min": -26, "max": 26}   
			}
		}
	}
)

f.adjust_rules(m)
m.verify()