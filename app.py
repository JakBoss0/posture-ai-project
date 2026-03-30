from flask import Flask, request, jsonify
import pickle
import os

# 1. โหลด model (แนะนำให้ใส่ try-except เผื่อหาไฟล์ไม่เจอ)
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    print("Error: ไม่พบไฟล์ model.pkl กรุณาตรวจสอบพาธไฟล์")

app = Flask(__name__)

@app.route("/")
def home():
    return "Posture AI Backend Running!"

# 2. รวม GET และ POST ไว้ด้วยกัน
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return "Please use POST method with JSON data (left, right, back)"
    
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    left = data.get("left")
    right = data.get("right")
    back = data.get("back")

    if left is None or right is None or back is None:
        return jsonify({"error": "Missing input fields (left, right, back)"}), 400

    # 3. Predict และแปลงผลลัพธ์เป็นมาตรฐาน Python (เช่น int หรือ str)
    prediction = model.predict([[left, right, back]])
    result = prediction[0]

    return jsonify({
        "posture": str(result) # แปลงเป็น str หรือ int เพื่อให้ jsonify ทำงานได้ 100%
    })

# 4. ต้องอยู่ล่างสุดเสมอ
if __name__ == "__main__":
    app.run(debug=True, port=5000)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
