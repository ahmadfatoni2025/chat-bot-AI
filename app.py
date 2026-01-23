from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
import os

class AIChatApp:
    def __init__(self, host="127.0.0.1", port=8000):
        # Load .env
        load_dotenv()

        # Ambil API key dari .env
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise RuntimeError("API_KEY belum di set di .env")

        self.client = genai.Client(api_key=self.api_key)

        self.host = host
        self.port = port

        self.app = Flask(__name__)
        CORS(self.app)  # biar frontend bisa fetch tanpa masalah

        self._register_routes()

    def _register_routes(self):
        @self.app.route("/")
        def home():
            return "Backend AI Chatbot aktif. Gunakan POST /chat"

        @self.app.route("/chat", methods=["POST"])
        def chat():
            data = request.get_json(silent=True)
            if not data or "message" not in data:
                return jsonify({"reply": "Request salah. Kirim JSON dengan field 'message'."}), 400

            message = data["message"].strip()
            if not message:
                return jsonify({"reply": "Pesan kosong. Server butuh teks."}), 400

            try:
                response = self.client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=message
                )
                return jsonify({"reply": response.text})

            except Exception as e:
                print("ERROR:", e)
                return jsonify({"reply": "Terjadi kesalahan di server."}), 500

    def run(self, debug=True):
        self.app.run(host=self.host, port=self.port, debug=debug)


if __name__ == "__main__":
    chat_app = AIChatApp()
    chat_app.run()
