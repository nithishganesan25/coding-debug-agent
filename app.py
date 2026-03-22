import os
import json
from flask import Flask, request, jsonify, render_template, Response
from main import analyze_code_stream

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/analyze_stream", methods=["POST"])
def analyze_stream():
    """ Handles Server-Sent Events (SSE) for live-streaming the Gemini response """
    data = request.json
    if not data or "code" not in data:
        return jsonify({"error": "Please provide your code in the JSON payload."}), 400
        
    code = data.get("code", "")
    error = data.get("error", "")
    mode = data.get("mode", "debug")

    def generate():
        try:
            for text_chunk in analyze_code_stream(code, error, mode):
                # Send the text chunk as a proper SSE JSON payload to perfectly handle newlines and quotes
                yield f"data: {json.dumps({'text': text_chunk})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'text': f'Server Stream Error: {str(e)}'})}\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route("/convert", methods=["POST"])
def convert():
    """ Dedicated endpoint to translate code block languages for the Convert & Download feature """
    import google.generativeai as genai
    data = request.json
    code = data.get("code", "")
    target_lang = data.get("language", "javascript")

    try:
        model = genai.GenerativeModel("gemini-1.5-pro") # use standard model for translation
        prompt = f"You are a master polyglot compiler. Translate the following code precisely into {target_lang}. Return ONLY the raw code, absolutely zero markdown formatting, no backticks, no explanations. Code:\n{code}"
        response = model.generate_content(prompt)
        clean_code = response.text.replace("```" + target_lang, "").replace("```", "").strip()
        return jsonify({"code": clean_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)