import streamlit as st
import pickle
import requests
import numpy as np

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
    try:import requests
import streamlit as st
import pandas as pd
import json


if 'page_number' not in st.session_state:
    st.session_state.page_number = 1
    st.session_state.button_states = {'previous_button': False, 'next_button': False}


@st.cache
def load_data(filename):
    return pd.read_json(filename)


genres = load_data("genres.json")
gentable = genres.set_index('name')['id'].to_dict()


data = load_data("popular.json")
casttable = data.set_index('name')['id'].to_dict()


def name_to_id(selected, table):
    return [table.get(i) for i in selected]


def fetch_data(api_key, params, url):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def display_results(results, item_name):
    items = results['results']
    title_m = [x[item_name] for x in items]
    post_m = [x["poster_path"] for x in items]
    rows = len(title_m) // 5 + 1
    for j in range(rows):
        st.container():
        cols = st.columns([1] * 5)
        for idx, name in enumerate(title_m[j*5:(j+1)*5]):
            if name is not None:
                cols[idx].text(name)
                cols[idx].image(
                    f"https://image.tmdb.org/t/p/w500/{post_m[j*5+idx]}")


def discover(params, genres, casts, api_key):
    params["with_genres"] = ",".join(str(genre)
                                     for genre in genres if genre is not None)
    params["with_cast"] = ",".join(str(cast)
                                   for cast in casts if cast is not None)
    results1 = fetch_data(api_key, params, "https://api.themoviedb.org/3/discover/movie")
    display_results(results1, "title")

    params["first_air_date_year"] = params["primary_release_year"]
    results2 = fetch_data(api_key, params, "https://api.themoviedb.org/3/discover/tv")
    display_results(results2, "original_name")


def app():
    col1, coldiscover(params, name_to_id(selected_genres, gentable),
                name_to_id(selected_casts, casttable),
                "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYjQ2ZDhkODhjNjgwYzAxOGYwMjZlYTAzOWQzNmY5OCIsInN1YiI6IjY1YTdmNzM0Mzg3NjUxMDEzMDFhNmViZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XGohA1BMLe83L_GR87D6hI8B2HVtdR0zpuJeizbH9_8")

    if st.session_state.get('button_states', {}).get('previous_button', True):
        st.button("previous")
    if st.session_state.get('button_states', {}).get('next_button', True):
        st.button("next")

if __name__ == "__main__":
    app()discover(params, name_to_id(selected_genres, gentable),
                name_to_id(selected_casts, casttable),
                "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYjQ2ZDhkODhjNjgwYzAxOGYwMjZlYTAzOWQzNmY5OCIsInN1YiI6IjY1YTdmNzM0Mzg3NjUxMDEzMDFhNmViZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XGohA1BMLe83L_GR87D6hI8B2HVtdR0zpuJeizbH9_8")

    if st.session_state.get('button_states', {}).get('previous_button', True):
        st.button("previous")
    if st.session_state.get('button_states', {}).get('next_button', True):
        st.button("next")

if __name__ == "__main__":
    app()
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

