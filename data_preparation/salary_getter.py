import requests
from bs4 import BeautifulSoup
import pandas as pd


def main():
    for year in range(0, 25):
        URL = 'https://hoopshype.com/salaries/players/' + \
            f'{1996 + year}-{1997 + year}/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="wrapper")
        results = results.find_all("table", class_="hh-salaries-ranking-tabl" +
                                   "e hh-salaries-table-sortable responsive")
        for result in results:
            info = result.find("tbody")
            players = {}
            for person in info.find_all("tr"):
                name = person.find("td", class_="name").text.strip()
                salary = person.find("td", style="color:black").text.strip()
                players.update({name: int(salary[1:].replace(',', ''))})
            players_info = pd.DataFrame.from_dict(players, orient='index')
            players_info.to_csv('data_preparation/salary/' +
                                f'{1996 + year}-{1997 + year}' +
                                '_salary.csv')

    URL = 'https://hoopshype.com/salaries/players/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="wrapper")
    results = results.find_all("table", class_="hh-salaries-ranking-table" +
                               " hh-salaries-table-sortable responsive")

    for result in results:
        info = result.find("tbody")
        players = {}
        for person in info.find_all("tr"):
            name = person.find("td", class_="name").text.strip()
            salary = person.find("td", class_="hh-salaries-sorted") \
                .text.strip()
            players.update({name: int(salary[1:].replace(',', ''))})
        players_info = pd.DataFrame.from_dict(players, orient='index')
        players_info.to_csv('data_preparation/salary/2021-2022_salary.csv')


if __name__ == "__main__":
    main()
