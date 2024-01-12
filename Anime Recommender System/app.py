import pickle
import requests
import warnings
import pandas as pd
import streamlit as st
from streamlit_player import st_player
from concurrent.futures import ThreadPoolExecutor
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

# Suppress warnings
warnings.filterwarnings('ignore')

# Set Streamlit page configuration
st.set_page_config(layout="wide")

# Add custom CSS to remove space at the top

custom_css = """
<style>
    #MainMenu {
        visibility: hidden;
    }

    .st-bk {
        height: 0px !important; /* Set height to 0px to remove space */
        margin-top: -20px !important; /* Adjust margin-top as needed */
    }

    [data-testid="stAppViewContainer"] {
        background-image: url('https://images6.alphacoders.com/133/1330235.png');
        background-size: cover;
        margin-top: 0px; /* Set margin-top to 0px to remove space */
    }

    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
        padding: 0px !important; /* Set padding to 0px to remove space */
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Lazy load DataFrame from CSV file
@st.cache_resource
def load_data():
    # Load preprocessed data from CSV file
    df = pd.read_csv('preprocessed_anime.csv')
    # Get unique movie titles
    movie_list = df['Title'].unique().tolist()
    return df, movie_list

# Lazy load similarity scores
@st.cache_resource
def load_similarity_scores():
    # Load precomputed similarity scores using TF-IDF
    with open('anime_similarity_1.pkl', 'rb') as file:
        similarity = pickle.load(file)
    return similarity

# Ensure similarity scores are loaded
similarity = load_similarity_scores()

def recommend(anime, df, similarity):
    try:
        # Get the index of the selected anime
        index = df[df['Title'] == anime].index[0]

        # Get the similarity scores for the selected anime
        anime_similarity_scores = similarity[index]

        # Sort and get top 5 recommended anime
        top_recommendations = sorted(
            enumerate(anime_similarity_scores), 
            key=lambda x: x[1], 
            reverse=True
        )[1:6]

        # Get the titles of the top recommended anime
        recommended_titles = [df.iloc[i[0]].Title for i in top_recommendations]

        return recommended_titles
    except IndexError:
        st.warning("Anime not found in the dataset.")
        return []

def recommend_knn(anime, df, similarity):
    try:
        # Get the index of the selected anime
        index = df[df['Title'] == anime].index[0]

        # Get the similarity scores for the selected anime
        anime_similarity_scores = similarity[index]

        # Sort and get top 5 recommended anime
        top_recommendations = sorted(
            enumerate(anime_similarity_scores), 
            key=lambda x: x[1], 
            reverse=True
        )[1:6]

        # Get the titles of the top recommended anime
        recommended_titles = [df.iloc[i[0]].Title for i in top_recommendations]

        return recommended_titles
    except IndexError:
        st.warning("Anime not found in the dataset.")
        return []

def anime_detail(anime_name):
    summary = df[df['Title']==anime_name].Summary.iloc[0]
    rating = df[df['Title']==anime_name].Rating.iloc[0]
    poster = df[df['Title']==anime_name].Poster.iloc[0]

    return anime_name,summary,rating,poster

# Streamlit application starts here
st.title("Anime Recommender System")

# Load data and get unique movie titles
df, movie_list = load_data()

# Dropdown to select a movie
selected_movie = st.selectbox(
    "Type or select a anime",
    movie_list
)

# Button to trigger movie recommendations
btn = st.button("Suggest Anime")

# Update the button click section
if btn:
    with st.spinner('Generating recommendations...'):
        recommendations = recommend_knn(selected_movie, df, similarity)

    if recommendations:
        # Display information about the selected movie
        st.info(f"Top 5 Anime like {selected_movie} are-")

        col1,col2,col3,col4,col5=st.columns(5)

        with col1:                
            anime = recommendations[0]
            anime_name,summary,rating,poster=anime_detail(anime)

            if poster:
                # Display the movie poster
                st.markdown(f'<img src="{poster}" style=" width: 200px;border-radius: 10%;">', unsafe_allow_html=True)
            st.markdown(f"**{anime_name}**")
            if rating:
                st.markdown(f"**Rating** - :star2: {round(rating, 1)}")

        with col2:                
            anime = recommendations[1]
            anime_name,summary,rating,poster=anime_detail(anime)

            if poster:
                # Display the movie poster
                st.markdown(f'<img src="{poster}" style="width: 200px;border-radius: 10%;">', unsafe_allow_html=True)
            st.markdown(f"**{anime_name}**")
            if rating:
                st.markdown(f"**Rating** - :star2: {round(rating, 1)}")

        with col3:                
            anime = recommendations[2]
            anime_name,summary,rating,poster=anime_detail(anime)

            if poster:
                # Display the movie poster
                st.markdown(f'<img src="{poster}" style="width: 200px;border-radius: 10%;">', unsafe_allow_html=True)
            st.markdown(f"**{anime_name}**")
            if rating:
                st.markdown(f"**Rating** - :star2: {round(rating, 1)}")

        with col4:                
            anime = recommendations[3]
            anime_name,summary,rating,poster=anime_detail(anime)

            if poster:
                # Display the movie poster
                st.markdown(f'<img src="{poster}" style="width: 200px;border-radius: 10%;">', unsafe_allow_html=True)
            st.markdown(f"**{anime_name}**")
            if rating:
                st.markdown(f"**Rating** - :star2: {round(rating, 1)}")

        with col5:                
            anime = recommendations[4]
            anime_name,summary,rating,poster=anime_detail(anime)

            if poster:
                # Display the movie poster
                st.markdown(f'<img src="{poster}" style="width: 200px;border-radius: 10%;">', unsafe_allow_html=True)
            st.markdown(f"**{anime_name}**")
            if rating:
                st.markdown(f"**Rating** - :star2: {round(rating, 1)}")
