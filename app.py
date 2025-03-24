import streamlit as st
from PIL import Image
import requests
import pandas as pd

# API endpoint
url = "https://wasteclassification-559456352882.europe-west1.run.app/predict"

# Inline CSS styling
st.markdown(
    """
    <style>
    .main > div {
        max-width: 800px;
        margin: 0 auto;
    }
    .big-header {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .sub-header {
        font-size: 1rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .bin-color-row {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
    }
    .bin-color-label {
        font-size: 1.1rem;
        margin-right: 0.5rem;
    }
    .bin-color-box {
        width: 40px;
        height: 20px;
        border-radius: 4px;
        border: 1px solid #ccc;
        margin-left: 0.5rem;
    }
    .progress-container {
        width: 100%;
        border: 1px solid #ccc;
        border-radius: 5px;
        margin-bottom: 10px;
        background-color: transparent;
    }
    .progress-bar {
        height: 20px;
        border-radius: 5px;
    }
    .progress-label {
        margin-bottom: 5px;
        font-weight: bold;
    }
    div.stButton > button {
        width: 100% !important;
    }
    div.stButton > button:hover,
    div.stButton > button:active {
        background-color: green !important;
        color: white !important;
        border: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header section
st.markdown('<h1 class="big-header">Classify Your Waste in Seconds</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Not sure which bin to use? Upload an image, and we’ll help!</p>', unsafe_allow_html=True)

# File uploader prompt (CENTERED)
st.markdown('<h3 style="text-align: center;">Upload a picture of your waste, and we’ll tell you where it belongs.</h3>', unsafe_allow_html=True)

# File uploader
img_file_buffer = st.file_uploader(
    "Drag & drop an image here or browse your files.",
    type=["jpg", "jpeg", "png"],
    help="Upload an image of your waste to classify"
)

# Function to display progress bars
def display_custom_progress_bar(category, percentage, color):
    progress_html = f"""
    <div class="progress-label">{category.capitalize()}: {percentage:.0f}%</div>
    <div class="progress-container">
        <div class="progress-bar" style="width: {percentage}%; background-color: {color};"></div>
    </div>
    """
    st.markdown(progress_html, unsafe_allow_html=True)

# Process image
if img_file_buffer is not None:
    st.markdown("---")
    col_left, col_right = st.columns([1, 1])

    with col_left:
        uploaded_img = Image.open(img_file_buffer)
        st.image(uploaded_img, caption="Your lovely piece of waste ☝️", use_container_width=True)

    with col_right:
        if st.button("Analyze Waste"):
            with st.spinner("Scanning your waste... Hang tight!"):
                img_bytes = img_file_buffer.getvalue()
                files = {"img": img_bytes}
                response = requests.post(url, files=files)

                if response.status_code == 200:
                    prediction = response.json()
                    category_colors = {
                        "battery": "red",
                        "biological": "brown",
                        "cardboard": "blue",
                        "clothes": "red",
                        "shoes": "red",
                        "glass": "white",
                        "metal": "yellow",
                        "paper": "blue",
                        "plastic": "yellow",
                        "trash": "black",
                    }

                    # Sort predictions by probability
                    sorted_preds = sorted(prediction.items(), key=lambda x: x[1], reverse=True)

                    # Store valid progress bars
                    progress_bars = []
                    top_cat, top_prob = sorted_preds[0]
                    progress_bars.append((top_cat, top_prob, category_colors.get(top_cat, "red")))

                    for cat, prob in sorted_preds[1:]:
                        if prob >= 0.15:  # Include 15%
                            progress_bars.append((cat, prob, category_colors.get(cat, "red")))

                    # Suggested bin
                    bin_color = category_colors.get(top_cat, "red")
                    st.markdown(f"**This looks like:** {top_cat.capitalize()}")
                    st.markdown(
                        f"""
                        <div class="bin-color-row">
                            <span class="bin-color-label"><strong>Suggested Bin:</strong> {bin_color.capitalize()}</span>
                            <div class="bin-color-box" style="background-color: {bin_color};"></div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Confidence section
                    st.markdown("### How confident am I?")
                    if len(progress_bars) > 2:
                        st.info("Hmm... I’m not 100% sure, but here are my best guesses!")
                        progress_bars = progress_bars[:3]

                    # Display progress bars
                    for cat, prob, col in progress_bars:
                        display_custom_progress_bar(cat, prob * 100, col)

                    # --- MOVE TABLE TO NEW SECTION BELOW COLUMNS ---
                    st.markdown("---")  # New section separator
                    st.markdown("### Full Breakdown:")  # Move title below
                    df = pd.DataFrame({
                        "Category": [k.capitalize() for k in prediction.keys()],
                        "Probability": [f"{v * 100:.0f}%" for v in prediction.values()]
                    })
                    st.table(df)  # Table now appears outside the columns

                else:
                    st.error("Oops! Something went wrong. Please try again later.")
