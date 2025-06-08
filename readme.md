# MindBlown Chatbot

## Project Description
MindBlown Chatbot is an intelligent conversational AI designed to provide interactive and helpful responses. It utilizes a fine-tuned local language model to run efficiently either locally or through Hugging Face Spaces using Docker.

## Features
- Uses a local Qwen model fine-tuned with LoRA (`qwen-psychika-lora`).
- Lightweight and efficient for both development and deployment.
- Flexible to run either on a local machine or hosted on Hugging Face Spaces.

---

## Running Locally

Follow the steps below to run the chatbot on your local machine:

### 1. Clone the Repository
```
git https://github.com/MindBlownDBS/Chatbot-Model.git
cd Chatbot-Model
```

### 2. Install Requirements (Recommended Using Python 3.11)
```
pip install -r requirements.txt
```

### 3. Downlaod Model Locally
```
python download_model.py
```

### 4. Setup .env
```
MONGO_URI
```

### 5. Uncommect All Code in Local Section in app.py
```
# This code is a Flask application that serves as a chatbot API using a local pre-trained language model.

....
```

### 6. Build and Run Docker
```
docker build -t mindblown-chatbot .
docker run -p 7860:7860 mindblown-chatbot
```

## Deploy in Hugging Face Spaces

Follow the steps below to deploy your model in Hugging Face Spaces:

### 1. Clone the Repository
```
git https://github.com/MindBlownDBS/Chatbot-Model.git
cd Chatbot-Model
```

### 2. Uncommect All Code in Remote Section in app.py
```
# This code is a Flask application that serves as a chatbot API using a remote pre-trained language model.

....
```

### 3. Create a Space on Hugging Face
- Visit Hugging Face Spaces
- Create a new Space and choose Docker as the runtime
- Upload all files from this repository

### 4. Set Environment Variables
- Go to the Secrets tab in the Space settings
- Add required environment variables (MONGO_URI & HUGGINGFACE_TOKEN)

### 5. Build and Deploy
Once everything is uploaded and secrets are configured, Hugging Face will automatically build and run your container.
