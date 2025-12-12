import pickle
import streamlit as st
import requests

st.set_page_config(page_title="Movie Recommender", layout="wide")

page_style = """
<style>
body {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: white;
}
h1, h2, h3, h4, h5 {
    color: #FFD700 !important;
}
.movie-card {
    background-color: rgba(255, 255, 255, 0.07);
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    transition: 0.3s;
}
.movie-card:hover {
    transform: scale(1.05);
    background-color: rgba(255, 255, 255, 0.15);
}
.stButton>button {
    background: linear-gradient(90deg, #ff8c00, #e52e71);
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 18px;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.1);
    background: linear-gradient(90deg, #e52e71, #ff8c00);
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = (
        "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    ).format(movie_id)
    data = requests.get(url).json()
    poster_path = data.get("poster_path", "")
    return "https://image.tmdb.org/t/p/w500/" + poster_path

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[movie_index])),
        reverse=True,
        key=lambda x: x[1],
    )

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_links = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_links.append(f"https://www.themoviedb.org/movie/{movie_id}")

    return recommended_movie_names, recommended_movie_posters, recommended_movie_links


movies = pickle.load(open("movie_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

st.markdown("<h1 style='text-align: center;'>🎬 Movie Recommender System by papon Biswas</h1>", unsafe_allow_html=True)

movie_list = movies["title"].values
selected_movie = st.selectbox("✨ Choose a Movie", movie_list)

if st.button("🔍 Show Recommendation"):
    names, posters, links = recommend(selected_movie)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(
                f"""
                <div class='movie-card'>
                    <h4>{names[idx]}</h4>
                    <a href="{links[idx]}" target="_blank">
                        <img src="{posters[idx]}" width="180">
                    </a>
                </div>
                """,
                unsafe_allow_html=True,
            )