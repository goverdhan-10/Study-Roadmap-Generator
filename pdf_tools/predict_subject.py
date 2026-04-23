import joblib

model = joblib.load("models/subject_model.pkl")

def predict_subject(text):

    prediction = model.predict([text])[0]

    return prediction