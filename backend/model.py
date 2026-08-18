from sentence_transformers import SentenceTransformer
import joblib
import numpy as np

class ResumeClassifier:

    def __init__(self):
        self.sbert = SentenceTransformer("all-MiniLM-L6-v2")
        self.model = joblib.load("saved_model/resume_classifier.pkl")
        self.encoder = joblib.load("saved_model/label_encoder.pkl")

    def predict_category(self, resume_text):
        embedding = self.sbert.encode(resume_text)
        embedding = np.array(embedding).reshape(1, -1)

        prediction = self.model.predict(embedding)
        category = self.encoder.inverse_transform(prediction)

        return category[0]