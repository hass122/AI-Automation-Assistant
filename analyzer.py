from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def analyze_jobs(jobs, keyword):
    """
    Small ML demonstration:
    TF-IDF converts text to vectors and cosine similarity measures
    how closely each record matches the user's keyword.
    """
    documents = [
        keyword,
        *[f"{job['title']} {job['description']}" for job in jobs]
    ]

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(documents)
    scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

    analyzed = []
    for job, score in zip(jobs, scores):
        if score >= 0.35:
            level = "High"
        elif score >= 0.12:
            level = "Medium"
        else:
            level = "Low"

        item = dict(job)
        item["score"] = round(float(score) * 100, 1)
        item["match"] = level
        analyzed.append(item)

    analyzed.sort(key=lambda x: x["score"], reverse=True)
    return analyzed
