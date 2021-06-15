from ResistanceModel.AbstractAgent import AbstractAgent
from ResistanceModel.mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star

class Spy(AbstractAgent):
	def __init__(self,unique_id, model):
		super().__init__(unique_id, model)

	def initKB(self):
		formula = str(self.unique_id)
		print(formula)
		self.KB.add(formula)

	def updateKB(self):
		print(f"Still needs to be implemented")

	def updateMissionPreference(self):
		print(f"Still needs to be updated")

