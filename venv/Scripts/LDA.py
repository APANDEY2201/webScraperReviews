# Step 0: Import packages and stopwords
import nltk

if __name__ == '__main__':
    from gensim.models import LdaModel, LdaMulticore
    from gensim import corpora
    import gensim.downloader as api
    from gensim.utils import simple_preprocess, lemmatize
    from nltk.corpus import stopwords
    import re
    import logging
    import csv
    from langdetect import detect
    import spacy
    import xlsxwriter
    import datetime
    from gensim import models
    import shutil
    import os

    setTfIDFThreshold = 0.2
    setImpKeywords = True
    setNoun = True
    setAdj = False
    setVerb = False
    setNoOfTopics = 10
    setAlpha = 0.01
    setEta = 0.0001
    setFitBundle = False
    setTempRun = '_temp'

    nlpDe = spacy.load('de_core_news_sm')

    nlpEn = spacy.load("en_core_web_sm")

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

    def germanSpacyPOS(token):
        return nlpDe(token)[0].pos_
    def englishSpacyPOS(token):
        return nlpEn(token)[0].pos_

    # print(germanSpacyPOS('gehen'))
    # print(englishSpacyPOS('language'))

    # print(englishSpacyLemmatizer('going'))
    # print(germanSpacyLemmatizer('gehst'))

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    stop_words_en = stopwords.words('english')
    # stop_words_en = stop_words_en + ['com', 'edu', 'subject', 'lines', 'organization', 'would', 'article', 'could']
    stop_words_de = stopwords.words('german')

    csvFileName1 = 'Master_Data_Milestone1_for_training' + setTempRun + '.csv' #Master_Data_Milestone1_Small_for_training.csv'
    masterDataSmall = list(csv.reader(open(csvFileName1, encoding='utf-8'), delimiter='|'))  # CSV file to 2 dimensional list of string
    reviews = [masterDataSmall[row][9] for row in range(1,len(masterDataSmall))]
    # print(reviews)

    # Step 1: Import the dataset and get the text and real topic of each news article
    # dataset = [['Although', 'our'], ['conceptual', 'arguments', 'are']]

    data_processed = []

    tokenizer = nltk.RegexpTokenizer(r"\w+")
    listNoun = []
    listAdj = []
    listVerb = []
    listNounIds = []
    listAdjIds = []
    listVerbIds = []
    for doc in reviews:
        # stemmerDe = nltk.stem.cistem.Cistem()
        # stemmerEn = nltk.SnowballStemmer("english")
        itsGerman = True
        try:
            if detect(doc) == 'en':
                itsGerman = False
        except:
            itsGerman = True

        doc_out = []

        # doc = nltk.tokenize.word_tokenize(doc)

        doc = tokenizer.tokenize(doc)

        if itsGerman == True:

            for wd in doc:
                wd = wd.lower()
                if wd not in stop_words_de:  # remove stopwords
                    # stemmed_word = stemmerDe.stem(wd).lower()  # stemming
                    lemmed_word = germanSpacyLemmatizer(wd)
                    if germanSpacyPOS(lemmed_word) == 'NOUN':
                        doc_out = doc_out + [lemmed_word]
                        listNoun.append(lemmed_word)
                    if germanSpacyPOS(lemmed_word) == 'ADJ':
                        doc_out = doc_out + [lemmed_word]
                        listAdj.append(lemmed_word)
                    if germanSpacyPOS(lemmed_word) == 'VERB':
                        doc_out = doc_out + [lemmed_word]
                        listVerb.append(lemmed_word)
                else:
                    continue

        else:

            for wd in doc:
                wd = wd.lower()
                if wd not in stop_words_en:  # remove stopwords
                    # stemmed_word = stemmerDe.stem(wd).lower()  # stemming
                    lemmed_word = englishSpacyLemmatizer(wd)
                    if germanSpacyPOS(lemmed_word) == 'NOUN':
                        doc_out = doc_out + [lemmed_word]
                        listNoun.append(lemmed_word)
                    if germanSpacyPOS(lemmed_word) == 'ADJ':
                        doc_out = doc_out + [lemmed_word]
                        listAdj.append(lemmed_word)
                    if germanSpacyPOS(lemmed_word) == 'VERB':
                        doc_out = doc_out + [lemmed_word]
                        listVerb.append(lemmed_word)
                else:
                    continue


        data_processed.append(doc_out)

    listNoun = list(set(listNoun))
    listAdj = list(set(listAdj))
    listVerb = list(set(listVerb))

    # Print a small sample
    # print(data_processed)
    #> ['anarchism', 'originated', 'term', 'abuse', 'first']

    # Step 3: Create the Inputs of LDA model: Dictionary and Corpus
    dct = corpora.Dictionary(data_processed)
    corpus = [dct.doc2bow(line) for line in data_processed]
    noOfTopics = setNoOfTopics

    wordProbs = []
    csvFileName1 = 'keywordsDe.csv'  # Master_Data_Milestone1_Small_for_training.csv'
    impKeywordsDe = list(csv.reader(open(csvFileName1, encoding='utf-8'), delimiter=','))  # CSV file to 2 dimensional list of string
    impKeywordsDeFinal = [i[0] for i in impKeywordsDe]
    csvFileName1 = 'keywordsEn.csv'  # Master_Data_Milestone1_Small_for_training.csv'
    impKeywordsEn = list(csv.reader(open(csvFileName1, encoding='utf-8'), delimiter=','))  # CSV file to 2 dimensional list of string
    impKeywordsEnFinal = [i[0] for i in impKeywordsEn]
    keywordsConstruct1 = [row[1] for row in [row for row in impKeywordsDe+impKeywordsEn if 'overall' == row[0]]]
    keywordsConstruct2 = [row[1] for row in [row for row in impKeywordsDe+impKeywordsEn if 'gender' == row[0]]]
    keywordsConstruct3 = [row[1] for row in [row for row in impKeywordsDe+impKeywordsEn if 'age' == row[0]]]
    keywordsConstruct4 = [row[1] for row in [row for row in impKeywordsDe+impKeywordsEn if 'cultural background' == row[0]]]
    keywordsConstruct5 = [row[1] for row in [row for row in impKeywordsDe+impKeywordsEn if 'sexual orientation' == row[0]]]
    keywordsConstruct6 = [row[1] for row in [row for row in impKeywordsDe+impKeywordsEn if 'handicap' == row[0]]]
    keywordsConstructAll = keywordsConstruct1+keywordsConstruct2+keywordsConstruct3+keywordsConstruct4+keywordsConstruct5+keywordsConstruct6
    keywordsConstructAllIDsInDct = []
    for token, id in dct.token2id.items():
        # print(str(token) + ' ::: ' + str(id))
        if token in keywordsConstructAll:
            keywordsConstructAllIDsInDct.append(id)
        if token in listNoun:
            listNounIds.append(id)
        if token in listAdj:
            listAdjIds.append(id)
        if token in listVerb:
            listVerbIds.append(id)
    # print('keywords in dictionary are : ' + str(len(keywordsConstructAllIDsInDct)))
    # print(keywordsConstructAllIDs)
    tfidf = models.TfidfModel(corpus, id2word=dct)
    tfidf_threshold = setTfIDFThreshold
    low_value_words = []
    for bow in corpus:
        # print(tfidf[bow])
        low_value_words += [id for id, value in tfidf[bow] if value < tfidf_threshold]

    dctOpsLog = []
    dctOpsLog.append('Dictionary contains ' + str(len(dct)) + ' terms before filtering out bad terms.')
    print(dctOpsLog[-1])
    dctOpsLog.append('Making Hit List of terms to filter out from dictionary...')
    print(dctOpsLog[-1])
    hitList = []

    dctOpsLog.append('HitList: Adding ' + str(len(set(low_value_words))) +' terms with TfIDF below threshold of ' + str(tfidf_threshold) + ' to HitList.')
    print(dctOpsLog[-1])
    hitList = set(low_value_words)
    dctOpsLog.append('HitList: Size is ' + str(len(hitList)))
    print(dctOpsLog[-1])

    if setImpKeywords == True:
        dctOpsLog.append('HitList: Removing ' +  str(len(keywordsConstructAllIDsInDct)) +' Important Keywords (which are there in dictionary) from HitList (Remove if occurs).')
        print(dctOpsLog[-1])
        hitList = hitList - set(keywordsConstructAllIDsInDct)
        dctOpsLog.append('HitList: Size is ' + str(len(hitList)))
        print(dctOpsLog[-1])

    if setNoun == True:
        dctOpsLog.append('HitList: Removing ' + str(len(listNounIds)) + ' Nouns (which are there in dictionary) from HitList (Remove if occurs).')
        print(dctOpsLog[-1])
        hitList = hitList - set(listNounIds)
        dctOpsLog.append('HitList: Size is ' + str(len(hitList)))
        print(dctOpsLog[-1])

    if setAdj == True:
        dctOpsLog.append('HitList: Removing ' + str(len(listAdjIds)) + ' Adjectives (which are there in dictionary) from HitList (Remove if occurs).')
        print(dctOpsLog[-1])
        hitList = hitList - set(listAdjIds)
        dctOpsLog.append('HitList: Size is ' + str(len(hitList)))
        print(dctOpsLog[-1])

    if setVerb == True:
        dctOpsLog.append('HitList: Removing ' + str(len(listVerbIds)) + ' Verbs (which are there in dictionary) from HitList (Remove if occurs).')
        print(dctOpsLog[-1])
        hitList = hitList - set(listVerbIds)
        dctOpsLog.append('HitList: Size is ' + str(len(hitList)))
        print(dctOpsLog[-1])

    dctOpsLog.append('Applying HitList filter on dictionary...')
    print(dctOpsLog[-1])
    dct.filter_tokens(bad_ids=list(hitList))
    dctOpsLog.append('Dictionary contains ' + str(len(dct)) + ' terms after filtering out bad terms.')
    print(dctOpsLog[-1])

    corpus = [dct.doc2bow(line) for line in data_processed]

    # print(keywordsConstruct5)
    probSkew=15

    # for t in range(noOfTopics):
    #     wordProbs_temp = []
    #     for d in range(len(dct)):
    #         wordProbs_temp.append(10)
    #         if t == 0:
    #             if dct[d] in keywordsConstruct1:
    #                 wordProbs_temp[d] = probSkew
    #         if t == 1:
    #             if dct[d] in keywordsConstruct2:
    #                 wordProbs_temp[d] = probSkew
    #         if t == 2:
    #             if dct[d] in keywordsConstruct3:
    #                 wordProbs_temp[d] = probSkew
    #         if t == 3:
    #             if dct[d] in keywordsConstruct4:
    #                 wordProbs_temp[d] = probSkew
    #         if t == 4:
    #             if dct[d] in keywordsConstruct5:
    #                 wordProbs_temp[d] = probSkew
    #         if t == 5:
    #             if dct[d] in keywordsConstruct6:
    #                 wordProbs_temp[d] = probSkew
    #     wordProbs.append(wordProbs_temp)

    for d in range(len(dct)):
        wordProbs.append(10)
        if dct[d] in keywordsConstructAll:
            wordProbs[d] = probSkew

    # Step 4: Train the LDA model
    lda_model = LdaModel(corpus=corpus,
                             id2word=dct,
                             random_state=100,
                             num_topics=noOfTopics,
                             passes=10,
                             chunksize=1000,
                             # batch=False,
                             alpha = setAlpha, #alpha='asymmetric', # alpha=1/2, #alpha=[0.5,0.5], #greater than 1 gives docs all topics alomost equal prob
                             decay=0.5,
                             offset=64,
                             eta = setEta, #wordProbs, #eta=None, # eta=1/370,
                             eval_every=0,
                             iterations=100,
                             gamma_threshold=0.001,
                             per_word_topics=True)

    # save the model
    lda_model.save('lda_model.model')

    # See the topics
    lda_model.print_topics(-1)
    # print(lda_model.get_topic_terms(0,370))
    # print(lda_model.get_topic_terms(1,370))
    # print(lda_model.get_term_topics(102,1))

    topicTermsFile = open('TopicTermsData.txt', 'w', encoding='utf-8')
    for s in range(noOfTopics):
        vec = lda_model.get_topic_terms(s,10)#len(dct))
        toPrint = 'Topic no.: ' + str(s) + ' | '
        for h in range(10):#len(dct)):
           toPrint = toPrint + dct.id2token[vec[h][0]] + ' : ' + str(vec[h][1]) + ' | '
        # print(toPrint)
        topicTermsFile.writelines(toPrint + '\n')

    csvFileName2 = 'Master_Data_Milestone1' + setTempRun + '.csv' #Master_Data_Milestone1_Big_for_fitting.csv'
    masterDataBig = list(csv.reader(open(csvFileName2, encoding='utf-8'), delimiter='|'))  # CSV file to 2 dimensional list of string

    csvFileNameOut = 'Master_Data_Milestone1_Fitted' + setTempRun + '.csv'
    csvFileOut = open(csvFileNameOut, "w", newline='', encoding='utf-8')
    csv_out = csv.writer(csvFileOut, delimiter='|')
    csv_out.writerow(masterDataBig[0] + ['topic' + str(i) for i in range(noOfTopics)])

    # for j in range(108, 110):  # len(masterDataBig)):
    benchmarkReviews = []
    loopStep = 1
    if setFitBundle == True:
        loopStep = 10
    for j in range(1, len(masterDataBig),1):
        doc = masterDataBig[j][9].strip()
        if setFitBundle == True:
            doc = ''
            for k in range(j, j + 10):
                doc = doc + ' ' + masterDataBig[k][9].strip()
            masterDataBig[j][9] = doc

        if len(doc) > 5:

            itsGerman = True
            try:
                if detect(doc) == 'en':
                    itsGerman = False
            except:
                itsGerman = True

            doc_out = []

            # doc = nltk.tokenize.word_tokenize(doc)

            doc = tokenizer.tokenize(doc)

            if itsGerman == True:

                for wd in doc:
                    wd = wd.lower()
                    if wd not in stop_words_de:  # remove stopwords
                        # stemmed_word = stemmerDe.stem(wd).lower()  # stemming
                        lemmed_word = germanSpacyLemmatizer(wd)
                        if lemmed_word:
                            doc_out = doc_out + [lemmed_word]
                    else:
                        continue

            else:

                for wd in doc:
                    wd = wd.lower()
                    if wd not in stop_words_en:  # remove stopwords
                        # stemmed_word = stemmerDe.stem(wd).lower()  # stemming
                        lemmed_word = englishSpacyLemmatizer(wd)
                        if lemmed_word:
                            doc_out = doc_out + [lemmed_word]
                    else:
                        continue

            corpus2 = [dct.doc2bow(doc_out)]
            # print(corpus2)
            # word_counts = [[(dct[id], count) for id, count in line] for line in corpus2]
            # print(word_counts)
            vector = lda_model[corpus2[0]]  # get topic probability distribution for a document
            # vector = lda_model[lda_model.id2word.doc2bow(doc_out)]  # get topic probability distribution for a document
            # print(vector)
            vector2 = vector[0]
            finalVector = []
            for k in range(noOfTopics):
                finalVector_temp = []
                finalVector_temp.append(k)
                finalVector_temp.append(0)
                for l in range(len(vector2)):
                    if vector2[l][0] == k:
                        finalVector_temp[1] = vector2[l][1]
                finalVector.append(finalVector_temp)
            csv_out.writerow(masterDataBig[j] + [row[1] for row in finalVector])
            if len(masterDataBig[j][9].strip()) > 50:
                benchmarkReviewsTemp = []
                benchmarkReviewsTemp.append(masterDataBig[j][7].strip())
                benchmarkReviewsTemp.append(masterDataBig[j][8].strip())
                benchmarkReviewsTemp.append(masterDataBig[j][9].strip())
                benchmarkReviewsTemp.append([row[1] for row in finalVector])
                benchmarkReviews.append(benchmarkReviewsTemp)
        if j % 100 == 0:
            print(str(j) + " reviews processed.")

    def reportIt(trainSetProps='', alphaProps='', etaProps='', trunTerms=len(dct)):
        # newpath = r'C:\Program Files\arbitrary'
        # if not os.path.exists(newpath):
        #     os.makedirs(newpath)
        now = datetime.datetime.now()
        currDateTime = (now.strftime("%d%m%Y_%H%M%S"))
        dir = 'LDA_Runs/01_All/' + currDateTime
        if not os.path.exists(dir):
            os.makedirs(dir)
        shutil.copy2('LDA.py', dir + '/LDA_' + currDateTime + '.py')
        shutil.copy2('reviewsPicker.py', dir + '/reviewsPicker_' + currDateTime + '.py')
        workbook = xlsxwriter.Workbook(dir + '/LDA_Report_' + currDateTime + '.xlsx')
        worksheet = workbook.add_worksheet()

        formatBold = workbook.add_format()
        formatBold.set_bold()
        formatRedLeft = workbook.add_format()
        formatRedLeft.set_font_color('red')
        formatRedLeft.set_align('left')
        formatLeft = workbook.add_format()
        formatLeft.set_align('left')
        formatLeftBold = workbook.add_format()
        formatLeftBold.set_bold()
        formatLeftBold.set_align('left')

        worksheet.write(0, 0, 'Training Set Properties:', formatLeftBold)
        worksheet.write(1, 0, trainSetProps, formatLeft)
        worksheet.write(2, 0, 'Alpha (Reviews-Topics Probability Distribution Prior):', formatLeftBold)
        worksheet.write(3, 0, alphaProps, formatLeft)
        worksheet.write(4, 0, 'Eta (Terms-Topics Probability Distribution Prior):', formatLeftBold)
        worksheet.write(5, 0, etaProps, formatLeft)
        worksheet.write(6, 0, 'No. of Topics:', formatLeftBold)
        worksheet.write(7, 0, noOfTopics, formatLeft)
        worksheet.write(8, 0, 'Corpus length:', formatLeftBold)
        worksheet.write(9, 0, len(corpus), formatLeft)
        worksheet.write(10, 0, 'Dictionary Operations:', formatLeftBold)
        dctOps = ''
        for ops in range(len(dctOpsLog)):
            dctOps = dctOps + dctOpsLog[ops] + ' /***/ '
        worksheet.write(11, 0, dctOps)
        worksheet.write(12, 0, 'Topics Terms Distribution:', formatLeftBold)
        if trunTerms == len(dct):
            worksheet.write(13, 0, 'It is not truncated. All topics have all words of dictionary', formatLeft)
        else:
            worksheet.write(13, 0, 'It is truncated for top ' + str(trunTerms) + ' terms in each topic.', formatLeft)

        for s in range(noOfTopics):
            worksheet.write(15, s * 3, 'Topic ' + str(s), formatLeftBold)
            worksheet.write(16, s * 3, 'Word', formatLeftBold)
            worksheet.write(16, (s * 3) + 1, 'Probability', formatLeftBold)
            vec = lda_model.get_topic_terms(s, trunTerms)
            for h in range(trunTerms):
                if dct.id2token[vec[h][0]] in keywordsConstructAll:
                    worksheet.write(h + 17, (s * 3), dct.id2token[vec[h][0]], formatRedLeft)
                else:
                    worksheet.write(h + 17, (s * 3), dct.id2token[vec[h][0]], formatLeft)
                worksheet.write(h + 17, (s * 3) + 1, vec[h][1], formatLeft)

        worksheet2 = workbook.add_worksheet()
        worksheet2.write(0, 0, 'Applying the model on some Benchmark Reviews:', formatLeftBold)
        worksheet2.write(2, 0, 'ReviewAbout', formatLeftBold)
        worksheet2.write(2, 1, 'ReviewScore', formatLeftBold)
        worksheet2.write(2, 2, 'Review', formatLeftBold)
        # print(benchmarkReviews)
        for s in range(noOfTopics):
            worksheet2.write(2, s + 3, 'Topic ' + str(s), formatLeftBold)
        worksheet2.write(2, noOfTopics + 3, 'Peak Topic', formatLeftBold)
        for s in range (len(benchmarkReviews)):
            worksheet2.write(s + 3, 0, str(benchmarkReviews[s][0]), formatLeft)
            worksheet2.write(s + 3, 1, str(benchmarkReviews[s][1]), formatLeft)
            worksheet2.write(s + 3, 2, str(benchmarkReviews[s][2]), formatLeft)
            for o in range(noOfTopics):
                worksheet2.write(s + 3, o + 3, benchmarkReviews[s][3][o], formatLeft)
            worksheet2.write(s+3, noOfTopics + 3, benchmarkReviews[s][3].index(max(benchmarkReviews[s][3])), formatLeft)
        workbook.close()

    reportIt('Out of all reviews, those reviews were selected in which review comments were not null. Reviews were bundled for a user.',
             'Alpha is 0.01',
             'Eta is custom list of probabilities (90 for words appearing in Important Keywords List, and 10 for other words).',
             len(dct))