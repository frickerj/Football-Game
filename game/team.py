from prettytable import PrettyTable
import time


class Team(object):
	"""docstring for Team"""
	def __init__(self, name,home):
		super(Team, self).__init__()
		self.name = name
		self.home = home
		self.rating = 0
		self.points = 0
		self.controlled = False
		self.wins = 0
		self.losses = 0
		self.draws = 0
		self.goalsFor = 0
		self.goalsAgainst = 0 
		self.goalDifference = 0
		self.matchesPlayed = 0
		self.players = []
		self.bestTeam = []
		self.youthTeam = []
		self.youthTeamBest = []


	def reset(self):
		# reset
		# used for end of season usually
		self.points = 0
		self.wins = 0
		self.losses = 0
		self.draws = 0
		self.goalsFor = 0
		self.goalsAgainst = 0 
		self.goalDifference = 0
		self.matchesPlayed = 0
		self.youthTeam.sort(key=lambda x: x.potential, reverse=True)
		self.players.sort(key=lambda x: x.potential, reverse=True)
		if(self.controlled == True):
			self.promotePlayers()
		else:
			p = self.youthTeam[0]
			k = self.players[-1]
			while(p.potential>k.potential and len(self.youthTeam)>0):
				self.players.remove(k)
				self.players.append(p)
				self.youthTeam.remove(p)
				p = self.youthTeam[0]
				k = self.players[-1]
		for i in self.youthTeam:
			if(i.age>20):
				self.youthTeam.remove(i)
		for i in self.players:
			i.endOfSeason()
		for i in self.youthTeam:
			i.endOfSeason()

		# fill up team
		while(len(self.players)<26 and len(self.youthTeam)>0):
			p = self.youthTeam[0]
			self.players.append(p)
			self.youthTeam.remove(p)
		for i in self.players:
			if(i.retired == True):
				if(self.controlled == True):
					print(i.name, "Retired at age ",i.age)
				self.players.remove(i)
		self.players.sort(key=lambda x: x.ability, reverse=True)

	def promotePlayers(self):
		k = 0
		while(k!="x"):
			self.printYouthTeam()
			print("CHOOSE WHICH PLAYERS TO PROMOTE")
			print("ENTER THE NUMBER")
			print("TYPE x TO EXIT")
			k = input()
			if(str(k)=="x"):
				break
			if(int(k)>0 and int(k)<=len(self.youthTeam)):
				p = self.youthTeam[int(k)-1]
				self.printAllPlayers()
				print("CHOOSE PLAYER TO REMOVE")
				print("ENTER THE NUMBER")
				print("TYPE x TO EXIT")
				h = input()
				print(h)
				if(str(h)=="x"):
						break
				if(int(h)>0 and int(h)<=len(self.players)):
					r = self.players[int(h)-1]
					self.players.remove(r)
					self.players.append(p)
					self.youthTeam.remove(p)
					print(r.name, "was sacked!")
					print(p.name, "was promoted!")
				else:
					h = input("Enter correct number")
			else:
				k = input("Enter correct number")
			


	def goalDifferenceCalc(self):
		self.goalDifference = self.goalsFor-self.goalsAgainst


	def result(self,r,gfr,gagainst):
		# result r
		# 1 = win
		# 0 = draw
		# -1 = loss
		self.goalsFor += gfr
		self.goalsAgainst += gagainst
		self.matchesPlayed+=1
		self.goalDifferenceCalc()

		if(r not in [-1,0,1]):
			print("INCORRECT RESULT INPUT")

		if(r==1):
			self.wins+=1
			self.points+=3
		if(r==0):
			self.draws +=1
			self.points+=1
		if(r==-1):
			self.losses+=1

	def addPlayer(self,player):
		self.players.append(player)

	def addYouthPlayer(self,player):
		self.youthTeam.append(player)

	def selectTeam(self):
		self.players = sorted(self.players,key=lambda x: x.ability, reverse=True)
		self.bestTeam = []

		allPlayers = []
		for i in self.youthTeam:
			allPlayers.append(i)
		for j in self.players:
			allPlayers.append(j)
		gk = []
		defe = []
		mid = []
		att = []
		for i in allPlayers:
			if(i.position == "GK"):
				gk.append(i)
			if(i.position == "DEF"):
				defe.append(i)
			if(i.position =="MID"):
				mid.append(i)
			if(i.position == "ATT"):
				att.append(i)

		gk.sort(key=lambda x: x.ability, reverse=True)
		defe.sort(key=lambda x: x.ability, reverse=True)
		mid.sort(key=lambda x: x.ability, reverse=True)
		att.sort(key=lambda x: x.ability, reverse=True)

		self.bestTeam.append(gk[0])
		if(len(defe)>0):	
			for i in range(min(3,len(defe))):
				self.bestTeam.append(defe[i])
		if(len(mid)>0):	
			for i in range(min(2,len(mid))):
				self.bestTeam.append(mid[i])
		if(len(att)>0):
			for i in range(min(1,len(att))):
				self.bestTeam.append(att[i])


		#print(self.bestTeam[0].name,self.bestTeam[0].position,self.bestTeam[0].ability)
		self.players = sorted(self.players,key=lambda x: x.ability, reverse=True)
		while(len(self.bestTeam)<11 and len(self.players)>10):
			for j in self.players:
				if(j not in self.bestTeam and j.position!="GK"):
					self.bestTeam.append(j)
					break
		self.calculateTeamRating()

			
	def calculateTeamRating(self):
		s = 0
		for i in self.bestTeam:
			s+=i.ability
		self.rating = round(s/11,2)

	def printBestTeam(self):
		c = 1
		t = PrettyTable(['Index','Name','Age','Position','Ability','Potential'])
		self.bestTeam.sort(key=lambda x: x.position, reverse=True)
		for i in self.bestTeam:
			#print(i.name,i.points,i.wins,i.draws,i.losses)
			t.add_row([c,i.name,i.age,i.position,round(i.ability,2),round(i.potential,2)])
			c+=1
		print(t)
		print('Team Ability is ', self.rating)

	def printAllPlayers(self):
		c = 1
		t = PrettyTable(['Index','Name','Age','Position','Ability','Potential'])
		for i in self.players:
			#print(i.name,i.points,i.wins,i.draws,i.losses)
			n = i.name
			if(i in self.bestTeam):
				n+=("**")
			t.add_row([c,n,i.age,i.position,round(i.ability,2),round(i.potential,2)])
			c+=1
		print(t)
		print('Team Ability is ', self.rating)

	def update(self):
		for i in self.players:
			i.update()
		for i in self.youthTeam:
			i.update()
		if(self.controlled == True):
			for i in self.bestTeam:
				if(i.age<21):
					i.potential+=0.1

		self.calculateTeamRating()

	def printYouthTeam(self):
		self.youthTeam.sort(key=lambda x: x.potential, reverse=True)
		c = 1
		t = PrettyTable(['Index','Name','Age','Position','Ability','Potential'])
		for i in self.youthTeam:
			#print(i.name,i.points,i.wins,i.draws,i.losses)
			t.add_row([c,i.name,i.age,i.position,round(i.ability,2),round(i.potential,2)])
			c+=1
		print(t)

	def customSelect(self):
		k = ""
		while(k!="x"):
			self.printAllPlayers()
			print("CHOOSE WHICH PLAYERS TO SWAP IN")
			print("ENTER THE NUMBER")
			print("TYPE x TO EXIT")
			print("TYPE s TO AUTO SELECT")
			k = input()
			if(str(k)=="x"):
				break
			if(str(k)=="s"):
				self.selectTeam()
				print("Team has been auto selected!")
				time.sleep(1)
				break
			if(int(k)>0 and int(k)<=len(self.players)):
				p = self.players[int(k)-1]
				print("YOU CHOSE: ",p.name)
				self.printBestTeam()
				print("CHOOSE PLAYER TO SWAP OUT")
				print("ENTER THE NUMBER")
				print("TYPE x TO EXIT")
				h = input()
				print(h)
				if(str(h)=="x"):
						break
				if(int(h)>0 and int(h)<=len(self.bestTeam)):
					r = self.bestTeam[int(h)-1]
					self.bestTeam.remove(r)
					self.bestTeam.append(p)
					print(r.name, "was put into the reserves!")
					print(p.name, "was placed into the first team!")
				else:
					h = input("Enter correct number")
			else:
				k = input("Enter correct number")
		self.calculateTeamRating()

	