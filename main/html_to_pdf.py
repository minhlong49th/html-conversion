import requests
from flask import request, make_response, jsonify, current_app
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from flask import Blueprint
from urllib.parse import urljoin  # Import the urljoin function
from PIL import Image
from io import BytesIO

html_to_pdf_bp = Blueprint('html_to_pdf', __name__)

@html_to_pdf_bp.route('/html-to-pdf', methods=['POST'])
def html_to_pdf():
    try:
        # Get the webpage URL from the POST request
        url = request.json.get('url')  # Assuming the URL is sent in JSON format
        
        # Fetch the webpage content including images
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        html_content = response.text
        
        # Font configuration for WeasyPrint
        font_config = FontConfiguration()
        
        # Convert the HTML to a PDF in memory
        pdf = HTML(string=html_content, base_url=response.url).write_pdf(font_config=font_config)
        
        # Create a response object with the PDF data
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
        
        return response
    except requests.exceptions.RequestException as e:
        # Log the error and return an error message
        current_app.logger.error(f'Error fetching webpage content: {e}')
        return jsonify({'error': 'An error occurred while fetching webpage content'}), 500
    except Exception as e:
        # Log the error and return an error message
        current_app.logger.error(f'Error converting HTML to PDF: {e}')
        return jsonify({'error': 'An error occurred during conversion'}), 500

def register_html_to_pdf_routes(app):
    app.register_blueprint(html_to_pdf_bp)

# Custom class to handle relative URLs for images
class RelativeURLImageLoader(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_image(self, url):
        if not url.startswith('http'):
            url = urljoin(self.base_url, url)
        response = requests.get(url)
        response.raise_for_status()
        
        # Check the image dimensions
        image = Image.open(BytesIO(response.content))
        width, height = image.size
        if width > 1000 or height > 1000:  # Adjust the threshold as needed
            # Resize the image to fit within the specified dimensions
            new_width = min(1000, width)
            new_height = min(1000, height)
            resized_image = image.resize((new_width, new_height))
            
            # Save the resized image as a new file
            resized_image_buffer = BytesIO()
            resized_image.save(resized_image_buffer, format=image.format)
            resized_image_buffer.seek(0)
            
            return resized_image_buffer.read()
        else:
            return response.content

# Register the custom image loader with WeasyPrint
HTML.default_loader = RelativeURLImageLoader