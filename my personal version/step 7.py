"""
 ######  ######## ######## ########      ######  ######## ##     ## ######## ##    ##
##    ##    ##    ##       ##     ##    ##    ## ##       ##     ## ##       ###   ##
##          ##    ##       ##     ##    ##       ##       ##     ## ##       ####  ##
 ######     ##    ######   ########      ######  ######   ##     ## ######   ## ## ##
      ##    ##    ##       ##                 ## ##        ##   ##  ##       ##  ####
##    ##    ##    ##       ##           ##    ## ##         ## ##   ##       ##   ###
 ######     ##    ######## ##            ######  ########    ###    ######## ##    ##
 (font banner 3)
"""
########################## importing packages ################################
print('importing packages.............................')
# main packages
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

# using PubMed API
from pymed import PubMed

# using NCBI API
from Bio import Entrez
from Bio import SeqIO
Entrez.email = 'kz.kalhor@gmail.com'
############################## input & output ###############################
print('importing the input........................')

input_path = 'input_for_step_7.csv'
#first_output_path = 'all_availible_seq_not_clean.csv'
final_output = 'all_availible_seq_clean.csv'
#############################################################################
# a def which reads CSV
def read_excell_as_dataFrame(path):
    DataFrame = pd.read_csv(path)
    return DataFrame
first_dataframe = read_excell_as_dataFrame(input_path)




# making some links to extract all availible data from BacDive
def gets_ids_give_BacDive_links(first_dataframe):
    link_part_one = r'https://bacdive.dsmz.de/strain/'
    links_list = []
    for i in first_dataframe['ID']:
        link = link_part_one + str(i)
        links_list.append(link)
    return links_list
links_list = gets_ids_give_BacDive_links(first_dataframe)

## to clean the memory
del first_dataframe

########################## extracting from BacDive ############################

def read_html(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    return None
    #CODE = 200 means the url is availible

my_data_frame = pd.DataFrame()
COUNTER = 0
for url in links_list:
    COUNTER = COUNTER +1
    html_doc = read_html(url)
    if html_doc is None:
        print("Something went wrong!!!  the following url seems to be wrong   ; " , url)
    soup = BeautifulSoup(html_doc, "lxml")


    listm = [url]

    #first step ==> extracting seq data
    tag = "valigntop border padding"
    data = soup.find_all("td", class_= tag)
    for td in data:
        listm.append(td.text)
        print('td is appending ' , COUNTER, '..................')
    # some of the lists contains more than 20 availible seq
    ########################### THIS IS MY HYPER-PARAMETER ##############################
    maximum_lenght_list = 300
    while len(listm) < maximum_lenght_list:
        listm.append('')


    my_data_frame[COUNTER] = pd.Series(listm)


## to clean the memory
del listm
del links_list



# teanspose the dataframe
my_data_frame = my_data_frame.T

# save the dataframe as csv
#print('saving my_data_frame ....................')
#my_data_frame.to_csv(first_output_path)



# this code seperates the sequence colums
print('seperating columns and cleaning data....................')

null = ''
my_new_dataframe = pd.DataFrame()


for i in range(0,len(my_data_frame)):
    print('its runnung...............')
    this_row = []
    for j in range (0, maximum_lenght_list):
        
        if "tax ID" not in str(my_data_frame.iloc[i][j]):
            this_row.append(my_data_frame.iloc[i][j])
            
        if "tax ID" in str(my_data_frame.iloc[i][j]):
            while len(this_row)%7 != 0:
                this_row.append(null)
            this_row.append(my_data_frame.iloc[i][j])

        
        
########################### THIS IS MY HYPER-PARAMETER ##############################
    maximum_lenght_this_row = 400
    while len(this_row) != maximum_lenght_this_row:
        this_row.append(null)
     
    my_new_dataframe[i] = pd.Series(this_row)
            
my_new_dataframe = my_new_dataframe.T

print('datafarme is ready..............')


# this code relocate the tax data
for i in range(0,len(my_new_dataframe)):
    for j in range (0,maximum_lenght_this_row):
        if 'tax' in str(my_new_dataframe.iloc[i][j]):
            my_new_dataframe.iloc[i][j-2] = my_new_dataframe.iloc[i][j]
            my_new_dataframe.iloc[i][j] = ''
                    
print('tax data have been relocated...............')                   
my_new_dataframe.to_csv(final_output)       



print('mission complete')
######################################################################