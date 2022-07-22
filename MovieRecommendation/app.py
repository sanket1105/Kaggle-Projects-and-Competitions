import os 
os.chdir("e:\Kaggle-Projects-and-Competitions\MovieRecommendation")
print(os.getcwd())
## changing the cwd 

import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movies = pd.DataFrame(movies_dict)

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Which movie you want to select",
    movies['title'].values)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path



def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x:x[1])[1:6]

    movie_arr = []
    movie_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        movie_posters.append(fetch_poster(movie_id))
        movie_arr.append(movies.iloc[i[0]].title)

    return movie_arr, movie_posters


if st.button("Recommend"):
    recommendation_movie, recommendation_posters=recommend(selected_movie_name)
    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.text(recommendation_movie[0])
        st.image(recommendation_posters[0])

    with col2:
        st.text(recommendation_movie[1])
        st.image(recommendation_posters[1])  

    with col3:
        st.text(recommendation_movie[2])
        st.image(recommendation_posters[2])  

    with col4:
        st.text(recommendation_movie[3])
        st.image(recommendation_posters[3])  

    with col5:
        st.text(recommendation_movie[4])
        st.image(recommendation_posters[4])                