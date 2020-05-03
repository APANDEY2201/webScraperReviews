import csv
import nltk
from langdetect import detect


def unique(list1):
    # intilize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)

    return unique_list

def sentenceWordRelation(sentence, wrdList, rvNo, feature,keywordLang):
    stemmerDe = nltk.stem.cistem.Cistem()
    stemmerEn = nltk.SnowballStemmer("english")
    itsGerman = True
    try:
        if detect(sentence) == 'en':
            itsGerman = False
    except:
        itsGerman = True

    itsGermanKeyword = True
    if keywordLang == "en:":
        itsGermanKeyword = False
    else:
        itsGermanKeyword = True

    word_tokens = nltk.tokenize.word_tokenize(sentence)
    tokensDe = []
    tokensEn = []
    for token in word_tokens:
        tokensDe.append(stemmerDe.stem(token).lower())
        tokensEn.append(stemmerEn.stem(token).lower())

    if itsGerman == True:
        cntDe = 0
        for tokenDe in tokensDe:
            if itsGermanKeyword == True:
                for wrd in wrdList:
                    wrd = wrd.replace("de:","")
                    if stemmerDe.stem(wrd) in tokenDe:
                        cntDe = cntDe + 1
                if cntDe == len(wrdList):
                    # print("review number: " + str(rvNo) + " belonging to feature " + feature.upper() + " and words are: " + str(wrdList))
                    return True
    else:
        cntEn = 0
        for tokenEn in tokensEn:
            if itsGermanKeyword == False:
                for wrd in wrdList:
                    wrd = wrd.replace("en:", "")
                    if stemmerEn.stem(wrd) in tokenEn:
                        cntEn = cntEn + 1
                if cntEn == len(wrdList):
                    return True

csvFileName = 'KeywordsTable_output.csv'
keywordsTable = list(csv.reader(open(csvFileName),delimiter=',')) # CSV file to 2 dimensional list of string

csvFileName = 'Master_Data_Milestone1_temp.csv'
masterData = list(csv.reader(open(csvFileName),delimiter='|')) # CSV file to 2 dimensional list of string

features = [i[0] for i in keywordsTable]

features = unique(features)

outFile = []

masterData[0] = masterData[0] + features

outFile.append(masterData[0])

for i in range(1,len(masterData)):
    sentence = masterData[i][9]
    scoreList = []
    for j in range(len(features)):
        score = 0
        for k in range(len(keywordsTable)):
            if features[j] == keywordsTable[k][0]:
                for l in range(1,len(keywordsTable[k])):
                    wrdList = keywordsTable[k][l].split(' ')
                    result = sentenceWordRelation(sentence,wrdList,i,features[j],keywordsTable[k][l][0:3])
                    if result == True:
                        score = score + 1
                        break
                if result == True:
                    break
        scoreList.append(score)
    masterData[i] = masterData[i] + scoreList
    outFile.append(masterData[i])

    if i%10 == 0:
        print(str(i) + " reviews processed.")

masterData_outputFileName = 'Master_Data_Features_Milestone1_temp.csv'
masterData_outputFile = open(masterData_outputFileName, "w", newline='', encoding='utf-8')
csv_out = csv.writer(masterData_outputFile, delimiter='|')
csv_out.writerows(outFile)