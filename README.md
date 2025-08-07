# ACL_scraper
This repository contains the code to scrape metadata and abstracts of all publications (where such data is found), starting from a list of URL locating proceedings for selected conferences for each year. Publications are then filtered according to given keywords.


## Source data

The data is scraped from URLs of Conference Proceedings, such as [Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics](https://aclanthology.org/volumes/2023.eacl-main/).

These pages contain data for all papers included in the proceedings of the conference.
 
 
## How to run the software
 To reuse the program, please install the requirements.txt:
```sh
pip install -r requirements.txt
```
 Users can run the program by cloning the repository and accessing it from shell. The command to launch the program is:
```sh
python run_workflow.py --keywords keywords_for_filtering --url_to_parse path_to_a_txt_file_with_URLS
```
 All the parameters are already set to default values, however, users can modify them depending on their needs. In case users do not need to specify any parameter, the command is as follows:
 ```sh
python run_workflow.py
``` 
The txt file path set as default is `example_url_to_parse.txt`. This file should take approximately 20 min to run in # add computer specs

The file `full_url_list.txt` include all 113 URLs manually gathered of our conferences of interest for this specific research.<br>
These conferences are:
- ACL
- EMNLP
- NAACL
- EACL
- COLING
- TACL
- CoNLL

At the present moment, it is possible that some data are not successfully retrieved. This is because older conferences didn't necessarily encode metadata in the webpage in the same way, and/or only present the abstract in the pdf file of the Publication. <br>
At the moment the code doesn't keep track of such cases, hopefully it will soon.

## Naming convention of Datasets 

While running the program, the data retrieved are organized in a csv files with the following header:

| title | year | publisher | url | doi | abstract |
|-------|------|-----------|-----|-----|----------|

* **title**: the title of the paper
* **year**: the year of publication
* **publisher**: the publisher of the proceedings, for instance "ELRA and ICCL" or "Association for Computational Linguistics"
* **url**: the URL of the publication page, for instance [Cross-Framework Evaluation for Statistical Parsing](https://aclanthology.org/E12-1006/)
* **doi**: the unique identifier, doi, of the publication
* **abstract**: the abstract of the publication

All Publication retrieved are saved as `ACL_all_data/ACL_data.csv` (the folder `ACL_all_data` is created automatically).<br>
The csv of the Publication filtered according to keywords are saved as `ACL_filtered_data/ACL_filtered_data.csv` (the folder `ACL_filtered_data` is created automatically).

Other csv files, each one representing a single URL scraped, are saved automatically in the folder `conferences_unique_year`, also created automatically. <br>
Each of this file is named after the resource identifier part of the URL, for instance: "https://aclanthology.org/volumes/2023.eacl-main/" generates "2023.eacl-main.csv".<br>
In these files headers depend on what data is retrieved from each bibtex file while running the program, therefore they may vary.

## Planned improvements

- Add Documentation of code
- double check bibtex files syntax and improve how data are extracted (for instance authors' names are now wrong), use bibtexparser (make it an independent class)
- extract missing Abstracts form pdf files
- keep track if some bibtex file is not successfully retrieved in data_extractor.py
- ensure retrials if request to a URL fails
- in CsvData class, upgrade to also accept a dataframe and not only a file path, enabling smoother integration.



