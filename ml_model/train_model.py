import pandas as pd
import re
import nltk
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

nltk.download('stopwords')
from nltk.corpus import stopwords

print("Step 1: Dataset load ho raha hai...")
fake = pd.read_csv('Fake.csv')
real = pd.read_csv('True.csv')

fake['label'] = 1
real['label'] = 0

df = pd.concat([fake, real], ignore_index=True)
df['content'] = df['title'] + ' ' + df['text']

print(f"Total articles: {len(df)}")

print("Step 2: Text clean ho raha hai...")
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', str(text).lower())
    stop_words = set(stopwords.words('english'))
    return ' '.join(w for w in text.split() if w not in stop_words)

df['clean'] = df['content'].apply(clean_text)

print("Step 3: Train/test split ho raha hai...")
X_train, X_test, y_train, y_test = train_test_split(
    df['clean'], df['label'], test_size=0.2, random_state=42
)

print("Step 4: TF-IDF vectorizer train ho raha hai...")
vectorizer = TfidfVectorizer(max_features=10000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec  = vectorizer.transform(X_test)

print("Step 5: Model train ho raha hai...")
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

preds = model.predict(X_test_vec)
acc = accuracy_score(y_test, preds)
print(f"Accuracy: {acc:.4f}")

print("Step 6: Model save ho raha hai...")
joblib.dump(model, 'fake_news_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

print("Done! Model save ho gaya!")