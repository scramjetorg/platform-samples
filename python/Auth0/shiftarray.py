class ShiftArray:
	def __init__(self, length=5):
		self.array = []
		self.length = length

	def append(self, value):
		if len(self.array) == self.length:
			self.array.pop(-1)
		self.array.append(value)

	def contains(self, value):
		return value in self.array

	def get_values(self):
		return self.array

	def __str__(self):
		return str(self.array)