import mysql.connector
import sys
import datetime
import re
import csv
import numpy as np
import pandas as pd
import time
import MySQLdb as sql

db=sql.connect(host = "chandra.cs.odu.edu", user = "", passwd = "", db = "s2orc_2020", charset = "utf8")

def get_time():
    x = datetime.datetime.now()
    print(x) 

def main():
    csv_header()
    r = db.cursor()
    i = 0
    
    file1 = '/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/known.txt'
    df = pd.read_csv('/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/NEWyearTrial.csv')
    df_i = df.set_index('corpus_id')
    #print(df_i)
    StartTime = datetime.datetime.now()
    elapsed_time = 0
    with open(file1) as f1:
        for x in f1:
            i += 1
            
            matches = []
            c = x.replace('\n','')
            original = f"SELECT title, year, field FROM s2orcDATA WHERE corpus_id = {c}"
            print(original)
            r.execute(original)
            
            t = time.process_time()
            
            Ori =  r.fetchone()
            oTitle = re.sub(r'[^A-Za-z0-9 ]+', '', Ori[0])
            #oTitle = Ori[0]
            oYear = Ori[1]
            oField = Ori[2]
            #print(oTitle)
            #df1 = df_i[df['title'].str.match(oTitle)]
            df1 = df_i['title'].str.match(oTitle)
            data = df1.to_frame()
            data.columns = ['bool']
            #print(data)
            for index, z in data.loc[data['bool'] == True].iterrows():
                print (index)
                matches.append(index)
                """if len(df1) > 1:
                print (df1['corpus_id'])
                for index, z in df1.iterrows():
                    matches.append(z['corpus_id'].item())"""
            if len(matches) > 1:
                csv_w(c, matches)
            
            #print(df1)
            """check = f"SELECT corpus_id FROM s2orcDATA WHERE MATCH(title) AGAINST('{oTitle}' IN NATURAL LANGUAGE MODE) AND year = {oYear} AND field = '{oField}' LIMIT 10"
            print(check)
            r.execute(check)
            che = r.fetchall()
            for x in che:
                for y in range(len(x)):
                    matches.append(x[y])
            if len(matches) > 1:
                csv_w(paperid, merged)"""
            """if len(df1) > 1:
                print (df1['corpus_id'])
                for index, z in df1.iterrows():
                    matches.append(z['corpus_id'].item())
                csv_w(paperid, merged)"""
            #print(i)
            del df1
            i += 1
            elapsed_time = (time.process_time() - t) + elapsed_time
    EndTime = datetime.datetime.now()

    print(StartTime, EndTime, elapsed_time)
            

            
def csv_w(Ocorpus, Dcourpus):
    oringinal_corpus = Ocorpus.replace('/n', '')
    with open('Results/TrueDuplicates.csv', mode='a') as csv_file:
        fieldNames = ['Corpus', 'Amount' , 'Duplicates']
        #writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        row = f'[{str(int(oringinal_corpus))}], [{str(len(Dcourpus))}], [{str(Dcourpus)}]'
        writer.writerow({'Corpus': f'{str(int(oringinal_corpus))}', 'Amount': f'{str(len(Dcourpus))}', 'Duplicates': f'{str(Dcourpus)}'})
        #writer.writerow(f'{row}')
        print(row)
        
def csv_header():
    with open('Results/TrueDuplicates.csv', mode='w') as csv_file:
        fieldNames = ['Corpus' , 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()

if __name__ == "__main__":

    main()