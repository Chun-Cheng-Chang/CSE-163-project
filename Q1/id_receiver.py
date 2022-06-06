"""
IDReceive class allows to translate ID to name and vice versa, for both
teams and players.
"""

import json
import requests

teams = json.loads(requests.get(
    'https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json')
    .text)
players = json.loads(requests.get(
    'https://raw.githubusercontent.com/bttmly/nba/master/data/players.json')
    .text)


class IDReceive:
    def get_team_id(queried_team):
        """
        Get the team id from the team name.
        """
        for team in teams:
            if team['teamName'] == queried_team:
                return team['teamId']
        return -1

    def get_team_name(queried_team_id):
        """
        Get the team name from the team id.
        """
        for team in teams:
            if team['teamId'] == queried_team_id:
                return team['teamName']
        return -1

    def get_player_id(first, last):
        """
        Get the player id from the player name.
        """
        for player in players:
            if player['firstName'] == first and player['lastName'] == last:
                return player['playerId']
        return -1

    def get_player_name(player_id):
        """
        Get the player name from the player id.
        """
        for player in players:
            if player['playerId'] == player_id:
                return player['firstName'] + '_' + player['lastName']
        return -1
