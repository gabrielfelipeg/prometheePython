# coding=utf-8
import utils
from preference_functions import PreferenceFunctions 

class Promethee:
	# defines the promethee class that we will use to run simulation
	# evalutionTable (array): table of evaluation of the alternatives w.r.t criteria
	# weights (vector): weights for the criteriacasa
	# preference function : list of preference function given (string)
	def __init__(self, evaluationTable, weights, preference_function, function_params):
		assert(len(weights)==len(evaluationTable[0]))
		self.evaluationTable = evaluationTable
		self.numberAlternatives = len(evaluationTable)
		self.numberCriteria = len(evaluationTable[0])
		self.weights = weights
		self.normalizeWeights()
		self.p = function_params['p']
		self.q = function_params['q']
		self.sigma = function_params['sigma']
		self.preference_function = preference_function
		self.assignShapeFunctions()
		self.computeFlows()

	def normalizeWeights(self):
		sumW = sum(self.weights)
		for i in range(len(self.weights)):
			self.weights[i] = self.weights[i]/sumW

	def assignShapeFunctions(self):
		self.shapeFunction = [None]*self.numberCriteria
		availablePreferenceFunctions = PreferenceFunctions(self.p, self.q, self.sigma).get_preference_functions()
		for i in xrange(self.numberCriteria):
			assert(self.preference_function[i] in availablePreferenceFunctions)
			self.shapeFunction[i] = availablePreferenceFunctions[self.preference_function[i]]

	def computeFlows(self):
		self.phi_plus = [0] * self.numberAlternatives
		self.phi_minus = [0] * self.numberAlternatives
		self.phi_global = [0] * self.numberAlternatives

		for a in xrange(self.numberAlternatives):
			for b in xrange(a + 1, self.numberAlternatives):
				sum = 0
				for k in xrange(self.numberCriteria):
					deltaAB = self.evaluationTable[a][k] - self.evaluationTable[b][k]
					deltaBA = deltaAB * -1
					self.phi_plus[a] += self.weights[k] * self.shapeFunction[k](deltaAB)
					self.phi_plus[b] -= self.weights[k] * self.shapeFunction[k](deltaAB)
					self.phi_minus[a] -= self.weights[k] * self.shapeFunction[k](deltaBA) 
					self.phi_plus[b] += self.weights[k] * self.shapeFunction[k](deltaBA)

		for i in xrange(self.numberAlternatives):
			self.phi_plus[i] /= self.numberCriteria
			self.phi_minus[i] /= self.numberCriteria
			self.phi_global = self.phi_plus + self.phi_minus

	def getGlobalFlow(self):
		return self.phi_global

	def getPlusFlow(self):
		return self.phi_plus

	def getMinusFlow(self):
		return self.phi_minus
		