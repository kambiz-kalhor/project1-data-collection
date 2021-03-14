okay! here we are
this is the main text file i will document what i am going to do.
you can read the details  in the powerpoint files located in each stage


project name:
the final goal:
number of steps: 6 (until now)
tools we used: python (pandas, re, beautiful soup),  jupyter notebook, NCBI API, PubMed API, regex101, Debuggex, git, github, gitkraken


-------------------------------------------  step one  -------------------------------------------
goal: downloding a table of species from BacDive including thier ID, link, isolation source, country, tag


-------------------------------------------  step two  -------------------------------------------
goal: cleaning the dataframe we have,  filling empty cells, get rid of redundencies, removing the duplicate rows


-------------------------------------------  step three  -------------------------------------------
goal: WEB SCRAPING from BacDive, extracting taxonomic data, optimum and growth temperature, optimum and growth pH


-------------------------------------------  step four  -------------------------------------------
goal:  another cleaning step, filling the empty cells, at the end of this step we have a message to see how many species are without temperature data


-------------------------------------------  step five  -------------------------------------------
goal: concat all the previous dataframes and producing an output


-------------------------------------------  step six  -------------------------------------------
goal: data mining from PubMed, using regexes to extract data from some abstracts


 
##########################################################
future goals : the sequence(16s) and the description of sequence



#########################################################
BUG REPORT:
first bug: at the end of the second step   -------->  its because of BacDive database
 i found a wired flaw in BacDive database : here in this code we remove the rows with the same species name , the result is
 a dataframe with 8681 row. now if we remove the rows with the same ID, the result will be a dataframe with 18040 rows.
 this means that there are some species with the same name but with different ID