import os, tempfile
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from counter import count_vehicles
from controller import plan

app = Flask(__name__)
CORS(app)
_prev = {"counts": None}


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/analyze")
def analyze():
    files = [request.files.get(f"video{i}") for i in range(4)]
    if not all(files):
        return jsonify(error="Upload 4 videos: video0..video3"), 400
    counts = []
    for f in files:
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as t:
            f.save(t.name)
        try:
            try:
                counts.append(count_vehicles(t.name))
            except ValueError as exc:
                return jsonify(error=str(exc)), 400
        finally:
            os.remove(t.name)
    emergency = request.form.get("emergency_lane", type=int)
    result = plan(counts, _prev["counts"], emergency)
    _prev["counts"] = counts
    return jsonify(result)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
