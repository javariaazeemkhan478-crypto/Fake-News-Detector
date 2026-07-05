# Fake News Detection System

AI-powered full-stack web application that detects whether a news article is FAKE or REAL using Machine Learning and NLP with 98.99% accuracy.

## Features
- Paste article text and get instant prediction
- Confidence score with progress bar
- Detected keywords explanation
- Analytics dashboard with charts
- Login and Register system
- PDF report download

## Tech Stack
- **Frontend:** React.js, Recharts, Axios
- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **ML:** TF-IDF, Logistic Regression, NLTK, scikit-learn
- **Auth:** Token Authentication

## ML Pipeline
- Dataset: 44,000+ articles (Reuters + PolitiFact)
- Preprocessing: NLP text cleaning, stop word removal
- Vectorization: TF-IDF (10,000 features)
- Algorithm: Logistic Regression
- Accuracy: 98.99%

## Setup

### Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

### Frontend
cd frontend
npm install
npm start

### ML Model
cd ml_model
pip install pandas scikit-learn nltk joblib
python train_model.py
