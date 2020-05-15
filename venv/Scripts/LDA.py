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

    csvFileName1 = 'Master_Data_Milestone1_for_training.csv' #Master_Data_Milestone1_Small_for_training.csv'
    masterDataSmall = list(csv.reader(open(csvFileName1, encoding='utf-8'), delimiter='|'))  # CSV file to 2 dimensional list of string
    reviews = [row[9] for row in masterDataSmall]
    # print(reviews)

    # Step 1: Import the dataset and get the text and real topic of each news article
    # dataset = [['Although', 'our'], ['conceptual', 'arguments', 'are']]

    data_processed = []

    tokenizer = nltk.RegexpTokenizer(r"\w+")

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
                    if germanSpacyPOS(lemmed_word) == 'NOUN' or germanSpacyPOS(lemmed_word) == 'ADJ' or germanSpacyPOS(lemmed_word) == 'VERB':
                        doc_out = doc_out + [lemmed_word]
                else:
                    continue

        else:

            for wd in doc:
                wd = wd.lower()
                if wd not in stop_words_en:  # remove stopwords
                    # stemmed_word = stemmerDe.stem(wd).lower()  # stemming
                    lemmed_word = englishSpacyLemmatizer(wd)
                    if englishSpacyPOS(lemmed_word) == 'NOUN' or englishSpacyPOS(lemmed_word) == 'ADJ' or englishSpacyPOS(lemmed_word) == 'VERB':
                        doc_out = doc_out + [lemmed_word]
                else:
                    continue


        data_processed.append(doc_out)

    # Print a small sample
    # print(data_processed)
    #> ['anarchism', 'originated', 'term', 'abuse', 'first']

    # Step 3: Create the Inputs of LDA model: Dictionary and Corpus
    dct = corpora.Dictionary(data_processed)
    corpus = [dct.doc2bow(line) for line in data_processed]

    noOfTopics = 10

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
    keywordsConstructAllIDs = []
    for token, id in dct.token2id.items():
        if token in keywordsConstructAll:
            keywordsConstructAllIDs.append(id)
    print('keywords in dictionary are : ' + str(len(keywordsConstructAllIDs)))
    # print(keywordsConstructAllIDs)
    tfidf = models.TfidfModel(corpus, id2word=dct)
    low_value = 0.6
    low_value_words = []
    for bow in corpus:
        low_value_words += [id for id, value in tfidf[bow] if value < low_value]
    # print(low_value_words)
    dct.filter_tokens(bad_ids=list(set(low_value_words) - set(keywordsConstructAllIDs)))
    corpus = [dct.doc2bow(line) for line in data_processed]

    # print(keywordsConstruct5)
    for t in range(noOfTopics):
        wordProbs_temp = []
        for d in range(len(dct)):
            wordProbs_temp.append(10)
            if t == 0:
                if dct[d] in keywordsConstruct1:
                    wordProbs_temp[d] = 90
            if t == 1:
                if dct[d] in keywordsConstruct2:
                    wordProbs_temp[d] = 90
            if t == 2:
                if dct[d] in keywordsConstruct3:
                    wordProbs_temp[d] = 90
            if t == 3:
                if dct[d] in keywordsConstruct4:
                    wordProbs_temp[d] = 90
            if t == 4:
                if dct[d] in keywordsConstruct5:
                    wordProbs_temp[d] = 90
            if t == 5:
                if dct[d] in keywordsConstruct6:
                    wordProbs_temp[d] = 90
        wordProbs.append(wordProbs_temp)

    # Step 4: Train the LDA model
    lda_model = LdaMulticore(corpus=corpus,
                             id2word=dct,
                             random_state=100,
                             num_topics=noOfTopics,
                             passes=10,
                             chunksize=1000,
                             batch=False,
                             alpha = 0.01, #alpha='asymmetric', # alpha=1/2, #alpha=[0.5,0.5], #greater than 1 gives docs all topics alomost equal prob
                             decay=0.5,
                             offset=64,
                             eta = wordProbs, #eta=None, # eta=1/370,
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

    csvFileName2 = 'Master_Data_Milestone1.csv' #Master_Data_Milestone1_Big_for_fitting.csv'
    masterDataBig = list(csv.reader(open(csvFileName2, encoding='utf-8'), delimiter='|'))  # CSV file to 2 dimensional list of string

    csvFileNameOut = 'Master_Data_Milestone1_Fitted.csv'
    csvFileOut = open(csvFileNameOut, "w", newline='', encoding='utf-8')
    csv_out = csv.writer(csvFileOut, delimiter='|')
    csv_out.writerow(masterDataBig[0] + ['topic' + str(i) for i in range(noOfTopics)])

    # for j in range(108, 110):  # len(masterDataBig)):
    benchmarkReviews = []
    for j in range(1, len(masterDataBig)):
        doc = masterDataBig[j][9].strip()
        if doc != '':

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
                benchmarkReviewsTemp.append(masterDataBig[j][9].strip())
                benchmarkReviewsTemp.append([row[1] for row in finalVector])
                benchmarkReviews.append(benchmarkReviewsTemp)
        if j % 100 == 0:
            print(str(j) + " reviews processed.")

    def reportIt(trainSetProps='', alphaProps='', etaProps='', trunTerms=len(dct)):
        now = datetime.datetime.now()
        currDateTime = (now.strftime("%d%m%Y_%H%M%S"))
        workbook = xlsxwriter.Workbook('LDA_Report_' + currDateTime + '.xlsx')
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
        worksheet.write(10, 0, 'Dictionary length:', formatLeftBold)
        worksheet.write(11, 0, len(dct), formatLeft)
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
        worksheet2.write(2, 0, 'Review', formatLeftBold)
        # print(benchmarkReviews)
        for s in range(noOfTopics):
            worksheet2.write(2, s + 1, 'Topic ' + str(s), formatLeftBold)
        for s in range (len(benchmarkReviews)):
            worksheet2.write(s + 3, 0, str(benchmarkReviews[s][0]), formatLeft)
            for o in range(noOfTopics):
                worksheet2.write(s + 3, o + 1, benchmarkReviews[s][1][o], formatLeft)
        workbook.close()

    reportIt('Out of all reviews, those reviews were selected in which review comments were not null.',
             'Alpha is 0.01',
             'Eta is custom list of probabilities (90 for words appearing in Important Keywords List, and 10 for other words.',
             len(dct))