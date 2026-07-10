# app/feed.py
import streamlit as st
import requests
from datetime import datetime

API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Feed", layout="wide")
st.title("📰 Post Feed")

# Fetch posts from FastAPI
@st.cache_data(ttl=60)  # cache for 60 seconds
def get_posts():
    try:
        response = requests.get(f"{API_BASE_URL}/feed")
        response.raise_for_status()
        data = response.json()
        return data.get("posts", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to load feed: {e}")
        return []

posts = get_posts()

if not posts:
    st.info("No posts yet. Be the first to create one!")
else:
    for post in posts:
        with st.container():
            # Use columns for layout
            col1, col2 = st.columns([1, 3])
            with col1:
                if post.get("url"):
                    st.image(post["url"], width="content")
                else:
                    st.write("📷 No image")
            with col2:
                st.subheader(post.get("subject", "Untitled"))
                st.write(post.get("description", ""))
                # Format created_at if present
                created_at = post.get("created_at")
                if created_at:
                    dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    st.caption(f"Posted: {dt.strftime('%Y-%m-%d %H:%M')}")
                # Show tags if stored
                if post.get("tags"):
                    tags = post["tags"].split(",") if isinstance(post["tags"], str) else post["tags"]
                    st.write("🏷️ " + ", ".join(tags))
                # Expandable content
                with st.expander("Read more"):
                    st.write(post.get("content", ""))
            st.divider()