import streamlit as st
from PIL import Image
import requests

# API endpoint
url = "https://wasteclassification-559456352882.europe-west1.run.app/predict"

st.header("Time to classify your trash!! 📸")
st.markdown("Some nice text will be added here in the future")
st.markdown("---")

st.markdown("### Give me some trash!👇")
img_file_buffer = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

st.markdown("---")


if img_file_buffer is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.image(Image.open(img_file_buffer), caption="Your lovely piece of waste ☝️")

    with col2:
        # Button to trigger the prediction
        if st.button("Classify Trash"):
            with st.spinner("Wait for it..."):
                # 1. Read the image bytes
                img_bytes = img_file_buffer.getvalue()
                files = {"img": img_bytes}

                # 2. Send image to API
                response = requests.post(url, files=files)

                if response.status_code == 200:
                    # 3. Parse prediction response
                    prediction = response.json()
                    max_key = max(prediction, key=prediction.get)

                    # 4. Define color mapping
                    category_colors = {
                        "cardboard": "blue",
                        "glass": "white",
                        "metal": "yellow",
                        "paper": "blue",
                        "plastic": "yellow",
                        "trash": "black",
                    }
                    bin_color = category_colors.get(max_key, "red")

                    # 5. Display top prediction and bin color
                    st.markdown(
                        f"""
                        <div style="display: flex; align-items: center;">
                            <span style="font-size: 22px;">🏷️ Type of Waste:</span>
                            <span style="margin-left: 10px; font-size: 22px;"><strong>{max_key.capitalize()}</strong></span>
                        </div>
                        <div style="display: flex; align-items: center; margin-top: 10px;">
                            <span style="font-size: 22px;"">🗑️ Bin color:</span>
                            <div style="width: 60px; height: 25px; background-color: {bin_color}; margin-left: 10px; border-radius: 5px; border: 1px solid grey;"></div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # 6. Format and display the full prediction table
                    formatted_predictions = "\n".join([f"| {key.capitalize()} | {value * 100:.0f}% |" for key, value in prediction.items()])

                    table_header = "| Category | Probability |\n| --- | --- |"
                    st.markdown("#### Predictions:")
                    st.markdown(f"{table_header}\n{formatted_predictions}")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
