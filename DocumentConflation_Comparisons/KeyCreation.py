import xlrd
import mysql.connector
import sys
import re

#Add the proper connection information depending on the server you are on
db = mysql.connector.connect(
    host = "", #hawking.cs.odu.edu is the server i think you need
    user = "", #sql user name
    passwd = "", #sql password
    database = "" #database name for citeseer
)

#I used this sql connector later in research but you will have to change code bellow so stick with above connector
#db=sql.connect(host = "", user = "", passwd = "", db = "", charset = "utf8")

def main():
    #the two arguments you need are for the loop, I believe I had these set as I had to run into issues but essentially its just the size of the database
    startValue = int(sys.argv[1])
    endValue = int(sys.argv[2]) 

    mycursor = db.cursor()

    first = ''
    second = ''
    third = ''
    forth = ''
    fifth = ''
    sixth = ''

    for i in range (startValue, endValue+1):
        
        #Change code below to the right sql for database name and title creation
        cur = f"SELECT database_id, corpus_id, title, authors, year FROM s2orcDATA WHERE database_id = {i}"
        mycursor.execute(cur)

        current =  mycursor.fetchone()
        databaseid = current[0]
        paperid = current[1]
        alphaNumericTitle = current[2].lower()

        alphaNumericTitle = alphaNumericTitle.replace("[", '')
        alphaNumericTitle = alphaNumericTitle.replace("]", '')
        alphaNumericTitle = alphaNumericTitle.replace(":", '')
        alphaNumericTitle = alphaNumericTitle.replace("'", '')
        alphaNumericTitle = alphaNumericTitle.replace('"', '')
        alphaNumericTitle = alphaNumericTitle.replace(';', '')
        alphaNumericTitle = alphaNumericTitle.replace('{', '')
        alphaNumericTitle = alphaNumericTitle.replace('}', '')
        alphaNumericTitle = alphaNumericTitle.replace('!', '')
        alphaNumericTitle = alphaNumericTitle.replace('.', '')
        alphaNumericTitle = alphaNumericTitle.replace(',', '')

        firstAuthor = firstA(current[3])
        lastAuthor = last(current[3])
        year = current[4]

        titleList = alphaNumericTitle.split()


        if len(titleList) > 5:
            first = longestString(titleList)
            titleList.remove(first)
            second = longestString(titleList)
            titleList.remove(second)
            third = longestString(titleList)
            titleList.remove(third)
            forth = longestString(titleList)
            titleList.remove(forth)
            fifth = longestString(titleList)
            titleList.remove(fifth)
            sixth = longestString(titleList)
            titleList.remove(sixth)

        elif len(titleList) > 4:
            first = longestString(titleList)
            titleList.remove(first)
            second = longestString(titleList)
            titleList.remove(second)
            third = longestString(titleList)
            titleList.remove(third)
            forth = longestString(titleList)
            titleList.remove(forth)
            fifth = longestString(titleList)
            titleList.remove(fifth)
            sixth = ''
            
        elif len(titleList) > 3:
            first = longestString(titleList)
            titleList.remove(first)
            second = longestString(titleList)
            titleList.remove(second)
            third = longestString(titleList)
            titleList.remove(third)
            forth = longestString(titleList)
            titleList.remove(forth)
            fifth = ''
            sixth = ''

        elif len(titleList) > 2:
            first = longestString(titleList)
            titleList.remove(first)
            second = longestString(titleList)
            titleList.remove(second)
            third = longestString(titleList)
            titleList.remove(third)
            forth = ''
            fifth = ''
            sixth = ''

        elif len(titleList) > 1:
            first = longestString(titleList)
            titleList.remove(first)
            second = longestString(titleList)
            titleList.remove(second)
            third = ''
            forth = ''

        elif len(titleList) == 1:
            first = longestString(titleList)
            titleList.remove(first)
            second = ''
            third = ''
            forth = ''
            fifth = ''
            sixth = ''

        else:
            first = ''
            second = ''
            third = ''
            forth = ''
            fifth = ''
            sixth = ''

        four_firstKey = FourkeyString(first, second, third, forth, firstAuthor)
        four_secondKey = FourkeyString(second, third, forth, fifth, firstAuthor)
        four_thirdKey = FourkeyString(first, second, third, forth, lastAuthor)
        four_forthKey = FourkeyString(second, third, forth, fifth, lastAuthor)

        five_firstKey = FivekeyString(first, second, third, forth, fifth, firstAuthor)
        five_secondKey = FivekeyString(second, third, forth, fifth, sixth, firstAuthor)
        five_thirdKey = FivekeyString(first, second, third, forth, fifth, lastAuthor)
        five_forthKey = FivekeyString(second, third, forth, fifth, sixth, lastAuthor)

        print(i)
        mycursor.execute("INSERT INTO FourWordsKey (database_id, corpus_id, key1, key2, key3, key4, year) VALUES(%s, %s, %s, %s, %s, %s,%s)", (databaseid, paperid, four_firstKey, four_secondKey, four_thirdKey, four_forthKey, year))
        db.commit()
        mycursor.execute("INSERT INTO FiveWordsKey (database_id, corpus_id, key1, key2, key3, key4, year) VALUES(%s, %s, %s, %s, %s, %s,%s)", (databaseid, paperid, five_firstKey, five_secondKey, five_thirdKey, five_forthKey, year))
        db.commit()

def longestString(List):
    longest_string = max(List, key=len)
    return longest_string

def keyString(one, two, three,four):
    if four == None:
        key = one+'_'+two+'_'+three
        return key
    else:
        key = one+'_'+two+'_'+three+'_'+four.lower()
        return key
    
def FourkeyString(one, two, three, four, author):
    if author == None:
        key = one+'_'+two+'_'+three+'_'+four
        return key
    else:
        key = one+'_'+two+'_'+three+'_'+four+'_'+author.lower()
        return key

def FivekeyString(one, two, three, four, five, author):
    if author == None:
        key = one+'_'+two+'_'+three+'_'+four+'_'+five
        return key
    else:
        key = one+'_'+two+'_'+three+'_'+four+'_'+five+'_'+author.lower()
        return key

def firstA(authors):
    author = authors.strip()
    author = author.lower()
    if ',' in author:
        author = author.replace(',', " , ")
        aList = author.split()
        pos = aList.index(',')
        return aList[pos-1]
    elif author == '':
        return None
    else:
        aList = authors.split()
        return aList[-1]
            
def last(authors):
    authors = authors.strip()
    authors = authors.lower()
    if authors == '':
        return None
    else:
        author = authors.split()
        return author[-1]

def keyCreator(title1, title2, title3, author):
    key = [title1, title2, title3, author]
    return key

if __name__ == "__main__":

    main()
