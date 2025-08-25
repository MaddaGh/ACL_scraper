# class to filter a dataset of conference based on keywords also gives you more info on the dataset
import pandas as pd
import re

class CsvDdata:
    def __init__(self, csv_path):
        self.csv = pd.read_csv(csv_path)

    # function do get percentage of data completeness

    def keyword_filter(self, keywords):
        pattern = r'\b(' + '|'.join(re.escape(k) for k in keywords) + r')\b' # keywords search turned to regex
        
        mask = (self.csv['title'].astype(str).str.contains(pattern, flags=re.IGNORECASE, regex=True) | self.csv['abstract'].astype(str).str.contains(pattern, flags=re.IGNORECASE, regex=True))
        filtered_data = self.csv[mask]
        print(len(filtered_data))
        return(filtered_data)



# exaple use
# keywords = [ "polyvocality", "polyperspectivity", "poliphony", "polysemy", "plurality", "polycentrism", "perspectivism", "multi perspective", "multiplicity", "multivocality"]

# data = CsvDdata("path")
# filtered_data = data.keyword_filter(keywords)

# filtered_data.to_csv("path")