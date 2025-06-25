from flask import Flask
from flask_cors import CORS
from routes.analyze import analyze_bp

app = Flask(__name__)
CORS(app)

# Register all routes
app.register_blueprint(analyze_bp)

if __name__ == '__main__':
    print("✅ Flask server running at http://localhost:5050")
    app.run(debug=True, port=5050)