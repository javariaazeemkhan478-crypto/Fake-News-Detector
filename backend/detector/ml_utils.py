import joblib
import re
import os
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = None
vectorizer = None

model_path = os.path.join(BASE_DIR, '..', '..', 'ml_model', 'fake_news_model.pkl')
vectorizer_path = os.path.join(BASE_DIR, '..', '..', 'ml_model', 'tfidf_vectorizer.pkl')

if os.path.exists(model_path):
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    stop_words = set(stopwords.words('english'))
    return ' '.join(w for w in text.split() if w not in stop_words)

def predict(text):
    if model is None:
        return {
            'label': 'UNAVAILABLE',
            'confidence': 0,
            'top_words': [],
            'explanation': 'ML model not trained yet'
        }
    cleaned = clean_text(text)
    vectorized = vectorizer.transform([cleaned])
    proba = model.predict_proba(vectorized)[0]
    label_idx = proba.argmax()
    label = 'FAKE' if label_idx == 1 else 'REAL'
    confidence = round(float(proba[label_idx]) * 100, 2)
    feature_names = vectorizer.get_feature_names_out()
    top_indices = vectorized.toarray()[0].argsort()[-5:][::-1]
    top_words = [feature_names[i] for i in top_indices]
    return {
        'label': label,
        'confidence': confidence,
        'top_words': top_words,
        'explanation': f"Top keywords: {', '.join(top_words)}"
    }