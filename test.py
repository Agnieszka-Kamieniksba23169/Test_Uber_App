source /home/adminuser/venv/bin/activate
pip install seaborn matplotlib streamlit
streamlit run /mount/src/test_uber_app/test.py

import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns




# Set visual style
sns.set(style="whitegrid")

# Load the dataset 
movie_df = pd.read_csv("movie_df.csv")

# Filter data for age group 18-35 based on assumptions (e.g., all users are in this group or user data not available)
st.title("🎬 Movie Insight Dashboard for Young Adults (18-35)")
st.markdown("Explore movie ratings and patterns through engaging visuals")

# Sidebar filters
genre_filter = st.sidebar.multiselect("Filter by Genre", options=movie_df['genres'].unique())
year_range = st.sidebar.slider("Select Year Range", int(movie_df['year'].min()), int(movie_df['year'].max()), (2000, 2020))
rating_threshold = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.0)

# Apply filters
filtered_df = movie_df.copy()
if genre_filter:
    filtered_df = filtered_df[filtered_df['genres'].isin(genre_filter)]

filtered_df = filtered_df[(filtered_df['year'] >= year_range[0]) & (filtered_df['year'] <= year_range[1])]
filtered_df = filtered_df[filtered_df['rating'] >= rating_threshold]

# Display data summary
st.subheader("Filtered Data Overview")
st.dataframe(filtered_df.head())

# Most Popular Movies
st.subheader("🎞️ Top Rated Movies")
top_movies = (filtered_df.groupby(['movieId', 'title'])
              .agg(avg_rating=('rating', 'mean'), rating_count=('rating', 'count'))
              .sort_values(by=['avg_rating', 'rating_count'], ascending=[False, False])
              .head(10)
              .reset_index())
st.table(top_movies)

# Rating distribution
st.subheader("⭐ Rating Distribution")
fig1, ax1 = plt.subplots()
sns.histplot(filtered_df['rating'], bins=20, kde=False, ax=ax1)
ax1.set_title("Distribution of Ratings")
ax1.set_xlabel("Rating")
ax1.set_ylabel("Count")
st.pyplot(fig1)

# Ratings over time
st.subheader("📅 Ratings Over Time")
filtered_df['datetime'] = pd.to_datetime(dict(year=filtered_df.year, month=filtered_df.month, day=filtered_df.day))
rating_over_time = (filtered_df.groupby('datetime')['rating'].mean().reset_index())
fig2, ax2 = plt.subplots()
sns.lineplot(data=rating_over_time, x='datetime', y='rating', ax=ax2)
ax2.set_title("Average Rating Over Time")
ax2.set_xlabel("Date")
ax2.set_ylabel("Average Rating")
st.pyplot(fig2)

# Genre popularity
st.subheader("🎭 Genre Popularity")
genre_counts = filtered_df['genres'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']
fig3, ax3 = plt.subplots()
sns.barplot(data=genre_counts, x='genre', y='count', ax=ax3)
ax3.set_title("Most Watched Genres")
ax3.set_xlabel("Genre")
ax3.set_ylabel("View Count")
ax3.tick_params(axis='x', rotation=45)
st.pyplot(fig3)

st.markdown("---")
st.caption("Dashboard for Movie Analysis | Targeting Viewers aged 18-35")