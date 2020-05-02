import requests
from nltk.corpus import wordnet
import nltk
from nltk.stem.snowball import SnowballStemmer
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

deWord = 'frau'
enWord = 'woman'
sentence = 'women are not given equal opportunities. Bis zum mittleren Management durchweg homogene Stellenbesetzung. Darüber leider keine einzige Frau.Beim Wiedereinstieg sollen Müttern volle Unterstützung bekommen. In der Realität sieht es manchmal leider anders aus.'

deSyns = []
enSyns = []

stemmer = nltk.stem.cistem.Cistem()
URL = "https://www.openthesaurus.de/synonyme/search?q=frau&format=application/json"
r = requests.get(url=URL)
data = r.json()
noDeSyns = len(data['synsets'][0]['terms'])
for i in range(noDeSyns):
    deSyns.append(stemmer.stem(data['synsets'][0]['terms'][i]['term'].lower()))
deSyns = unique(deSyns)
# print(deSyns)

stemmer = SnowballStemmer("english")
enSynsTemp = wordnet.synsets(enWord)
noEnSyns = len(enSynsTemp)
for i in range(len(enSynsTemp)):
    enSyns.append(stemmer.stem(enSynsTemp[i].lemmas()[0].name().lower()))
enSyns = unique(enSyns)
# print(enSyns)

stemmerDe = nltk.stem.cistem.Cistem()
stemmerEn = SnowballStemmer("english")

word_tokens = nltk.tokenize.word_tokenize(sentence.lower())
# print(word_tokens)

comparators = enSyns + deSyns

matchBool = False
for i in range(len(comparators)):
    for j in range(len(word_tokens)):
        if comparators[i] in stemmerEn.stem(word_tokens[j]):
            matchBool = True
            break
        if comparators[i] in stemmerDe.stem(word_tokens[j]):
            matchBool = True
            break

if matchBool == True:
    print('Yes, its a match.')
else:
    print('No, its not a match.')