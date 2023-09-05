from django.core.management.base import BaseCommand
from news.models import *
from django.db import connection
import pandas as pd
import joblib
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

# Test file
import os
from django.conf import settings

from pythainlp.corpus import thai_stopwords 
stop_words = thai_stopwords()
from pythainlp.tokenize import word_tokenize
import sqlite3

connect = sqlite3.connect('db.sqlite3')
query = str(News.objects.all().query)
df = pd.read_sql_query(query,connect)
connect.close()
data = list(News.objects.values('id','title','text','label','category'))
df= pd.DataFrame(data)
# print(df)


def text_tokenizer(text):
    terms = [k.strip() for k in word_tokenize(text) if len(k.strip()) > 0 and k.strip()] 
    return [t for t in terms]

def text_processor(text):
    text = re.sub(r'[!@#$%^&*()_+\-=\[\]{};\'\\:"|<,./<>? ]', '', text)
    text = re.sub(r'\n+', ' ', text.strip())
    text = re.sub(r'\s+', ' ', text.strip())
    return text

text = df.text
labels = df.label

stop_words = [t.encode('utf-8') for t in list(thai_stopwords())]

tfidf_vectors = TfidfVectorizer(
    tokenizer = text_tokenizer,
    preprocessor = text_processor,
    ngram_range=(2,3),
    stop_words=stop_words,
    token_pattern=None,
)


x_train,x_test,y_train,y_test=train_test_split( text, labels, test_size=0.2, random_state=7)
tfidf_train = tfidf_vectors.fit_transform(x_train)
tfidf_test= tfidf_vectors.transform(x_test)        

class Command(BaseCommand):
    help = 'train model'
    
    def handle(self, *args, **options):
        # xtrain ytrain csv  model.pkl accu 
        pac = PassiveAggressiveClassifier(max_iter=50)
        pac.fit(tfidf_train,y_train)
        y_pred=pac.predict(tfidf_test)
        score = accuracy_score(y_test,y_pred)
        print(f'Accurary:{round(score*100,2)}%')
        filename = 'model_feedback.joblib'
        file_path = os.path.join(settings.BASE_DIR, 'model', filename)
        joblib.dump(pac, file_path) 

        self.stdout.write(self.style.SUCCESS(f'Successfully saved file model "{filename}"'))   
        