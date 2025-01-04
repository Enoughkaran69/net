from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import random
import time

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/verify')
def verify():
    try:
        # URL of the initial website
        url = "https://iosmirror.cc/verify2.php"
        
        # Make a request to the website
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the body tag and get the value of data-addhash
            body_tag = soup.find('body')
            if body_tag and 'data-addhash' in body_tag.attrs:
                data_addhash = body_tag['data-addhash']
                
                # Replace 'su' with 'ni' in data_addhash
                modified_data_addhash = data_addhash.replace("su", "ni")
                
                # Generate a random value for 't'
                random_value = random.randint(1000000000, 9999999999)
                
                # Prepare the URL for the second request
                second_url = f"https://userverify.netmirror.app/?fr3={modified_data_addhash}&a=y&t={random_value}"
                
                # Make the second request
                second_response = requests.get(second_url)
                if second_response.status_code == 200:
                    return jsonify({
                        "status": "success",
                        "second_request_response": second_response.text
                    })
                else:
                    return jsonify({
                        "status": "failure",
                        "message": f"Failed second request. Status code: {second_response.status_code}"
                    }), second_response.status_code
            else:
                return jsonify({
                    "status": "failure",
                    "message": "data-addhash attribute not found in body tag."
                }), 404
        else:
            return jsonify({
                "status": "failure",
                "message": f"Failed to retrieve content. Status code: {response.status_code}"
            }), response.status_code
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
