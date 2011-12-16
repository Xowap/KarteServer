# -*- encoding: utf-8 -*-

class StockingsException(Exception):
	pass

class StockingsModelNotFound(StockingsException):
	pass

class StockingsModelNoInstance(StockingsException):
	pass

class Stockings(object):
	def __init__(self):
		pass

	def headers(self):
		return ('Void',)

	def data(self):
		return [(1, 'None',)]

	def checkMoreData(self):
		return False

	def getMoreData(self):
		return []

class ProductsModel(Stockings):
	def headers(self):
		return ('Name', 'Price')

	def data(self):
		return [
			(1, 'Karmeliet', 4200, ""),
			(2, 'Kwak', 2712, ""),
			(3, 'Chimay', 4323, ""),
		]

	def checkMoreData(self):
		return not hasattr(self, '_sentmore')

	def getMoreData(self):
		if not self.checkMoreData():
			return []

		self._sentmore = True
		return [
			(4, 'Cuvée des Trolls', 9867, "")
		]

	def filtr(self, filtr):
		pass

class StockingsFactory(object):
	def __init__(self):
		self.models = []

	def getModel(self, name):
		cls = {
			'Void': Stockings,
			'Products': ProductsModel,
		}

		if not name in cls:
			raise StockingsModelNotFound()

		mid = len(self.models)
		self.models.append(cls[name]())

		return mid

	def fromId(self, mid):
		if mid >= len(self.models):
			raise StockingsModelNoInstance()

		return self.models[mid]
