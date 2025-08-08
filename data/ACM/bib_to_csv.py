# code to transform a bib file into a csv 

"""
@inproceedings{10.1145/3706599.3719747,
author : {Pang, Rock Yuren and Maheshwari, Rohit and Yu, Julie and Reinecke, Katharina},
title : {Synthetic Conversation: How Computing Researchers Engage Multi-Perspective Dialogues to Brainstorm Societal Impacts},
year : {2025},
isbn : {9798400713958},
publisher : {Association for Computing Machinery},
address : {New York, NY, USA},
url : {https://doi.org/10.1145/3706599.3719747},
doi : {10.1145/3706599.3719747},
abstract : {There have been increasing calls for computing researchers to consider the negative societal impacts of their work. However, anticipating these impacts remains challenging, as computing researchers often do not have access to diverse perspectives. Here, we explore how computing researchers brainstorm the negative societal impacts of computing innovations using a multi-agent dialog prototype called Weaver as a probe that represents synthetic stakeholder conversations. Through think-aloud sessions and interviews with 12 participants, we evaluate how computing researchers perceive and engage with such a system, and whether they find it beneficial compared to using no such system or using ChatGPT. Our findings revealed that participants valued the conversations with the multi-agent system and considered societal impacts from new angles. Participants reported gaining insights and agency to reflect on issues rather than passively consuming pre-generated content. We discuss the findings, implications, and next steps for using a multi-agent system to brainstorm about the societal impacts of computing technologies.},
booktitle : {Proceedings of the Extended Abstracts of the CHI Conference on Human Factors in Computing Systems},
articleno : {497},
numpages : {7},
keywords : {Multi-agent systems, Brainstorming, Human-AI Interaction, LLM},
location : {
},
series : {CHI EA '25}
}
"""
import pandas as pd
from pprint import pprint
import os

# get the bib file path as a list
def get_bib_file_path(directory):
    bib_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.bib'):
                bib_files.append(os.path.join(root, file))
    return bib_files

def convert_bib_to_csv(bib_file):
    # initialize empty dataframe
    bib_dataframe = pd.DataFrame()
    bib_dictionary = {}
    count = 0
    # print(len(bib_dataframe))
    with open(bib_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            # remove leading and trailing whitespace
            line = line.strip() 
            # standard case where there is a new entry to append
            if line.startswith('@') and count > 0:
                # create a new row from the current bib entry by concatenation the row and returns the updated dataframe
                bib_dataframe = new_row_from_bib(bib_dictionary, bib_dataframe)
                count = len(bib_dataframe) # update the count to the current length of the dataframe
            # case where a line of bibtex file is not a new entry ex. the firt line '@inproceedings' or parenthesis due to formatting issues
            elif line.startswith('@') and count == 0 or line.startswith('}'):
                # skip the line
                count += 1
                continue
            # case where a line is a key-value pair, check that there's a key walue pair
            elif '=' in line:
                # split the line into key and value
                key, value = line.split(' = ', 1) # adding spaces around = and the maxsplit parameter to ensure the string is only splitted in two and random = in urls don't cause more splits
                # remove any leading or trailing whitespace and quotes
                key = key.strip()
                value = value.strip().strip('{}"')
                # add the key-value pair to the dictionary
                bib_dictionary[key] = value
                # print(bib_dictionary)
            else:
                print('unexpected line format:', line)
                continue
        # print(len(bib_dataframe), bib_dataframe)

        bib_dataframe = bib_dataframe.applymap(lambda x: x.rstrip('},') if isinstance(x, str) and x.endswith('},') else x)
        bib_dataframe.to_csv(f"{bib_file[:-4]}.csv", index=False)  # save the dataframe to a csv file

# script to add rows to the dataframe
def new_row_from_bib(dictionary, dataframe):
    dataframe = pd.concat([dataframe, pd.DataFrame([dictionary])], ignore_index=True)
    return dataframe

# print(new_row_from_bib({'author' :  'Pang, Rock Yuren and Maheshwari, Rohit and Yu, Julie and Reinecke, Katharina','title' : 'Synthetic Conversation: How Computing Researchers Engage Multi-Perspective Dialogues to Brainstorm Societal Impacts','year' : '2025', 'isbn' : '9798400713958','publisher' : 'Association for Computing Machinery','address' : 'New York, NY, USA','url' : 'https://doi.org/10.1145/3706599.3719747','doi' : '10.1145/3706599.3719747','abstract' : 'There have been increasing calls for computing researchers to consider the negative societal impacts of their work. However, anticipating these impacts remains challenging, as computing researchers often do not have access to diverse perspectives. Here, we explore how computing researchers brainstorm the negative societal impacts of computing innovations using a multi-agent dialog prototype called Weaver as a probe that represents synthetic stakeholder conversations. Through think-aloud sessions and interviews with 12 participants, we evaluate how computing researchers perceive and engage with such a system, and whether they find it beneficial compared to using no such system or using ChatGPT. Our findings revealed that participants valued the conversations with the multi-agent system and considered societal impacts from new angles. Participants reported gaining insights and agency to reflect on issues rather than passively consuming pre-generated content. We discuss the findings, implications, and next steps for using a multi-agent system to brainstorm about the societal impacts of computing technologies.','booktitle' : 'Proceedings of the Extended Abstracts of the CHI Conference on Human Factors in Computing Systems','articleno' : '497','numpages' : '7','keywords' : 'Multi-agent systems, Brainstorming, Human-AI Interaction, LLM','location' : '','series' : 'CHI EA 25'}, pd.DataFrame()))
# print(convert_bib_to_csv(bib_file))
# bib_files = get_bib_file_path('RAW_DATA\CHI.bib')
print(convert_bib_to_csv('path_to_bib_file'))