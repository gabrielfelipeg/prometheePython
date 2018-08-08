import utils
import sys
import random
from promethee import Promethee
from preference_functions import generate_preference_function_parameters

def run():


	rows = 404
	coluns = 466

	n_criteria = 2
	n_alternatives = rows * coluns
	
	input_mat = utils.initialise_matrix(n_criteria, n_alternatives)
	
	with open('IMD-I/VPR10_nmim_null_WGS_CONVERTED.txt', 'rb') as f:
		i = 0
		for line in f:
			numbers = map(float, line.split(' '))
			j = 0
			for number in numbers:
				input_mat[i * coluns + j][0] = number
				j += 1
			i += 1

	with open('IMD-I/VVAAmm_nmin_null_WGS_CONVERTED.txt', 'rb') as f:
		i = 0
		for line in f:
			numbers = map(float, line.split(' '))
			j = 0
			for number in numbers:
				input_mat[i * coluns + j][1] = number
				j += 1
			i += 1

	input_weight = [0.470, 0.530]
 
	input_preference = ['linear', 'linear']

	input_param = {'p': 1, 'q': 0, 'sigma': 0}

	algorithmPromethee = Promethee(input_mat, input_weight, input_preference, input_param)

	output = algorithmPromethee.getPlusFlow()

	for i in xrange(rows):
		for j in xrange(coluns):
			print output[i * coluns + j],
		print



if __name__ == '__main__':
	run()
