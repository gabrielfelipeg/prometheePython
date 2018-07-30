import utils
import sys
import random
from promethee import Promethee
from preference_functions import generate_preference_function_parameters

def run():


	rows = 408
	coluns = 470

	n_criteria = 2
	n_alternatives = rows * coluns
	
	input_mat = utils.initialise_matrix(n_criteria, n_alternatives)
	
	with open('IMD-I/VPR10', 'rb') as f:
		i = 0
		for line in f:
			numbers = map(float, line.split(' '))
			j = 0
			for number in numbers:
				input_mat[i * coluns + j][0] = number
				j += 1
			i += 1

	with open('IMD-I/VVAAmm', 'rb') as f:
		i = 0
		for line in f:
			numbers = map(float, line.split(' '))
			j = 0
			for number in numbers:
				input_mat[i * coluns + j][1] = number
				j += 1
			i += 1

	input_weight = [3.1, 3.5]
 
	input_preference = ['usual', 'usual']

	input_param = {'p': 0, 'q': 0, 'sigma': 0}

	algorithmPromethee = Promethee(input_mat, input_weight, input_preference, input_param)

	output = algorithmPromethee.phi_plus

	for i in xrange(rows):
		for j in xrange(coluns):
			print output[i * coluns + j],
		print



if __name__ == '__main__':
	run()
