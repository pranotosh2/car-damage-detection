import os
from pathlib import Path
from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.routes.predict import predict_bp

app = Flask(__name__)
CORS(app)

# Register Blueprint
app.register_blueprint(predict_bp)

# Path to frontend
_root = Path(__file__).resolve().parent.parent.parent
frontend_path = _root / "frontend"

@app.route("/")
def serve_index():
    return send_from_directory(frontend_path, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(port=port, host="0.0.0.0", debug=True)
