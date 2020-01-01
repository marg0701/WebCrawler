import pandas as pd
import pickle
import nltk
from nltk.corpus import stopwords
import numpy as np
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import logging
import pyLDAvis
import pyLDAvis.gensim
np.random.seed(2019)
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.corpus import stopwords

from bson.json_util import dumps
from pymongo import MongoClient
import json

#URL = "mongodb://db:27017/"
#news_client = MongoClient(URL)
#news_database = news_client["news_database"]
#news = news_database["news"]
#df_news = pd.DataFrame(json.loads(dumps(news.find({}))))

def dataset_headers (dataframe):
    data_text = dataframe[['Content', '_id']]
    data_text['index'] = data_text.index
    documents = data_text
    return documents


# Function to perform lemmatize and stem preprocessing steps on the data set
def lemmatize_stemming(text):
    stemmer = PorterStemmer()
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in set(stopwords.words('spanish')) and len(token) > 3:
            #Posesive pronouns
            token.replace("'s", "")
            #Special character cleaning
            token.replace("\r", " ")
            token.replace("\n", " ")
            token.replace("    ", " ")
            #Upcase/downcase
            token.lower()
            #Punctuaction signs
            token.replace('?', '')
            token.replace(':', '')
            token.replace('!', '')
            token.replace('.', '')
            token.replace(',', '')
            token.replace(';', '')
            token.replace("'", '')
            result.append(lemmatize_stemming(token))
    return result

# LDA
def lda (df_news):
    documents = dataset_headers(df_news)
    processed_docs = documents['Content'].map(preprocess)
    documents['Content_processed'] = documents['Content'].map(preprocess)
    dictionary = gensim.corpora.Dictionary(processed_docs)
    dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=100000)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
    # Running LDA using Bag of Words
    lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=5, id2word=dictionary, passes=3, workers=2)
    vis = pyLDAvis.gensim.prepare(topic_model=lda_model, corpus=bow_corpus, dictionary=dictionary)
    pyLDAvis.save_html(vis, 'lda.html')
    return dictionary, bow_corpus, lda_model, processed_docs, documents['Content_processed']

def ldavis(df_news):
    documents = dataset_headers(df_news)
    processed_docs = documents['Content'].map(preprocess)
    documents['Content_processed'] = documents['Content'].map(preprocess)
    dictionary = gensim.corpora.Dictionary(processed_docs)
    dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=100000)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
    # Running LDA using Bag of Words
    lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=5, id2word=dictionary, passes=3, workers=2)
    vis = pyLDAvis.gensim.prepare(topic_model=lda_model, corpus=bow_corpus, dictionary=dictionary)
    return vis


from gensim import corpora, models

"""def lda_tfidf():
    documents = dataset_headers(df_news)
    y,x,_,_,_ = lda()
    tfidf = models.TfidfModel(x)
    corpus_tfidf = tfidf[x]
    lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=10, id2word=y, minimum_probability = .2, passes=2, workers=4)
    return lda_model_tfidf"""


def format_topics_sentences(ldamodel=None, corpus=None, texts=None, ID=None):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row_list in enumerate(ldamodel[corpus]):
        row = row_list[0] if ldamodel.per_word_topics else row_list            
        # print(row)
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    contents_1= pd.Series(ID)
    sent_topics_df = pd.concat([sent_topics_df, contents,contents_1], axis=1)
    return(sent_topics_df)


def show_docs(df_news):
    documents = dataset_headers(df_news)
    _,b,a,c,_ = lda(df_news)
    df_topic_sents_keywords = format_topics_sentences(ldamodel= a, corpus=b, texts=c, ID=df_news['_id'])
    # Format
    df_dominant_topic = df_topic_sents_keywords.reset_index()
    df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text', 'ID']
    return df_dominant_topic  

# Import the wordcloud library
from wordcloud import WordCloud

def word_cloud(topico, nombre, df_news):
    df = show_docs(df_news)
    data = df['Keywords'].unique()
    # Join the different processed titles together.
    long_string = ','.join(pd.Series(data[topico]))
    # Create a WordCloud object
    wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
    # Generate a word cloud
    wordcloud.generate(long_string)
    # Save the image in the img folder:
    wordcloud.to_file("img/" + nombre + ".png")
    # Visualize the word cloud
    return wordcloud.to_image()