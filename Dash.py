import streamlit as st
import pandas as pd
import requests
from io import StringIO
import streamlit as st

def load_original_data():
    url = 'https://raw.githubusercontent.com/Agnieszka-Kamieniksba23169/Test_Uber_App/refs/heads/main/top_movies.csv'
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("Failed to load data from GitHub.")
        return None

def load_original_data():
    url = 'https://raw.githubusercontent.com/Agnieszka-Kamieniksba23169/Test_Uber_App/refs/heads/main/user_frequency.csv'
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("Failed to load data from GitHub.")
        return None


def load_original_data():
    url = 'https://raw.githubusercontent.com/Agnieszka-Kamieniksba23169/Test_Uber_App/refs/heads/main/processed_ratings.csv'
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("Failed to load data from GitHub.")
        return None



# Page Config
st.set_page_config(page_title="Youth Movie Rating Dashboard", layout="wide")

st.title("Movie Ratings Dashboard for Young Adults (18–35)")
st.markdown("Interactive dashboard to explore user behavior and ML potential from movie ratings.")

# Summary Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Ratings", f"{len(rating):,}")
col2.metric("Unique Users", f"{rating['userId'].nunique():,}")
col3.metric("Movies Rated", f"{rating['movieId'].nunique():,}")

st.markdown("---")

# Top Movies by Rating Count
st.subheader("Top 10 Most Rated Movies")
fig_top_movies = px.bar(top_movies, x='movieId', y='count',
                        hover_data=['mean'], labels={'count': 'num_ratings'},
                        color='mean', title="Top Rated Movies by Number of Ratings")
st.plotly_chart(fig_top_movies, use_container_width=True)

# Rating Activity Over Time
st.subheader("Rating Activity Over Time")
activity = ratings.groupby('hour')['rating'].count().reset_index()
fig_activity = px.line(activity, x='hour', y='rating', markers=True,
                       title="Ratings by Hour of Day", labels={'rating': 'Number of Ratings'})
st.plotly_chart(fig_activity, use_container_width=True)

# User Rating Frequency
st.subheader("User Rating Frequency")
fig_users = px.histogram(user_freq, x='num_ratings', nbins=50, title="User Rating Distribution",
                         labels={'num_ratings': 'Ratings per User'})
st.plotly_chart(fig_users, use_container_width=True)

# Heatmap of Ratings (Machine Learning Suitability)
st.subheader("Ratings Heatmap (ML Suitability)")

# Sample data for heatmap
sample = ratings.sample(1000, random_state=42)
pivot = sample.pivot_table(index='userId', columns='movieId', values='rating')
fig_heatmap = px.imshow(pivot, color_continuous_scale='Viridis',
                        labels=dict(color="Rating"),
                        title="User-Movie Interaction Matrix (Sampled)")
st.plotly_chart(fig_heatmap, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("👩‍💻 Designed for young adults (18–35) with interactive exploration, minimal clutter, and machine learning relevance.")
