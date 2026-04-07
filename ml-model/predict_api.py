from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd

# load model
model = pickle.load(open("model.pkl","rb"))

# load symptoms
symptoms_list = pickle.load(open("symptoms.pkl","rb"))

# load precautions dataset
precautions_df = pd.read_csv("../dataset/precautions.csv")

app = Flask(__name__)
CORS(app)


@app.route("/symptoms", methods=["GET"])
def get_symptoms():
    return jsonify(symptoms_list)


@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    if not data or "symptoms" not in data:
        return jsonify({"error": "No symptoms provided"}), 400

    user_symptoms = data["symptoms"]

    input_data = [0] * len(symptoms_list)

    for symptom in user_symptoms:
        if symptom in symptoms_list:
            index = symptoms_list.index(symptom)
            input_data[index] = 1

    input_df = pd.DataFrame([input_data], columns=symptoms_list)

    probs = model.predict_proba(input_df)[0]

    top_indices = probs.argsort()[-3:][::-1]

    predictions = []

    for i in top_indices:

        disease = model.classes_[i]

        row = precautions_df[precautions_df["Disease"] == disease]

        if not row.empty:

            precautions = [
                row["Precaution_1"].values[0],
                row["Precaution_2"].values[0],
                row["Precaution_3"].values[0],
                row["Precaution_4"].values[0]
            ]

            # Remove NaN values (important fix)
            precautions = [p for p in precautions if pd.notna(p)]

        else:

            precautions = [
                "Consult a doctor",
                "Take rest",
                "Stay hydrated",
                "Maintain healthy lifestyle"
            ]

        predictions.append({
            "disease": disease,
            "confidence": float(probs[i]),
            "precautions": precautions
        })

    # sort predictions by confidence
    predictions = sorted(predictions, key=lambda x: x["confidence"], reverse=True)

    return jsonify({
        "predictions": predictions
    })


if __name__ == "__main__":
    app.run(port=8000)