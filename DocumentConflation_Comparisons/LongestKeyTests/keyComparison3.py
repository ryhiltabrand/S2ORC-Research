import mysql.connector
import sys
import datetime
import re

db = mysql.connector.connect(
    host = "localhost",
    user = "",
    passwd = "",
    database = "s2orc_2020"
)

def main(count):
    
    mycursor = db.cursor()
    
    cases = []
    File = open(f'Set{count}/Set{count}.txt', 'r')
    for row in File:
        nrow = row.replace('\n','')
        cases.append(nrow)
    
    for i in range (len(cases)):
        
        cur = f"SELECT database_id, corpus_id, key1, key2, key3, key4, year FROM  LongWordsKeys WHERE corpus_id = {cases[i]}"
        mycursor.execute(cur)
        ct = datetime.datetime.now()
        current =  mycursor.fetchone()
        databaseid = current[0]
        paperid = current[1]
        key1 = current[2]
        key2 = current[3]
        key3 = current[4]
        key4 = current[5]
        year = current[6]
        mycursor.reset()
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
            fin = open(f"Results/Three/Set{count}Three_WordsMatchesCorpus.txt", "a")
            fin.writelines(f"{paperid}\n")
            fin.close()
        if len(merged) > 1:
            fin = open(f"Results/Three/Set{count}Three_WordsMMatchesAmount.txt", "a")
            fin.writelines(f"{len(merged)}\n")
            fin.close()
        if len(merged) > 1:
            fin = open(f"Results/Three/Set{count}Three_WordsMMatchesCorpusMatches.txt", "a")
            fin.writelines(f"{str(merged)}\n")
            fin.close()
        print(i)
        
        
        

        

        
def keyString(key, year):
    keymatches = []
    mycursor = db.cursor()
    key_string = f'SELECT corpus_id FROM  LongWordsKeys WHERE year = "{year}" AND (key1 = "{key}" OR key2 = "{key}" OR key3 = "{key}" OR key4 = "{key}")'

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
    for count in range(20):
        main(count)