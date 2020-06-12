"""
Basic class for loading data from file or database systems
"""
from typing import List
from enum import Enum, unique
import csv
import logging
import sys
sys.path.append('..')
from abstract.mdd import MDD

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

@unique
class SourceType(Enum):
	LOCAL_FILE = 'local_file'
	HDFS = 'hdfs'


class LoaderConfig(object):
	"""
	The config object to load data from various sources
	"""
	def __init__(
		self, 
		source_type: SourceType = SourceType.LOCAL_FILE, 
		source_uris: List = [], 
		data_name: str = ''
		) -> None:
		self._source_type = source_type
		# support loading multiple files
		self._source_uri = source_uris
		self._data_name = data_name

	@property
	def source_type(self):
		return self._source_type
	
	@source_type.setter
	def source_type(self, source_type: Enum):
		self._source_type = source_type

	@property
	def source_uris(self):
		return self._source_uris
	
	@source_uris.setter
	def source_uris(self, source_uris: str):
		self._source_uris = source_uris

	@property
	def data_name(self):
		return self._data_name
	
	@data_name.setter
	def data_name(self, data_name: str):
		self._data_name = data_name


class Loader(object):
	""" basic loader from multiple data sources """

	def __init__(self, config: LoaderConfig) -> None:
		self.config = config
		self.dataset = self._read_data()

	def _read_data(self) -> MDD:
		""" read data from multiple sources and return MDD """
		if self.config.source_type == SourceType.LOCAL_FILE:
			return self._read_files()
		elif self.config.source_type == SourceType.HDFS:
			return self._read_hdfs()
		else:
			logging.warn("The source type " + LoaderConfig.source_type + "has not been implemented yet.")
			return NotImplemented


	def _read_files(self) -> MDD:
		""" Currently support csv file format from local """
		headers = []
		bodies = []
		for uri in self.config.source_uris:
			csv_reader = csv.reader(open(uri, newline='', encoding='utf-8'))
			headers.append(next(csv_reader))
			bodies.append(csv_reader)
		MDD.name = self.config.data_name
		MDD.headers = headers
		MDD.bodies = bodies
		return MDD

	def _read_hdfs(self):
		""" Access HDFS with delimiter """
		return NotImplemented

if __name__ == '__main__':
	LoaderConfig.source_type = SourceType.LOCAL_FILE
	LoaderConfig.source_uris = ['../data/ent_test1.csv', '../data/ent_test2.csv', '../data/rel_test.csv']
	LoaderConfig.data_name = 'test'
	loader = Loader(LoaderConfig)
	print(MDD.headers)
	for body in MDD.bodies:
		for line in body:
			print(line)
