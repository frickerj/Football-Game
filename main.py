import random
import time
from prettytable import PrettyTable
import pandas as pd
import numpy 

from game.team import Team
from game.player import Player

class Manager(object):
    """docstring for Manager"""
    def __init__(self, name, ability):
        super(Manager, self).__init__()
        self.name = name
        self.ability = ability

class Fixture(object):
	"""docstring for fixture"""
	def __init__(self, teamA,teamB,date):
		super(Fixture, self).__init__()
		self.teamA = teamA
		self.teamB = teamB
		self.date = date
		self.place = teamA.home

def advancedMatchEngine(fixture):
	# want to make the game some kind of random walk
	# starts at 0, between -1 and 1
	# when the walk gets to -1 or 1, then a goal is scored
	# we have 90 walks, as the game is 90 minutes
	teamA = fixture.teamA
	teamB = fixture.teamB
	playerView = False
	if(teamA.controlled == True or teamB.controlled == True):
		playerView = True
	goalTeamA = 0
	goalTeamB = 0
	initial = 0
	delta = 0
	if teamA.rating>teamB.rating:
		initial =  (teamA.rating/teamB.rating) - 1
		delta = (teamA.rating - teamB.rating) /500
	else:
		initial =  -(teamB.rating/teamA.rating -1)
		delta = -(teamB.rating - teamA.rating) /500

	# team A is the home team and thus recieves a little bonus
	initial += 0.025
	if playerView == True:
		print(teamA.name,"v",teamB.name, "at",teamA.home)
		print(teamA.name," rating is ", teamA.rating)
		print(teamB.name," rating is ", teamB.rating)

	# setup to make sure there are no instant goals
	if initial>0.95:
		initial = 0.95
	elif initial<-0.95:
		initial = -0.95

	state = initial
	#print('Match Start.....')
	for moments in range(91):
		n = numpy.random.normal(delta,0.2)
		state+=n
		if state>1:
			goalTeamA+=1
			state = initial
			if playerView == True:
				print('GOAL!',teamA.name, "in the", moments,"minute")
				print('Score is: ',goalTeamA,'-',goalTeamB)

		elif state<-1:
			goalTeamB+=1
			state = initial
			if playerView == True:
				print('GOAL!',teamB.name, "in the", moments,"minute")
				print('Score is: ',goalTeamA,'-',goalTeamB)

		#if(playerView == True):
		#	# comment line below when testing
		#	time.sleep(0.1)

	print('End of Game ',teamA.name,"v",teamB.name)
	print("Final Score is: ",goalTeamA,"-",goalTeamB)
	# comment out below when testing
	#
	if playerView == True:
		#time.sleep(2)
		print("**********")

	ra = 0
	rb = 0
	if goalTeamA>goalTeamB:
		ra = 1
		rb = -1
	elif goalTeamB>goalTeamA:
		rb = 1
		ra = -1

	# team A
	teamA.result(ra,goalTeamA,goalTeamB)
	# team B
	teamB.result(rb,goalTeamB,goalTeamA)

def createPlayer(player_type = "senior"):
	firstNames =  open("data/firstnames.txt", "r").read().splitlines()
	lastNames =  open("data/lastnames.txt", "r").read().splitlines()

	a = random.randrange(len(firstNames))
	b = random.randrange(len(lastNames))

	first = firstNames[a]
	last = lastNames[b]
	if player_type == "youth":
		age = random.randrange(3)+15
		ability = numpy.random.normal(60,3)
		potential = numpy.random.normal(78,5)

	elif player_type == "senior":
		age = random.randrange(13)+18
		ability = numpy.random.normal(50+age,5)
		potential = ability+numpy.random.normal((30-age),2)

	if ability>99 :
		ability = 98
		potential = 99

	ability = round(ability,2)
	potential = round(potential,2)

	position = ""
	pos = random.randrange(11)
	if pos==0:
		position = "GK"
	if 1<=pos<=4:
		position = "DEF"
	if 5<=pos<=8:
		position = "MID"
	if 9<=pos<=10:
		position = "ATT"

	player = Player(first + " " + last, age,position,ability,potential)

	return player

def getTeamData():
	data = pd.read_csv('data/teams.csv')
	names = data['Team Name']
	home = data['Home']
	return names,home

def createGame():
	names,home = getTeamData()
	t = []
	teamsCreated = 0
	for i in range(20):
		t.append(Team(names[i],home[i]))
		gk = 0
		for j in range(23):
			p = createPlayer('senior')
			if(p.position == "GK"):
				gk+1
			t[i].addPlayer(p)
		while(gk<2):
			p = createPlayer()
			if(p.position == "GK"):
				t[i].addPlayer(p)
				gk+=1
		for j in range(12):
			p = createPlayer('youth')
			t[i].addYouthPlayer(p)
		teamsCreated+=1
		print('Created',teamsCreated,"Teams")
	return t

def getWorstYouthPlayer(team):
	while(len(team.youthTeam)<1):
		team.youthTeam.append(Player("",0,"GK",1,1))
	worst_pot = 1000
	worst = 0
	for i in team.youthTeam:
		if(i.potential<worst_pot):
			worst = i
			worst_pot = i.potential
	return worst

def youthIntake(teams):
	print("YOUTH INTAKE!")
	for i in teams:
		for j in range(12):
			p = createPlayer('youth')
			k = getWorstYouthPlayer(i)
			if(len(i.youthTeam)<12):
				i.addYouthPlayer(p)
				if(i.controlled == True):
					print("Added New Player",p.name,"Ability",p.ability,"Potential",p.potential)
			else:
				if(p.potential>k.potential):
					i.youthTeam.remove(k)
					i.addYouthPlayer(p)
					if(i.controlled == True):
						print("Added New Player",p.name,"Ability",p.ability,"Potential",p.potential)
						time.sleep(1)
		checkGoalkeeper(i)

def checkGoalkeeper(team):
	hasGk = False
	for j in team.players:
		if(j.position=="GK"):
			hasGk = True
	if(hasGk==False):
		team.players.append(Player("DUMMY",0,"GK",1,1))

def createFixtures(teams):
	# fixtures[round][match][team]
	rounds = (len(teams)-1)*2
	gamesPerRound = len(teams)//2
	fixtures = [[0 for j in range(gamesPerRound)] for i in range(rounds)]
	print('Creating ',rounds,"rounds, with ",gamesPerRound,"games per Round")
	# set first round fixtures
	pos = [k for k in range(len(teams))]
	for i in range(rounds):
		ha = i%2
		# ha = 1 // home
		# ha = 0 // away
		for j in range(len(teams)//2):
			#print('Accessing teams at',pos[j],pos[len(teams)-j-1])
			# create fixtures
			# need to alternate for fixtures to get home and away correct
			if(ha==0):
				fixtures[i][j] = Fixture(teams[pos[j]],teams[pos[len(teams)-j-1]],i)
			else:
				fixtures[i][j] = Fixture(teams[pos[len(teams)-j-1]],teams[pos[j]],i)
		for k in range(1,len(pos)):
			pos[k]-=1
			if(pos[k]==0):
				pos[k]=len(teams)-1
		#print('New Positions: ',pos)
	return fixtures

def printFixtures(fixtures):
	r = 1
	print("PRINTING FIXTURES")
	for i in fixtures:
		print('ROUND ',r)
		r+=1
		for j in i:
			print(j[0].name,j[1].name)
	return fixtures


def playGames(fixturesWeek):
	for game in fixturesWeek:
		advancedMatchEngine(game)

def showTable(teams):
	newlist = sorted(teams, key=lambda x: (x.points,x.goalDifference), reverse=True)
	t = PrettyTable(['P','Team','Played','Won','Drawn','Lost','Points','GF','GA','GD'])
	index = 1
	for i in newlist:
		n = i.name
		if(i.controlled == True):
			n+="**"
		#print(i.name,i.points,i.wins,i.draws,i.losses)
		t.add_row([index,n,i.matchesPlayed,i.wins,i.draws,i.losses,i.points,i.goalsFor,i.goalsAgainst,i.goalDifference])
		index+=1
	print(t)

def endOfSeason(team):
	print("CONGRATULATIONS ON ANOTHER SUCCESSFUL SEASON")
	best = team.players[0]
	for i in team.players:
		if(i.ability>best.ability):
			best = i
	talent = team.players[-1]
	for i in team.players:
		if(i.age<21 and i.potential>talent.potential):
			talent = i
	print("THE BEST PLAYER IS",best.name,best.position,"ABILITY IS",round(best.ability,2))
	time.sleep(5)
	print("THE BEST PROSPECT IS",talent.name,talent.position,"POTENTIAL IS",round(talent.potential,2))
	time.sleep(5)

def chooseTeam(teams):
	while(True):
		x = input("Choose a Team To Manage:")
		index = -1
		for i in teams:
			if(str(x) == i.name):
				return i
		print("Incorrect Name Entered")
		print("You Entered ",x,"and they are not a team")
		print("**************************")


def main():
	print('Program Start')
	#m=tkinter.Tk()
	teams = createGame()
	for i in teams:
		i.selectTeam()
	fixtures = createFixtures(teams)
	playerTeam = 0
	season = 0
	for i in teams:
		print(i.name)

	playerTeam = chooseTeam(teams)
	playerTeam.controlled = True

	week = 0
	print("You are managing",playerTeam.name)
	while(True):
		if(week == len(fixtures)):
			season+=1
			print('END OF SEASON',season)
			playerTeam.printAllPlayers()
			showTable(teams)
			endOfSeason(playerTeam)
			print('Reseting Season.....')
			week = 0
			fixtures = createFixtures(teams)
			for i in teams:
				checkGoalkeeper(i)
				i.reset()
			time.sleep(5)
		for i in teams:
			if(i != playerTeam):
				checkGoalkeeper(i)
				i.selectTeam()
		print('WEEK',week+1)
		print('Press 1 to play next round')
		print('Press 2 to check the Table')
		print('Press 3 to view your team')
		print('Press 4 to view your whole squad')
		print('Press 5 to view your youth team')
		print('Press 6 to change first team')
		print('Press "x" to exit')
		x = input()
		if(x==str(1)):
			playGames(fixtures[week])
			week+=1
			for i in teams:
				i.update()
				i.calculateTeamRating()
			if(week==22):
				youthIntake(teams)
		if(x==str(2)):
			showTable(teams)
		if(x==str(3)):
			playerTeam.printBestTeam()
		if(x==str(4)):
			playerTeam.printAllPlayers()
		if(x==str(5)):
			playerTeam.printYouthTeam()
		if(x==str(6)):
			playerTeam.customSelect()
		if(x=='x'):
			break



	print('FINAL TABLE')
	showTable(teams)
	return 0

if __name__ == '__main__':
	main()
