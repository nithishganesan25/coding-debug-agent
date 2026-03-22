import os
from flask import Flask, request, jsonify, render_template
from main import analyze_code

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        if not data or "code" not in data:
            return jsonify({"error": "Please provide your code in the JSON payload."}), 400
            
        code = data.get("code", "")
        error = data.get("error", "")
        mode = data.get("mode", "debug")

        result = analyze_code(code, error, mode)

        return jsonify({"response": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)