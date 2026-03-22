import os
from flask import Flask, request, jsonify, render_template
from main import debug_code

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/debug", methods=["POST"])
def debug():
    try:
        data = request.json
        if not data or "code" not in data or "error" not in data:
            return jsonify({"error": "Please provide both 'code' and 'error' in the JSON payload."}), 400
            
        code = data["code"]
        error = data["error"]

        result = debug_code(code, error)

        return jsonify({"response": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)