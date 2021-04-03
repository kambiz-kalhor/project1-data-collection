#!/usr/bin/env python
# coding: utf-8

# # for the dear user

# In[2]:


# please give me the string of path for the file "stage1_step1_export_bacdive_iso_table before cleaning.csv"
# for example  --->   r'C:\Users\kamy\Desktop\stage1_step1_export_bacdive_iso_table before cleaning.csv'
input_path = r'C:\Users\kamy\Desktop\INPUT.csv'


# and again please give me the output path to save the final result
output_path = r'C:\Users\kamy\Desktop\OUTPUT.csv'

# this is another output which includes all_availible_seq_in_Bacdive
second_output = r"C:\Users\kamy\Desktop\all_availible_seq_in_Bacdive.csv"


# # importing all the packages we need

# In[3]:


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


# # STEP ONE

# download a table from BacDive

# i did it and the result is "saved as stage1_step1_export_bacdive_iso_table before cleaning.csv"

# this file is our input and we rename it as 'INPUT.CSV'

# you can access it in git_hub repository

# # STEP TWO

# read stage1_step1_export_bacdive_iso_table before cleaning.csv

# In[17]:


# read stage1_step1_export_bacdive_iso_table before cleaning.csv
bacDive = pd.read_csv(input_path)


# In[18]:


# filling the table # replacing NaN with no in three colums (Category 1, Category 2, Category 3)
bacDive["Category 3"].fillna("#no", inplace = True)
bacDive["Category 2"].fillna("#no", inplace = True)
bacDive["Category 1"].fillna("#no", inplace = True) 


# In[19]:


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


# In[20]:


######## we wont need this if we are going to maintain other Tags in future
######## this code is written to remove all the rows without a specific Tag(here : #Environmental)


#temporary_list =[]
#for counter in range (0,len(bacDive.index)):
    #if (bacDive.iloc[counter,6] != '#Environmental') :
        #temporary_list.append(counter)

######## we run this code at the end in order to keep all other category 1 tags 
#for i in temporary_list:
    #bacDive = bacDive.drop([i])


# In[21]:


# now we have a dataframe whithout any tags other than #Environmental  but there are still some redundency, there are some rows with the same Species name
# here the goal is to merge rows with the same Species name


temporary_list =[]
x = len(bacDive['ID'])-1
for counter in range(0,x):
    if bacDive.iloc[counter,0] == bacDive.iloc[counter+1,0]:
        temporary_list.append(counter)
        bacDive.iloc[counter+1,7] = bacDive.iloc[counter,7] +  bacDive.iloc[counter+1,7]
        bacDive.iloc[counter+1,8] = bacDive.iloc[counter,8] +  bacDive.iloc[counter+1,8]
        


# In[22]:


# and now we remove the duplicate row (consecutive duplicated rows only)
for i in temporary_list:
    bacDive = bacDive.drop([i])


# In[23]:


# removing the repeated species 
list_of_Indexes = []

new_list_of_IDs =[]
for i in bacDive.index:
    if bacDive.loc[i,'ID'] not in new_list_of_IDs:
        new_list_of_IDs.append(bacDive.loc[i,'ID'])
    else:
        list_of_Indexes.append(i)
        
        
bacDive = bacDive.drop(list_of_Indexes)

#################################################################
# i found a wired flaw in BacDive database : here in this code we remove the rows with the same species name 
# the result is a dataframe with 8681 row
# now if we remove the rows with the same ID, the result will be a dataframe with 18040 rows
# this means that there are some species with the same name but with different ID
#################################################################


# # STEP THREE

# WEB SCRAPING from BacDive

# In[24]:


# we want to creat URLs using the BacDive IDs
all_IDs = bacDive['ID']


# producing links for web scrapping

# In[25]:


def get_ID_give_URL(ID):
    url = 'https://bacdive.dsmz.de/strain/' + str(ID)
    return url


# reading html

# In[26]:


def read_html(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    return None
#CODE = 200 means the url is availible


# In[27]:


# my regex to extract temperature data from BacDive
# in future i should improve this regex 
my_regex_temperature = re.compile("(Ref\.\:.\#\d+)\]\<\/a\>\<\/td\>\s\<td\>\<\/td\>\s\<td.class\=\"border\_rightfree\ textalign\_right\"\>\<\/td\>\s\<td.class\=\"border\_leftfree\"\>(\w+)\<\/td\>\s\<td.class\=\"border_leftfree textalign_center\"\>(\d{2}\-\d{2}|\d{2}\.\d{1}|\d{2})")

# my regex to extract pH data from BacDive
# in future i should improve this regex 
x=str('(Ref\.\:.\#\d+)\]\<\/a\>\<\/td\>\\n\<td\>\<\/td\>\\n\<td\sclass=\"border\_rightfree\stextalign\_right\"\>\<\/td\>\\n\<td\sclass=\"border\_leftfree\"\>(\w+)\<\/td\>\\n\<td\sclass=\"valigntop\sborder\stextalign\_center\"\>(\d+\.\d+\-\d\.\d+)')
my_regex_pH = re.compile(x)


# In[28]:


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
    temperature_data = my_regex_temperature.findall(soup)
    list_of_extracted_data = list_of_extracted_data +temperature_data
    while len(list_of_extracted_data) != 16:
        list_of_extracted_data.append("")
    
    
    
    #third step ==> extracting phylogeny data
    
    soup = str(soup)
    pH_data = my_regex_pH.findall(soup)
    list_of_extracted_data = list_of_extracted_data + pH_data
    while len(list_of_extracted_data) != 22:
        list_of_extracted_data.append("")
    my_data_frame[ID] = pd.Series(list_of_extracted_data)
    
   


# transpose the dataframe
my_data_frame = my_data_frame.T
# naming columns
my_data_frame = my_data_frame.rename(columns={0: 'ID',  1: 'Last LPSN update', 2: 'Domain', 3: 'Phylum', 4: 'Class', 5: 'Order', 6: 'Family', 7: 'Genus', 8: 'species', 9: 'temperature Ref 1', 10: 'temperature Ref 2', 11: 'temperature Ref 3', 12: 'temperature Ref 4', 13: 'temperature Ref 5', 14: 'temperature Ref 6', 15: 'temperature Ref 7', 16: 'pH 1', 17: 'pH 2', 18: 'pH 3', 19: 'pH 4', 20: 'pH 5', 21: 'pH 6'})


# # STEP FOUR

# another cleaning and filling step

# In[29]:


# fill the cells and replacing "NaN" with "#no"
# this will clean the dataframe for future use
my_data_frame["temperature Ref 1"].fillna("#no", inplace = True)
my_data_frame["temperature Ref 2"].fillna("#no", inplace = True)
my_data_frame["temperature Ref 3"].fillna("#no", inplace = True)
my_data_frame["temperature Ref 4"].fillna("#no", inplace = True)
my_data_frame["temperature Ref 5"].fillna("#no", inplace = True)
my_data_frame["temperature Ref 6"].fillna("#no", inplace = True)
my_data_frame["temperature Ref 7"].fillna("#no", inplace = True)
my_data_frame["pH 1"].fillna("#no", inplace = True)
my_data_frame["pH 2"].fillna("#no", inplace = True)
my_data_frame["pH 3"].fillna("#no", inplace = True)
my_data_frame["pH 4"].fillna("#no", inplace = True)
my_data_frame["pH 5"].fillna("#no", inplace = True)
my_data_frame["pH 6"].fillna("#no", inplace = True)


# In[30]:


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

# In[31]:


# making to dataframes look the same , so we can use concat()
s = pd.Series(range(len(bacDive)))
bacDive = bacDive.set_index([s])
###########################################
s = pd.Series(range(len(my_data_frame)))
my_data_frame = my_data_frame.set_index([s])
###########################################
result = pd.concat([bacDive, my_data_frame], axis=1)

###########################################
#result.to_csv(output_path)


# # STEP SIX

# in this step we want to collect some data using PubMed API

# creating queries to download the species

# In[32]:


list_of_species = result['Species']
list_of_IDs = result['ID']

#this code is because we have to ID columns in the result dataframe --> i should remove it in the future
list_of_IDs = list_of_IDs.iloc[:,1]


# we dont need this step here

# In[33]:


# removing the repeated species  (no need)
#new_list_of_species =[]
#for i in list_of_species:
    #if i not in new_list_of_species:
        #new_list_of_species.append(i)
        
#list_of_species = new_list_of_species


# # our regexes to extract pH and optimum pH (bad regex)

# In[64]:


######################################## regexes to find pH  #############################################################

regex1 = r'[^p].[^i][^m][^u][^m].pH (\d\d?)[^\.][^\d]'                                          # pH 4
regex2 = r'[^p].[^i][^m][^u][^m].pH of (\d\d?\.?\d?\d?)\-?(\d?\d?\.?\d?\d?) '                   # pH of 7-11   #pH of 7
regex3 = r'[^p].[^i][^m][^u][^m].pH (\d\d?\.\d?\d?)'                                            # pH 4.54 
regex4 = r'[^p].[^i][^m][^u][^m].pH (\d\d?\.?\d?\d?) to (\d\d?\.?\d?\d?)'                       # pH 4.54 to 5.32
regex5 = r'[^p].[^i][^m][^u][^m].pH (\d\d?\.?\d?\d?) and (\d\d?\.?\d?\d?)'                      # pH 4.54 and 5.32
regex6 = r'[^p].[^i][^m][^u][^m].pH (\d\d?\.?\d?\d?) and pH (\d\d?\.?\d?\d?)'                   # pH 3.23 and pH 6.5
regex7 = r'[^p].[^i][^m][^u][^m].pH (\d\d?\.?\d?\d?)\-(\d\d?\.?\d?\d?)'                         # pH 5.33-4.23
regex8 = r'[^p].[^i][^m][^u][^m].pH of the medium was adjusted to (\d\d?\.?\d?\d?)'             # pH of the medium was adjusted to 6.4
regex9 = r'[^p].[^i][^m][^u][^m].pH range.+?from (\d\d?\.?\d?\d?) to (\d\d?\.?\d?\d?)'          # pH range for growth at 70 "C was from 4.4 to 7.5
regex10 = r'[^p].[^i][^m][^u][^m].pH range.+?from (\d\d?\.?\d?\d?) to pH (\d\d?\.?\d?\d?)'      # pH range for growth at 70 "C was from 4.4 to pH 7.5
regex11 = r'[^p].[^i][^m][^u][^m].pH range.+?from (\d\d?\.?\d?\d?) to pH (\d\d?\.?\d?\d?)'      # pH range 6-9
regex12 = r'from pH (\d\d?\.?\d?\d?) to (\d\d?\.?\d?\d?)'                                       # from pH 5?5 to 7?0
regex13 = r'from pH (\d\d?\.?\d?\d?) to pH (\d\d?\.?\d?\d?)'                                    # from pH 5?5 to pH 7?0
regex14 = r'[^p].[^i][^m][^u][^m].pH from (\d\d?\.?\d?\d?) to pH (\d\d?\.?\d?\d?)'              # pH from 5?5 to pH 7?0
regex15 = r'[^p].[^i][^m][^u][^m].pH from (\d\d?\.?\d?\d?) to (\d\d?\.?\d?\d?)'                 # pH from 5?5 to 7?0
regex16 = r'[^p].[^i][^m][^u][^m].pH values of (\d\d?\.?\d?\d?)\-(\d\d?\.?\d?\d?)'              # pH values of 4.8–5.8
regex17 = r'[^p].[^i][^m][^u][^m].pH values.+?(\d\d?\.?\d?\d?)\-(\d\d?\.?\d?\d?)'               # pH values (4.8–5.8)
regex18 = r'[^p].[^i][^m][^u][^m].pH values of (\d\d?\.?\d?\d?)'                                # pH values of 4.8
regex19 = r'pH values ranging from (\d\d?\.?\d?\d?)[ toand\-or]+?(\d\d?\.?\d?\d?)'              # pH values ranging from 7.5 to 9.0
regex20 = r'[^p].[^i][^m][^u][^m].pH around (\d\d?\.?\d?\d?)\-(\d\d?\.?\d?\d?)'                 # pH around 6.0–6.5
regex21 = r'[^p].[^i][^m][^u][^m].pH around (\d\d?\.?\d?\d?)'                                   # pH around 6.0
regex22 = r'[^p].[^i][^m][^u][^m].pH growth range (\d\d?\.?\d?\d?)\-(\d\d?\.?\d?\d?)'           # pH growth range 3.5-6.4
regex23 = r'[^p].[^i][^m][^u][^m].pH range for growth[is was for of]+?(\d\d?\.?\d?\d?)\-(\d\d?\.?\d?\d?)'    # the pH range for growth of 2.0-6.0  # the pH range for growth is 2.0-6.0   # the pH range for growth was 2.0-6.0
regex24 = r'[^p].[^i][^m][^u][^m].pH between (\d\d?\.?\d?\d?) and (\d?\d?\.?\d?\d?)'                         # pH between 7.5 and 10.5 (optimum 8.8-9)
regex25 = r'[^m][^u][^m] pH\(\d\d.+?\).+?(\d\d?\.?\d?\d?)[ -andorto]+?(\d?\d[\.]\d?\d?)'                     #The pH(60 degrees C) range for growth was 4.0-8.0


######################################## regexes to find optimum pH  #############################################################


reggex1 = r'(optimum) pH (\d\d?\.?\d?\d?)'                                  #optimum pH 5.6
reggex2 = r'(optimum) pH (\d\d?\.?\d?\d?)'                                  #optimum pH 5.6
reggex3 = r'(optimum) pH (\d\d?\.?\d?\d?)\-(\d\d?\.?\d?\d?)'                #optimum pH 5.6-6.5
reggex4 = r'(optimum) pH (\d\d?\.?\d?\d?) or (\d\d?\.?\d?\d?)'              #optimum pH 5.6 or 6.5
reggex5 = r'(optimum) pH (\d\d?\.?\d?\d?) and (\d\d?\.?\d?\d?)'             #optimum pH 5.6 and 6.5
reggex6 = r'(optimum) at pH (\d\d?\.?\d?\d?)'                               #optimum at pH 7.25
reggex7 = r'(optimum), pH (\d\d?\.?\d?\d?)\-?(\d?\d?\.?\d?\d?)'             #optimum, pH 8.0-9.0
reggex8 = r'(optimum) pH was (\d\d?\.?\d?\d?)'                              #optimum pH was 2.3
reggex9 = r'(optimum) pH was (\d\d?\.?\d?\d?)\-(\d\d?\.?\d?\d)'             #optimum pH was 2.3-9.2
reggex10 = r'growing (optimally) at pH (\d\d?\.?\d?\d?)\-(\d\d?\.?\d?\d?)'  #growing optimally at pH 3.5-4.0
reggex11 = r'ptimum pH around (\d\d?\.?\d?\d?)'                             #optimum pH around 6.0
reggex12 = r'ptimum pH of the medium was adjusted to (\d\d?\.?\d?\d?)'                        #optimum pH of the medium was adjusted to 6.4
reggex13 = r'ptimum pH range.+?from (\d\d?\.?\d?\d?) to (\d\d?\.?\d?\d?)'                     #optimum pH range for growth at 70 "C was from 4.4 to 7.5
reggex14 = r'ptimum pH range.+?from (\d\d?\.?\d?\d?) to pH (\d\d?\.?\d?\d?)'                  #optimum pH range for growth at 70 "C was from 4.4 to pH 7.5
reggex15 = r'[^p].[^i][^m][^u][^m].pH range (\d\d?\.?\d?\d?)[ toand\-or]+?(\d\d?\.?\d?\d?)'   #from optimum pH 5?5 to 7?0
reggex16 = r'from optimum pH (\d\d?\.?\d?\d?) to (\d\d?\.?\d?\d?)'                            #from optimum pH 5?5 to 7?0
reggex17 = r'from optimum pH (\d\d?\.?\d?\d?) to pH (\d\d?\.?\d?\d?)'                         #from optimum pH 5?5 to pH 7?0
reggex18 = r'ptimum pH from (\d\d?\.?\d?\d?) to pH (\d\d?\.?\d?\d?)'                          #optimum pH from 5?5 to pH 7?0
reggex19 = r'ptimum pH values of (\d\d?\.?\d?\d?)\-(\d\d?\.?\d?\d?)'                          #optimum pH values of 4.8–5.8
reggex20 = r'ptimum pH values.+?(\d\d?\.?\d?\d?)\-(\d\d?\.?\d?\d?)'                           #optimum pH values (4.8–5.8)
reggex21 = r'ptimum pH values of (\d\d?\.?\d?\d?)'                                            #optimum pH values of 4.8 
reggex22 = r'ptimum pH around (\d\d?\.?\d?\d?)\-(\d\d?\.?\d?\d?)'                             #optimum pH around 6.0–6.5
reggex23 = r'ptimum pH around (\d\d?\.?\d?\d?)'                                               #optimum pH around 6.0
reggex24 = r'ptimum pH growth range (\d\d?\.?\d?\d?)\-(\d\d?\.?\d?\d?)'                       #optimum pH growth range 3.5-6.4
reggex25 = r'ptimum pH range for growth of (\d\d?\.?\d?\d?)\-(\d\d?\.?\d?\d?)'                #optimum the pH range for growth of 2.0-6.0
reggex26 = r'pH growth range \d\d?\.?\d?\d?\-\d\d?\.?\d?\d?.?.?.?.?.?(optimum).*?(\d\d?\.?\d?\d?)\-(\d\d?\.?\d?\d)'            #(pH growth range 3.5-6.4; optimum, 4.0-4.5) than strain KA1(T)
reggex27 = r'pH range for growth of \d\d?\.?\d?\d?\-\d\d?\.?\d?\d \(with an (optimum) at (\d\d?\.?\d?\d?)\-?(\d?\d?\.?\d?\d?)' #the pH range for growth of 2.0-6.0 (with an optimum at 3.8)
reggex28 = r'The (optimum) growth temperature and pH were found to be \d\d?\.?\d?\d?-\d\d?\.?\d?\d?.+?and (\d\d?\.?\d?\d?)-(\d\d?\.?\d?\d?).+?respectively'
#The optimum growth temperature and pH were found to be 25-30 °C and 5.0-7.0, respectively
reggex29 = r'(optimal) pH of (\d\d?\.?\d?\d?)-(\d\d?\.?\d?\d?)'      #optimal pH of 6-8
reggex30 = r'pH between \d\d?\.?\d?\d? and \d?\d?\.?\d?\d? \((optimum) (\d\d?\.?\d?\d?)\-(\d?\d?\.?\d?\d?)'
reggex31 = r'(optimum) pH for growth was (\d\d?\.?\d?\d?)'           #optimum pH for growth was 9.5
reggex32 = r'(optimum) pH for growth was (\d\d?\.?\d?\d?)[ toand\-or]+?(\d\d?\.?\d?\d?)'
#optimum pH for growth was 9.5 to 3.43   #optimum pH for growth was 9.5 and 8.4    #optimum pH for growth was 9.5-3.4    #optimum pH for growth was 9.5 or 3.2
reggex33 = r'(optimum).pH was between (\d\d?\.?\d?\d?)[ toand\-or]+?(\d\d?\.?\d?\d?)'
reggex34 = r'pH range for growth[is was for of]+?\d\d?\.?\d?\d?\-\d\d?\.?\d?\d?.+?(optimum) (\d\d?\.?\d?\d?)\-?(\d?\d?\.?\d?\d?)'
reggex35 = r'(optimum) pH[ isbetween,;:was]+(\d\d?\.?\d?\d?)[ \-andto]+(\d\d?\.?\d?\d?)'    #optimum pH between 7.0 and 8.5
reggex36 = r'(optimum) pH[ isbetween,;:was]+(\d\d?\.?\d?\d?)'
reggex37 = r'temperature and pH for (optimum) growth were \d+[^\d]+(\d\d?\.?\d?\d?)' #The temperature and pH for optimum growth were 30 °C and 7.5



#####################################  make a list of regexes   #################################################
bad_regexes = [regex1,regex2,regex3,regex4,regex5,regex6,regex7,regex8,regex9,regex10,regex11,regex12,regex13,regex14,regex15,regex16,regex17,regex18,regex19,regex20,regex21,regex22,regex23,regex24,regex25,      reggex1,reggex2,reggex3,reggex4,reggex5,reggex6,reggex7,reggex8,reggex9,reggex10,reggex11,reggex12,reggex13,reggex14,reggex15,reggex16,reggex17,reggex18,reggex19,reggex20,reggex21,reggex22,reggex23,reggex24,reggex25,reggex26,reggex27,reggex28,reggex29,reggex30,reggex31,reggex32,reggex33,reggex34,reggex35,reggex36,reggex37]


# # more advanced kind of regex

# In[65]:


general_regex_for_pH =r'(?: from | range |)(?:(?:(optimally)|(optimum)|(optimal)|(optima)|growth|(?#next step is because we dont want and/to/or before our pH))(?: |, | at |)pH(?:s|)(?: growth|)(?: (optimal)| (optimum)| (optima)|(?: |)\(\d.*?(?:C|c).*?\) ?|(?: |)\(\d.*?degrees.*?\) ?| range| ranged| |))(?:(?:(?: for.+?|)|(?: growth|)(?:| range(?:| for growth)| values))(?:(?: was| were| is| are)(?:.{0,30}?)|)(?:| of| at| approximately| around| between| from| ranging from)| of the medium was adjusted to)(?#from here its about digits)(?:(?: |\(| \(|)(?#here is the first pH)((?:[1][01234]|[0-9])(?:\.\d|\.\d\d|))(?:(?#here is the seperators)(?: |–|\-| to | and | or | and pH | or pH | to pH |\-pH | and pH| or pH| to pH|\-pH)(?#here is the second pH)((?:[1][01234]|[0-9])(?:\.\d|\.\d\d|))|))(?#end of digits)(?#what comes after pH digits)(?:.{0,20}(optimum)(?#from here is the optimum that sometimes comes at the end of the main part, so from now the main sentence is finished)(?:(?#from here its about digits)(?:(?#here is the first pH)(?:.{0,10}?((?:[1][01234]|[0-9])(?:\.\d|\.\d\d|)))(?:(?#here is the seperators)(?: |–|\-| to | and | or | and pH | or pH | to pH |\-pH )(?#here is the second pH)((?:[1][01234]|[0-9])(?:\.\d|\.\d\d|))|)))|)(?#end of digits)(?#what comes after pH digits)(?=(?:\)|,|;|:| |\.))(?![c|C|°|d|%]| [c|C|°|d|%]|  [c|C|°|d|%])'
other_regexes = r'(neutral) pH|(neutral to alkaline) pH'

advanced_regexes = [general_regex_for_pH, other_regexes]


# # last resort regex for the missing data

# In[66]:


# this needs to be checked
last_resort =r'(?:(opti).{0,40}|)pH.{0,80}?(?:(optimally)|(optimum)|(optimal)|(optima)|).{0,20}?\D((?:[1][01234]|[0-9])(?:\.\d|\.\d\d|))(?:(?#here is the seperators)(?: |–|\-| to | and | or | and pH | or pH | to pH |\-pH )(?#here is the second pH)((?:[1][01234]|[0-9])(?:\.\d|\.\d\d|))|)(?=(?:\)|,|;|:| |\.\D))(?![c|C|°|d|%]| [c|C|°|d|%]|  [c|C|°|d|%])'

last_regexes = [last_resort]


# # first regex for temperature data

# In[67]:


first_version = r'(?: |\()(\d\d|\d)(?:(?:(?:c|C|°|degrees)|.(?:c|C|°|degrees)|..(?:c|C|°|degrees))|)(?:(?: |–|\-| to | and | or | and pH | or temperature | to temperature | temperature )(\d\d|\d)|)(?:(?:c|C|°|degrees)|.(?:c|C|°|degrees)|..(?:c|C|°|degrees))(?!%|.%|..%|\d|\w)'
first_temperature_regex = [first_version]


# # my def

# In[68]:


# this def gets an species name and gives a string(query) which we can later use to search pubmed
# here we want "nov" to be in our title ----> nov means
# we want pH to be in either Title or Abstract

def make_pubmed_advance_search_query(species_name):
    query = '((' + str(species_name) + '[Title]) AND (nov[Title])) AND (pH[Title/Abstract])'
    
    return (query)


# In[69]:


# this def gets a string(query include species name) and gives an abstract using pubmed API

def get_abstract_from_pubmed(query):
    
    # Create a PubMed object that GraphQL can use to query
    # Note that the parameters are not required but kindly requested by PubMed Central
    # https://www.ncbi.nlm.nih.gov/pmc/tools/developers/
    pubmed = PubMed(tool="MyTool", email="kz.kalhor@gmail.com")

    # Execute the query against the API
    results = pubmed.query(query, max_results=500)

    # Loop over the retrieved articles
    for article in results:

        # Extract and format information from the article
        article_id = article.pubmed_id
        title = article.title
        if article.keywords:
            if None in article.keywords:
                article.keywords.remove(None)
            keywords = '", "'.join(article.keywords)
        publication_date = article.publication_date
        abstract = article.abstract


        # # make a file for the next step
        result_of_search = (
            f'{article_id} - {publication_date} - {title}\n \n{abstract}\n'
        )
        
        return(result_of_search)
        
        


# In[88]:


# with this function I remove unicode characters
# in future i had to learn a better way to remove this characters ---> finally i made it better at 30 march 2021
# remmember that in future you can add other characters you dont want to be removed

def get_abstract_make_changes(abstract):
    abstract = re.sub("[^a-zA-Z0-9 ,;%:°.\-\(\)\–\_]+", "" ,abstract)
    return(abstract)


# In[89]:


# this def gets an Abstract and gives an important sentence which includes pH
# this step is not neccessary but i need it because i want to check the results using this sentences

def find_sentence_with_pH_data(abstract):
    the_sentence_about_pH = None
    # a is where the pH is located in the text
    if 'pH' in abstract:
        a = abstract.index('pH')
        # here we selecte the surrounding text
        s = abstract[a-300:a+300]
        # spliting the right sentence
        x = s.split(". ")
        for i in range(0,len(x)):
            if 'pH' in x[i]:
                the_sentence_about_pH = x[i].replace('\u2009', ' ')  # this code removes a unicode problem

        return (the_sentence_about_pH)


# In[90]:


# this def gets an Abstract and gives an important sentence which includes temperature
# this step is not neccessary but i need it because i want to check the results using this sentences

def find_sentence_with_temerature_data(abstract):
    the_sentence_about_temerature = None
    # a is where the temerature is located in the text
    if 'temperature' in abstract:
        a = abstract.index('temperature')
        # here we selecte the surrounding text
        s = abstract[a-300:a+300]
        # spliting the right sentence
        x = s.split(". ")
        for i in range(0,len(x)):
            if 'temperature' in x[i]:
                the_sentence_about_temerature = x[i].replace('\u2009', ' ')  # this code removes a unicode problem

        return (the_sentence_about_temerature)


# In[91]:


# the final def to search for whatever information we want from a string
# the string can be either the pH sentence or the complete abstract
# it gets the 'pH_sentence' and gives a list of what_regex_find

def get_sentence_give_pH_data(pH_sentence):
    regexes = regexes_pH
    pH_sentence = str(pH_sentence)    #I did this because of an error
    what_regex_found = []
    for regex in regexes:
        
        
        what_is_found = re.findall(regex, pH_sentence)
        if what_is_found != []:
            what_regex_found.append(what_is_found)
        
    return (what_regex_found)

# this code needs a list of regexes
# it gets a sentence as an imput
# the output is a list of what regex found


# In[92]:


# the final def to search for whatever information we want from a string
# the string can be either temerature sentence or the complete abstract
# it gets the 'the_sentence_about_temerature' and gives a list of what_regex_find

def get_sentence_give_temperature_data(the_sentence_about_temerature):
    regexes = first_temperature_regex
    the_sentence_about_temerature = str(the_sentence_about_temerature)    #I did this because of an error
    what_regex_found = []
    for regex in regexes:
        
        
        what_is_found = re.findall(regex, the_sentence_about_temerature)
        if what_is_found != []:
            what_regex_found.append(what_is_found)
        
    return (what_regex_found)

# this code needs a list of regexes
# it gets a sentence as an imput
# the output is a list of what regex found


# # assemble all the pervious codes

# In[93]:


#first tell me which regex do you want to use??

#regexes_pH = bad_regexes
regexes_pH = advanced_regexes
#regexes_pH = last_regexes


regexes_temperature = first_temperature_regex


# In[96]:


#make a data frame for final storage
df = pd.DataFrame(columns = ['ID', 'species_name' ,  'query' ,  'abstract' ,   'pH_sentence' , 'what_regexss_found_pH', 'the_sentence_about_temerature','what_regexss_found_temperature'])
# this list help me to find specied with no record
list_of_species_with_no_record = []

for i in range(0,len(list_of_species)):
    ID = list_of_IDs[i]
    species_name = list_of_species[i]
    
    
    
    query = make_pubmed_advance_search_query(species_name)
    abstract = get_abstract_from_pubmed(query)
    

    if abstract is None:                  #this occurs when there is no search result for a query
        list_of_species_with_no_record.append(species_name)
        pH_sentence = '---'
        what_regexss_found_pH = '---'
        the_sentence_about_temerature = '---'
        what_regexss_found_temperature = '---'
        

    if abstract is not None:
        abstract = get_abstract_make_changes(abstract)
        
        
        
        pH_sentence = find_sentence_with_pH_data(abstract)
        the_sentence_about_temerature = find_sentence_with_temerature_data(abstract)
        what_regexss_found_pH = get_sentence_give_pH_data(pH_sentence)
        what_regexss_found_temperature = get_sentence_give_temperature_data(the_sentence_about_temerature)



    #print (species_name , "===================" , query , "++++++++++++++++++++", abstract , "******************" , pH_sentence , ">>>>>>>>>>>>>>>" , what_regex_found)
    #print (pH_sentence , ">>>>>>>>>>>>>>>" , what_regexss_found)

    #making lists and finally a dataframe
    list_data = [ID, species_name , query , abstract , pH_sentence ,  what_regexss_found_pH,the_sentence_about_temerature, what_regexss_found_temperature]
    while len (list_data) != 8:
        list_data.append(' ')
    #print(list_data)

    data_series = pd.Series(list_data,index = df.columns)
    df = df.append(data_series, ignore_index=True) 

#we dont need this output
#df.to_csv(r'C:\Users\kamy\Desktop\final_df.csv')


# In[97]:


print('hi! , using PubMed API we found' , len(list_of_species)-len(list_of_species_with_no_record) , 'species with some records and we extracted the data we need , but there is still ', str(len(list_of_species_with_no_record)) , 'species without any records')


# In[98]:


# putting all the data together
all_data_together = pd.concat([result, df], axis=1)
######################################################
# save the output
all_data_together.to_csv(output_path)


# In[ ]:





# In[ ]:





# # STEP SEVEN

# what are the availible seq data according to BacDive????

# In[12]:


all_data_together = pd.read_csv(r'C:\Users\kamy\Desktop\OUTPUT.csv')


# In[15]:


#making some links to extract all availible data from BacDive

link_part_one = r'https://bacdive.dsmz.de/strain/'
links_list = []
for i in all_data_together['ID']:
    link = link_part_one + str(i)
    links_list.append(link)


# In[16]:


# extracting from BacDive

all_urls = links_list

def read_html(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    return None
    #CODE = 200 means the url is availible



my_data_frame = pd.DataFrame()
COUNTER = 0
for url in all_urls:
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
    # some of the lists contains more than 20 availible seq
    ########################### THIS IS MY HYPER-PARAMETER ##############################
    maximum_lenght_list = 200
    while len(listm) < maximum_lenght_list:
        listm.append('')


    my_data_frame[COUNTER] = pd.Series(listm)
    

my_data_frame = my_data_frame.T

#my_data_frame.to_csv(r"C:\Users\kamy\Desktop\1.csv")


# # cleaning the data

# In[39]:


# this code seperates the sequence colums

null = ''
df = pd.DataFrame()


for i in range(0,len(my_data_frame)):
    this_row = []
    for j in range (0, maximum_lenght_list):
        
        if "tax ID" not in str(my_data_frame.iloc[i][j]):
            this_row.append(my_data_frame.iloc[i][j])
            
        if "tax ID" in str(my_data_frame.iloc[i][j]):
            while len(this_row)%6 != 0:
                this_row.append(null)
            this_row.append(my_data_frame.iloc[i][j])

        
        
########################### THIS IS MY HYPER-PARAMETER ##############################
    maximum_lenght_this_row = 400
    while len(this_row) != maximum_lenght_this_row:
        this_row.append(null)
     
    df[i] = pd.Series(this_row)
            
df = df.T


# this code relocate the tax data
for i in range(0,len(df)):
    for j in range (0,maximum_lenght_this_row):
        if 'tax' in str(df.iloc[i][j]):
            df.iloc[i][j-1] = df.iloc[i][j]
            df.iloc[i][j] = ''
                    
                    
df.to_csv(r"C:\Users\kamy\Desktop\3.csv")       


# # STEP EIGHT

# In[77]:


list_of_accession_numbers = []
for counter in range (2,300,6):
    column_of_accessions_in_df = df[counter]

    for accession_number in column_of_accessions_in_df:
        if accession_number != '':
            list_of_accession_numbers.append(accession_number)
    


# In[130]:


len(list_of_accession_numbers)


# now its time to extract the subsequent sequence data using their accession numbers

# In[117]:


erorrs = []
list_id = []
list_seq =[]
list_description =[]
for i in list_of_accession_numbers:
    try:
        #handle = Entrez.efetch(db = "nucleotide", id = i, rettype = "fasta")
        handle = Entrez.efetch(db = "ALL", id = i, rettype = "fasta")
        record = SeqIO.read( handle, "fasta" )
        list_id.append(record.id)
        list_description.append(record.description)
        list_seq.append(record.seq)
        
    except:
        erorrs.append(i)
    list_of_tuples = list(zip(list_of_accession_numbers, list_description, list_seq))
    df = pd.DataFrame(list_of_tuples,columns = ['accession number', "description",'sequence'])
    df.to_csv(r"C:\Users\kamy\Desktop\16S_seq.csv")

