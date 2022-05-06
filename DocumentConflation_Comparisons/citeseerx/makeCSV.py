import sys
import datetime
import re
import csv
import numpy as np
import pandas as pd
import MySQLdb as sql

db=sql.connect(host = "hawking.cs.odu.edu", user = "rhiltabrand", passwd = "", db = "citeseerx", charset = "utf8")

def main():
    r = db.cursor()

    comparison_content = [] #list to hold titles of sample
    
    file1 = '/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/citeseerx/known.txt'
    with open(file1) as f:
        content = f.readlines()
    for lines in content:
        print (lines)
        temp = lines.strip().split(' ')
        comparison_content.extend(temp)
        print(temp)

    comparison_content = unique(comparison_content)
    print(comparison_content)
    while("" in comparison_content) :
        comparison_content.remove("")
    df = pd.DataFrame(columns = ['id', 'title', 'year', 'abstract'])
    for i in comparison_content:
        #print(i)
        r.execute(f"SELECT title, year, abstract FROM papers WHERE id = '{i}'")
        Ori =  r.fetchone()
        oT = Ori[0]
        oY = Ori[1]
        oA = Ori[2]

        dftemp = pd.DataFrame([[i, oT, oY, oA]], columns = ['id', 'title', 'year', 'abstract'])
        #dftemp = pd.DataFrame([[i]], columns = ['corpus_id'])
        #print(dftemp)
        if (oA == None or oA==""):
            print(oT, oA)
        else: 
            df = df.append(dftemp, ignore_index=True)   
        
        
        
    #print(df)
    #np.savetxt(r'trial.txt', df.values, fmt='%s')
    df.to_csv(r'TrialAbstract.csv', index = False)

def unique(list1):
 
    # initialize a null list
    unique_list = []
     
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    return(unique_list)
        
          
if __name__ == "__main__":

    main()

   
