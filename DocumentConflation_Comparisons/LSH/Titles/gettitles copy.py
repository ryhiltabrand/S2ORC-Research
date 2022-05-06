import MySQLdb as sql
import numpy as np
import pandas as pd

#mysql login
db=sql.connect(host = "chandra.infra.cs.odu.edu", user = "", passwd = "", db = "s2orc_2020", charset = "utf8")

def main():
    r = db.cursor()

    comparison_content = [] #list to hold titles of sample
    cases = []
    file1 = '/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/test.txt'
    with open(file1) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    #print(content)
    df = pd.DataFrame(columns = ['corpus_id', 'title'])
    for i in content:
        r.execute(f"SELECT title FROM s2orcDATA WHERE corpus_id = {i}")
        Ori =  r.fetchone()
        oT = Ori[0]
        dftemp = pd.DataFrame([[i, oT]], columns = ['corpus_id', 'title'])
        print(dftemp)
        df = df.append(dftemp, ignore_index=True)
        
    print(df)
    np.savetxt(r'testtitles.txt', df.values, fmt='%s')

    
if __name__ == "__main__":

    main()

   

