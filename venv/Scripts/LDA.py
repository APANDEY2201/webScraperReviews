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

    # print(englishSpacyLemmatizer('going'))
    # print(germanSpacyLemmatizer('gehst'))

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    stop_words_en = stopwords.words('english')
    stop_words_en = stop_words_en + ['com', 'edu', 'subject', 'lines', 'organization', 'would', 'article', 'could']
    stop_words_de = stopwords.words('german')

    csvFileName = 'Master_Data_Milestone1_Small_for_training.csv'
    masterDataSmall = list(csv.reader(open(csvFileName), delimiter='|'))  # CSV file to 2 dimensional list of string
    reviews = [row[9] for row in masterDataSmall]
    # print(reviews)

    # Step 1: Import the dataset and get the text and real topic of each news article
    # dataset = [['Although', 'our'], ['conceptual', 'arguments', 'are']]

    data_processed = []

    tokenizer = nltk.RegexpTokenizer(r"\w+")

    for doc in reviews:
        stemmerDe = nltk.stem.cistem.Cistem()
        stemmerEn = nltk.SnowballStemmer("english")
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


        data_processed.append(doc_out)

    # Print a small sample
    # print(data_processed)
    #> ['anarchism', 'originated', 'term', 'abuse', 'first']

    # Step 3: Create the Inputs of LDA model: Dictionary and Corpus
    dct = corpora.Dictionary(data_processed)
    corpus = [dct.doc2bow(line) for line in data_processed]

    # Step 4: Train the LDA model
    lda_model = LdaMulticore(corpus=corpus,
                             id2word=dct,
                             random_state=100,
                             num_topics=7,
                             passes=10,
                             chunksize=1000,
                             batch=False,
                             alpha='asymmetric',
                             decay=0.5,
                             offset=64,
                             eta=None,
                             eval_every=0,
                             iterations=100,
                             gamma_threshold=0.001,
                             per_word_topics=True)

    # save the model
    lda_model.save('lda_model.model')

    # See the topics
    lda_model.print_topics(-1)