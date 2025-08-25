from ACL_web_scraper import WebScraper
from ACL_url_manager import URLManager
from data_extractor import DataExtractor
from keyword_filter import CsvDdata
import pandas as pd
import os
# import argparse

def main(keywords, url_to_parse):
    os.makedirs("conferences_unique_year", exist_ok=True) # make the dir to save data from each conference year separately
    os.makedirs("ACL_all_data", exist_ok=True) # make the dir to save data from all conferences
    os.makedirs("ACL_filtered_data", exist_ok=True) # make the dir to save data after filtering conferences

    no_abstract_url = []
    bib_not_found = []

    url_manager = URLManager(url_to_parse)
    url_list = url_manager.get_urls()
    url_count = url_manager.get_url_count()
    print("number of URLs to be parsed:  " + str(url_count)) 

    all_data = pd.DataFrame()

    for url in url_list:
        scraper = WebScraper(url) # initializes scraper
        conf = scraper.conference_name
        state_scraper = scraper.parse() # gets the html
        if not state_scraper:
            continue 
        html = scraper.soup
        extractor = DataExtractor(html, conf, True)
        state_extractor = extractor.extract_data()
        abstract_bool = extractor.abs_bool
        bib_not_found.extend(extractor.bib_link_not_found)
        data = extractor.data

        # code to catch the urls where there is no abstract found
        if not abstract_bool:
            no_abstract_url.append(url)

        if state_extractor: # check if the dataset is not empty
            # saver the data from a single URL in csv
            data.to_csv(f"conferences_unique_year/{conf}.csv", index=False, encoding="utf-8")
            # save dataset info

            with open(f"conferences_unique_year/{conf}_stats.txt", "w") as f:
                data.info(buf=f)    
                f.write("\n\n--- Describe ---\n\n")
                f.write(str(data.describe(include="all")))
                

            all_data = pd.concat([all_data, data]) # concatenating the data from different conferences

        # if the html and data has been succesfully retrieved, the url gets removed from url_list and the count of urls in the list is printed, the parsed url is also added to the parsed url list
        if state_scraper and state_extractor: 
            url_manager.remove_url() 
            url_count = url_manager.get_url_count()
            print("number of left URLs to be parsed:  " + str(url_count))  # prints the urls left to parse
        
        # add part of code that tries again to parse the url if it failed
        # print(all_data)

    all_data = all_data[["title", "year", "publisher", "url", "doi", "abstract"]]
    all_data.to_csv("ACL_all_data/ACL_data.csv", index=False, encoding="utf-8") # saving a complete csv with ALL unfiltered publication

    # load all data csv
    all_data = CsvDdata("ACL_all_data/ACL_data.csv")
    filtered_data = all_data.keyword_filter(keywords)
    filtered_data.to_csv(f"ACL_filtered_data/ACL_filtered_data.csv", index=False, encoding="utf-8") # saving a complete csv with filtered publication

    # print unretrieved data
    print(no_abstract_url)
    print(bib_not_found)


# all variables

keywords = [ "polyvocality", "polyperspectivity", "poliphony", "polysemy", "plurality",
        "polycentrism", "perspectivism", "multi perspective", "multiplicity", "multivocality"]

url_to_parse = "example_url_to_parse.txt"

if __name__ == "__main__":
    main(keywords, url_to_parse)


'''if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--keywords", nargs="+", default=["polyvocality", "polyperspectivity", "poliphony", "polysemy", "plurality", "polycentrism", "perspectivism", "multi perspective", "multiplicity", "multivocality"], help="Space-separated list of keywords. Example: --keywords polyvocality poliphony")
    parser.add_argument("--url_to_parse", default="example_url_to_parse.txt", type=str, required=True, help="the path to the file containing the url to parse")
 
    args = parser.parse_args()
    main(args)



'''




