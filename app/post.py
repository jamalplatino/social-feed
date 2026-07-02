import streamlit as st
import requests


# --- Configuration ---
# Change this to your FastAPI server address
API_BASE_URL = "http://localhost:8000"

# Page setup
st.set_page_config(page_title="New Post", layout="centered")
st.title("✍️ Create a New Post")

# --- Form ---
with st.form(key="post_form"):
    subject = st.text_input("Subject", max_chars=100, placeholder="Enter the post subject")
    description = st.text_area("Description", height=100, placeholder="Brief description of the post")
    tags_input = st.text_input("Tags", placeholder="e.g. python, data, tutorial")
    uploaded_image = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg", "gif", "bmp"],
        help="Supported formats: PNG, JPG, JPEG, GIF, BMP"
    )
    content = st.text_area("Content", height=300, placeholder="Write the full post content here...")
    
    submitted = st.form_submit_button("Submit Post")

# --- Submission Handling ---
if submitted:
    # Validate required fields
    if not subject.strip():
        st.error("Subject is required.")
    elif not content.strip():
        st.error("Content is required.")
    else:
        # Parse tags
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        
        # 1. Upload image to FastAPI (which forwards to ImageKit.io)
        image_url = None
        if uploaded_image is not None:
            with st.spinner("Uploading image..."):
                try:
                    files = {"file": (uploaded_image.name, uploaded_image.getvalue(), uploaded_image.type)}
                    response = requests.post(f"{API_BASE_URL}/upload-image/", files=files)
                    response.raise_for_status()
                    image_data = response.json()
                    image_url = image_data.get("url")
                    st.success("Image uploaded successfully!")
                except requests.exceptions.RequestException as e:
                    st.error(f"Image upload failed: {e}")
                    st.stop()  # Stop execution if image upload fails

        # 2. Prepare final post payload
        payload = {
            "subject": subject.strip(),
            "description": description.strip() if description else None,
            "tags": tags,
            "image_url": image_url,  # None if no image was uploaded
            "content": content.strip()
        }

        # 3. Submit the full post to FastAPI
        with st.spinner("Submitting post..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/create-post/",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                st.success("✅ Post created successfully!")

                # Show preview
                st.subheader("📋 Post Preview")
                st.write(f"**Subject:** {subject}")
                st.write(f"**Description:** {description}")
                st.write(f"**Tags:** {', '.join(tags) if tags else 'None'}")
                if image_url:
                    st.image(image_url, caption="Uploaded Image (via ImageKit)", use_container_width=True)
                else:
                    st.write("No image uploaded.")
                st.write("**Content:**")
                st.write(content)

            except requests.exceptions.RequestException as e:
                st.error(f"Post submission failed: {e}")