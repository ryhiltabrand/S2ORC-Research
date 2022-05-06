import MySQLdb as sql
import numpy as np
import pandas as pd

#mysql login
db=sql.connect(host = "chandra.infra.cs.odu.edu", user = "", passwd = "", db = "s2orc_2020", charset = "utf8")

def main():
    r = db.cursor()

    comparison_content = [] #list to hold titles of sample
    cases = []
    file1 = '/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/alltitles.txt'
    r.execute(f"SELECT corpus_id, title FROM s2orcDATA WHERE database_id")
    df = pd.DataFrame(r.fetchall(), columns = ['corpus_id', 'title'])
    np.savetxt(r'alltitles.txt', df.values, fmt='%s')
if __name__ == "__main__":

    main()

   

