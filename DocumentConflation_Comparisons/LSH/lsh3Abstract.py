from datasketch import MinHash, MinHashLSH
#import kshingle as ks
#import MySQLdb as sql
import pandas as pd
import csv
import datetime



Thresh = 0.5
shingles = 10
Perm = 256


CSVtitle = f'Results/{Thresh}J{shingles}k{Perm}permTrueDuplicatesAbstract.csv'

#need to change
def csv_w(Ocorpus, Dcourpus):
    oringinal_corpus = Ocorpus.replace('/n', '')
    with open(CSVtitle, mode='a') as csv_file:
        fieldNames = ['id', 'Amount' , 'Duplicates']
        #writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        row = f'[{str(oringinal_corpus)}], [{str(len(Dcourpus))}], [{str(Dcourpus)}]'
        writer.writerow({'id': f'{str(oringinal_corpus)}', 'Amount': f'{str(len(Dcourpus))}', 'Duplicates': f'{str(Dcourpus)}'})
        #writer.writerow(f'{row}')
        print(row)
        
def csv_header():
    with open(CSVtitle, mode='w') as csv_file:
        fieldNames = ['id' , 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()


csv_header()
StartTime = datetime.datetime.now()

df = pd.read_csv('../TrialAbstract.csv')


d={}    
with_wildcard = False
count = 0
lsh = MinHashLSH(threshold=Thresh, num_perm=Perm)

for index, z in df.iterrows():
    id = z['id'] #need to change
    Title = z['abstract']      #need to change
    #s = ks.shingleset_k(Title, k = shingles)
    d["{0}".format(id)] = MinHash(num_perm=Perm)
    for shingle in s:
        d["{0}".format(id)].update(shingle.encode('utf8'))
    lsh.insert(f"{id}", d["{0}".format(id)])
    print(id)
    
TestFile = '../abstractKnown.txt'

with open(TestFile) as f:
    test = f.readlines()
test = [x.strip() for x in test]
for y in test:
    #print(y)
    results = lsh.query(d["{0}".format(y)])
    print(results)
    if len(results) > 1:
        results = [x for x in results]
        csv_w(y, results)

EndTime = datetime.datetime.now()

print(StartTime, EndTime)