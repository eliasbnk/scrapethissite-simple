# Countries of the World: A Simple Example - Walkthrough
> walkthrough for the web-scrapping exercise found on https://www.scrapethissite.com
## Step 0: Install necessary dependencies
### - Step 0.1: Create a virtual environment:
```bash 
python -m venv venv
```


### - Step 0.2: Activate the virtual environment:

***Windows***:	
```bash
venv\Scripts\activate
```

***Mac/Linux***:
```bash
source venv/bin/activate
```
### - Step 0.3: Install dependencies:
```bash
pip install requests beautifulsoup4
```
* * *
## Step 1: Get the Webpage HTML
Start by fetching the HTML content of the target webpage. We'll use the `requests` library to do this.

```python
import requests

# Define the URL of the webpage
url = 'https://www.scrapethissite.com/pages/simple/'

# Send a GET request to fetch the webpage content
response = requests.get(url)

# Extract the HTML content from the response
html_content = response.text
```
* * *
## Step 2: Spot HTML Patterns

Inspect the HTML structure for any recurring patterns. It appears that each country's data is contained within `<div>` elements having the class ``"country"``.

```html
<div class="col-md-4 country">
    <h3 class="country-name">
        <i class="flag-icon flag-icon-af"></i>
        Afghanistan
    </h3>
    <div class="country-info">
        <strong>Capital:</strong> <span class="country-capital">Kabul</span><br>
        <strong>Population:</strong> <span class="country-population">29,121,286</span><br>
        <strong>Area (km<sup>2</sup>):</strong> <span class="country-area">647,500.0</span><br>
    </div>
</div>
<!--.col-->

<div class="col-md-4 country">
    <h3 class="country-name">
        <i class="flag-icon flag-icon-ai"></i>
        Anguilla
    </h3>
    <div class="country-info">
        <strong>Capital:</strong> <span class="country-capital">The Valley</span><br>
        <strong>Population:</strong> <span class="country-population">13,254</span><br>
        <strong>Area (km<sup>2</sup>):</strong> <span class="country-area">102.0</span><br>
    </div>
</div>
<!--.col-->
```
* * *
## Step 3: Parse the HTML

We'll use ``BeautifulSoup``, to parse the HTML content and make it ready for extraction.

```python
from bs4 import BeautifulSoup

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')
```
* * *
## Step 4: Extract the Data

Having identified the pattern, we can gather all `<div>` elements with the class ``"country"`` as individual datasets. Then, we'll loop through each dataset and extract details like country name, capital, population, and area.

```python
# Find all <div> elements with the class "country"
country_divs = soup.select('div.country')

# Iterate through each <div> element for data extraction
for country_div in country_divs:

    # Extract country name
    country_name = country_div.select_one('h3.country-name')

    # gets:

    # <h3 class="country-name">
    #     <i class="flag-icon flag-icon-ad"></i>
    #     Andorra
    # </h3>

    # We only need the text:

    country_name = country_name.text

    # returns:

    # Andorra

    # But with extra whitespace

    # We can remove the extra whitespace:

    country_name = country_name.strip()

    # returns:

    # Andorra

    # Without any extra whitespace

    # We can achieve clean text extraction in a single line by appending the .text.strip() methods.
    # For example, to extract the country capital, we can write:

    # Extract country capital
    country_capital = country_div.select_one('span.country-capital').text.strip()

    # This line not only selects the country capital element but also extracts its text content
    # and removes any leading or trailing whitespace, ensuring clean and properly formatted data.

    # Extract country population
    country_population = country_div.select_one('span.country-population').text.strip()

    # Extract country area
    country_area = country_div.select_one('span.country-area').text.strip()
```

* * *
### Put it all together:
```python
import json # optional, added for output formating
import requests
from bs4 import BeautifulSoup

url = 'https://www.scrapethissite.com/pages/simple/'

response = requests.get(url)

html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

country_divs = soup.select('div.country')

country_data = []

# note [:5], only will extract first 5 countries
for country_div in country_divs[:5]:
    
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

# you can just do:
# print(country_data)

# but this will output the country_data, with indentation
print(json.dumps(country_data, indent=4))

```
### Outputs:
```json
[
    {
        "country_name": "Andorra",
        "country_capital": "Andorra la Vella",
        "country_population": "84000",
        "country_area": "468.0"
    },
    {
        "country_name": "United Arab Emirates",
        "country_capital": "Abu Dhabi",
        "country_population": "4975593",
        "country_area": "82880.0"
    },
    {
        "country_name": "Afghanistan",
        "country_capital": "Kabul",
        "country_population": "29121286",
        "country_area": "647500.0"
    },
    {
        "country_name": "Antigua and Barbuda",
        "country_capital": "St. John's",
        "country_population": "86754",
        "country_area": "443.0"
    },
    {
        "country_name": "Anguilla",
        "country_capital": "The Valley",
        "country_population": "13254",
        "country_area": "102.0"
    }
]
```