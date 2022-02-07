import random
import math

class Player(object):
	"""docstring for Player"""
	def __init__(self, name, age, position, ability,potential):
		super(Player, self).__init__()
		self.name = name
		self.age = age
		self.position = position
		self.ability = ability
		self.potential = potential
		self.currentClub = ""
		self.retirementAge = 50
		self.setRetirementAge()
		self.retired = False

	def setCurrentClub(self,club):
		self.currentClub = club

	def setRetirementAge(self):
		self.retirementAge = random.randrange(6)+31
		if(self.retirementAge<self.age):
			self.retirementAge = self.age+1

	def update(self):
		# aiming to be updated every week
		before = math.floor(self.ability)
		self.ability += round((self.age/self.retirementAge) * (self.potential - self.ability)/self.potential,2)
		after = math.floor(self.ability)
	
	def endOfSeason(self):
		self.age+=1
		if(self.age == self.retirementAge):
			self.retired = True




