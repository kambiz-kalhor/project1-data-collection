#!/usr/bin/env python
# coding: utf-8

# # importing all the packages we need

# In[7]:


import pandas as pd
from bs4 import BeautifulSoup
import requests
import re


# # STEP ONE download a table from BacDive

# i did it and the result is saved as stage1_step1_export_bacdive_iso_table before cleaning.csv

# # STEP TWO

# read stage1_step1_export_bacdive_iso_table before cleaning.csv

# In[195]:


# read stage1_step1_export_bacdive_iso_table before cleaning.csv
bacDive = pd.read_csv(r"C:\Users\kamy\Desktop\stage1_step1_export_bacdive_iso_table before cleaning.csv")


# In[196]:


bacDive


# In[197]:


# filling the table # replacing NaN with no in three colums (Category 1, Category 2, Category 3)
bacDive["Category 3"].fillna("#no", inplace = True)
bacDive["Category 2"].fillna("#no", inplace = True)
bacDive["Category 1"].fillna("#no", inplace = True) 


# In[198]:


bacDive


# In[199]:


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


# In[200]:


######## we wont need this if we are going to maintain other Tags in future
######## this code is written to remove all the rows without a specific Tag(here : #Environmental)


#temporary_list =[]
#for counter in range (0,len(bacDive.index)):
    #if (bacDive.iloc[counter,6] != '#Environmental') :
        #temporary_list.append(counter)

######## we run this code at the end in order to keep all other category 1 tags 
#for i in temporary_list:
    #bacDive = bacDive.drop([i])


# In[202]:


# now we have a dataframe whithout any tags other than #Environmental  but there are still some redundency, there are some rows with the same Species name
# here the goal is to merge rows with the same Species name


temporary_list =[]
x = len(bacDive['ID'])-1
for counter in range(0,x):
    if bacDive.iloc[counter,0] == bacDive.iloc[counter+1,0]:
        temporary_list.append(counter)
        bacDive.iloc[counter+1,7] = bacDive.iloc[counter,7] +  bacDive.iloc[counter+1,7]
        bacDive.iloc[counter+1,8] = bacDive.iloc[counter,8] +  bacDive.iloc[counter+1,8]
        


# In[203]:


# and now we remove the duplicate row
for i in temporary_list:
    bacDive = bacDive.drop([i])


# In[204]:


bacDive


# In[205]:


bacDive.to_csv(r'C:\Users\kamy\Desktop\stage1_step2_export_bacdive_iso_table cleaned.csv')


# # STEP THREE

# WEB SCRAPING from BacDive

# In[102]:


bacDive = pd.read_csv(r"C:\Users\kamy\Desktop\stage1_step2_export_bacdive_iso_table cleaned.csv")


# In[103]:


bacDive


# In[104]:


# we want to creat URLs using the BacDive IDs
all_IDs = bacDive['ID']

#######################  reducing the size   this step must be removed  ###############
all_IDs = all_IDs[0:10]
######################################################################################


# producing links for web scrapping

# In[105]:


def get_ID_give_URL(ID):
    url = 'https://bacdive.dsmz.de/strain/' + str(ID)
    return url


# In[106]:


def read_html(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    return None
#CODE = 200 means the url is availible


# In[107]:


# in future i should improve this regex # its a regex to find temperature Data
my_regex = re.compile("(Ref\.\:.\#\d+)\]\<\/a\>\<\/td\>\s\<td\>\<\/td\>\s\<td.class\=\"border\_rightfree\ textalign\_right\"\>\<\/td\>\s\<td.class\=\"border\_leftfree\"\>(\w+)\<\/td\>\s\<td.class\=\"border_leftfree textalign_center\"\>(\d{2}\-\d{2}|\d{2}\.\d{1}|\d{2})")


# In[108]:


my_data_frame = pd.DataFrame()


for ID in all_IDs:
    url = get_ID_give_URL(ID)
    html_doc = read_html(url)
    
    
    if html_doc is None:
        print("Something went wrong!!!  the following url seems to be wrong   ; " , url)
    
    soup = BeautifulSoup(html_doc, "lxml")
    list_of_extracted_data = []
    
    
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
    while len(list_of_extracted_data) != 20:
        list_of_extracted_data.append("")
    my_data_frame[ID] = pd.Series(list_of_extracted_data)
    
   


# transpose the dataframe
my_data_frame = my_data_frame.T
# naming columns
my_data_frame = my_data_frame.rename(columns={0: 'Last LPSN update', 1: 'Domain', 2: 'Phylum', 3: 'Class', 4: 'Order', 5: 'Family', 6: 'Genus', 7: 'Species', 8: 'temperature Ref 1', 9: 'temperature Ref 2', 10: 'temperature Ref 3', 11: 'temperature Ref 4', 12: 'temperature Ref 5', 13: 'temperature Ref 6', 14: 'temperature Ref 7'})


# saving the data

# In[54]:


my_data_frame.to_csv(r'C:\Users\kamy\Desktop\webscrapping_output.csv')


# or you can put data together

# In[111]:


# i will do it later in my free time

