"""player class for game"""
import random

class Player(object):
    """docstring for Player"""
    def __init__(self, name, age, position, ability,potential):
        super(Player, self).__init__()
        self.name = name
        self.age = age
        self.position = position
        self.ability = ability
        self.potential = potential
        self.current_club = ""
        self.retirement_age = 50
        self.set_retirement_age()
        self.retired = False

    def set_current_club(self,club):
        """set current club"""
        self.current_club = club

    def set_retirement_age(self):
        """set player retirement age"""
        self.retirement_age = random.randrange(6)+31
        if self.retirement_age<self.age:
            self.retirement_age = self.age+1

    def update(self):
        """update players ability, and potential"""
        # aiming to be updated every week
        self.ability += round((self.age/self.retirement_age) *
            (self.potential - self.ability)/self.potential,2)

    def end_of_season(self):
        """increase age at EOS"""
        self.age+=1
        if self.age == self.retirement_age:
            self.retired = True
