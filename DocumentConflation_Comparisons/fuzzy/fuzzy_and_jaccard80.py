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

db=sql.connect(host = "chandra.cs.odu.edu", user = "", passwd = "", db = "s2orc_2020", charset = "utf8")
#db=mysql.connector.connect(host = "chandra.cs.odu.edu", user = "rhiltabrand", passwd = "WedSep2211:36:18AM", db = "s2orc_2020", charset = "utf8")

def get_time():
    x = datetime.datetime.now()
    print(x) 

def main():
    csv_header()
    r = db.cursor()
    StartTime = datetime.datetime.now()
    get_time()
    elapsed_time = 0
    #r.execute(f"SELECT corpus_id, title, authors, year, field FROM s2orcDATA")
    #df = pd.DataFrame(r.fetchall(), columns = ['corpus_id', 'title', 'authors', 'year', 'field'])
    
    #df = pd.read_csv('/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/trial.csv')
    #df = pd.read_csv('/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/yearTrial4.csv')
    #df = pd.read_csv('/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/NEWyearTrial.csv')
    df = pd.read_csv('/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/TrialAbstract.csv')

    #df = pd.read_csv('../s2orc.csv')
    df['year'] = df['year'].fillna(0.0).astype(int)
    df.set_index('year')
    #df.set_index('field')
    print(df)
    get_time()

    #file1 = '/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/test.txt'
    #file1 = '/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/known.txt'
    #file1 = '/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/kno4.txt'
    file1 = '/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/abstractKnown.txt'

    with open(file1) as f1:
        for x in f1:
            c = x.replace('\n','')
            original = f"SELECT title, authors, year, field, abstract FROM s2orcDATA WHERE corpus_id = {c}"
            r.execute(original)
            t = time.process_time()
            Ori =  r.fetchone()
            oTitle = Ori[0]
            oAuthor = Ori[1]
            oYear = Ori[2]
            oField = Ori[3]
            oAbstract = Ori[4]
            
                
            oAuthor = re.sub(' +', ' ', oAuthor)
            oAuthorList = oAuthor.split(',')

            #print(oTitle)
            #print(c)
            #print(oAuthorList)
                
            #print(x)
            #print(type(f2list))
            new = 0    
            matches = []
            #for index, z in df.loc[df['year'] == oYear].iterrows():
            for index, z in df.iterrows():           
                dCorpus = z['id']
                #dTitle = z['title']
                dAbstract = z['abstract']
                #dAuthor = z['authors']
                #dAuthor = re.sub(' +', ' ', dAuthor)
                #dAuthorList = dAuthor.split(',')
                print (z)
                if fuzzy_score(oAbstract, dAbstract) > 80:
                    print (dCorpus)
                    matches.append(dCorpus)
                    
            if(len(matches) > 1):  
                print(matches)   
                csv_w(c, matches)
            elapsed_time = (time.process_time() - t) + elapsed_time
    EndTime = datetime.datetime.now()
    file2 = open("time80.txt","a")
    file2.write(elapsed_time)
    print(StartTime, EndTime, elapsed_time)

                
def fuzzy_score(Otitle, Dtitle):
    score = fuzz.partial_ratio(Otitle, Dtitle)
    print(score)
    return score

def jaccard_score(Oauthors, Dauthors):
    intersection = len(list(set(Oauthors).intersection(Dauthors)))
    union = (len(Oauthors) + len(Dauthors)) - intersection
    return float(intersection) / union

def csv_w(Ocorpus, Dcourpus):
    oringinal_corpus = Ocorpus.replace('/n', '')
    with open('Results/80TrueDuplicatesAbstract.csv', mode='a') as csv_file:
        fieldNames = ['Corpus', 'Amount' , 'Duplicates']
        #writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        row = f'[{str(int(oringinal_corpus))}], [{str(len(Dcourpus))}], [{str(Dcourpus)}]'
        writer.writerow({'Corpus': f'{str(int(oringinal_corpus))}', 'Amount': f'{str(len(Dcourpus))}', 'Duplicates': f'{str(Dcourpus)}'})
        #writer.writerow(f'{row}')
        print(row)
        
def csv_header():
    with open('Results/80TrueDuplicatesAbstract.csv', mode='w') as csv_file:
        fieldNames = ['Corpus' , 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()

if __name__ == "__main__":

    main()