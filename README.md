
## 📱 Try the App

Scan the QR code below to download or open the app:

![QR Code](./waste_classification_App.png)

https://wasteclassificationfront.streamlit.app/


—-------------------------------------------------------------------------------------------------------------------------

# ⚡ Waste Classification API – FastAPI

Build your API- helpful links:

- *https://courageous-jitterbug-be8.notion.site/Projects-Tips-4846cbe1aec44df1b1335ab73f683547*

- *https://github.com/lewagon/data-templates/blob/main/project-boilerplates/sending-images-streamlit-fastapi/backend/fast_api/api.py*

- *https://github.com/julesvanrie/base_project_front/blob/main/.gitignore*

### **API Backend Overview**

This backend service uses **FastAPI** to expose a set of HTTP endpoints for real-time waste classification. It supports both the **primary waste classifier** (10 general categories) and the **glass subclassifier** (brown, green, transparent) in a **two-stage inference pipeline**.

The API is designed for integration with a frontend or automated system and supports image uploads, preprocessing, prediction, and JSON-formatted responses.

### **📌 Overview**

- **Framework**: FastAPI used to create the API.

- **Server**: Running the API with FastAPI and a** Uvicorn Server**

1. **requirements.txt** (we need it in all steps of building our API)   # all the dependencies you need to run the package

1. Pip install -e .

—-------------------------------------------------------------------------------------------------------------------------

**FastAPI skeleton in the fast.py :**

- This FastAPI application provides an image classification API for waste classification, including a specialized model for classifying glass types. In fast.py:

**Root endpoint(app.get): **Returns a simple JSON response confirming that the API is running.

**/predict**** Endpoint (General Waste Classification):**

**/glass**** Endpoint (Glass Classification):**

✅ **What This API Does:**

Accepts an **image file** as input.

**Processes the image** (resizing, formatting for the model). \
**Classifies waste** into 10 categories. \
If the waste is **glass**, it further classifies it as **brown, green, or transparent**. \
Returns **classification probabilities**.

—-------------------------------------------------------------------------------------------------------------------------

🚀 **Use Cases: **Waste classification for **recycling programs**. Integration with **mobile apps or smart bins**.

├── Dockerfile          *# 🆕 Building instructions*

├── Makefile

├── README.md

├── requirements.txt    *# All the dependencies you need to run the package*

├── setup.py            *# Package installer*

├── waste_classification

│   ├── api

│   │   ├── __init__.py

│   │   └── fast.py     *# ✅ Where the API lays*

│   ├── interface

│   ├── __init__.py

│   ├── main.py


### **Running the API with Uvicorn**

To run the FastAPI application locally, use the following command:

uvicorn waste_classification.api.fast:app --reload

Once the server is running, you can access the app at:

- **API Root**:[ ](http://127.0.0.1:8000/)[URL \
](http://127.0.0.1:8000/)

- **API Documentation**:[ ](http://127.0.0.1:8000/docs)[URL/docs \
](http://127.0.0.1:8000/docs)

**Interacting with the API**

You can see the available API endpoints (e.g., GET and POST methods) in the documentation at /docs. This provides an easy way to test and interact with the API directly from the browser.

**🐳****Docker**

In docker we do pip install requirements.txt.

### **.env file**

—-------------------------------------------------------------------------------------------------------------------------

API on Artifact Registry
GAR_IMAGE=waste_classification   **Choose a Docker image name and add it to your ****.env****. **

GAR_REPO=**waste-repo we name it**

GCP_PROJECT= **<project_id>   we need to change it to our project_ID in GCP**

GCP_REGION=europe-west1

GAR_MEMORY=2Gi

—-------------------------------------------------------------------------------------------------------------------------

### **Making the API Available to the World 🌍**

To deploy the API, we first need to containerize it using Docker. Here’s the step-by-step process:

 1️⃣ **Create a Docker Image** – Build an image that includes all dependencies required to run the API. \
 2️⃣ **Write a Dockerfile** – Define the instructions for building the API inside a container. \
 3️⃣ **Build the Docker Image** – Use the Dockerfile to generate an image. \
 4️⃣ **Run the API Locally** – Start a container from the image and test if everything works correctly.

This ensures the API runs consistently across different environments before making it publicly available.

- You need the Docker daemon running on your machine to build and run the image, but **no** additional actions are needed within Docker itself.

- We've created the API locally; now we encapsulate it in Docker, run it locally, and once it works, we deploy it on Google Cloud.

For docker we first make a** docker file**:

**In docker file (building instruction):**

—-------------------------------------------------------------------------------------------------------------------------

- **python:3.10.6-buster** is a Python 3.10.6 image based on Debian Buster. \
This ensures the container has Python pre-installed, making it easier to run the FastAPI application.

- **WORKDIR /prod** sets the working directory inside the container to /prod. \
Any subsequent commands (like COPY or RUN) will be executed in this directory.

**Copies the necessary files from the host machine to the container:**

- **waste_classification** → The application’s source code. \
**requirements.txt** → List of dependencies to install.

- **models** → Pre-trained machine learning models for waste classification.

**Upgrades ****pip** to the latest version before installing dependencies.

**Installs additional system dependencies** required for image processing:

- **Runs the FastAPI application using Uvicorn**:

- **waste_classification.api.fast:app** → Refers to the FastAPI app (app) inside waste_classification/api/fast.py.

 \
—-------------------------------------------------------------------------------------------------------------------------

# 📌 Local Development Commands

### **Makefile:**** Explanation of the Makefile Commands**

This Makefile defines a set of commands to facilitate the building, running, and deploying of a Dockerized FastAPI application. It supports both local execution (for development) and deployment to Google Cloud Platform (GCP).

**Run a Single Command in the Makefile: make <****command-name****>**

Then in make file run section by section (for each section(number) we can look into Makefile and find the corresponding command line) :

1️⃣ Build a Local Docker Image

2️⃣ Run the Local Docker Container

3️⃣ Run the Container Interactively (with Bash) **(for debug)**

# 📌 Cloud Deployment (Google Cloud Platform - GCP)

4️⃣ Configure Google Artifact Registry (GAR)

5️⃣ Build Docker Image for Cloud (Linux/AMD64)

6️⃣ Push the Image to Google Artifact Registry

7️⃣ Run the Cloud Image Locally

8️⃣ Run Container in Interactive Mode (Cloud Image)

9️⃣ Deploy to Google Cloud Run

After that: Copy the service URL, and check in your browser that it works.

And we go to [https://console.cloud.google.com/](https://console.cloud.google.com/) and check **cloud run**, Should be run there.

—---

**setup.py **:

This Python script is used to package the waste_classification project(**folder**) for distribution. By packaging the project, it can be installed like any other Python package using:

**Pip install .**

This makes it easier to set up on different machines or environments.

If the project needs to be deployed to cloud platforms (e.g., Google Cloud, AWS), a packaged version simplifies deployment.

For example in fast.py we have :

from **waste_classification.interface.main** import **load_model, load_glass_model**

**We can import ****waste_classification**** because setup.py defines it as a package. This means:**

**✅ The ****waste_classification**** folder is now recognized as a Python package.**

**✅ ****interface.main**** becomes a module within the package.**

- It **defines** how the waste_classification package should be installed.

- It **automatically detects** and includes all Python packages in the project.

- It **installs required dependencies** from requirements.txt.

#

## **API-Frontend**

**Create a separate repo** for the user interface

- Develop a user interface with Streamlit

- Plug a user interface to your FastAPI

- Deploy your front end on Streamlit Cloud

├── app.py

├── Makefile

├── media

├── pages

├── README.md

└── requirements.txt

## **app.py: **This Streamlit app provides a user-friendly waste classification interface. Users can upload an image of waste, which is then sent to an API for classification. The app displays predictions with confidence levels and suggests the correct bin for disposal.

In app.py we have to **include the URL** we made in **the backend**. The **FastAPI endpoint** that processes the image and returns waste classification results.

To design our front end: [https://streamlit.lewagon.ai/#Images,%20Audio,%20Video](https://streamlit.lewagon.ai/#Images,%20Audio,%20Video)

## **Requirements.txt: **This file is needed for Streamlit to handle the package dependencies of your application.

streamlit run app.py: We used it to test the front end locally. When you run the command, you can see the changes you make in the code, directly in the local frontend.

## **Deploying the App on Streamlit Cloud**

App URL xxx.streamlit.app

1️⃣ Go to [https://share.streamlit.io/](https://share.streamlit.io/)

2️⃣ Click **"Create app"**

3️⃣ **Deploy a public app from GitHub**

- **Repository**: mahshid90/waste_classification_front

- **Branch**: master

- **Main file path**: app.py

4️⃣ **App URL**: xxx.streamlit.app

✅ Once deployed, your app will be live and accessible! 🚀
