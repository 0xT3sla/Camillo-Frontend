from flask import Flask, request, render_template, jsonify
import requests
import base64
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urljoin
import json
import html
app = Flask(__name__)

API_URL = "http://127.0.0.1:6969/api/analyze-url"

@app.route('/',  methods=['GET','POST'])
def home():
    try:
        if request.method == 'POST' and 'url' in request.form:
            url = request.form['url'].strip()
            # Encode URL to base64
            encoded_url = base64.urlsafe_b64encode(url.encode('utf-8')).decode('utf-8')
            # JSON data containing the encoded URL
            data = {'url': encoded_url}
            # Send POST request to the API endpoint
            response = requests.post(API_URL, json=data)
            if response.status_code == 200:
                # Convert JSON response to dictionary
                output = response.json()
            else:
                output = {'status': 'ERROR', 'msg': f"Failed to analyze URL: {response.status_code} - {response.text}"}
        else:
            output = 'NA'
    except Exception as e:
        output = {'status': 'ERROR', 'msg': str(e)}

    return render_template('index.html', output=output)


@app.route('/preview', methods=['POST'])
def preview():
    try:
        url = request.form.get('url')
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # inject external resources into HTML
        for link in soup.find_all('link'):
            if link.get('href'):
                link['href'] = urljoin(url, link['href'])
        
        # Uncomment this if you want to enable script
        # for script in soup.find_all('script'):
        #     if script.get('src'):
        #         script['src'] = urljoin(url, script['src'])

        for img in soup.find_all('img'):
            if img.get('src'):
                img['src'] = urljoin(url, img['src'])

        return render_template('preview.html', content=soup.prettify())
    except Exception as e:
        return  f"Error: {e}"


@app.route('/source-code', methods=['GET','POST'])
def view_source_code():

    try:
        url = request.form.get('url')
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        formatted_html = soup.prettify()
        
        return render_template('source_code.html', formatted_html = formatted_html, url = url)
    
    except Exception as e:
        return  f"Error: {e}"

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/verified', methods=['GET', 'POST'])
def verified():
    # Assuming 'output' is a variable containing the data you want to pass to the template
    # output = {
    #     'google_verified': 'Some value for Google Verified',
    #     'platform_type': 'Some value for Platform Type',
    #     'rank': 'Some value for Rank',
    #     'response_status': 'Some value for Response Status',
    #     'is_url_shortened': 'Some value for URL Shortened',
    #     'ip': 'Some value for IP',
    #     'trust_score': 90,
    #     'msg': 'Verification successful',
        
    # }
    return render_template('verified.html')


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
