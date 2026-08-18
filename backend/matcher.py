from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ResumeMatcher:

    def __init__(self):
        self.sbert = SentenceTransformer("all-MiniLM-L6-v2")

    def compute_similarity(self, resume_text, job_description):
        embeddings = self.sbert.encode([resume_text, job_description])
        score = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]]
        )[0][0]

        return float(score)

    def classify_similarity(self, score):
        if score >= 0.75:
            return "High Match"
        elif score >= 0.55:
            return "Medium Match"
        else:
            return "Low Match"