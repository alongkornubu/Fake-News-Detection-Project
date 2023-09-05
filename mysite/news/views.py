from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.models import Group
from django.contrib.auth import login , authenticate , logout as auth_logout
from django.contrib import messages
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users , admin_only
import sqlite3
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.linear_model import PassiveAggressiveClassifier
import re

from .forms import *
from .models import *


import requests
from bs4 import BeautifulSoup


from pythainlp.corpus import thai_stopwords 
stop_words = thai_stopwords()
from pythainlp.tokenize import word_tokenize 


# dataframe = pd.read_csv('data/Data.csv')
# tfidf_vectors = pickle.load(open('data/tfidf.pkl','rb'))
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




stop_words = [t.encode('utf-8') for t in list(thai_stopwords())]


tfidf_vectors = TfidfVectorizer(
    tokenizer = text_tokenizer,
    preprocessor = text_processor,
    stop_words=stop_words,
    token_pattern=None,
)



text = df.text
labels = df.label


x_train,x_test,y_train,y_test=train_test_split( text, labels, test_size=0.2, random_state=7)
tfidf_train = tfidf_vectors.fit_transform(x_train)
tfidf_test= tfidf_vectors.transform(x_test)

# Test
# pac=PassiveAggressiveClassifier(max_iter=50)
# pac.fit(tfidf_train,y_train)
# y_pred=pac.predict(tfidf_test)


model = joblib.load('model/model_pac.joblib')
model.fit(tfidf_train,y_train)
y_pred=model.predict(tfidf_test)


def detect(text):
    input_data = [text]

    vectorized_input_data = tfidf_vectors.transform(input_data)
    prediction = model.predict(vectorized_input_data)
    return prediction

def detect_news(request):
    context = {}
    if request.method == 'POST':
        text = request.POST.get('text')
        results = scrap_website(text)
        context['results'] = results
        pred = detect(text)        
        # print('ข้อมูล:',text)
        # print('ทำนาย:',pred)
        if pred == True:
            context['status'] = 'real'
            return render(request, 'news/index.html', context)  
        else:
            context['status'] = 'fake'
        
       
    return render(request, 'news/index.html', context)


@login_required(login_url = 'login')
@admin_only
def upload_csv(request):
    context = {}
    if request.method == 'POST':
        csv_file = request.FILES['csv_upload']
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'ไม่ใช่ไฟล์ .csv')
        else:
            file_path = os.path.join(settings.BASE_DIR, 'data', csv_file.name)
            messages.success(request,'อัพโหลดเสร็จเรียบร้อย',file_path) 
        data = pd.read_csv(csv_file)
        # print("test file",data)
        # print(data)
        my_models = train_model(data)
        context['my_models'] = my_models
    return render(request,'news/train.html',context)

def train_model(csv):
    texts = csv.text
    label = csv.label
    
    x_train,x_test,y_train,y_test=train_test_split( texts, label, test_size=0.2, random_state=7)
    tfidf_train = tfidf_vectors.fit_transform(x_train)
    tfidf_test= tfidf_vectors.transform(x_test)
    pac = PassiveAggressiveClassifier(max_iter=50)
    pac.fit(tfidf_train,y_train)
    y_pred=pac.predict(tfidf_test)
    score = accuracy_score(y_test,y_pred)
    scores = f'Accurary:{round(score*100,2)}%'
    filename = 'model_pac.joblib'
    file_path = os.path.join(settings.BASE_DIR, 'model', filename)
    my_models = joblib.dump(pac, file_path) 
    return my_models, scores

def news_feedback(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        title = request.POST.get('title')
        label = request.POST.get('label')
        category_name = request.POST.get('category')
        text = request.POST.get('text')
        # categorys = Category.objects.all()
       
        if name == '' or label == '' or name == '' or title == '' or text == '' or category_name == '':
            context['status'] = 'alert'
            return render(request, 'news/feedback.html',context)
        category, _ = Category.objects.get_or_create(name=category_name)
        
        f = News.objects.create(name=name,title=title,label=label,text=text,category=category)
        if 'images' in request.FILES:
            img = request.FILES['images']
            f.image = img
            f.save()
        context['status'] = 'success'
    return render(request, 'news/feedback.html',context)



def follow(request):
    news = News.objects.all()
    categories = Category.objects.all()
    category_id = request.GET.get('category')

    if category_id:
        news = news.filter(category_id=category_id)
    context = {'categories': categories, 'news': news}
    return render(request,'news/follow.html',context)

def details(request,id):
    id_news = News.objects.get(id=id)
   
    context = {
        'id_news':id_news,
        
    }
    return render(request,'news/details.html',context)
    

def signup_view(request):
    form= Registerform()
    if request.method == 'POST':
        form = Registerform(request.POST)
        if form.is_valid():
            user =  form.save()
            group = Group.objects.get(name='member')
            user.groups.add(group)
            return redirect('login')
        else:
            messages.error(request,('กรุณากรอกข้อมูลให้ถูกต้อง'))
            form = Registerform()
    return render (request,'news/signup.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("follow")
        else:
            messages.error(request, ('กรุณากรอกข้อมูลให้ถูกต้อง'))
            return redirect("login")
    else:
        return render(request,"news/login.html")

def logout(request):
    auth_logout(request)
    return redirect('/')


        
def feed_model(request):
    datas = News.objects.last()
    context = {'datas':[datas]}
    return render(request,'news/feed_model.html',context)



def scrap_website(query):
    url = f'https://www.google.com/search?q={query}&num=2'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for g in soup.find_all('div', class_='g'):
        link = g.find('a')['href']
        title = g.find('h3').text
        result = {'title': title, 'link': link,}

        results.append(result)
    return results






