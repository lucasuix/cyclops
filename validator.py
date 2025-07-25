from cerberus import Validator
from datetime import datetime, timedelta
import numbers

"""
Aqui podemos escrever as regras personalizadas
de validação.

Cerberus cria métodos de validação da seguinte maneira, considerando o schema:
{
    'recent': 5
}

Cerberus procura por um método chamado _validate_<rule-name>,
como no exemplo acima <rule-name> é recent,
encontramos _validate_recent

Cerberus não se importa com valores no JSON
se não houver nenhum comportamento definido para eles desde que
no RULES esteja definido como dicionário vazio.

Isso vale para o RULES possuir um campo que o payload
não tem.
Mas não para o contrário, se houver um campo no payload
que não há no rules o Cerberus lança um erro de 'Campo desconhecido'.

Posso utilizar o próprio campo de documentos que especifiquei para realizar as
verificações.
"""

class Cyclops(Validator):
    def _validate_recent(self, max_age_minutes, field, value):
        """{'type': 'integer'}"""
        # Testa se a diferença de tempo de value, até a data
        # atual está dentro do limite de max_age_minutes
        # (Precisa trocar depois porque TCUs ficam em um fusos diferentes)
        if not isinstance(value, datetime):
            self._error(field, "Must be a datetime object")
            return

        threshold = datetime.now() - timedelta(minutes=max_age_minutes)
        if value < threshold:
            self._error(field, f"Must be within the last {max_age_minutes} minutes")
    
    def _validate_angletolerance(self, angle_tolerance, field, angle):
        """{'type': 'float'}"""
        # Testa se o ângulo real da TCU está muito longe do target.
        target = self.docs.get('target')
        if target is None or not isinstance(target, numbers.Number):
            self._error(field, "Field 'target' não é um número ou não existe.")

        if not isinstance(angle, numbers.Number):
            self._error(field, "Angle deve ser um número.")
        
        max_angle = target + angle_tolerance
        min_angle = target - angle_tolerance

        if not max_angle > angle > min_angle:
            self._error(field, f"Ângulo da TCU além da tolerância {angle_tolerance}° especificada.")
    
    def preloaded_doc(self, docs): 
        # Para poder acessar os valores do payload dentro da classe
        # Poupa ter que passar argumentos como listas quando comparar um que já existe na classe
        self.docs = docs