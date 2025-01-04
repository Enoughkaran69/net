from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import random
import time

app = Flask(__name__)

@app.route('/verify', methods=['GET'])
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
                random_value = random.random()
                new_url = f"https://userverify.netmirror.app/?fr3={data_addhash}&a=y&t={random_value}"
                
                # Make the second request
                new_response = requests.get(new_url)
                if new_response.status_code == 200:
                  verify_value = data_addhash
                  data = {"verify": verify_value}
                  cookies = {
                    "addhash": verify_value
                  }
                  while True:  # Infinite loop to retry until "All Done"
                    try:
                      # Send POST request
                      response = requests.post(url, data=data, cookies=cookies)
                      response.raise_for_status()
                      result = response.json()
                      if result.get("statusup") == "All Done":
                        return jsonify({
                        "status": "success",
                        "data_addhash": data_addhash,
                        "new_url": new_url,
                        "second_response": new_response.text[:200],
                        "need": response.cookies.get_dict())
                        })
                    
                        break
                      else:
                    except requests.exceptions.RequestException as e:
                    time.sleep(5)
                        
                    
                  
                  
                    
                else:
                    return jsonify({"status": "failed", "error": "Second request failed"}), 400
            else:
                return jsonify({"status": "failed", "error": "data-addhash attribute not found"}), 400
        else:
            return jsonify({"status": "failed", "error": "Failed to fetch the initial page"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
