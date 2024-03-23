import streamlit as st
import requests

def search_videos(api_key, query):
    # Search for videos related to the given query
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&q={query}&part=snippet,id&order=viewCount&maxResults=10&type=video"
    response = requests.get(url)
    data = response.json()
    
    # Check if 'items' key exists in the response
    if 'items' not in data:
        st.error("Error: No items found in the response.")
        return []
    
    # Extract relevant video information
    videos = []
    for item in data['items']:
        video_title = item['snippet']['title']
        video_description = item['snippet']['description']
        
        # Check if the video is related to coding
        if is_coding_related(video_title, video_description):
            videos.append({'title': video_title, 'description': video_description})
    
    return videos

def is_coding_related(title, description):
    # Check if the title or description contains keywords related to coding
    coding_keywords = ['coding', 'programming', 'software development', 'computer science', 'coding tutorial']
    for keyword in coding_keywords:
        if keyword.lower() in title.lower() or keyword.lower() in description.lower():
            return True
    return False

def display_videos(videos):
    # Display videos
    if not videos:
        st.write("No coding-related videos found.")
        return
    
    st.write("Top Viral Coding Videos:")
    for index, video in enumerate(videos, start=1):
        st.write(f"{index}. Title: {video['title']}")
        st.write(f"   Description: {video['description']}")
        st.write("---")

# Default query for coding-related content
default_query = "coding"
api_key = "AIzaSyBCDioV4Ehnd6Inmc8uH2jW3X_5qbAlYMQ" # Replace with your actual API key

videos = search_videos(api_key, default_query)

# Display trending coding-related videos sorted by view count
display_videos(videos)
