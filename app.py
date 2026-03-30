from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os

app = Flask(__name__)
CORS(app)

# โหลด model
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully")
except Exception as e:
    print("❌ Error loading model:", e)
    model = None

# Home route (เช็คว่า server ทำงาน)
@app.route("/")
def home():
    return "Posture AI Backend Running!"

# GET สำหรับเปิดใน browser กันงง
@app.route("/predict", methods=["GET"])
def predict_get():
    return "Use POST method with JSON data"

# POST สำหรับ AI จริง
@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    left = data.get("left")
    right = data.get("right")
    back = data.get("back")

    # เช็ค input
    if left is None or right is None or back is None:
        return jsonify({"error": "Missing data"}), 400

    try:
        prediction = model.predict([[left, right, back]])
        return jsonify({
            "posture": prediction[0]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# สำหรับ Render (สำคัญมาก)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
