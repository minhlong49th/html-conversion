import requests
from flask import request, jsonify
from bs4 import BeautifulSoup
from flask import Blueprint

html_to_notions_bp = Blueprint("html_to_notion_blocks",__name__)

def convert_html_to_notion_blocks(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')

        blocks = []

        for element in soup.find_all():
            if element.name == 'h1':
                blocks.extend(split_text_into_blocks(element.text, 'heading_1'))
            elif element.name == 'h2':
                blocks.extend(split_text_into_blocks(element.text, 'heading_2'))
            elif element.name == 'p':
                blocks.extend(split_text_into_blocks(element.text, 'paragraph'))
            elif element.name == 'ul':
                blocks.extend(split_text_into_blocks(element.text, 'bulleted_list_item'))
            elif element.name == 'ol':
                blocks.extend(split_text_into_blocks(element.text, 'numbered_list_item'))
            elif element.name == 'img':
                if element.has_attr('src') and (element['src'].startswith('http') or element['src'].startswith('https')):
                    img_src = element['src']
                    blocks.append({
                        'object': 'block',
                        'type': 'image',
                        'image': {
                            'type': 'external',
                            'external': {
                                'url': img_src
                            }
                        }
                    })

        return blocks
    except Exception as e:
        return None
    
def split_text_into_blocks(text, block_type):
    blocks = []
    current_block_text = ''

    for char in text:
        if len(current_block_text) == 2000:
            blocks.append({
                "object": "block",
                "type": block_type,
                block_type: {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": current_block_text,
                            "link": None
                        }
                    }],
                    "color": "default"
                }
            })
            current_block_text = ''
        current_block_text += char

    if current_block_text:
        blocks.append({
            "object": "block",
            "type": block_type,
            block_type: {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": current_block_text,
                        "link": None
                    }
                }],
                "color": "default"
            }
        })

    return blocks

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

@html_to_notions_bp.route('/convert_html_to_notion_blocks', methods=['POST'])
def convert_html_to_notion_blocks_api():
    try:
        data = request.get_json()
        url = data.get('url')

        html = fetch_html_content(url)
        if html:
            blocks = convert_html_to_notion_blocks(html)
            if blocks:
                return jsonify({'blocks': blocks})
            else:
                return jsonify({'error': 'Failed to convert HTML to Notion blocks'}), 500
        else:
            return jsonify({'error': 'Failed to fetch HTML content'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def register_html_to_notion_routes(app):
        app.register_blueprint(html_to_notions_bp)