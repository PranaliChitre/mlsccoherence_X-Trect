import streamlit as st
from googleapiclient.discovery import build

# Define function to get YouTube channel information
def get_channel_info():
    api_key = "AIzaSyCXP5L4iH389iGNm3e28ky0IkY08K7LWfs"
    channel_id = "UChVzP7gNOlkymoo000Y9_6Q"

    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id
    )
    response = request.execute()
    return response['items'][0]

# Streamlit app
def main():
    st.title("YouTube Channel Info")

    if st.button("Get Channel Info"):
        try:
            # Get channel information
            channel_info = get_channel_info()

            # Display channel information
            st.subheader("Channel Information")
            st.write(f"Title: {channel_info['snippet']['title']}")
            st.write(f"Description: {channel_info['snippet']['description']}")
            st.write(f"Published At: {channel_info['snippet']['publishedAt']}")
            st.write(f"Country: {channel_info['snippet']['country']}")
            st.write(f"View Count: {channel_info['statistics']['viewCount']}")
            st.write(f"Subscriber Count: {channel_info['statistics']['subscriberCount']}")
            st.write(f"Video Count: {channel_info['statistics']['videoCount']}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
