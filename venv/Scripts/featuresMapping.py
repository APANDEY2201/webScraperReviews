import csv
import nltk


def unique(list1):
    # intilize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)

    return unique_list

def sentenceWordRelation(sentence, wrdList):
    cnt = 0
    stemmerDe = nltk.stem.cistem.Cistem()
    stemmerEn = nltk.SnowballStemmer("english")

    for wrd in wrdList:
        if wrd in sentence:
            cnt = cnt + 1
    if cnt == len(wrdList):
        return True

csvFileName = 'KeywordsTable_output.csv'
keywordsTable = list(csv.reader(open(csvFileName),delimiter=',')) # CSV file to 2 dimensional list of string

csvFileName = 'Master_Data_Milestone1_temp.csv'
masterData = list(csv.reader(open(csvFileName),delimiter='|')) # CSV file to 2 dimensional list of string

features = [i[0] for i in keywordsTable]

features = unique(features)

masterData[0] = masterData[0] + features

print(features)

for i in range(1,len(masterData)):
    sentence = masterData[i][9]
    scoreList = []
    for j in range(len(features)):
        score = 0
        for k in range(len(keywordsTable)):
            if features[j] == keywordsTable[k][0]:
                for l in range(1,len(keywordsTable[k])):
                    wrdList = keywordsTable[k][l].split(' ')
                    result = sentenceWordRelation(sentence,wrdList)
                    if result == True:
                        score = score + 1
                        break
        scoreList.append(score)
    masterData[i] = masterData[i] + scoreList

masterData_outputFileName = 'Master_Data_Features_Milestone1_temp.csv.csv'
masterData_outputFile = open(masterData_outputFileName, "w", newline='', encoding='utf-8')
csv_out = csv.writer(masterData_outputFile, delimiter='|')
csv_out.writerows(masterData)