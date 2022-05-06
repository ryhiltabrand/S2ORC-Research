from datasketch import MinHash, MinHashLSH
import kshingle as ks
#import MySQLdb as sql
import pandas as pd
import csv
import datetime

CSVtitle = 'Results/.9J10k256permTrueDuplicates.csv'
def csv_w(Ocorpus, Dcourpus):
    oringinal_corpus = Ocorpus.replace('/n', '')
    with open(CSVtitle, mode='a') as csv_file:
        fieldNames = ['Corpus', 'Amount' , 'Duplicates']
        #writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        row = f'[{str(int(oringinal_corpus))}], [{str(len(Dcourpus))}], [{str(Dcourpus)}]'
        writer.writerow({'Corpus': f'{str(int(oringinal_corpus))}', 'Amount': f'{str(len(Dcourpus))}', 'Duplicates': f'{str(Dcourpus)}'})
        #writer.writerow(f'{row}')
        print(row)
        
def csv_header():
    with open(CSVtitle, mode='w') as csv_file:
        fieldNames = ['Corpus' , 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)


#r = db.cursor()
csv_header()
StartTime = datetime.datetime.now()
#r.execute(f"SELECT corpus_id, title FROM s2orcDATA")
#df = pd.DataFrame(r.fetchall(), columns = ['corpus_id', 'title'])
df = pd.read_csv('/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/NEWyearTrial.csv')
#df = pd.read_csv('../s2orc.csv')

d={}    
with_wildcard = False
count = 0
lsh = MinHashLSH(threshold=0.9, num_perm=256)

for index, z in df.iterrows():
    Corpus = z['corpus_id']
    Title = z['title']
    s = ks.shingleset_k(Title, k = 10)
    d["{0}".format(Corpus)] = MinHash(num_perm=256)
    for shingle in s:
        d["{0}".format(Corpus)].update(shingle.encode('utf8'))
    lsh.insert(f"{Corpus}", d["{0}".format(Corpus)])
    print(Corpus)
#TestFile = '/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/test.txt'
TestFile = '/data/rhiltabr/s2/S2ORC_RESEARCH/DocumentConflation_Comparisons/known.txt'

with open(TestFile) as f:
    test = f.readlines()
test = [x.strip() for x in test]
for y in test:
    results = lsh.query(d["{0}".format(y)])
    #print(results)
    if len(results) > 1:
        results = [int(x) for x in results]
        csv_w(y, results)

EndTime = datetime.datetime.now()

print(StartTime, EndTime)