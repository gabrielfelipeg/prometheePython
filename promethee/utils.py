import random
import csv
import datetime
import os

def random_number():
	return random.random()

def initialise_matrix(width,height):
	mtx=[[0 for x in range(width)] for y in range(height)]
	return mtx

def initialize_array(length):
	array = [0 for x in range(length)]
	return array

def random_matrix(width, height):
	mtx = [[random.random() for x in range(width)] for y in range(height)]
	return mtx

def random_array(length):
	array = [random.random() for x in range(length)];
	return array

def random_weight(length):
	array = [random.random() for x in range(length)];
	return array

def random_normalized_array(length):
	array = random_array(length)
	arraySum = sum(array)
	for x in range(length):
		array[x] = array[x]/arraySum
	return array

def divide_integers(numerator, denumerator):
	return float(numerator) / float(denumerator)

def write_table_to_csv(array,path_to_csv):
	print("opening file %s to write") % (path_to_csv)
	try:
		with open(path_to_csv, 'w+') as csvfile:
			writer = csv.writer(csvfile)
			[writer.writerow(r) for r in array]
		print("FILE SUCCESFULLY WRITTEN")
	except IOError:
		try:
			if not os.path.exists(directory):
				os.makedirs(directory)
			with open(path_to_csv, 'w+') as csvfile:
				writer = csv.writer(csvfile)
				[writer.writerow(r) for r in array]
			print("FILE SUCCESFULLY WRITTEN")
		except OSError:
			print ('Error: Creating directory. ' + directory)

def read_table_from_csv(path_to_csv):
	with open(path_to_csv, 'r') as csvfile:
		reader = csv.reader(csvfile)
		table = [[e for e in r] for r in reader]
	return table

def format_to_2(string):
	if len(string) == 1:
		string = '0' + string
	return string

def generate_date_time_stamp():
	now = datetime.datetime.now()
	year = str(now.year)
	month = format_to_2( str(now.month) )
	day = format_to_2( str(now.day) )
	hour = format_to_2( str(now.hour) )
	minute = format_to_2( str(now.minute) )
	return year + month + day + hour + minute


