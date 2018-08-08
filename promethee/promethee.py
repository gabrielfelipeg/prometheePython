# coding=utf-8
import utils
import math
from threading import Thread
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

		parameter = {
			'criteria' : self.numberCriteria,
			'table' : self.evaluationTable,
			'weight': self.weights,
			'function': self.shapeFunction
		}

		nA = self.numberAlternatives

		rangeIJ = [
			{'beginI' : 0, 'beginJ': 0, 'endI': nA/2, 'endJ': nA/2 },
			{'beginI' : 0, 'beginJ': nA/2, 'endI': nA/2, 'endJ': nA},
			{'beginI' : nA/2, 'beginJ': 0, 'endI': nA, 'endJ': nA/2},
			{'beginI' : nA/2, 'beginJ': nA/2, 'endI': nA, 'endJ': nA}
		]

		threads = [
			FlowCalculator(self.phi_plus, self.phi_minus, parameter, rangeIJ[0]),
			FlowCalculator(self.phi_plus, self.phi_minus, parameter, rangeIJ[1]),
			FlowCalculator(self.phi_plus, self.phi_minus, parameter, rangeIJ[2]),
			FlowCalculator(self.phi_plus, self.phi_minus, parameter, rangeIJ[3])			
		]

		for thread in threads:
			thread.start()

		for thread in threads:
			thread.join()

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
	
class FlowCalculator(Thread):

	def __init__(self, phi_plus, phi_minus, parameter, range):
		
		self.phi_plus = phi_plus
		self.phi_minus = phi_minus
		self.numberCriteria = parameter['criteria']
		self.weights = parameter['weight']
		self.shapeFunction = parameter['function']
		self.evaluationTable = parameter['table']
		self.beginI = range['beginI']
		self.beginJ = range['beginJ']
		self.endI = range['endI']
		self.endJ = range['endJ']

		Thread.__init__(self)

	def run(self):
		for a in xrange(self.beginI, self.endI):
			for b in xrange(self.beginJ, self.endJ):
				for k in xrange(self.numberCriteria):
					if a == b: 
						continue
					
					if math.isnan(self.phi_minus[a]) or self.evaluationTable[a][k] == -1:
						self.phi_plus[a] = float('nan')
						continue

					if math.isnan(self.phi_minus[b]) or self.evaluationTable[b][k] == -1:
						self.phi_minus[b] = float('nan')
						continue

					deltaAB = self.evaluationTable[a][k] - self.evaluationTable[b][k]
					self.phi_plus[a] += self.weights[k] * self.shapeFunction[k](deltaAB)
					self.phi_minus[b] -= self.weights[k] * self.shapeFunction[k](deltaAB)