# this class takes a url and describes method to get the full html corresponding to that url

import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, url: str):
        self.url = url 
        self.soup = None
        self.conference_name = url.split("/")[-2] # gets the name of the conference from the url, or the code used by ACL to identify it


    def _is_valid_url(self) -> bool: # Check if the URL starts with http or https.
        return self.url.startswith("http") # returns True or False

    def parse(self) -> bool: # validate the URL, and requests the html, returns a beautifulSoup object

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.google.com/',
            'DNT': '1',  # Do Not Track
        }

        if not self._is_valid_url():
            raise ValueError(f"Invalid URL: {self.url}. All URLs must start with 'http'.")
        try:
            response = requests.get(self.url, headers=headers)
            # returns False if status != 200
            if response.status_code != 200:
                return False

            html_content = response.text
            #print(response.status_code, response.text[:1000])  # Print first 1000 characters of the response for debugging
            self.soup = BeautifulSoup(html_content, "html.parser") # soup is the url html 
            print(f"Scraped: {self.url}")
            return True

        except requests.RequestException as e:
            print(f"Error fetching {self.url}: {e}")
            self.soup = None
            return False
    
# example use

# scraper = WebScraper("https://aclanthology.org/volumes/2023.eacl-main/") # initializes object
# print(scraper.soup) # tries to access the html, should be none
# print(scraper.parse()) # calls the parse method that returns true or false after scraping the webpage
# print(scraper.soup) # tries to access the html, should be the html page as a string
# save html as txt
# with open('html.txt', 'w', encoding="utf-8") as output:
    # output.write(str(scraper.soup))

