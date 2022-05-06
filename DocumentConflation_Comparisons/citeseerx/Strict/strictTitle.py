import mysql.connector
import sys
import datetime
import re
import csv
import numpy as np
import pandas as pd
import time
import MySQLdb as sql

db=sql.connect(host = "hawking.cs.odu.edu", user = "rhiltabrand", passwd = "Bigblue22.", db = "citeseerx", charset = "utf8")

def get_time():
    x = datetime.datetime.now()
    print(x) 

def main():
    csv_header()
    r = db.cursor()
    i = 0
    
    file1 = '/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/citeseerx/known.txt'
    df = pd.read_csv('/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/citeseerx/Trial.csv')
    df_i = df.set_index('id')
    #print(df_i)
    StartTime = datetime.datetime.now()
    elapsed_time = 0
    with open(file1) as f1:
        for x in f1:
            i += 1
            
            matches = []
            c = x.replace('\n','')
            original = f"SELECT title, year FROM papers WHERE id = '{c}'"
            print(original)
            r.execute(original)
            
            t = time.process_time()
            
            Ori =  r.fetchone()
            oTitle = re.sub(r'[^A-Za-z0-9 ]+', '', Ori[0])
            #oTitle = Ori[0]
            oYear = Ori[1]
            #oField = Ori[2]
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
            
            del df1
            i += 1
            elapsed_time = (time.process_time() - t) + elapsed_time
    EndTime = datetime.datetime.now()

    print(StartTime, EndTime, elapsed_time)
            

            
def csv_w(Ocorpus, Dcourpus):
    oringinal_corpus = Ocorpus.replace('/n', '')
    with open('Results/TrueDuplicates.csv', mode='a') as csv_file:
        fieldNames = ['id', 'Amount' , 'Duplicates']

        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        row = f'[{str(oringinal_corpus)}], [{str(len(Dcourpus))}], [{str(Dcourpus)}]'
        writer.writerow({'id': f'{str(oringinal_corpus)}', 'Amount': f'{str(len(Dcourpus))}', 'Duplicates': f'{str(Dcourpus)}'})
        
        print(row)
        
def csv_header():
    with open('Results/TrueDuplicates.csv', mode='w') as csv_file:
        fieldNames = ['id' , 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()

if __name__ == "__main__":

    main()