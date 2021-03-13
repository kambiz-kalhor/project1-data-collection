#!/usr/bin/env python
# coding: utf-8

# # importing all the packages we need

# In[194]:


import pandas as pd


# # read stage1_step1_export_bacdive_iso_table before cleaning.csv

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


# In[ ]:




