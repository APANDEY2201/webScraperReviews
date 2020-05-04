import requests
from nltk.corpus import wordnet
import nltk
import csv
import re

# print(wn.synsets('equality')[1].lemmas()[].name())

for syn in wordnet.synsets('equality'):
    for l in syn.lemmas():
        print(l.name().lower().replace('-',' ').replace('_',' ').replace(',',' ').strip())


csvFileName = 'KeywordsTable_input.csv'

keywordsTable_input = list(csv.reader(open(csvFileName),delimiter=',')) # CSV file to 2 dimensional list of string

for i in range(len(keywordsTable_input)):

    deWord = keywordsTable_input[i][1]
    enWord = keywordsTable_input[i][2]

    print (deWord + " and " + enWord)

    deSyns = []
    enSyns = []

    URL = "https://www.openthesaurus.de/synonyme/search?q=" + deWord + "&format=application/json"
    r = requests.get(url=URL)
    data = r.json()
    try:
        for k in range(len(data['synsets'])):
            noDeSyns = len(data['synsets'][k]['terms'])
            for j in range(noDeSyns):
                wrd = data['synsets'][k]['terms'][j]['term'].lower()
                result = re.sub("[\(\[].*?[\)\]]", "", wrd)
                deSyns.append("de:" + result.replace('-',' ').replace('_',' ').replace(',',' ').strip())
    except:
        deSyns = []

    for syn in wordnet.synsets(enWord):
        for l in syn.lemmas():
            enSyns.append("en:" + l.name().lower().replace('-',' ').replace('_',' ').replace(',',' ').strip())

    comparators = enSyns + deSyns

    keywordsTable_input[i][1] =  "de:" + keywordsTable_input[i][1]
    keywordsTable_input[i][2] = "en:" + keywordsTable_input[i][2]
    keywordsTable_input[i] = keywordsTable_input[i] + comparators

    print(keywordsTable_input[i])

keywordsTable_output = keywordsTable_input

keywordsTable_outputFileName = 'KeywordsTable_output2222.csv'
keywordsTable_outputFile = open(keywordsTable_outputFileName, "w", newline='', encoding='utf-8')
csv_out = csv.writer(keywordsTable_outputFile, delimiter=',')
csv_out.writerows(keywordsTable_output)