import requests
from bs4 import BeautifulSoup
import pandas as pd

for year in range(0, 26):
    URL = f'https://hoopshype.com/salaries/players/{1996 + year}-{1997 + year}/'
    page = requests.get('https://hoopshype.com/salaries/players/1996-1997/')
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="wrapper")
    results = results.find_all("table", class_="hh-salaries-ranking-table hh-salaries-table-sortable responsive")
    for result in results:
        info = result.find("tbody")
        players = {}
        for person in info.find_all("tr"):
            name = person.find("td", class_="name").text.strip()
            salary = person.find("td", style="color:black").text.strip()
            players.update({name: int(salary[1:].replace(',', ''))})
        players_info = pd.DataFrame.from_dict(players, orient='index')
        players_info.to_csv(f'salary/{1996 + year}-{1997 + year}_salary.csv')
            