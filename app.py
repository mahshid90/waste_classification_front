import streamlit as st
from PIL import Image
import requests
import pandas as pd

# API endpoint
# API endpoint
url = "https://waste-api-42960119981.europe-west1.run.app/predict"


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

# Initialize session state for uploaded image
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

# File uploader
img_file_buffer = st.file_uploader(
    "Drag & drop an image here or browse your files.",
    type=["jpg", "jpeg", "png"],
    help="Upload an image of your waste to classify"
)

# If a new image is uploaded, store it in session state
if img_file_buffer is not None:
    st.session_state.uploaded_image = img_file_buffer

# Function to display progress bars
def display_custom_progress_bar(category, percentage, color):
    progress_html = f"""
    <div class="progress-label">{category.capitalize()}: {percentage:.0f}%</div>
    <div class="progress-container">
        <div class="progress-bar" style="width: {percentage}%; background-color: {color};"></div>
    </div>
    """
    st.markdown(progress_html, unsafe_allow_html=True)

# Process the uploaded image
if st.session_state.uploaded_image:
    st.markdown("---")
    col_left, col_right = st.columns([1, 1])

    with col_left:
        uploaded_img = Image.open(st.session_state.uploaded_image)
        st.image(uploaded_img, caption="Your lovely piece of waste ☝️", use_container_width=True)

    with col_right:
        with st.spinner("Scanning your waste... Hang tight!"):
            img_bytes = st.session_state.uploaded_image.getvalue()
            files = {"img": img_bytes}
            response = requests.post(url, files=files)

            try:
                response_data = response.json()
                if not isinstance(response_data, dict) or not response_data:
                    raise ValueError("Unexpected API response format.")
            except (ValueError, requests.exceptions.JSONDecodeError) as e:
                st.error(f"Error processing response: {e}")
                st.stop()

            # Category color mapping
            category_colors = {
                "battery": "red",
                "biological": "brown",
                "cardboard": "blue",
                "clothes": "red",
                "shoes": "red",
                "glass": "#D3D3D3",
                "metal": "yellow",
                "paper": "blue",
                "plastic": "yellow",
                "trash": "black",
                "glass_brown": "brown",
                "glass_green": "green",
                "glass_transparent": "#D3D3D3",
            }
            default_color = "grey"

            # Category bin mapping
            category_bin = {
                "battery": "Battery disposal",
                "biological": "Bio bin",
                "cardboard": "Blue bin",
                "clothes": "Red cross donation",
                "shoes": "Red cross donatio",
                "glass": "Glass container",
                "metal": "Yellow bin",
                "paper": "Blue bin",
                "plastic": "Yellow bin",
                "trash": "Black bin",
                "glass_brown": "Brown glass container",
                "glass_green": "Green glass container",
                "glass_transparent": "White glass container",
            }
            default_bin = "trash"

            # Sort and filter predictions
            sorted_preds = [(cat, prob, category_colors.get(cat, default_color), category_bin.get(cat, default_bin))
                            for cat, prob in sorted(response_data.items(), key=lambda x: x[1], reverse=True) if prob >= 0.15]
            #sorted_preds = [(cat, float(prob), category_colors.get(cat, default_color), category_bin.get(cat, default_bin))
                            #for cat, prob in sorted(response_data.items(), key=lambda x: float(x[1]), reverse=True) if float(prob) >= 0.15]


            if not sorted_preds:
                st.error("No valid classification results found.")
                st.stop()

            # Suggested bin
            top_cat, top_prob, bin_color, bin_type = sorted_preds[0]

            st.markdown(f"**This looks like:** {top_cat.capitalize()}")
            st.markdown(f"""
            <div class="bin-color-row">
                <span><strong>Suggested Bin:</strong> {bin_type}</span>
                <div class="bin-color-box" style="background-color: {bin_color};"></div>
            </div>
            """, unsafe_allow_html=True)

            # Confidence section
            st.markdown("### How confident am I?")
            if len(sorted_preds) > 2:
                st.info("Hmm... I’m not 100% sure, but here are my best guesses!")
                sorted_preds = sorted_preds[:3]

            # Display progress bars
            for cat, prob, col, bin_type in sorted_preds:
                display_custom_progress_bar(cat, prob * 100, col)

            # Full breakdown table
            st.markdown("---")
            st.markdown("### Full Breakdown:")
            df = pd.DataFrame({
                "Category": [k.capitalize() for k in response_data.keys()],
                "Probability": [f"{v * 100:.0f}%" for v in response_data.values()]
            })
            st.table(df)

    # ✅ **Reset file uploader** to allow a new image to be uploaded
    st.session_state.uploaded_image = None
