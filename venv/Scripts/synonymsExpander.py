import requests
from nltk.corpus import wordnet
import nltk
import csv
import re

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
        noDeSyns = len(data['synsets'][0]['terms'])
        for j in range(noDeSyns):
            wrd = data['synsets'][0]['terms'][j]['term'].lower()
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

    # sentence = 'women are not given equal opportunities. Bis zum mittleren Management durchweg homogene Stellenbesetzung. Darüber leider keine einzige Frau.Beim Wiedereinstieg sollen Müttern volle Unterstützung bekommen. In der Realität sieht es manchmal leider anders aus.'
    #
    # stemmerDe = nltk.stem.cistem.Cistem()
    # stemmerEn = SnowballStemmer("english")
    #
    # word_tokens = nltk.tokenize.word_tokenize(sentence.lower())
    # # print(word_tokens)
    #
    # matchBool = False
    # for i in range(len(comparators)):
    #     for j in range(len(word_tokens)):
    #         if comparators[i] in stemmerEn.stem(word_tokens[j]):
    #             matchBool = True
    #             break
    #         if comparators[i] in stemmerDe.stem(word_tokens[j]):
    #             matchBool = True
    #             break
    #
    # if matchBool == True:
    #     print('Yes, its a match.')
    # else:
    #     print('No, its not a match.')

keywordsTable_output = keywordsTable_input

keywordsTable_outputFileName = 'KeywordsTable_output.csv'
keywordsTable_outputFile = open(keywordsTable_outputFileName, "w", newline='', encoding='utf-8')
csv_out = csv.writer(keywordsTable_outputFile, delimiter=',')
csv_out.writerows(keywordsTable_output)