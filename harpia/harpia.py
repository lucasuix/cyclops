from harpia.model import Model
from harpia.validator import Cyclops

class Harpia:

	def __init__(self, filters):
		try:
				self.validations = filters
		except Exception as e:
			# FilterErrorHandler(e)
			print(e)

		self.custom_validations = {}
		self.default_validations = {}

		for key, validation in self.validations.items():
			if key.startswith("$"):
				self.custom_validations[key] = validation
			else:
				self.default_validations[key] = validation

	def adjust_rules(self, model: Model):
		self._load_model(model)
		self._default_validation()
		self._custom_validation()

	def _load_model(self, model: Model):
		self.model = model

	def _custom_validation(self):
		for code, validations in self.custom_validations.items(): # Todos os itens que começam com $
			for key, data in validations.items():
				if not key.startswith("SORT_"):
					continue

				reference = self._create_reference(data)
				if not reference:
					continue

				v = Cyclops(data)
				v.validate(reference)
				if self._get_custom_variable(key)(v, data):
					self.model.update_rules(validations["rule"])
	
	def _create_reference(self, data):
		reference = {}
		for key in data:
			reference[key] = self._get_custom_variable(key)
		return reference

	def _SORT_anyof(self, val, data): # Qualquer condição que passar é válida
		return data.keys() != val.errors.keys()

	def _SORT_noneof(self, val, data): # Todas as condições tem que falhar
		return data.keys() == val.errors.keys()

	def _SORT_allof(self, val, data): # Todas as condições tem que ser verdadeiras
		return not val.errors.keys()

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
			method = getattr(self, f"_{harpia_variable}")
			return method()
		elif harpia_variable.startswith("SORT_"):
			method = getattr(self, f"_{harpia_variable}")
			return method
		else:
			raise RuntimeError("harpia_variable should start with 'MODEL_' for model data or 'HARPIA_' for a custom method.")