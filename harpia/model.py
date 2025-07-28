from harpia.validator import Cyclops

class Model:

	def __init__(self, data, rules):
		self.data = data
		self.rules = rules
		self.errors = {}
		pass

	def update_rules(self, rule):
		type_join = rule.pop('type_join')
		match type_join:
			case "u+":
				self._u_plus_join(rule)
		print(f"Regras atualizadas para {self.rules}\n\n")
		pass

	def _u_plus_join(self, rule):
		# Garante que as novas verificacoes
		# a elementos das mesmas chaves
		# também passem pelo join
		for rule_key in rule.keys():
			if rule_key in self.rules.keys():
				self.rules[rule_key] |= rule[rule_key]
	
	def verify(self):
		v = Cyclops(self.rules)
		v.preloaded_doc(self.data)
		# v.validate(self.data)
		print(v.validate(self.data), v.errors)