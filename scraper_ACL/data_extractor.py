# class defining methods to extract the chosen data from the html. It is initialised with a list of html strings
import pandas as pd
import requests
from ACL_web_scraper import WebScraper
import re

class DataExtractor:
    def __init__(self, html_soup, conference_name, abstract_bool):
        self.html = html_soup
        self.data = None # is going to be the dataframe
        self.conference_name = conference_name
        self.abs_bool = abstract_bool
        self.bib_link_not_found = []  # bib list to save uncresolved links

    def extract_data(self):
        bibtex_data = pd.DataFrame() # empty dataframe
        abstract_data =pd.DataFrame()

     
        

        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com/',
        'DNT': '1',  # Do Not Track
        } # maybe put as global var ?

        for bib_link in self.html.find_all('a', class_='badge badge-secondary align-middle mr-1', href=True): # returns a list with ALL the bib urls and iterates over them
            # code could go in a class to manage bib files
            if 'bib' in bib_link.get('href'):
                bib_file = bib_link.get('href') # gets a specific part of the html where the bib link is
                # print(bib_file)
                bib_resolve = requests.get(f"https://aclanthology.org{bib_file}", headers=headers, timeout=20) # FIX 
                # print(bib_resolve.status_code, bib_resolve.text[:1000])
                if bib_resolve.status_code != 200:
                    self.bib_link_not_found.append(bib_file)
                    continue

                bib_dictionary = {}
                bib_dictionary["bib_url"] = bib_file # adds the bib file url as ID in the dictionary
                # gets the paper id with regular expressions
                id_match = re.search(r'(\d+)$', str(bib_file.split(".")[-2])) 
                # print(id_match.group(1) if id_match else None)
                # adds paper id to the dictionary
                bib_dictionary["ID"] = id_match.group(1)

                for line in bib_resolve.text.split("\n"):
                    if line.startswith('@') or line.startswith('}'):
                        continue
                    elif ' = ' in line:
                        # split the line into key and value
                        key, value = line.split(' = ', 1) # adding spaces around = and the maxsplit parameter to ensure the string is only splitted in two and random = in urls don't cause more splits
                        # remove any leading or trailing whitespace and quotes
                        key = key.strip()
                        value = value.strip().strip('{}"')
                        # add the key-value pair to the dictionary
                        bib_dictionary[key] = value    

                # concatenates the dictionary as a new row in the bib entries dataframe
                bibtex_data = pd.concat([bibtex_data, pd.DataFrame([bib_dictionary])], ignore_index=True)
        print(bibtex_data) # print the full dataframe

                
        # get abstract from <div class="card bg-light mb-2 mb-lg-3 collapse abstract-collapse" id=abstract-2024--eacl-long--1><div class="card-body p-3 small">abstract </div></div>
        for abstract in self.html.find_all('div', class_='card bg-light mb-2 mb-lg-3 collapse abstract-collapse'):
            # get the abstract id at every iteration (abstract entry)
            abstract_id = abstract.get('id')

            abstract_dictionary = {}

            abstr_id_match = re.search(r'(\d+)$', str(abstract_id.split("--")[-1])) 
            # print(abstr_id_match.group(1) if abstr_id_match else None)
            # adds paper id to the dictionary
            abstract_dictionary["ID"] = abstr_id_match.group(1)
            
            if abstract.find('div', class_='card-body p-3 small'):
                abstract_text = abstract.find('div', class_='card-body p-3 small').text.strip()
                abstract_dictionary["abstract"] = abstract_text

                abstract_data = pd.concat([abstract_data, pd.DataFrame([abstract_dictionary])], ignore_index=True)
        print(abstract_data)

        if not abstract_data.empty: # if the dataframe with abstracts is not empty
            self.abs_bool = True
            self.data = pd.merge(bibtex_data, abstract_data, on="ID", how="inner")
            # print(self.data)
            return True
        elif not bibtex_data.empty: # if the dataframe with abstracts is empty
            self.abs_bool = False
            bibtex_data["abstract"] = pd.NA # adds the empty abstract column so that it can be concatenated
            self.data = bibtex_data
            return True
        elif bibtex_data.empty:
            self.abs_bool = False
            return False
       

# function to change headers?

# example use

# first need a WebScraper object
# scraper = WebScraper("https://aclanthology.org/volumes/2023.eacl-main/")
# scraper.parse()
# html = scraper.soup

# extractor = DataExtractor(html, "eacl", True)
# print(extractor.extract_data())
# data = extractor.data
# data.to_csv("eacl_data.csv", index=False, encoding="utf-8")