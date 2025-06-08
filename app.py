# This code is a Flask application that serves as a chatbot API using a remote pre-trained language model.

# import os

# # --- Setup environment variable for cache BEFORE imports ---
# os.environ["HF_HOME"] = "/tmp/.cache/huggingface"
# os.makedirs(os.environ["HF_HOME"], exist_ok=True)

# from datetime import datetime
# from flask import Flask, request, jsonify
# from pymongo import MongoClient
# from dotenv import load_dotenv

# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM
# from peft import PeftModel

# load_dotenv()

# token = os.getenv("HUGGINGFACE_TOKEN")
# mongo_uri = os.getenv("MONGO_URI")

# if not token:
#     raise ValueError("HUGGINGFACE_TOKEN env variable missing")
# if not mongo_uri:
#     raise ValueError("MONGO_URI env variable missing")

# # --- Setup Flask ---
# app = Flask(__name__)

# # --- Setup MongoDB ---
# client = MongoClient(mongo_uri)
# db = client["mind-blown"]
# collection = db["chatHistory"]

# # --- Load Model and Tokenizer ---
# device = "cpu"
# base_model_path = "Qwen/Qwen1.5-1.8B-Chat"
# adapter_path = "./qwen-psychika-lora"

# ------------------------------- Choose Remote or Local Model --------------------------------

# This code is a Flask application that serves as a chatbot API using a local pre-trained language model.

# from flask import Flask, request, jsonify
# from pymongo import MongoClient
# from datetime import datetime
# from dotenv import load_dotenv
# import os

# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM
# from peft import PeftModel

# load_dotenv()

# # --- Setup Flask ---
# app = Flask(__name__)

# # --- Setup MongoDB ---
# mongo_uri = os.getenv("MONGO_URI")
# client = MongoClient(mongo_uri)  # ganti sesuai MongoDB-mu
# db = client["mind-blown"]
# collection = db["chatHistory"]

# # --- Load Model and Tokenizer ---
# device = "cpu"
# base_model_path = "./qwen-1.5-1.8B-local"  # folder lokal
# adapter_path = "./qwen-psychika-lora"  # LoRA folder lokal

tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
base_model = AutoModelForCausalLM.from_pretrained(base_model_path, trust_remote_code=True)

model = PeftModel.from_pretrained(base_model, adapter_path).to(device)

# --- Utility: Fetch last 5 messages per user ---
def get_chat_history(user_id, limit=5):
    history = (
        collection.find({"user_id": user_id})
        .sort("timestamp", -1)
        .limit(limit)
    )
    return list(history)[::-1]  # reverse to chronological

# --- Utility: Format chat into prompt ---
def build_prompt(history, current_msg):
    chat = []
    for h in history:
        chat.append({"role": "user", "content": h["message"]})
        chat.append({"role": "assistant", "content": h["response"]})
    chat.append({"role": "user", "content": current_msg})
    prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
    return prompt

# --- Generate response ---
def generate_response(user_id, message):
    history = get_chat_history(user_id)
    prompt = build_prompt(history, message)
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

    output = model.generate(input_ids, max_new_tokens=256, do_sample=True, top_p=0.85, temperature=0.9)
    result = tokenizer.decode(output[0][input_ids.shape[-1]:], skip_special_tokens=True).strip()
    return result

# --- Save to MongoDB ---
def save_to_db(user_id, message, response):
    chat_record = {
        "user_id": user_id,
        "message": message,
        "response": response,
        "timestamp": datetime.now()
    }
    collection.insert_one(chat_record)

# --- API Route ---
@app.route("/generate", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id")
    message = data.get("message")

    if not user_id or not message:
        return jsonify({"error": "user_id and message required"}), 400

    response = generate_response(user_id, message)
    save_to_db(user_id, message, response)

    return jsonify({"response": response})

# --- Health check ---
@app.route("/")
def home():
    return "Chatbot API is running"

# --- Run ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
