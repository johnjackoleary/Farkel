import random	# For randomizing sides

class Dice(object):
	"""Holds dice information"""
	set_aside = False
	def __init__(self):
		self.possible_sides = [1,2,3,4,5,6]
		self.current_side = 0
	def roll(self):
		random.shuffle(self.possible_sides)
		self.current_side = self.possible_sides[0]
		return self.current_side

