from harpia import Harpia
from model import Model
from datetime import datetime

# Uso uma class personalizada para definir os métodos personalizados
class tcu_Harpia(Harpia):

	def _user_HARPIA_GEOTIME(self):
		"""
		Aqui eu vou devolver um datetime baseado na longitude e latitude,
		coloquei um de exemplo apenas
		"""
		return datetime.now()

m = Model(
		{
		"serialnumber": "0225030209595",
		"anemometro": 39
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

		# $ são condições personalizadas
		# Aqui VARIABLE passa pelos conditions
		# Se retornar True
		# Aí sim aplicamos o rule
		"$posicao-seguranca": {
			"condition": {
			# Problema aqui é que as duas tem que ser verdadeiras para retornar True, mas o ideal seria um OR
				"anyof": {
					"HARPIA_GEOTIME": {"type": "datetime", "min": datetime(2025, 7, 27, 13), "max": datetime(2025, 7, 27, 23)},
					"MODEL_anemometro": {"type": "float", "min": 38}
				}
				# allof
				# noneof
			},
			"rule": {
				"type_join": "u+",
				"angle": {"type": "float", "min": -26, "max": 26}   
			}
		}
	}
)

f.verify(m)