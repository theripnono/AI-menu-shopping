import unittest
from  ..db import import_data


input_file = './clean_output_ids.json'
nodes = import_data(input_file) 