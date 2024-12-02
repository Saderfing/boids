from math import degrees, sqrt, atan2, sin, cos
from random import randint, random, choice

from regex import D

def inv_sqrt(x:int) -> int:
	if x == 0:
		raise ZeroDivisionError("can't divide by 0")
	return x ** -0.5


# This class was made with the help of PasPatate : 
class Vec2:
	def __init__(self, x:int = 0, y:int = 0) -> None:
		self.x = x
		self.y = y
	
	def __getitem__(self, i):
		if i == 0: 
			return self.x
		elif i == 1:
			return self.y
		raise IndexError("Vec2 only have x and y value")
		
	def __repr__(self) -> str:
		return "x: "+ str(self.x) + " y: " + str(self.y)
	
	def __add__(self, other):
		return Vec2(self.x + other.x, self.y + other.y)        
		
	def __sub__(self, other):
		return Vec2(self.x - other.x, self.y - other.y)
	
	def __mul__(self, other):
		if type(other) == int or type(other) == float: return Vec2(self.x * other, self.y * other)

	def __rmul__(self, other):
		if type(other) == int or type(other) == float: return Vec2(self.x * other, self.y * other)
	
	def __truediv__(self, other):
		return Vec2(self.x/other, self.y/other)

	def __floordiv__(self, other):
		return Vec2(self.x//other, self.y//other)

	def __round__(self):
		return Vec2(round(self.x), round(self.y))
		
	def __iter__(self):
		for key in "x", "y":
			yield getattr(self, key)
	
	def normalized(self):
		if (self.x*self.x) + (self.y*self.y) == 0:
			return Vec2(0,0)
		invsqrt = inv_sqrt((self.x*self.x) + (self.y*self.y))
		x = self.x * invsqrt
		y = self.y * invsqrt
		return Vec2(x, y)
	
	def set_magnitude(self, magnitude):
		vect = self.normalized()
		return vect * magnitude
	
	def magnitude(self):
		return sqrt(self.x*self.x + self.y*self.y)
	
	def random_vector(self):
		signe = [-1, 1]
		return Vec2(random() * choice(signe), random() * choice(signe))
	
	def clamp_norm(self, max_magnitude):
		magnitude = self.magnitude()
		if magnitude <= 0:
			magnitude = 0.001
		step = min(magnitude, max_magnitude) / magnitude
		return Vec2(step * self.x, step * self.y)
	
	@classmethod
	def average(self, vectors:list):
		x = 0
		y = 0
		for vec in vectors:
			x += vec.x
			y += vec.y
		
		return Vec2(x/len(vectors), y/len(vectors))
	
	@classmethod
	def distance(self, vecA, vecB):
		return ((vecB.x - vecA.x)*(vecB.x - vecA.x) + (vecB.y - vecA.y)*(vecB.y - vecA.y )) ** 0.5

	@classmethod
	def polar_to_vector(self, lenght, angle):
		pass
	
	def to_polar(self):
		polar_radius = self.magnitude()
		angle = degrees(atan2(self.y, self.x)) % 360
		
		return polar_radius, angle

	def is_null_vector(self):
		return self.x == self.y == 0

def check_interval(num, min_value, max_value):
	if num > max_value:
		return min_value
	elif num < min_value:
		return max_value
	else: 
		return num

def is_in_circle(x, y, center_x, center_y, radius):
	return (x-center_x)**2 + (y - center_y)**2 < radius**2

def average(lst:list):
	val = 0
	for i in lst:
		val += i
	
	return val//len(lst)
		
def clamp(value:int, min_value:int, max_value:int):
	return min(max(value, min_value), max_value)

def is_in_sector(point:Vec2, min_angle:int or float, max_angle:int or float, center:Vec2, radius:int or float):
	vect = Vec2(point.x - center.x, point.y - center.y)
	magnitude, angle = vect.to_polar()
	
	if angle >= min_angle and angle <= max_angle and magnitude <= radius:
		return True
	
	return False

def get_range_of_index(lst, center, radius):
	start_x = center[0] - radius
	start_y = center[1] - radius
	col = []
	
	for y in range(max(0, start_y), min(len(lst), start_y + (radius * 2) + 1)):
		row = []
		for x in range(max(0, start_x), min(len(lst), start_x + (radius * 2) + 1)):
			row.append(lst[y][x])
		col.append(row)
	
	return col
