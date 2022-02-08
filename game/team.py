"""class for teams in game"""
import time
from prettytable import PrettyTable


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
        self.goals_for = 0
        self.goals_against = 0
        self.goal_difference = 0
        self.matches_played = 0
        self.players = []
        self.best_team = []
        self.youth_team = []
        self.youth_team_best = []


    def reset(self):
        # reset
        # used for end of season usually
        self.points = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.goals_for = 0
        self.goals_against = 0
        self.goal_difference = 0
        self.matches_played = 0
        self.youth_team.sort(key=lambda x: x.potential, reverse=True)
        self.players.sort(key=lambda x: x.potential, reverse=True)
        if self.controlled is True:
            self.promote_players()
        else:
            p = self.youth_team[0]
            k = self.players[-1]
            while p.potential>k.potential and len(self.youth_team)>0:
                self.players.remove(k)
                self.players.append(p)
                self.youth_team.remove(p)
                p = self.youth_team[0]
                k = self.players[-1]
        for i in self.youth_team:
            if i.age>20:
                self.youth_team.remove(i)
        for i in self.players:
            i.end_of_season()
        for i in self.youth_team:
            i.end_of_season()

        # fill up team
        while len(self.players)<26 and len(self.youth_team)>0:
            p = self.youth_team[0]
            self.players.append(p)
            self.youth_team.remove(p)
        for i in self.players:
            if i.retired is True:
                if self.controlled is True:
                    print(i.name, "Retired at age ",i.age)
                self.players.remove(i)
        self.players.sort(key=lambda x: x.ability, reverse=True)

    def promote_players(self):
        k = 0
        while k!="x":
            self.print_youth_team()
            print("CHOOSE WHICH PLAYERS TO PROMOTE")
            print("ENTER THE NUMBER")
            print("TYPE x TO EXIT")
            k = input()
            if str(k)=="x":
                break
            if int(k)>0 and int(k)<=len(self.youth_team):
                p = self.youth_team[int(k)-1]
                self.print_all_players()
                print("CHOOSE PLAYER TO REMOVE")
                print("ENTER THE NUMBER")
                print("TYPE x TO EXIT")
                h = input()
                print(h)
                if str(h)=="x":
                    break
                if int(h)>0 and int(h)<=len(self.players):
                    r = self.players[int(h)-1]
                    self.players.remove(r)
                    self.players.append(p)
                    self.youth_team.remove(p)
                    print(r.name, "was sacked!")
                    print(p.name, "was promoted!")
                else:
                    h = input("Enter correct number")
            else:
                k = input("Enter correct number")


    def goal_difference_calc(self):
        self.goal_difference = self.goals_for-self.goals_against


    def result(self,match_result,goals_for,goals_against):
        # result r
        # 1 = win
        # 0 = draw
        # -1 = loss
        self.goals_for += goals_for
        self.goals_against += goals_against
        self.matches_played+=1
        self.goal_difference_calc()

        if(match_result not in [-1,0,1]):
            print("INCORRECT RESULT INPUT")

        if match_result==1:
            self.wins+=1
            self.points+=3
        if match_result==0:
            self.draws +=1
            self.points+=1
        if match_result==-1:
            self.losses+=1

    def add_player(self,player):
        self.players.append(player)

    def add_youth_player(self,player):
        self.youth_team.append(player)

    def select_team(self):
        self.players = sorted(self.players,key=lambda x: x.ability, reverse=True)
        self.best_team = []

        all_players = []
        for i in self.youth_team:
            all_players.append(i)
        for j in self.players:
            all_players.append(j)
        gk = []
        defe = []
        mid = []
        att = []
        for i in all_players:
            if i.position == "GK":
                gk.append(i)
            if i.position == "DEF":
                defe.append(i)
            if i.position =="MID":
                mid.append(i)
            if i.position == "ATT":
                att.append(i)

        gk.sort(key=lambda x: x.ability, reverse=True)
        defe.sort(key=lambda x: x.ability, reverse=True)
        mid.sort(key=lambda x: x.ability, reverse=True)
        att.sort(key=lambda x: x.ability, reverse=True)

        self.best_team.append(gk[0])
        if len(defe)>0:
            for i in range(min(3,len(defe))):
                self.best_team.append(defe[i])
        if len(mid)>0:
            for i in range(min(2,len(mid))):
                self.best_team.append(mid[i])
        if len(att)>0:
            for i in range(min(1,len(att))):
                self.best_team.append(att[i])


        #print(self.best_team[0].name,self.best_team[0].position,self.best_team[0].ability)
        self.players = sorted(self.players,key=lambda x: x.ability, reverse=True)
        while len(self.best_team)<11 and len(self.players)>10:
            for j in self.players:
                if j not in self.best_team and j.position!="GK":
                    self.best_team.append(j)
                    break
        self.calculate_team_rating()

    def calculate_team_rating(self):
        s = 0
        for i in self.best_team:
            s+=i.ability
        self.rating = round(s/11,2)

    def print_best_team(self):
        c = 1
        t = PrettyTable(['Index','Name','Age','Position','Ability','Potential'])
        self.best_team.sort(key=lambda x: x.position, reverse=True)
        for i in self.best_team:
            #print(i.name,i.points,i.wins,i.draws,i.losses)
            t.add_row([c,i.name,i.age,i.position,round(i.ability,2),round(i.potential,2)])
            c+=1
        print(t)
        print('Team Ability is ', self.rating)

    def print_all_players(self):
        c = 1
        all_players_table = PrettyTable(['Index','Name','Age','Position','Ability','Potential'])
        for i in self.players:
            #print(i.name,i.points,i.wins,i.draws,i.losses)
            n = i.name
            if i in self.best_team:
                n+=("**")
            all_players_table.add_row([c,n,i.age,i.position,round(i.ability,2),round(i.potential,2)])
            c+=1
        print(all_players_table)
        print('Team Ability is ', self.rating)

    def update(self):
        for i in self.players:
            i.update()
        for i in self.youth_team:
            i.update()
        if self.controlled is True:
            for i in self.best_team:
                if i.age<21:
                    i.potential+=0.1

        self.calculate_team_rating()

    def print_youth_team(self):
        self.youth_team.sort(key=lambda x: x.potential, reverse=True)
        c = 1
        t = PrettyTable(['Index','Name','Age','Position','Ability','Potential'])
        for i in self.youth_team:
            #print(i.name,i.points,i.wins,i.draws,i.losses)
            t.add_row([c,i.name,i.age,i.position,round(i.ability,2),round(i.potential,2)])
            c+=1
        print(t)

    def custom_team_select(self):
        k = ""
        while k!="x" :
            self.print_all_players()
            print("CHOOSE WHICH PLAYERS TO SWAP IN")
            print("ENTER THE NUMBER")
            print("TYPE x TO EXIT")
            print("TYPE s TO AUTO SELECT")
            k = input()
            if str(k)=="x" :
                break
            if str(k)=="s" :
                self.select_team()
                print("Team has been auto selected!")
                time.sleep(1)
                break
            if int(k)>0 and int(k)<=len(self.players):
                p = self.players[int(k)-1]
                print("YOU CHOSE: ",p.name)
                self.print_best_team()
                print("CHOOSE PLAYER TO SWAP OUT")
                print("ENTER THE NUMBER")
                print("TYPE x TO EXIT")
                h = input()
                print(h)
                if str(h)=="x":
                    break
                if int(h)>0 and int(h)<=len(self.best_team):
                    r = self.best_team[int(h)-1]
                    self.best_team.remove(r)
                    self.best_team.append(p)
                    print(r.name, "was put into the reserves!")
                    print(p.name, "was placed into the first team!")
                else:
                    h = input("Enter correct number")
            else:
                k = input("Enter correct number")
        self.calculate_team_rating()
    