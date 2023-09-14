import streamlit as st
import pickle
import pandas as pd
import requests
import main



def fetch_posters(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=1c5ac1007dba4d853b6b7312cb3fa3b0&language=en-US".format(movie_id)
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data= response.json()
    return "https://image.tmdb.org/t/p/original" + data['poster_path']




def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_lists = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_lists:
        movie_id=movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_posters(movie_id))
    return recommended_movies,recommended_movies_posters




if __name__ == '__main__':
    movies_dict = pickle.load(open('movies_dict.pkl','rb'))
    movies = pd.DataFrame(movies_dict)
    similarity=pickle.load(open('siml.pkl','rb'))
    st.title('MOVIE RECOMMENDATION SYSTEM')
    selected_movie_name = st.selectbox(
        'How would you like to be contacted?',
        movies['title'].values)

    if st.button('Recommend'):

        names,posters=recommend(selected_movie_name)

        col1, col2, col3,col4 ,col5 = st.columns(5)

        with col1:
            st.header(names[0])
            st.image(posters[0])

        with col2:
            st.header(names[1])
            st.image(posters[1])

        with col3:
            st.header(names[2])
            st.image(posters[2])

        with col4:
            st.header(names[3])
            st.image(posters[3])
        with col5:
            st.header(names[4])
            st.image(posters[4])