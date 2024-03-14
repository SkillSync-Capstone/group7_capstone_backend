from flask import Blueprint, request, jsonify
from services.pdf_service import handle_pdf
from services.url_service import process_url
from services.query_service import handle_query
from services.text_service import process_text


api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/process_pdf', methods=['POST'])
def pdf_api():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file provided'}), 400
    pdf_file = request.files['pdf']
    result = handle_pdf(pdf_file)
    return jsonify(result)

@api_routes.route('/process_text', methods=['POST'])
def text_api():
    data = request.get_json()
    text = data.get('text') if data else None
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    result = process_text(text)
    return jsonify(result)

@api_routes.route('/process_url', methods=['POST'])
def url_api():
    data = request.get_json()
    url = data.get('url') if data else None
    
    if not url:
        return jsonify({'error': 'No url provided'}), 400
    result = process_url(url)
    return result

@api_routes.route('/handle_query', methods=['POST'])
def query_api():
    data = request.get_json()
    query = data.get('query') if data else None
    
    if not query:
        return jsonify({'error': 'No text provided'}), 400
    result = handle_query(query)
    return jsonify(result)
