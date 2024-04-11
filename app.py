from flask import Flask
from dotenv import load_dotenv
from routes.routes import api_routes
from flask_cors import CORS

load_dotenv()  # Load environment variables

app = Flask(__name__)
CORS(app)

# Register the Blueprint from routes.py
app.register_blueprint(api_routes)

if __name__ == '__main__':
    app.run(debug=True)
