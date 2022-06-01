from nba_api.stats.endpoints import leaguedashteamstats
import json
import pandas as pd


def main():
    for year in range(0, 26):
        team_json = leaguedashteamstats.LeagueDashTeamStats(
            season=f'{1996 + year}-{str(1996 + year + 1)[2:]}')

        team_data = json.loads(team_json.get_json())
        relevant_data = team_data['resultSets'][0]
        headers = relevant_data['headers']
        rows = relevant_data['rowSet']

        total = pd.DataFrame(rows)
        total.columns = headers
        total = total[['TEAM_ID', 'TEAM_NAME', 'GP', 'W_PCT']]

        total.to_csv(
            f'past_win_pct/{1996 + year}-{str(1997 + year)[2:]}' +
            '_winning_rate.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    main()
