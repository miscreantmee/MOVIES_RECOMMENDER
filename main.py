import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle


def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name']) 
    return L


def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
        counter+=1
    return L 


def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L 


def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1


movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pickle.load(open('crdits.pkl','rb'))

movies = movies.merge(credits,on='title')

movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.dropna(inplace=True)

movies['genres'] = movies['genres'].apply(convert)

movies['keywords'] = movies['keywords'].apply(convert)

movies['cast'] = movies['cast'].apply(convert)

movies['cast'] = movies['cast'].apply(lambda x:x[0:3])

movies['crew'] = movies['crew'].apply(fetch_director)

movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)

movies['overview'] = movies['overview'].apply(lambda x:x.split())

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new = movies.drop(columns=['overview','genres','keywords','cast','crew'])

new['tags'] = new['tags'].apply(lambda x: " ".join(x))

cv = CountVectorizer(max_features=5000,stop_words='english')

vector = cv.fit_transform(new['tags']).toarray()

similarity = cosine_similarity(vector)

pickle.dump(similarity,open('siml.pkl','wb'))