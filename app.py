from flask import Flask, request, jsonify
import pickle

# โหลด model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

# test route
@app.route("/")
def home():
    return "Posture AI Backend Running!"

# predict route
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    left = data.get("left")
    right = data.get("right")
    back = data.get("back")

    # เช็ค input
    if left is None or right is None or back is None:
        return jsonify({"error": "Missing data"}), 400

    # predict
    prediction = model.predict([[left, right, back]])

    return jsonify({
        "posture": prediction[0]
    })

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/predict", methods=["GET"])
def predict_get():
    return "Use POST method with JSON data"
