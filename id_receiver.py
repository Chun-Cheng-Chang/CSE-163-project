from nba_api.stats.endpoints import leaguedashteamstats
import json
import requests
import pandas as pd

teams = json.loads(requests.get(
    'https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)
players = json.loads(requests.get(
    'https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)


class IDReceive:

    def get_team_id(queried_team):
        for team in teams:
            if team['teamName'] == queried_team:
                return team['teamId']
        return -1


    def get_player_id(first, last):
        for player in players:
            if player['firstName'] == first and player['lastName'] == last:
                return player['playerId']
        return -1