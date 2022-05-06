#import mysql.connector
import sys
import datetime
import re
import MySQLdb as sql
import csv
import time
db=sql.connect(host = "chandra.cs.odu.edu", user = "", passwd = "", db = "s2orc_2020", charset = "utf8")

def main():
    csv_header()
    #r = db.cursor(buffered=True)
    r = db.cursor()
    start = time.process_time()
    cases = []
    #File = open(f'../../test.txt', 'r')
    File = open(f'../../known.txt', 'r')

    for row in File:
        nrow = row.replace('\n','')
        cases.append(nrow)
    
    for i in cases:
        
        cur = f"SELECT database_id, corpus_id, key1, key2, key3, key4, year FROM  FiveWordsKey WHERE corpus_id = {i}"
        r.execute(cur)
        ct = datetime.datetime.now()
        current =  r.fetchone()
        databaseid = current[0]
        paperid = current[1]
        key1 = current[2]
        key2 = current[3]
        key3 = current[4]
        key4 = current[5]
        year = current[6]

        print("current time:-", ct)
        
        first_key = keyString(key1, year)
        print(first_key)   
        second_key = keyString(key2, year) 
        print(second_key)
        third_key = keyString(key3, year)
        print(third_key)
        forth_key = keyString(key4, year)
        print(forth_key)
        merged = list(set(first_key + second_key + third_key + forth_key))
        print(merged)
        
        if len(merged) > 1:
            csv_w(paperid, merged)
        print(i)
        end = time.process_time()
        file2 = open("time5.txt","a")
        file2.write(f'{start-end}')
        #r.reset()
        
def csv_w(Ocorpus, Dcourpus):
    #oringinal_corpus = Ocorpus.replace('/n', '')
    with open('Results/6WordTrueDuplicates.csv', mode='a') as csv_file:
        fieldNames = ['Corpus', 'Amount' , 'Duplicates']
        #writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        row = f'[{str(int(Ocorpus))}], [{str(len(Dcourpus))}], [{str(Dcourpus)}]'
        writer.writerow({'Corpus': f'{str(int(Ocorpus))}', 'Amount': f'{str(len(Dcourpus))}', 'Duplicates': f'{str(Dcourpus)}'})
        #writer.writerow(f'{row}')
        print(row)
        
def csv_header():
    with open('Results/6WordTrueDuplicates.csv', mode='w') as csv_file:
        fieldNames = ['Corpus' , 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()        
              
def keyString(key, year):
    keymatches = []
    mycursor = db.cursor()
    if(isinstance(year, int)):
        key_string = f'SELECT corpus_id FROM FiveWordsKey WHERE (year = "{year}" OR year = "{year+1}" OR year = "{year+2}" OR year = "{year-1}"OR year = "{year-1}") AND (key1 = "{key}" OR key2 = "{key}" OR key3 = "{key}" OR key4 = "{key}")'
    else:
        key_string = f'SELECT corpus_id FROM FiveWordsKey WHERE year = "{year}" AND (key1 = "{key}" OR key2 = "{key}" OR key3 = "{key}" OR key4 = "{key}")'
 
    #key_string = f'SELECT corpus_id FROM FiveWordsKey WHERE key1 = "{key}" OR key2 = "{key}" OR key3 = "{key}" OR key4 = "{key}"'

    mycursor.execute(key_string)
    result = mycursor.fetchall()
    for x in result:
        for y in range(len(x)):
            keymatches.append(x[y])

    ct = datetime.datetime.now()
    print(ct)

    return keymatches
    

'''def insert(item_list, key, value): 
    item_list.append((key, value))
 
def search(item_list, key):
    for item in item_list:
        if item[0] == key:
            return item[1]'''



if __name__ == "__main__":
    
    main()