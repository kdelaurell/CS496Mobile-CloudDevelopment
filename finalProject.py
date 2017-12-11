import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import ast
import json

class Team(ndb.Model):
    id = ndb.TextProperty()
    teamName = ndb.TextProperty()
    teamCity = ndb.TextProperty()
    teamCaptain = ndb.TextProperty()
    arenaName = ndb.TextProperty()
    players = ndb.TextProperty(repeated=True)
    namedPlayers = ndb.TextProperty

class Players(ndb.Model):
    id = ndb.TextProperty()
    firstName = ndb.TextProperty()
    lastName = ndb.TextProperty()
    position = ndb.TextProperty()
    assignedTeam = ndb.BooleanProperty()


class TeamHandler(webapp2.RequestHandler):
        def get(self):
                team_query = Team.query()
                teamList = []
                for team in team_query:
                    teamList.append(team.to_dict())
                self.response.write(json.dumps(teamList))

        def post(self):
                team_data = json.loads(self.request.body)
                new_team = Team(teamName = team_data['teamName'], teamCity = team_data['teamCity'], arenaName = team_data['arenaName'])
                new_team.put()
                new_team.id = new_team.key.urlsafe()
                new_team.put()
                team_dict = new_team.to_dict()
                self.response.status = 201
                self.response.write(json.dumps(team_dict))

class TeamsHandler(webapp2.RequestHandler):
    def get(self, id=None):
        if id:
            team = ndb.Key(urlsafe=id).get()
            playerList = []
            for player in team.players:
                new_player = ndb.Key(urlsafe=player).get()
                playerList.append(new_player.firstName + new_player.lastName)
                
            team_d = team.to_dict()
            self.response.write(json.dumps(team_d))

    def delete(self, id=None):
        if id:
            team = ndb.Key(urlsafe=id).get()
            team.key.delete()


class PlayersHandler(webapp2.RequestHandler):
    def get(self):
        players_query = Players.query()
        playerList = []
        for player in players_query:
            playerList.append(player.to_dict())
        self.response.write(json.dumps(playerList))

    def post(self):
        player_data = json.loads(self.request.body)
        new_player = Players(firstName = player_data['firstName'], lastName = player_data['lastName'], position = player_data['position'], assignedTeam = True)
        player_team = player_data['assignedTeam']
        new_player.put()
        new_player.id = new_player.key.urlsafe()
        new_player.put()
        player_dict = new_player.to_dict()
        team = ndb.Key(urlsafe=player_team).get()
        print team
        team.players.append(new_player.id)
        team.put()
        self.response.status = 201
        self.response.write(json.dumps(player_dict))

class PlayerHandler(webapp2.RequestHandler):
    def get(self, id=None):
        if id:
            player = ndb.Key(urlsafe=id).get()
            player_d = player.to_dict()
            self.response.write(json.dumps(player_d))

    def delete(self, id=None):
        if id:
            player = ndb.Key(urlsafe=id).get()
            player.key.delete()


app = webapp2.WSGIApplication([
    ('/teams', TeamHandler),
    ('/players', PlayersHandler),
    ('/teams/(.*)', TeamsHandler),
    ('/player/(.*)', PlayerHandler)
], debug=True)
