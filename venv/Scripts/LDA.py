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

    nlpDe = spacy.load('de_core_news_sm')

    nlpEn = spacy.load("en_core_web_sm")

    def germanSpacyLemmatizer(token):
        lemmed = ''
        for t in nlpDe.tokenizer(token):
            lemmed = lemmed + ' ' + t.lemma_
        return lemmed.strip()

    def englishSpacyLemmatizer(token):
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

    csvFileName1 = 'Master_Data_Milestone1_for_training_temp.csv' #Master_Data_Milestone1_Small_for_training.csv'
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
    # print(str(len(dct)) + ' unique tokens')
    corpus = [dct.doc2bow(line) for line in data_processed]

    noOfTopics = 10

    # Step 4: Train the LDA model
    lda_model = LdaMulticore(corpus=corpus,
                             id2word=dct,
                             random_state=100,
                             num_topics=noOfTopics,
                             passes=10,
                             chunksize=1000,
                             batch=False,
                             alpha = 0.8, #alpha='asymmetric', # alpha=1/2, #alpha=[0.5,0.5], #greater than 1 gives docs all topics alomost equal prob
                             decay=0.5,
                             offset=64,
                             eta = 1/len(dct), #eta=None, # eta=1/370,
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

    topicTermsFile = open('TopicTermsData.txt', 'w')
    for s in range(noOfTopics):
        vec = lda_model.get_topic_terms(s,len(dct))
        toPrint = 'Topic no.: ' + str(s) + ' | '
        for h in range(len(dct)):
           toPrint = toPrint + dct.id2token[vec[h][0]] + ' : ' + str(vec[h][1]) + ' | '
        print(toPrint)
        topicTermsFile.writelines(toPrint + '\n')

    csvFileName2 = 'Master_Data_Milestone1_temp.csv' #Master_Data_Milestone1_Big_for_fitting.csv'
    masterDataBig = list(csv.reader(open(csvFileName2), delimiter='|'))  # CSV file to 2 dimensional list of string

    csvFileNameOut = 'Master_Data_Milestone1_Fitted_temp.csv'
    csvFileOut = open(csvFileNameOut, "w", newline='', encoding='utf-8')
    csv_out = csv.writer(csvFileOut, delimiter='|')
    csv_out.writerow(masterDataBig[0] + ['topic' + str(i) for i in range(noOfTopics)])

    # for j in range(108, 110):  # len(masterDataBig)):
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

        if j % 100 == 0:
            print(str(j) + " reviews processed.")