import streamlit as st
from PIL import Image
import requests
import pandas as pd
import imghdr

# API endpoint
url = "https://wasteclassification-559456352882.europe-west1.run.app/predict"

default_color = "#808080"  # Gray for unknown categories
category_colors = {
    "battery": "red", "biological": "brown", "cardboard": "blue", "clothes": "red",
    "shoes": "red", "glass": "white", "metal": "yellow", "paper": "blue",
    "plastic": "yellow", "trash": "black"
}

# Inline CSS styling
st.markdown(
    """
    <style>
    .main > div { max-width: 800px; margin: 0 auto; }
    .big-header { font-size: 2rem; font-weight: 700; text-align: center; }
    .sub-header { font-size: 1rem; color: #6c757d; text-align: center; margin-bottom: 1.5rem; }
    .bin-color-row { display: flex; align-items: center; margin: 0.5rem 0; }
    .bin-color-box { width: 40px; height: 20px; border-radius: 4px; border: 1px solid #ccc; margin-left: 0.5rem; }
    .progress-container { width: 100%; border: 1px solid #ccc; border-radius: 5px; }
    .progress-bar { height: 20px; border-radius: 5px; }
    div.stButton > button { width: 100% !important; }
    div.stButton > button:hover, div.stButton > button:active { background-color: green !important; color: white !important; border: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="big-header">Classify Your Waste in Seconds</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Not sure which bin to use? Upload an image, and we’ll help!</p>', unsafe_allow_html=True)

# File uploader
img_file_buffer = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

# Ensure file is fully uploaded
if img_file_buffer is not None:
    file_type = imghdr.what(None, h=img_file_buffer.getvalue())
    if file_type not in ["jpeg", "png"]:
        st.error("Invalid file format. Please upload a JPG or PNG image.")
        st.stop()
    if img_file_buffer.size == 0:
        st.warning("The file is not fully uploaded. Try again.")
        st.stop()

    st.write("✅ Image uploaded successfully!")  # Debugging message


# Function to display progress bars
def display_custom_progress_bar(category, percentage, color):
    st.markdown(f"""
    <div class="progress-label">{category.capitalize()}: {percentage:.0f}%</div>
    <div class="progress-container">
        <div class="progress-bar" style="width: {percentage}%; background-color: {color};"></div>
    </div>
    """, unsafe_allow_html=True)

if img_file_buffer is not None:
    st.markdown("---")
    col_left, col_right = st.columns([1, 1])

    with col_left:
        uploaded_img = Image.open(img_file_buffer)
        st.image(uploaded_img, caption="Your lovely piece of waste ☝️", use_container_width=True)

    with col_right:
        with st.spinner("Scanning your waste... Hang tight!"):
            img_bytes = img_file_buffer.getvalue()
            files = {"img": img_bytes}
            response = requests.post(url, files=files)

            try:
                response_data = response.json()
                if not isinstance(response_data, dict) or not response_data:
                    raise ValueError("Unexpected API response format.")
            except (ValueError, requests.exceptions.JSONDecodeError) as e:
                st.error(f"Error processing response: {e}")
                st.stop()

            # Sort and filter predictions
            sorted_preds = [(cat, prob, category_colors.get(cat, default_color))
                            for cat, prob in sorted(response_data.items(), key=lambda x: x[1], reverse=True) if prob >= 0.15]

            if not sorted_preds:
                st.error("No valid classification results found.")
                st.stop()

            top_cat, top_prob, bin_color = sorted_preds[0]
            st.markdown(f"**This looks like:** {top_cat.capitalize()}")
            st.markdown(f"""
            <div class="bin-color-row">
                <span><strong>Suggested Bin:</strong> {bin_color.capitalize()}</span>
                <div class="bin-color-box" style="background-color: {bin_color};"></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### How confident am I?")
            if len(sorted_preds) > 2:
                st.info("Hmm... I’m not 100% sure, but here are my best guesses!")
                sorted_preds = sorted_preds[:3]

            for cat, prob, col in sorted_preds:
                display_custom_progress_bar(cat, prob * 100, col)

            # Full breakdown table
            st.markdown("---")
            st.markdown("### Full Breakdown:")
            df = pd.DataFrame({
                "Category": [k.capitalize() for k in response_data.keys()],
                "Probability": [f"{v * 100:.0f}%" for v in response_data.values()]
            })
            st.table(df)
