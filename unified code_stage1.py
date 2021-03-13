#!/usr/bin/env python
# coding: utf-8

# # importing all the packages we need

# In[293]:


import pandas as pd
from bs4 import BeautifulSoup
import requests
import re


# # STEP ONE

# download a table from BacDive

# i did it and the result is "saved as stage1_step1_export_bacdive_iso_table before cleaning.csv"

# you can access it in git_hub repository

# # STEP TWO

# read stage1_step1_export_bacdive_iso_table before cleaning.csv

# In[294]:


# read stage1_step1_export_bacdive_iso_table before cleaning.csv
bacDive = pd.read_csv(r"C:\Users\kamy\Desktop\stage1_step1_export_bacdive_iso_table before cleaning.csv")


# In[296]:


# filling the table # replacing NaN with no in three colums (Category 1, Category 2, Category 3)
bacDive["Category 3"].fillna("#no", inplace = True)
bacDive["Category 2"].fillna("#no", inplace = True)
bacDive["Category 1"].fillna("#no", inplace = True) 


# In[298]:


# the reason i used this code is to fill empty cells
# this code means --> check the IDs, if the ID of two consecutive rows are the same than fill the second row with the cells of first row

temporary_list =[]
x = len(bacDive['ID'])-1
for counter in range(0,x):
    if bacDive.iloc[counter,0] == bacDive.iloc[counter+1,0]:
        temporary_list.append(counter)
        bacDive.iloc[counter+1,1] = bacDive.iloc[counter,1]
        bacDive.iloc[counter+1,2] = bacDive.iloc[counter,2]
        bacDive.iloc[counter+1,3] = bacDive.iloc[counter,3]
        bacDive.iloc[counter+1,4] = bacDive.iloc[counter,4]
        bacDive.iloc[counter+1,5] = bacDive.iloc[counter,5]
        
        # we do not need the next code because we want to maintain the Tag data
        #bacDive.iloc[counter+1,7] = bacDive.iloc[counter,7] +  bacDive.iloc[counter+1,7]
        #bacDive.iloc[counter+1,8] = bacDive.iloc[counter,8] +  bacDive.iloc[counter+1,8]


# In[299]:


######## we wont need this if we are going to maintain other Tags in future
######## this code is written to remove all the rows without a specific Tag(here : #Environmental)


#temporary_list =[]
#for counter in range (0,len(bacDive.index)):
    #if (bacDive.iloc[counter,6] != '#Environmental') :
        #temporary_list.append(counter)

######## we run this code at the end in order to keep all other category 1 tags 
#for i in temporary_list:
    #bacDive = bacDive.drop([i])


# In[300]:


# now we have a dataframe whithout any tags other than #Environmental  but there are still some redundency, there are some rows with the same Species name
# here the goal is to merge rows with the same Species name


temporary_list =[]
x = len(bacDive['ID'])-1
for counter in range(0,x):
    if bacDive.iloc[counter,0] == bacDive.iloc[counter+1,0]:
        temporary_list.append(counter)
        bacDive.iloc[counter+1,7] = bacDive.iloc[counter,7] +  bacDive.iloc[counter+1,7]
        bacDive.iloc[counter+1,8] = bacDive.iloc[counter,8] +  bacDive.iloc[counter+1,8]
        


# In[301]:


# and now we remove the duplicate row
for i in temporary_list:
    bacDive = bacDive.drop([i])


# # STEP THREE

# WEB SCRAPING from BacDive

# In[313]:


# we want to creat URLs using the BacDive IDs
all_IDs = bacDive['ID']


# producing links for web scrapping

# In[304]:


def get_ID_give_URL(ID):
    url = 'https://bacdive.dsmz.de/strain/' + str(ID)
    return url


# reading html

# In[305]:


def read_html(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    return None
#CODE = 200 means the url is availible


# In[306]:


# my regex to extract temperature data from BacDive
# in future i should improve this regex # its a regex to find temperature Data
my_regex = re.compile("(Ref\.\:.\#\d+)\]\<\/a\>\<\/td\>\s\<td\>\<\/td\>\s\<td.class\=\"border\_rightfree\ textalign\_right\"\>\<\/td\>\s\<td.class\=\"border\_leftfree\"\>(\w+)\<\/td\>\s\<td.class\=\"border_leftfree textalign_center\"\>(\d{2}\-\d{2}|\d{2}\.\d{1}|\d{2})")


# In[307]:


my_data_frame = pd.DataFrame()


for ID in all_IDs:
    url = get_ID_give_URL(ID)
    html_doc = read_html(url)
    
    
    if html_doc is None:
        print("Something went wrong!!!  the following url seems to be wrong   ; " , url)
    
    soup = BeautifulSoup(html_doc, "lxml")
    list_of_extracted_data = [ID]
    
    
    #first step ==> extracting phylogeny data
    tag = "valigntop paddingright"
    data = soup.find_all("td", class_= tag)
    for td in data:
        list_of_extracted_data.append(td.text)
        if len(list_of_extracted_data) == 9:
            break
        
    #second step ==> extracting temp data
    soup = str(soup)
    temperature_data = my_regex.findall(soup)
    list_of_extracted_data = list_of_extracted_data +temperature_data
    while len(list_of_extracted_data) != 16:
        list_of_extracted_data.append("")
    my_data_frame[ID] = pd.Series(list_of_extracted_data)
    
   


# transpose the dataframe
my_data_frame = my_data_frame.T
# naming columns
my_data_frame = my_data_frame.rename(columns={0: 'ID',  1: 'Last LPSN update', 2: 'Domain', 3: 'Phylum', 4: 'Class', 5: 'Order', 6: 'Family', 7: 'Genus', 8: 'Species', 9: 'Full Scientific Name (PNU)', 10: 'temperature Ref 1', 11: 'temperature Ref 2', 12: 'temperature Ref 3', 13: 'temperature Ref 4', 14: 'temperature Ref 5', 15: 'temperature Ref 6', 16: 'temperature Ref 7'})


# # STEP FOUR

# another cleaning and filling step

# In[308]:


# fill the cells and replacing "NaN" with "#no"
# this will clean the dataframe for future use
my_data_frame["temperature Ref 1"].fillna("#no", inplace = True)
my_data_frame["temperature Ref 2"].fillna("#no", inplace = True)
my_data_frame["temperature Ref 3"].fillna("#no", inplace = True)
my_data_frame["temperature Ref 4"].fillna("#no", inplace = True)
my_data_frame["temperature Ref 5"].fillna("#no", inplace = True)
my_data_frame["temperature Ref 6"].fillna("#no", inplace = True)


# In[309]:


#### in order to know the species with no temperature data  ####
list_index_no_temp = []
list_no_temp_species_ID = []

for counter in range (0,len(my_data_frame)):
    if (my_data_frame.iloc[counter,10] == "#no"):
        list_index_no_temp.append(counter)
        list_no_temp_species_ID.append(my_data_frame.iloc[counter,0])
        
# give me an overview please
print('until now, there are', str(len(list_no_temp_species_ID)) , 'species with no temperature data and you can see the list of IDs with no temp data in this: list_no_temp_species_ID')


# # STEP FIVE

# concat all the previous dataframes and producing an output

# In[312]:


# making to dataframes look the same , so we can use concat()
s = pd.Series(range(len(bacDive)))
new_bac = new_bac.set_index([s])
###########################################
s = pd.Series(range(len(my_data_frame)))
my_data_frame = my_data_frame.set_index([s])
###########################################
result = pd.concat([new_bac, my_data_frame], axis=1)
###########################################
result.to_csv(r'C:\Users\kamy\Desktop\final_output_of_stage1.csv')

