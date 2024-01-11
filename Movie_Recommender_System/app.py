import pickle
import requests
import warnings
import pandas as pd
import streamlit as st
from streamlit_player import st_player
from concurrent.futures import ThreadPoolExecutor
from helper import movie_meta_data, director_meta_data, cast_meta_data

warnings.filterwarnings('ignore')

st.set_page_config(layout="wide")

# Lazy load DataFrame from CSV file
@st.cache_resource
def load_data():
    df = pd.read_csv('25K_movies_preprocessed.csv', usecols=['title', 'movie_id'])
    movie_list = df['title'].unique().tolist()
    return df, movie_list

# Lazy load similarity scores
@st.cache_resource
def load_similarity_scores():
    similarity = pickle.load(open('similarity_with_5000_tfidf.pkl', 'rb'))
    return similarity

similarity = load_similarity_scores()  
def recommend_parallel(movie, df, similarity, batch_size=1000):
    try:
        index = df[df['title'] == movie].index[0]

        # Calculate the number of batches
        num_batches = len(similarity[index]) // batch_size + 1

        # Process similarity matrix in batches
        recommended_movies = []
        with ThreadPoolExecutor() as executor:
            for batch_num in range(num_batches):
                start_idx = batch_num * batch_size
                end_idx = (batch_num + 1) * batch_size
                batch_distances = list(executor.map(lambda x: (x[0], x[1]), enumerate(similarity[index][start_idx:end_idx])))
                recommended_movies.extend(batch_distances)

        # Sort and get top 5 recommended movies
        distances = sorted(recommended_movies, reverse=True, key=lambda x: x[1])
        top_recommendations = [df.iloc[i[0]].movie_id for i in distances[1:6]]
        return top_recommendations
    except IndexError:
        st.warning("Movie not found in the dataset.")
        return []


st.title("Movie Recommender System")

df, movie_list = load_data()  # Ensure data is loaded

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

btn = st.button("Suggest Movie")

# Update the button click section
if btn:
    with st.spinner('Generating recommendations...'):
        recommendations = recommend_parallel(selected_movie, df, similarity)

    if recommendations:
        index_selected_movie=df[df['title'] == selected_movie]['movie_id'].iloc[0]
        title1, summary1, movie_poster1, youtube_trailer_url1, genre_text1, rating1 = movie_meta_data(index_selected_movie)

        st.info(f'Selected Movie - {selected_movie}')
        c1,c2=st.columns(2)
        with c1:
            if movie_poster1:
                st.markdown(f'<img src="{movie_poster1}" style="width: 160px; height:200px;border-radius: 10%;">', unsafe_allow_html=True)
        with c2:    
            if rating1:
                st.markdown(f"**Rating** - :star2: {round(rating1, 1)}")
    
            if genre_text1:
                st.write(f"Genre - {genre_text1}")
            
            if summary1:
                st.write(f"Summary - {summary1}")

        st.write(" ")
        st.success(f"Top 5 Recommended Movies are --")

            
        for movie_id in recommendations:
            try:
                movie_info = movie_meta_data(movie_id)

                if movie_info:
                    title, summary, movie_poster, youtube_trailer_url, genre_text, rating = movie_info
                    cast = cast_meta_data(movie_id)
                    director = director_meta_data(movie_id)

                    st.write("")
                    tab1, tab2 = st.tabs(["Movie Details", "Trailer"])

                    with tab1:
                        col1, col2 = st.columns(2)
                        with col1:
                            if movie_poster:
                                st.markdown(f'<img src="{movie_poster}" style="height: 600px; border-radius: 10%;">', unsafe_allow_html=True)

                        with col2:
                            if title:
                                st.markdown(f"<h5><b>{title}</b></h5>", unsafe_allow_html=True)
                            if rating:
                                st.markdown(f"**Rating** - :star2: {round(rating, 1)}")
                            if genre_text:
                                st.markdown(f"<h6>Genre - {genre_text}</h6>", unsafe_allow_html=True)
                            if summary:
                                st.markdown(f"<h5><b>Summary-</b></h5> {summary}", unsafe_allow_html=True)

                            if cast:
                                st.subheader("Cast:")
                                col1, col2, col3, col4, col5 = st.columns(5)

                                cast1 = cast[0]
                                cast2 = cast[1]
                                cast3 = cast[2]
                                cast4 = cast[3]
                                cast5 = cast[4]
                                
                                with col1:
                                    st.markdown(f'<img src="{cast1["profile_url"]}" style="width: 70px; border-radius: 20%;">', unsafe_allow_html=True)
                                    st.markdown(f"<b>{cast1['name']}</b> <br> {cast1['character'].split('/')[0]}", unsafe_allow_html=True)

                                with col2:
                                    st.markdown(f'<img src="{cast2["profile_url"]}" style="width: 70px; border-radius: 20%;">', unsafe_allow_html=True)
                                    st.markdown(f"<b>{cast2['name']}</b> <br> {cast2['character'].split('/')[0]}", unsafe_allow_html=True)

                                with col3:
                                    st.markdown(f'<img src="{cast3["profile_url"]}" style="width: 70px; border-radius: 20%;">', unsafe_allow_html=True)
                                    st.markdown(f"<b>{cast3['name']}</b> <br> {cast3['character'].split('/')[0]}", unsafe_allow_html=True)

                                with col4:
                                    st.markdown(f'<img src="{cast4["profile_url"]}" style="width: 70px; border-radius: 20%;">', unsafe_allow_html=True)
                                    st.markdown(f"<b>{cast4['name']}</b> <br> {cast4['character'].split('/')[0]}", unsafe_allow_html=True)

                                with col5:
                                    st.markdown(f'<img src="{cast5["profile_url"]}" style="width: 70px; border-radius: 20%;">', unsafe_allow_html=True)
                                    st.markdown(f"<b>{cast5['name']}</b> <br> {cast5['character'].split('/')[0]}", unsafe_allow_html=True)
     

                        with tab2:
                            st.subheader(f"Trailer - {title}")
                            st_player(youtube_trailer_url)
                            # Display director information
                            # if director:
                            #     st.markdown(f"<h5><b>Director-</b></h5>", unsafe_allow_html=True)
                            #     if director[1]:
                            #         st.markdown(f'<img src="{director[1]}" style="width: 70px; border-radius: 20%;">', unsafe_allow_html=True)
                            #     if director[0]:
                            #         st.markdown(f"<b>{director[0]}</b>", unsafe_allow_html=True)
                else:
                    st.warning("Movie details not available.")
            except Exception as e:
                st.warning(f"An error occurred: {str(e)}")

       
    else:
        st.warning("No recommendations available.")
