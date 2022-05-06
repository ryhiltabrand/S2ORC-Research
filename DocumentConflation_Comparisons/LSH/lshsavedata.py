from datasketch import MinHash, MinHashLSH
import pandas as pd
import csv
import datetime
import pickle

CSVtitle = 'Results/initialRun.csv'

def create_shingles(doc, k):
    """
    Creates shingles and stores them in sets
    
    Paramaters
    ----------

    Returns
    -------
    """
    shingled_set = set() # create an empty set
    
    doc_length = len(doc) 
    
    # iterate through the string and slice it up by k-chars at a time
    for idx in range(doc_length - k + 1):
        doc_slice = doc[idx:idx + k]
        shingled_set.add(doc_slice)
        
    return shingled_set

def csv_w(Ocorpus, Dcourpus):
    """
    
    
    Paramaters
    ----------

    Returns
    -------
    """
    oringinal_corpus = Ocorpus.replace('/n', '')
    with open(CSVtitle, mode='a') as csv_file:
        fieldNames = ['Corpus', 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        row = f'[{str(int(oringinal_corpus))}], [{str(len(Dcourpus))}], [{str(Dcourpus)}]'
        writer.writerow({'Corpus': f'{str(int(oringinal_corpus))}', 'Amount': f'{str(len(Dcourpus))}', 'Duplicates': f'{str(Dcourpus)}'})
        #print(row)
        
def csv_header():
    """
    
    
    Paramaters
    ----------

    Returns
    -------
    """
    with open(CSVtitle, mode='w') as csv_file:
        fieldNames = ['Corpus' , 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)


csv_header()
StartTime = datetime.datetime.now()
df = pd.read_csv('F:\\S2ORC_RESEARCH_new\\DocumentConflation_Comparisons\\NEWyearTrial.csv')

d={}    
with_wildcard = False
count = 0
lsh = MinHashLSH(threshold=0.5, num_perm=128)

for index, z in df.iterrows():
    Corpus = z['corpus_id']
    Title = z['title']
    
    s = create_shingles(Title, 5)

    d["{0}".format(Corpus)] = MinHash(num_perm=128)
    for shingle in s:
        d["{0}".format(Corpus)].update(shingle.encode('utf8'))
    lsh.insert(f"{Corpus}", d["{0}".format(Corpus)])
    #print(Corpus)

TestFile = 'F:\\S2ORC_RESEARCH_new\\DocumentConflation_Comparisons\\known.txt'

with open(TestFile) as f:
    test = f.readlines()
test = [x.strip() for x in test]
for y in test:
    results = lsh.query(d["{0}".format(y)])
    if len(results) > 1:
        results = [int(x) for x in results]
        csv_w(y, results)

EndTime = datetime.datetime.now()
print(EndTime-StartTime)
data = pickle.dumps(lsh)
dfile = open("data", "wb")
dfile.write(data)


CSVtitle1 = 'Results/resultsSaved.csv'
def csv_w1(Ocorpus, Dcourpus):
    oringinal_corpus = Ocorpus.replace('/n', '')
    with open(CSVtitle1, mode='a') as csv_file:
        fieldNames = ['Corpus', 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        row = f'[{str(int(oringinal_corpus))}], [{str(len(Dcourpus))}], [{str(Dcourpus)}]'
        writer.writerow({'Corpus': f'{str(int(oringinal_corpus))}', 'Amount': f'{str(len(Dcourpus))}', 'Duplicates': f'{str(Dcourpus)}'})
        #print(row)
        
def csv_header1():
    with open(CSVtitle1, mode='w') as csv_file:
        fieldNames = ['Corpus' , 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)

start = datetime.datetime.now()

rfile = open("data", "rb")
lsh_loaded = pickle.load(rfile)

with open(TestFile) as f:
    test = f.readlines()
test = [x.strip() for x in test]
for y in test:
    results = lsh_loaded.query(d["{0}".format(y)])
    if len(results) > 1:
        results = [int(x) for x in results]
        csv_w1(y, results)

print(datetime.datetime.now() - start)