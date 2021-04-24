"""
####    ##    ##    ########     ##     ##    ########     ######       ####        #######     ##     ##    ########    ########     ##     ##    ########     ######
 ##     ###   ##    ##     ##    ##     ##       ##       ##    ##     ##  ##      ##     ##    ##     ##       ##       ##     ##    ##     ##       ##       ##    ##
 ##     ####  ##    ##     ##    ##     ##       ##       ##            ####       ##     ##    ##     ##       ##       ##     ##    ##     ##       ##       ##
 ##     ## ## ##    ########     ##     ##       ##        ######      ####        ##     ##    ##     ##       ##       ########     ##     ##       ##        ######
 ##     ##  ####    ##           ##     ##       ##             ##    ##  ## ##    ##     ##    ##     ##       ##       ##           ##     ##       ##             ##
 ##     ##   ###    ##           ##     ##       ##       ##    ##    ##   ##      ##     ##    ##     ##       ##       ##           ##     ##       ##       ##    ##
####    ##    ##    ##            #######        ##        ######      ####  ##     #######      #######        ##       ##            #######        ##        ######
 
(font banner 3)
"""
## for the dear user
print('getting inputs and outputs......................')

### step_seven_input_path = step_one_to_six_output_path
#step_seven_input_path = r'Data_collection_project/step_one_to_six_output_MAIN.csv'
step_seven_input_path = r'Data_collection_project/step_one_to_six_output_test.csv'


#this is output from step 7
#it includes all the availible_seq data frame  note that there is no seq download yet
#step_seven_output = 'Data_collection_project/all_availible_seq_clean_MAIN(step7 output).csv'
step_seven_output_path = 'Data_collection_project/all_availible_seq_clean(step7 output).csv'


#this is output from step 8
#step_eight_output_path = 'Data_collection_project/all_availible_seq_clean_MAIN(step7 output).csv'
step_eight_output_path = 'Data_collection_project/all_availible_seq_clean(step7 output).csv'



"""
####    ##     ##    ########      #######     ########     ########    ####    ##    ##     ######
 ##     ###   ###    ##     ##    ##     ##    ##     ##       ##        ##     ###   ##    ##    ##
 ##     #### ####    ##     ##    ##     ##    ##     ##       ##        ##     ####  ##    ##
 ##     ## ### ##    ########     ##     ##    ########        ##        ##     ## ## ##    ##   ####
 ##     ##     ##    ##           ##     ##    ##   ##         ##        ##     ##  ####    ##    ##
 ##     ##     ##    ##           ##     ##    ##    ##        ##        ##     ##   ###    ##    ##
####    ##     ##    ##            #######     ##     ##       ##       ####    ##    ##     ######


########        ###        ######     ##    ##       ###        ######      ########     ######
##     ##      ## ##      ##    ##    ##   ##       ## ##      ##    ##     ##          ##    ##
##     ##     ##   ##     ##          ##  ##       ##   ##     ##           ##          ##
########     ##     ##    ##          #####       ##     ##    ##   ####    ######       ######
##           #########    ##          ##  ##      #########    ##    ##     ##                ##
##           ##     ##    ##    ##    ##   ##     ##     ##    ##    ##     ##          ##    ##
##           ##     ##     ######     ##    ##    ##     ##     ######      ########     ######

(font banner 3)
"""

print('importing packages.............................')
# main packages
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import time

# using PubMed API
from pymed import PubMed

# using NCBI API
from Bio import Entrez
from Bio import SeqIO
Entrez.email = 'kalhor.kz@gmail.com'

# for downloading from NCBI>assembly
import os

######################
#  estimating time   #
start = time.time()  #
#                    #
######################






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

#goal: finding out what are the availible seq data  -----> searching BacDive

#############################################################################
# a def which reads CSV
def read_excell_as_dataFrame(path):
    DataFrame = pd.read_csv(path)
    return DataFrame
first_dataframe = read_excell_as_dataFrame(step_seven_input_path)




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
my_new_dataframe.to_csv(step_seven_output_path)       







"""
 ######     ########    ########    ########           ########    ####     ######      ##     ##    ########
##    ##       ##       ##          ##     ##          ##           ##     ##    ##     ##     ##       ##
##             ##       ##          ##     ##          ##           ##     ##           ##     ##       ##
 ######        ##       ######      ########           ######       ##     ##   ####    #########       ##
      ##       ##       ##          ##                 ##           ##     ##    ##     ##     ##       ##
##    ##       ##       ##          ##                 ##           ##     ##    ##     ##     ##       ##
 ######        ##       ########    ##                 ########    ####     ######      ##     ##       ##

(font banner 3)
"""


#############################################################################################

# this is a separate code  #we use it to download file from assembly
def give_error_download_the_assembly_file(erorr):
    # searching to find sequnces for errors
    # searching assembly database in NCBI
    print('downloading from assembly>NCBI   please wait.....................')


    ############################give_accesstion_numbers(id)_return_esummary_record
    def get_id_give_assembly_summary(id):
        """Get esummary for an entrez id"""

        #print('+++++++', id)
        esummary_handle = Entrez.esummary(db="assembly", id=id, report="full")
        esummary_record = Entrez.read(esummary_handle)
        #print('=======',esummary_record)
        return esummary_record
    ##############################################################################

    ############################give_accesstion_numbers(term)_return_links
    def get_assemblies_link_from_accession_number(term):
        """Download genbank assemblies for a given search term.
        Args:
            term: search term, usually organism name
        """
        ###########print('+++++++',term)
        # provide your own mail here # I wrote the email at the begining of the codes
        handle = Entrez.esearch(db="assembly", term=term, retmax="200")
        record = Entrez.read(handle)
        ids = record["IdList"]
        links = []
        for aid in ids:
            summary = get_id_give_assembly_summary(aid)  # get summary
            url = summary["DocumentSummarySet"]["DocumentSummary"][0]["FtpPath_RefSeq"]
            if url == "":
                continue
            label = os.path.basename(url)
            # get the fasta link - change this to get other formats
            link = url + "/" + label + "_genomic.fna.gz"
            link = link.replace("ftp://", "https://")
            links.append(link)
        
        #############print('=======', links)
        return links
    ######################################################################

    ############################give_accesstion_numbers_return_link
    def get_link(accesstion_number):
        """ Get link from internet and return it."""
        #print('=======', accesstion_numbers)

        # read links from interent
        

        link = get_assemblies_link_from_accession_number(accesstion_number)
        


        return link
    ###############################################################

    ################# download a url and save it using path
    def download(url, path):
        """Download file based on url and save file to the path"""
        response = requests.get(url)

        if response.ok:
            print("response is ok file is downloading ... ")
            # start to download file from url.
            with open(path, "wb") as f:
                f.write(response.content)
        else:
            print("Error!", response.status_code)
            return False

        print("File downloaded succusfully.")
        return True
    #######################################################

    # giving the accesstion_numbers
    accesstion_number = erorr

    # read links from internet
    link = get_link(accesstion_number)

    # download of each link's data and save them with path name
    if link != []:
        link = link[0]
        filename = link.split("/")[-1]
        download(link, f"Data_collection_project//downloaded_files_in_step_8//{filename}")

    # download data from each links
#############################################################################################

# now its time to extract the subsequent sequence data using their accession numbers
# this code gets accession_number and gives you Id,Description,Seq
# it will try to get data frome NCBI_nucleotide but if there were no data - 
# then it tries to download assemly file using pervious code
def get_accession_number_give_seq_from_NCBI_nucleotide(accession_number):

    print('searching for', accession_number)
    try:
        handle = Entrez.efetch(db = "nucleotide", id = accession_number, rettype = "fasta")
        record = SeqIO.read( handle, "fasta" )
        ID = record.id
        Description = record.description
        Seq = record.seq
        print('sequence found')
    except:
        print(accession_number , ' without any sequnce on NCBI>nucleotide: ')
        give_error_download_the_assembly_file(accession_number)

        #if you want to do anything with .fna.gz file you should do it in here

        ID, Description, Seq = "downloaded","downloaded","downloaded"
    return ID, Description, Seq

#############################################################################################   

#@@@@@@@@@ example of what two pervious codes do
#get data from neculotide
#Id,Description,Seq = get_accession_number_give_seq_from_NCBI_nucleotide('AB665079')
#print(Id,Description,Seq)
#downloads from assembly
#Id,Description,Seq = get_accession_number_give_seq_from_NCBI_nucleotide('GCA_002082135')
#print(Id,Description,Seq)


####################### importing the csv ########################
print('importing the csv........................')

# read the input
my_dataframe =  pd.read_csv(step_seven_output_path)


####################### making index lists ########################
print('making index lists ...............')

list_accession_number_columns = []
for columns in range (3,300,7):
    list_accession_number_columns.append(columns)
    
list_description_columns = []
for columns in range (7,300,7):
    list_description_columns.append(columns)
    
list_seq_columns = []
for columns in range (8,300,7):
    list_seq_columns.append(columns)


################ palcing descriptions & sequences #################

for row in range(0,len(my_dataframe)):

    #the following code makes a list with row value
    #for example: list_number_75 = []
    list_name = f"list_number_{row}"
    exec(list_name + " = []")
    

    for column in range (0,300):
        
        if column in list_accession_number_columns:
            accession_number = my_dataframe.iloc[row,column]
            if str(accession_number) != 'nan':
                #print(accession_number,'+++++++++++ do sth and find seq')
                Id,Description,Seq = get_accession_number_give_seq_from_NCBI_nucleotide(accession_number)
                
            if str(accession_number) == 'nan':
                Description = ''
                Seq = ''
                
            
            
        if column in list_description_columns:
            exec(list_name +'.append(Description)')
        
        if column in list_seq_columns:
            exec(list_name +'.append(Seq)')

        if ((column not in list_description_columns) and (column not in list_seq_columns)):
            exec(list_name +'.append(my_dataframe.iloc[row,column])')




############################## making a datafarame ################################

# dictionary of lists 
string = '{'
for i in range (0,len(my_dataframe)):
    string = string + str(i) +': list_number_'+str(i)
    if i != (len(my_dataframe)-1):
        string = string +','
    if i == (len(my_dataframe)-1):
        string = string +'}'

exec('dict ='+ string)
df = pd.DataFrame(dict)
df = df.T

################################ export csv file #################################

df.to_csv(step_eight_output_path)








print('STEP 7 AND 8 are done :) :)  :) .................')
######################################################################
print('mission complete')
######################
#                    # 
end = time.time()    #
#                    #
######################
print('estimated time is ', end-start ,' seconds or ',(end-start)/60 , ' minutes or ',(end-start)/3600 , ' hours')
########################################################################










"""
 #######     ########    ##     ##    ########    ########            ######      #######     ########     ########     ######
##     ##       ##       ##     ##    ##          ##     ##          ##    ##    ##     ##    ##     ##    ##          ##    ##
##     ##       ##       ##     ##    ##          ##     ##          ##          ##     ##    ##     ##    ##          ##
##     ##       ##       #########    ######      ########           ##          ##     ##    ##     ##    ######       ######
##     ##       ##       ##     ##    ##          ##   ##            ##          ##     ##    ##     ##    ##                ##
##     ##       ##       ##     ##    ##          ##    ##           ##    ##    ##     ##    ##     ##    ##          ##    ##
 #######        ##       ##     ##    ########    ##     ##           ######      #######     ########     ########     ######

(font banner 3)
"""

###********************************************************************
###this code reads .gz file which is a compressed file
###for example
#import gzip
#input_path = r'Data_collection_project/downloaded_files_in_step_8/GCF_000754095.2_ASM75409v2_genomic.fna.gz'
#def read_gz_files(input_path):
    #with gzip.open(input_path, 'rb') as f:
        #file_content = f.read()
    #return file_content

#print(read_gz_files(input_path))
#**********************************************************************