import json
import requests
from bs4 import BeautifulSoup


def scrape_countries():
    url = 'https://www.scrapethissite.com/pages/simple/'

    response = requests.get(url)

    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    country_divs = soup.select('div.country')

    country_data = []

    for country_div in country_divs:
        country_name = country_div.select_one('h3.country-name').text.strip()
        country_capital = country_div.select_one('span.country-capital').text.strip()
        country_population = country_div.select_one('span.country-population').text.strip()
        country_area = country_div.select_one('span.country-area').text.strip()

        country_data.append({
            'country_name': country_name,
            'country_capital': country_capital,
            'country_population': country_population,
            'country_area': country_area
        })
    return country_data


if __name__ == '__main__':
    country_data = scrape_countries()
    print(json.dumps(country_data, indent=4))
