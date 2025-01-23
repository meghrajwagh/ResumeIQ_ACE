from flask import *
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# IBM API Key from .env file
API_KEY = os.getenv('API_KEY')

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

    # Invoke IBM API
    iam_token = "eyJraWQiOiIyMDI0MTIzMTA4NDMiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTgwMDBKVk4yIiwiaWQiOiJJQk1pZC02OTgwMDBKVk4yIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiM2Q5MjBiM2UtODJhOC00Y2NjLTkwNWYtYzZhMjE5Njk1OWI3IiwiaWRlbnRpZmllciI6IjY5ODAwMEpWTjIiLCJnaXZlbl9uYW1lIjoiVmFpYmhhdiIsImZhbWlseV9uYW1lIjoiTmF3YWxlIiwibmFtZSI6IlZhaWJoYXYgTmF3YWxlIiwiZW1haWwiOiJ2YWliaGF2bmF3YWxlMDVAZ21haWwuY29tIiwic3ViIjoidmFpYmhhdm5hd2FsZTA1QGdtYWlsLmNvbSIsImF1dGhuIjp7InN1YiI6InZhaWJoYXZuYXdhbGUwNUBnbWFpbC5jb20iLCJpYW1faWQiOiJJQk1pZC02OTgwMDBKVk4yIiwibmFtZSI6IlZhaWJoYXYgTmF3YWxlIiwiZ2l2ZW5fbmFtZSI6IlZhaWJoYXYiLCJmYW1pbHlfbmFtZSI6Ik5hd2FsZSIsImVtYWlsIjoidmFpYmhhdm5hd2FsZTA1QGdtYWlsLmNvbSJ9LCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiJlYzUzNDE1Zjc4OTU0ZTU2YjUwMGU0MzQxN2E0ZjkyOCIsImZyb3plbiI6dHJ1ZX0sImlhdCI6MTczNzY2MDg2MSwiZXhwIjoxNzM3NjY0NDYxLCJpc3MiOiJodHRwczovL2lhbS5jbG91ZC5pYm0uY29tL2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6YXBpa2V5Iiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiZGVmYXVsdCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.oMZm2CK5qGG-C1dDxxgiOsah0UIvNBEydcuyNrS3CwouI3_S4W3SGCbmnVCNHY1_tL3Dw5lNbrP2KR2vxOrc0pXr9swEcfY08YAEg2mPeYKECjohmRffD-_e8vejvXzT5iRFci7o-QcBz4oWisBW6w1OTcsOBHA7U-xv70X9-wxFwnicmgVrmM8-W0sJveGiO0dPlhJ_ctblzbwzVxYLiGIRatKnHKTSq8BRAiVtYoKm-Pt4WLZhTEN7iNUa7-160xBEjF7ECPV7lfMrYv_HWhdg8mnJ8lqzIJhonJ8VYeDEMuuBp1FyD5kyPzIlX-P4K4yIgMQSYwakxHc42t7sHg"
    api_response = invoke_ibm_api(cv_data, iam_token)
    
    # Extract questions from the generated text
    questions = api_response.get("results", [])[0].get("generated_text", "")
    formatted_questions = questions.strip()  # Remove any unwanted leading/trailing spaces
    # print(formatted_questions)
    
    # Return the questions to the frontend
    return render_template("index.html", questions=formatted_questions)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
