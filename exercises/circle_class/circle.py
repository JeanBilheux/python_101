from math import pi


class Circle:

	def __init__(self, radius=1):
		self.radius = radius

	@property
	def radius(self):
		return self._radius

	@radius.setter
	def radius(self, radius):
		if radius < 0:
			raise ValueError("Radius cannot be negative")
		self._radius = radius

	@property
	def diameter(self):
		return 2 * self._radius

	@diameter.setter
	def diameter(self, value):
		self.radius = value / 2.

	@property
	def area(self):
		return pi * self._radius**2

	@area.setter
	def area(self, value):
		raise AttributeError

	def __repr__(self):
		return(f"{self.__class__.__name__}({self.radius})")
