import tmdbsimple as tmdb

tmdb.API_KEY = 'b4f4e5073f49c9bba30dd68659314a41'

def movie_meta_data(movie_id):
    try:
        movie = tmdb.Movies(movie_id)
        response = movie.info()

        # Construct the complete poster URL
        base_url = 'https://image.tmdb.org/t/p/w500'
        poster_path = response['poster_path']
        movie_poster = f"{base_url}{poster_path}"

        title = response['title']
        summary = response['overview']

        genres = response['genres']
        genre_names = [genre['name'] for genre in genres]  # Extract genre names
        genre_text = ", ".join(genre_names)

        # Fetching movie rating
        rating = response['vote_average']

        # Fetching YouTube trailer
        trailers = movie.videos()  # Get available videos
        youtube_trailer_url = None
        for trailer in trailers['results']:
            if trailer.get('type') == 'Trailer':
                youtube_trailer_key = trailer['key']
                youtube_trailer_url = f"https://www.youtube.com/watch?v={youtube_trailer_key}"
                break

        return [title, summary, movie_poster, youtube_trailer_url, genre_text, rating]
    except Exception as e:
        print(f"Error fetching movie metadata: {e}")
        return None


def director_meta_data(movie_id):
    try:
        tmdb.API_KEY = 'b4f4e5073f49c9bba30dd68659314a41'
        movie = tmdb.Movies(movie_id)

        # Get movie credits
        credits = movie.credits()

        # Extract director name and their TMDb ID
        director_name = credits['crew'][0]['name']
        director_id = credits['crew'][0]['id']

        # Get director details (including profile image path)
        director_details = tmdb.People(director_id).info()  # Use People instead of Persons
        director_profile_path = director_details['profile_path']

        # Construct director's image URL
        director_url = f"https://image.tmdb.org/t/p/w500{director_profile_path}"

        return [director_name, director_url]
    except Exception as e:
        print(f"Error fetching director metadata: {e}")
        return None


def cast_meta_data(movie_id):
    try:
        tmdb.API_KEY = 'b4f4e5073f49c9bba30dd68659314a41'  # Replace with your actual API key

        movie = tmdb.Movies(movie_id)

        # Get movie credits
        credits = movie.credits()

        # Get top 5 cast members with images
        cast = credits['cast'][:5]  # Get the first 5 cast members
        top_cast = []
        for person in cast:
            profile_path = person['profile_path']  # Get profile image path
            profile_url = f"https://image.tmdb.org/t/p/w500{profile_path}"  # Construct full URL
            top_cast.append({
                'name': person['name'],
                'character': person['character'],
                'profile_url': profile_url
            })
        return top_cast
    except Exception as e:
        print(f"Error fetching cast metadata: {e}")
        return None
