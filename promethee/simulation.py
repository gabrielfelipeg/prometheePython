# coding=utf-8

import utils
import sys
import random
from promethee import Promethee
from preference_functions import generate_preference_function_parameters

def run(n_alternatives, n_criteria, output_file):

	# preference functions to be considered
	preference_functions = ['usual', 'quasi-criterion', 'linear', 'gaussian', 'level', 'linear_with_indifference']
	
	input_mat = utils.random_matrix(n_criteria, n_alternatives)
	
	input_weight = utils.random_array(n_criteria)

	input_preference = [preference_functions[random.randint(0, 5)] for x in range(n_criteria)]
	input_param = {'p': utils.random_number(), 'q': utils.random_number(), 'sigma': utils.random_number()}
	if input_param['p'] < input_param['q']:
		input_param['p'], input_param['q'] = input_param['q'], input_param['p']
	algorithmPromethee = Promethee(input_mat, input_weight, input_preference, input_param)
	
	utils.write_table_to_csv(algorithmPromethee.getPairwiseComparisonMatrix(), output_file)

if __name__ == '__main__':
	if len(sys.argv) != 4:
		raise Exception("Illegal Arguments: python simulation.py number_alternatives number_criteria output_file")
	run(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
