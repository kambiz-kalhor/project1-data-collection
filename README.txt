okay! here we are
Here, I will document what i have done so far and what i am going to do.
you can read the details  in the powerpoint files located in each stage


project name :

the final goal : 

supervisors : Dr. Andrew Steen, Dr. Donato Giovannelli

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


-------------------------------------------  step seven  -------------------------------------------
goal: finding out what are the availible seq data  -----> searching BacDive



-------------------------------------------  step eight  -------------------------------------------
goal: adding seq data  -----> from BacDive
here we have some problems:
1- we can only use biopython to download from nucleoutide database and we can not use assembly database (this problem is my focous right now)
two parts:
1-  seq from nuecleotide
2- seq from essembly
 
##########################################################
future goals : 
For every organism possible

Add 16S sequence from the strain in BacDive -----> mostly done
[] Add genome from the strain in BacDive
[] Add 16S and/or genome sequence from other sources (e.g. RefSeq, IMG/M, SRA, ENA) for precisely the same organism
[] Add genome sequence for different organisms having the identical 16S sequence to organisms in BacDive



#########################################################
BUG REPORT:
first bug: at the end of the second step   -------- >  its because of BacDive database
 I found a flaw in BacDive database : here in this code we remove the rows with the same species name , the result is
 a dataframe with 8681 row. now if we remove the rows with the same ID, the result will be a dataframe with 18040 rows.
 this means that there are some species with the same name but with different ID

Second bug: some wierd characters   -------- >  i dont know why they appear in text
although i removed all aother characters but they still  appear in the text
characters like ------> Â
i will solve this in my next meeting with my programming teacher.

#########################################################
TO DO LIST
1-write a regex for salinity
2-add some details about my regex for better documentation using debuggex (I already added one example "view_temperature regex.PNG")
3-
