import requests
from flask import request, jsonify
from flask import Blueprint
import html2text


html_to_google_docs_bp = Blueprint("html_to_google_docs",__name__)

def fetch_html_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except requests.exceptions.RequestException as e:
        return None
    except Exception as e:
        return None
    
@html_to_google_docs_bp.route('/html-to-google-docs', methods=['POST'])
def convert_html_to_google_docs():
    try:
        data = request.get_json()
        url = data.get('url')

        html = fetch_html_content(url)
        if html:
            # Convert the HTML content to Google Docs format
            h = html2text.HTML2Text()
            h.google_docs = True
            
            document = h.handle(html)
            if document:
                return jsonify({'document': document})
            else:
                return jsonify({'error': 'Failed to convert HTML to Google Docs format'}), 500
        else:
            return jsonify({'error': 'Failed to fetch HTML content'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500