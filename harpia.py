from model import Model
from validator import Cyclops

class Harpia:

	def __init__(self, filters):
		try:
				self.validations = filters
		except Exception as e:
			# FilterErrorHandler(e)
			print(e)

		self.result = False

		self.custom_validations = {}
		self.default_validations = {}

		for key, validation in self.validations.items():
			if key.startswith("$"):
				self.custom_validations[key] = validation
			else:
			 	self.default_validations[key] = validation

	def verify(self, model: Model):
		self._load_model(model)
		self._default_validation()
		self._custom_validation()

	def _load_model(self, model: Model):
		self.model = model

	def _custom_validation(self):
		"""
		Cada item do self.customvalidations tem essa cara:

				"$nome-da-custom-rule": {
					-> Os dados que serão validados:
					-> HARPIA_ são dados que são obtidos externamente (Ex.: Horário em algum lugar do mundo)
					-> MODEL_ são dados que são obtidos através do model carregado

					"refer": ["HARPIA_GEOTIME", "MODEL_anemometro"],

					-> Será gerado um dicionaŕio reference
					-> Esse dicionário será usado para verificação através do Cerberus

					-> Condition é o schema que será usado para validar os dados do reference
					"condition": {
						"HARPIA_GEOTIME": {"type": "datetime", "min": datetime(hours=16), "max": datetime(hours=6)},
						"MODEL_anemometro": {"type": "float", "min": 38}
					},

					-> Se após a verificação Cerberus retornar True, significa que a rule da custom rule será aplicada ao Model
					-> invés da rule normal
					
					"rule": {
						"type_join": "u+",
						"angle": {"type": "float", "min": -26, "max": 26}	
					}
				}
		"""
		for key, rules in self.custom_validations.items():

			v = Cyclops(rules["condition"])
			reference = {}
			for refer in rules["refer"]:
				reference[refer] = self._get_custom_variable(refer)

			if reference and v.validate(reference):
				self.model.update_rules(rules["rule"])

	def _anyof(self):
		pass

	def _noneof(self):
		pass

	def _allof(self):
		pass

	def _default_validation(self):
		for key, rules in self.default_validations.items():
			if rules:
				rule = rules[self.model.data[key]]
				self.model.update_rules(rule)

	def _get_custom_variable(self, harpia_variable):
		if harpia_variable.startswith("MODEL_"):
			key = harpia_variable.lstrip("MODEL_")
			data = self.model.data[key]
			return data
		elif harpia_variable.startswith("HARPIA_"):
			method = getattr(self, f"_user_{harpia_variable}")
			return method()
		else:
			raise RunTimeError("harpia_variable should start with 'MODEL_' for model data or 'HARPIA_' for a custom method.")