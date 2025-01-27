from flask import *
import requests
import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path


load_dotenv("API_KEY.env")

# Initialize Flask app
app = Flask(__name__)


API_KEY = os.getenv('API_KEY')

def generate_access_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        return response.json().get("access_token")
    except Exception as e:
        return None

@app.route('/')
def index():
    return render_template("index.html")

# Function to send resume to IBM API
def invoke_ibm_api(cv_data, iam_token):
    url = "https://au-syd.ml.cloud.ibm.com/ml/v1/deployments/3dc4844a-704e-42de-8488-9f9608224f6b/text/generation?version=2021-05-01"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {iam_token}"
    }
    payload = {
        "parameters": {
            "prompt_variables": {
                "cv": cv_data
            }
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

@app.route('/submit_cv', methods=['POST'])
def submit_cv():
    # Get the resume (CV) content from the request
    cv_data = request.form.get('data_cv')
    #print(cv_data)

    iam_token = generate_access_token(API_KEY)
   
    api_response = invoke_ibm_api(cv_data, iam_token)
    
    # Extract questions from the generated text
    questions = api_response.get("results", [])[0].get("generated_text", "")
    formatted_questions = questions.strip()  
    # print(formatted_questions)
    
    # Return the questions to the frontend
    return render_template("index.html", questions=formatted_questions)

app.run(debug=True)
