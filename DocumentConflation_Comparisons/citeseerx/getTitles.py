#from bs4 import BeautifulSoup
import requests
import sys
import datetime
import re
import MySQLdb as sql
import csv
import time
db=sql.connect(host = "hawking.cs.odu.edu", user = "rhiltabrand", passwd = "", db = "citeseerx", charset = "utf8")
cases = []
r = db.cursor()
file1 = '/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/citeseerx/new.txt'
file2 = open("titles.txt","a")

'''for row in file1:
    nrow = row.replace('\n','')
    cases.append(nrow)'''
        
with open(file1) as f1:
    for x in f1:
        #n = x.replace('\n', '') 
        #x = x.replace('.body','')
        x = x.replace('\n', "")        
        #x = x.replace(',', '\n')
        
        cur = f'SELECT title FROM papers where id = "{x}"'
        r.execute(cur)
        print (cur)
        current =  r.fetchone()
        print(current[0])
        file2.write(f"{x}:{current[0]}\n")