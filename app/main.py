from flask import Flask
from app.api.routes import api_bp
from app.utils.rate_lim import limiter
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(api_bp, url_prefix='/api')
    limiter.init_app(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)