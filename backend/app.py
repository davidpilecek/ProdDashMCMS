from flask import Flask
from flask_cors import CORS

from routes.report import report_bp
from routes.production import production_bp
from routes.statistics import statistics_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(production_bp)
app.register_blueprint(statistics_bp)
app.register_blueprint(report_bp)


@app.get("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )