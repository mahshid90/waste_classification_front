import streamlit as st
from PIL import Image
import requests
import os


# Set page tab display
st.set_page_config(
   page_title="Waste classification",
   page_icon= '🗑️',
   layout="wide",
   initial_sidebar_state="expanded",
)

# Example local Docker container URL
# url = 'http://api:8000'
# Example localhost development URL
# url = 'http://localhost:8000'

url ='https://wasteclassification-559456352882.europe-west1.run.app/predict'


# App title and description
st.header('Time to classify your trash! 📸')
st.markdown(''' Some nice text will be added here in the future
            ''')

st.markdown("---")

### Create a native Streamlit file upload input
st.markdown("### Give me some trash!👇")
img_file_buffer = st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png'])

if img_file_buffer is not None:

  col1, col2 = st.columns(2)

  with col1:
    ### Display the image user uploaded
    st.image(Image.open(img_file_buffer), caption="Your lovely peace of watse ☝️")

  with col2:
    with st.spinner("Wait for it..."):
      ### Get bytes from the file buffer
      img_bytes = img_file_buffer.getvalue()
      files = {'img': img_bytes}
      response = requests.post(url, files=files)

      ### Make request to  API (stream=True to stream response as bytes)

    if response.status_code == 200:
        ### Display the image returned by the API
        prediction = response.json()
        st.markdown(f"**Prediction:** {prediction}")
        st.markdown(f"**Prediction:** {prediction}")

    else:
        st.markdown(response.text)
        ### Display the image returned by the API
        #st.image(res.content, caption="Image returned from API ☝️")
        st.markdown(response.status_code)

    #   else:
    #     st.markdown("**Oops**, something went wrong 😓 Please try again.")
    #     print(res.status_code, res.content)
