import csv
from langdetect import detect
import spacy
import nltk
from nltk.corpus import stopwords

nlpDe = spacy.load('de_core_news_sm')
nlpEn = spacy.load("en_core_web_sm")

stop_words_en = stopwords.words('english')
stop_words_de = stopwords.words('german')

tokenizer = nltk.RegexpTokenizer(r"\w+")

rev_org_dict={'adidas ag':'adidas','Allianz SE':'allianz-deutschland','BASF SE':'basf-se','Bayerische Motoren Werke AG':'bayerische-motoren-werke','Beiersdorf Aktiengesellschaft':'beiersdorf','Deutsche Bank AG':'deutsche-bank','Deutsche Lufthansa AG':'deutsche-lufthansa','Deutsche Post AG':'deusche-post','SAP SE':'sap','Wirecard AG':'wirecard'}
rev_orgnum_dict={'adidas ag':0,'Allianz SE':1,'BASF SE':2,'Bayerische Motoren Werke AG':3,'Beiersdorf Aktiengesellschaft':4,'Deutsche Bank AG':5,'Deutsche Lufthansa AG':6,'Deutsche Post AG':7,'SAP SE':8,'Wirecard AG':9}

def fetchDescAnalysisWords():
    csvFileName3 = 'Usage of words - RDT Inventory.csv'  # Master_Data_Milestone1_Small_for_training.csv'
    descFile = list(
        csv.reader(open(csvFileName3, encoding='Latin-1'), delimiter=','))  # CSV file to 2 dimensional list of string
    # descFile = pd.read_csv("Usage of words - RDT Inventory.csv", sep=",", encoding='Latin-1')
    # descFile2 = descFile.values.tolist()
    return descFile

def unique(list1):
    # intilize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)

    return unique_list

def germanSpacyLemmatizer(token):
    token = token.lower()
    lemmed = ''
    for t in nlpDe.tokenizer(token):
        lemmed = lemmed + ' ' + t.lemma_
    return lemmed.strip()

def englishSpacyLemmatizer(token):
    token = token.lower()
    lemmed = ''
    for t in nlpEn.tokenizer(token):
        lemmed = lemmed + ' ' + t.lemma_
    return lemmed.strip()

descAnalysis = fetchDescAnalysisWords()
columnHeader = ['engWord', 'sentiment', 'deWord', 'temp']
for org in rev_orgnum_dict:
    columnHeader.append(str(org) + " : " + str(rev_orgnum_dict[org]))
for o in range(len(descAnalysis)):
    wd = descAnalysis[o][0].lower()
    lemmed_word = englishSpacyLemmatizer(wd)
    if lemmed_word:
        descAnalysis[o][0]=lemmed_word
    wd = descAnalysis[o][2].lower()
    lemmed_word = germanSpacyLemmatizer(wd)
    if lemmed_word:
        descAnalysis[o][2] = lemmed_word
    for p in range(len(rev_orgnum_dict)):
        descAnalysis[o].append(0)

csvFileName = 'Master_Data_Milestone1.csv'
masterData = list(csv.reader(open(csvFileName,encoding='utf-8'),delimiter='|')) # CSV file to 2 dimensional list of string

csvFileNameOut = 'DescriptiveAnalysis_output.csv'
csvFileOut = open(csvFileNameOut, "w", newline='', encoding='utf-8')
csv_out = csv.writer(csvFileOut, delimiter='|')

csv_out.writerow(columnHeader)

for i in range(1,len(masterData)):
    review = masterData[i][9].strip()
    if (review != ''):
        for p in range(len(descAnalysis)):
            if (descAnalysis[p][0] in review or descAnalysis[p][2] in review):
                descAnalysis[p][rev_orgnum_dict[masterData[i][0]]+4] = descAnalysis[p][rev_orgnum_dict[masterData[i][0]]+4] + 1
        # csv_out.writerow(masterData[i])
    # if ((masterData[i][7] == 'Gleichberechtigung' or masterData[i][7] ==  'Umgang mit älteren Kollegen') and review != '') or reviewHit(review) == True:
    #     csv_out.writerow(masterData[i])
    # if reviewHit(review) == True:
    #     csv_out.writerow(masterData[i])

    if i%100 == 0:
        print(str(i) + " reviews processed.")

for i in range(len(descAnalysis)):
    csv_out.writerow(descAnalysis[i])