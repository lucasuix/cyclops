
class Model:

	def __init__(self, data):
		self.data = data
		self.errors = {}
		pass

	def update_rules(self, rule):
		type_join = rule.pop('type_join')
		print(f"Regras atualizadas para {rule}")
		pass