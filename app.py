from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

@app.route("/reply", methods=["POST"])
def reply():
    data = request.json
    mensaje = data.get("message", "")
    
    groq_response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "Respondé mensajes de WhatsApp de manera corta y natural. Si alguien pregunta por Ozono decí que está ocupado y que ya responde."},
                {"role": "user", "content": mensaje}
            ]
        }
    )
    
    response = groq_response.json()
    
    if "choices" not in response:
        return jsonify({"error": response}), 500
    
    respuesta = response["choices"][0]["message"]["content"]
    return jsonify({"reply": respuesta})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
