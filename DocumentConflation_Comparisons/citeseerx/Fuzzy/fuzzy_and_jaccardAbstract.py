import mysql.connector
import sys
import datetime
import re
import csv
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import MySQLdb as sql
import time

db=sql.connect(host = "hawking.cs.odu.edu", user = "rhiltabrand", passwd = "Bigblue22.", db = "citeseerx", charset = "utf8")

def get_time():
    x = datetime.datetime.now()
    print(x) 

def main():
    csv_header()
    r = db.cursor()
    StartTime = datetime.datetime.now()
    get_time()
    elapsed_time = 0
    
    df = pd.read_csv('/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/citeseerx/TrialAbstract.csv')
    
    df['year'] = df['year'].fillna(0.0).astype(int)
    df.set_index('year')
    #df.set_index('field')
    print(df)
    get_time()

    file1 = '/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/citeseerx/known.txt'

    with open(file1) as f1:
        for x in f1:
            c = x.replace('\n','')
            original = f"SELECT abstract, year FROM papers WHERE id = '{c}'" #need to change
            r.execute(original)
            t = time.process_time()
            Ori =  r.fetchone()
            oAbstract = Ori[0]
            oYear = Ori[1]

            new = 0    
            matches = []
            
            for index, z in df.iterrows():           
                dCorpus = z['id'] #needToChange
                dAbstract = z['abstract'] #needToChange
                
                #print (z)
                print(f'{c}: {oAbstract}')
                print(f'{dCorpus}: {dAbstract}')
                if fuzzy_score(oAbstract, dAbstract) > 90:
                    print (dCorpus)
                    matches.append(dCorpus)
                    
            if(len(matches) > 1):  
                print(matches)   
                csv_w(c, matches)
            elapsed_time = (time.process_time() - t) + elapsed_time
    EndTime = datetime.datetime.now()

    print(StartTime, EndTime, elapsed_time)

                
def fuzzy_score(oAbstract, dAbstract):
    score = fuzz.partial_ratio(oAbstract, dAbstract)
    print(score)
    return score

def jaccard_score(Oauthors, Dauthors):
    intersection = len(list(set(Oauthors).intersection(Dauthors)))
    union = (len(Oauthors) + len(Dauthors)) - intersection
    return float(intersection) / union

def csv_w(Ocorpus, Dcourpus):
    oringinal_corpus = Ocorpus.replace('/n', '')
    with open('Results/90TrueDuplicatesAbstract.csv', mode='a') as csv_file:
        fieldNames = ['id', 'Amount' , 'Duplicates']
        #writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        row = f'[{str(oringinal_corpus)}], [{str(len(Dcourpus))}], [{str(Dcourpus)}]'
        writer.writerow({'id': f'{str(oringinal_corpus)}', 'Amount': f'{str(len(Dcourpus))}', 'Duplicates': f'{str(Dcourpus)}'})
        #writer.writerow(f'{row}')
        print(row)
        
def csv_header():
    with open('Results/90TrueDuplicatesAbstract.csv', mode='w') as csv_file:
        fieldNames = ['id' , 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()

if __name__ == "__main__":

    main()