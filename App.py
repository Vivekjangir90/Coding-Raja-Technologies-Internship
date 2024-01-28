import streamlit as st
import pickle
import requests
import numpy as np
import pandas as pd

st.title('Movie Recommender System')

# Assuming you have these variables defined somewhere
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
number = np.arange(1, 21)

selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)
selected_number = st.selectbox("How many results you want !", number)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=1b46d8d88c680c018f026ea039d36f98&language=en-US".format(movie_id)
    try:
        data = requests.get(url)
        data.raise_for_status()
        data = data.json()

        # Check if 'poster_path' is present and not None
        if 'poster_path' in data and data['poster_path'] is not None:
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            # Handle the case where 'poster_path' is None or not present
            return "No poster available"
    except Exception as e:
        # Suppress the error message for any exception
        return "No poster available"

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []

        for i in distances[1:selected_number + 1]:
            # fetch the movie poster
            movie_id = movies.iloc[i[0]].movie_id
            try:
                recommended_movie_posters.append(fetch_poster(movie_id))
                recommended_movie_names.append(movies.iloc[i[0]].title)
            except Exception as e:
                # Handle any exception for fetch_poster
                pass  # Do nothing, silently ignore the error

        return recommended_movie_names, recommended_movie_posters

    except IndexError:
        # Handle the IndexError for movies['title']
        pass  # Do nothing, silently ignore the error
        return [], []

if st.button("recommend"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    num_rows = selected_number // 5 + 1
    a = 0
    for num in range(num_rows):
        cols = st.columns(5)

        for i, j in enumerate(recommended_movie_names):
            try:
                if i <= 4:
                    movie_name = recommended_movie_names[i + a] 
                    if movie_name is not None:
                        with cols[i]:
                            st.text(movie_name)
                            try:
                                st.image(recommended_movie_posters[i + a])
                            except Exception as e:
                                # movie_name = recommended_movie_names[i + a]
                                # if movie_name is None:
                                a+=1
                                st.image(recommended_movie_posters[i + a])
                                pass  # Suppress the error, do nothing
                
            except Exception as e:
                pass
        a += 5

