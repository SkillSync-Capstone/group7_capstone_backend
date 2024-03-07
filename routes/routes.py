from flask import Blueprint, request, jsonify
from services.pdf_service import handle_pdf
from services.url_service import process_url
from services.query_service import handle_query

# Create a Blueprint for all routes
api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/process_pdf', methods=['POST'])
def pdf_api():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file provided'}), 400
    pdf_file = request.files['pdf']
    result = handle_pdf(pdf_file)
    return jsonify(result)

@api_routes.route('/process_url', methods=['POST'])
def url_api():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    result = process_url(url)
    return jsonify(result)

@api_routes.route('/handle_query', methods=['POST'])
def query_api():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    result = handle_query(query)
    return jsonify(result)

@api_routes.route('/', methods=['GET'])
def queryDemo():
    return  jsonify("hello")