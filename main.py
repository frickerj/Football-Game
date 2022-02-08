"""This Module Contains items for the game"""

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
    def __init__(self, team_a,team_b,date):
        super(Fixture, self).__init__()
        self.team_a = team_a
        self.team_b = team_b
        self.date = date
        self.place = team_a.home


def advanced_match_engine(fixture):
    """this is the match engine for a fixture"""
    # want to make the game some kind of random walk
    # starts at 0, between -1 and 1
    # when the walk gets to -1 or 1, then a goal is scored
    # we have 90 walks, as the game is 90 minutes
    team_a = fixture.team_a
    team_b = fixture.team_b
    player_view = False
    if team_a.controlled is True or team_b.controlled is True:
        player_view = True
    goal_team_a = 0
    goal_team_b = 0
    initial = 0
    delta = 0
    if team_a.rating>team_b.rating:
        initial =  (team_a.rating/team_b.rating) - 1
        delta = (team_a.rating - team_b.rating) /500
    else:
        initial =  -(team_b.rating/team_a.rating -1)
        delta = -(team_b.rating - team_a.rating) /500

    # team A is the home team and thus recieves a little bonus
    initial += 0.025
    if player_view is True:
        print(team_a.name,"v",team_b.name, "at",team_a.home)
        print(team_a.name," rating is ", team_a.rating)
        print(team_b.name," rating is ", team_b.rating)

    # setup to make sure there are no instant goals
    if initial>0.95:
        initial = 0.95
    elif initial<-0.95:
        initial = -0.95

    state = initial
    #print('Match Start.....')
    for moments in range(91):
        next_state = numpy.random.normal(delta,0.2)
        state+=next_state
        if state>1:
            goal_team_a+=1
            state = initial
            if player_view is True:
                print('GOAL!',team_a.name, "in the", moments,"minute")
                print('Score is: ',goal_team_a,'-',goal_team_b)

        elif state<-1:
            goal_team_b+=1
            state = initial
            if player_view is True:
                print('GOAL!',team_b.name, "in the", moments,"minute")
                print('Score is: ',goal_team_a,'-',goal_team_b)

        #if(player_view == True):
        #    # comment line below when testing
        #    time.sleep(0.1)

    print('End of Game ',team_a.name,"v",team_b.name)
    print("Final Score is: ",goal_team_a,"-",goal_team_b)
    # comment out below when testing
    #
    if player_view is True:
        #time.sleep(2)
        print("**********")

    r_a = 0
    r_b = 0
    if goal_team_a>goal_team_b:
        r_a = 1
        r_b = -1
    elif goal_team_b>goal_team_a:
        r_b = 1
        r_a = -1

    # team A
    team_a.result(r_a,goal_team_a,goal_team_b)
    # team B
    team_b.result(r_b,goal_team_b,goal_team_a)

def create_player(player_type = "senior"):
    """this function creates a player"""
    first_names =  open("data/firstnames.txt", "r",encoding='UTF-8').read().splitlines()
    last_names =  open("data/lastnames.txt", "r",encoding='UTF-8').read().splitlines()

    first = first_names[random.randrange(len(first_names))]
    last = last_names[random.randrange(len(last_names))]
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

def load_team_data():
    """loads the team data from csv file"""
    data = pd.read_csv('data/teams.csv')
    names = data['Team Name']
    home = data['Home']
    return names,home

def create_new_game():
    """creates a new game"""
    names,home = load_team_data()
    team_players = []
    teams_created = 0
    for i in range(20):
        team_players.append(Team(names[i],home[i]))
        gk_count = 0
        player_count=0
        while player_count<23:
            new_player = create_player('senior')
            if new_player.position == "GK":
                gk_count+=1
            team_players[i].add_player(new_player)
            player_count+=1
        while gk_count<2:
            new_player = create_player()
            if new_player.position == "GK":
                team_players[i].add_player(new_player)
                gk_count +=1

        youth_player_count = 0
        while youth_player_count<12:
            new_player = create_player('youth')
            team_players[i].add_youth_player(new_player)
            youth_player_count +=1
        teams_created+=1
        print('Created',teams_created,"Teams")
    return team_players

def get_worst_youth_player(team):
    """gets the worst player in the team
    they will be let go and better youth players
    will be automattically added"""
    while len(team.youth_team)<1:
        team.youth_team.append(Player("",0,"GK",1,1))
    worst_pot = 1000
    worst = 0
    for i in team.youth_team:
        if i.potential<worst_pot:
            worst = i
            worst_pot = i.potential
    return worst

def youth_intake(teams):
    """creates new youth players"""
    print("YOUTH INTAKE!")
    for i in teams:
        youth_player_count = 0
        while youth_player_count <12:
            new_youth_player = create_player('youth')
            k = get_worst_youth_player(i)
            if len(i.youth_team)<12:
                i.add_youth_player(new_youth_player)
                if i.controlled is True:
                    print("Added New Player",new_youth_player.name,
                    "Ability", new_youth_player.ability,
                    "Potential",new_youth_player.potential)
            else:
                if new_youth_player.potential>k.potential:
                    i.youth_team.remove(k)
                    i.add_youth_player(new_youth_player)
                    if i.controlled is True:
                        print("Added New Player",new_youth_player.name,
                        "Ability",new_youth_player.ability,
                        "Potential",new_youth_player.potential)
                        time.sleep(1)
        check_goalkeeper(i)

def check_goalkeeper(team):
    """checks if the team has a gk"""
    has_gk = False
    for j in team.players:
        if j.position=="GK":
            has_gk = True
    if has_gk is False:
        team.players.append(Player("DUMMY",0,"GK",1,1))

def create_fixtures(teams):
    """creates fixtures for the season"""
    # fixtures[round][match][team]
    rounds = (len(teams)-1)*2
    games_per_round = len(teams)//2
    fixtures = [[0 for j in range(games_per_round)] for i in range(rounds)]
    print('Creating ',rounds,"rounds, with ",games_per_round,"games per Round")
    # set first round fixtures
    pos = [k for k in range(len(teams))]
    for i in range(rounds):
        home_away = i%2
        # ha = 1 // home
        # ha = 0 // away
        for j in range(len(teams)//2):
            #print('Accessing teams at',pos[j],pos[len(teams)-j-1])
            # create fixtures
            # need to alternate for fixtures to get home and away correct
            if home_away==0:
                fixtures[i][j] = Fixture(teams[pos[j]],teams[pos[len(teams)-j-1]],i)
            else:
                fixtures[i][j] = Fixture(teams[pos[len(teams)-j-1]],teams[pos[j]],i)
        for k in range(1,len(pos)):
            pos[k]-=1
            if pos[k]==0:
                pos[k]=len(teams)-1
        #print('New Positions: ',pos)
    return fixtures

def print_fixtures(fixtures):
    """prints the fixtures to screen"""
    season_round = 1
    print("PRINTING FIXTURES")
    for i in fixtures:
        print('ROUND ',season_round)
        season_round+=1
        for j in i:
            print(j[0].name,j[1].name)
    return fixtures


def play_games(fixtures_week):
    """plays all games in a round"""
    for game in fixtures_week:
        advanced_match_engine(game)

def show_table(teams):
    """prints out the season table"""
    newlist = sorted(teams, key=lambda x: (x.points,x.goal_difference), reverse=True)
    table = PrettyTable(['P','Team','Played','Won','Drawn','Lost','Points','GF','GA','GD'])
    index = 1
    for i in newlist:
        team_name = i.name
        if i.controlled is True:
            team_name+="**"
        #print(i.name,i.points,i.wins,i.draws,i.losses)
        table.add_row([index,team_name,i.matches_played,i.wins,i.draws,
            i.losses,i.points,i.goalsFor,i.goalsAgainst,i.goal_difference])
        index+=1
    print(table)

def end_of_season(team):
    """this is the end of seasons stats/credits"""
    print("CONGRATULATIONS ON ANOTHER SUCCESSFUL SEASON")
    best = team.players[0]
    for i in team.players:
        if i.ability>best.ability:
            best = i
    talent = team.players[-1]
    for i in team.players:
        if i.age<21 and i.potential>talent.potential:
            talent = i
    print("THE BEST PLAYER IS",
        best.name,best.position,"ABILITY IS",round(best.ability,2))
    time.sleep(5)
    print("THE BEST PROSPECT IS",
        talent.name,talent.position,"POTENTIAL IS",round(talent.potential,2))
    time.sleep(5)

def choose_team(teams):
    """player chooses a team at the start of the season"""
    while True:
        team_user_input = input("Choose a Team To Manage:")
        for i in teams:
            if str(team_user_input) == i.name:
                return i
        print("Incorrect Name Entered")
        print("You Entered ",team_user_input,"and they are not a team")
        print("**************************")


def main():
    """main function to play the game!"""
    print('Program Start')
    #m=tkinter.Tk()
    teams = create_new_game()
    for i in teams:
        i.select_team()
    fixtures = create_fixtures(teams)
    player_team = 0
    season = 0
    for i in teams:
        print(i.name)

    player_team = choose_team(teams)
    player_team.controlled = True

    week = 0
    print("You are managing",player_team.name)
    while True:
        if week == len(fixtures):
            season+=1
            print('END OF SEASON',season)
            player_team.print_all_players()
            show_table(teams)
            end_of_season(player_team)
            print('Reseting Season.....')
            week = 0
            fixtures = create_fixtures(teams)
            for i in teams:
                check_goalkeeper(i)
                i.reset()
            time.sleep(5)
        for i in teams:
            if i != player_team:
                check_goalkeeper(i)
                i.select_team()
        print('WEEK',week+1)
        print('Press 1 to play next round')
        print('Press 2 to check the Table')
        print('Press 3 to view your team')
        print('Press 4 to view your whole squad')
        print('Press 5 to view your youth team')
        print('Press 6 to change first team')
        print('Press "x" to exit')
        user_input = input()
        if user_input==str(1):
            play_games(fixtures[week])
            week+=1
            for i in teams:
                i.update()
                i.calculate_team_rating()
            if week==22:
                youth_intake(teams)
        if user_input==str(2):
            show_table(teams)
        if user_input==str(3):
            player_team.print_best_team()
        if user_input==str(4):
            player_team.print_all_players()
        if user_input==str(5):
            player_team.print_youth_team()
        if user_input==str(6):
            player_team.custom_team_select()
        if user_input=='x':
            break



    print('FINAL TABLE')
    show_table(teams)
    return 0

if __name__ == '__main__':
    main()
