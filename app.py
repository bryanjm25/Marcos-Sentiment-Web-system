from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pickle
import os
import re
from collections import Counter
import logging
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentiment_analysis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour session timeout

db = SQLAlchemy(app)

# Database Models
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback_text = db.Column(db.Text, nullable=False)
    sentiment_label = db.Column(db.String(20), nullable=False)
    confidence_score = db.Column(db.Float, nullable=True)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating_value = db.Column(db.Integer, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

# Sentiment Analysis Class
class SentimentAnalyzer:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.scaler = None
        self.encoder = None
        self.load_models()
    
    def load_models(self):
        try:
            with open('model.pkl', 'rb') as f:
                self.model = pickle.load(f)
            with open('vectorizer.pkl', 'rb') as f:
                self.vectorizer = pickle.load(f)
            with open('scaler.pkl', 'rb') as f:
                self.scaler = pickle.load(f)
            with open('encoder.pkl', 'rb') as f:
                self.encoder = pickle.load(f)
            logger.info("Models loaded successfully")
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            # Create dummy models for testing if files don't exist
            self.create_dummy_models()
    
    def create_dummy_models(self):
        """Create dummy models for testing when pkl files are not available"""
        logger.warning("Using dummy models for testing")
        self.model = None
        self.vectorizer = None
        self.scaler = None
        self.encoder = None
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def predict_sentiment(self, text):
        """Predict sentiment of given text"""
        try:
            if not self.model:
                # Dummy prediction for testing
                import random
                sentiments = ['Positive', 'Negative', 'Neutral']
                return random.choice(sentiments), random.uniform(0.6, 0.95)
            
            processed_text = self.preprocess_text(text)
            vectorized = self.vectorizer.transform([processed_text])
            
            if self.scaler:
                vectorized = self.scaler.transform(vectorized)
            
            prediction = self.model.predict(vectorized)[0]
            confidence = max(self.model.predict_proba(vectorized)[0])
            
            if self.encoder:
                sentiment = self.encoder.inverse_transform([prediction])[0]
            else:
                sentiment = prediction
                
            return sentiment, confidence
            
        except Exception as e:
            logger.error(f"Error in sentiment prediction: {str(e)}")
            return "Neutral", 0.5

# Initialize sentiment analyzer
sentiment_analyzer = SentimentAnalyzer()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def auto_logout_if_non_admin():
    if session.get('logged_in'):
        # Check if current path is within /admin/*
        if not request.path.startswith('/admin'):
            session.clear()  # clear session when accessing non-admin routes
            flash('You have been logged out for accessing a public page.', 'info')
            return redirect(url_for('home'))




# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        feedback_text = request.form.get('feedback', '').strip()
        rating = request.form.get('rating')
        
        if not feedback_text:
            return jsonify({'success': False, 'message': 'Feedback text is required'})
        
        # Analyze sentiment
        sentiment, confidence = sentiment_analyzer.predict_sentiment(feedback_text)
        
        # Save feedback
        feedback = Feedback(
            feedback_text=feedback_text,
            sentiment_label=sentiment,
            confidence_score=confidence
        )
        db.session.add(feedback)
        
        # Save rating if provided
        if rating:
            rating_obj = Rating(rating_value=int(rating))
            db.session.add(rating_obj)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Your feedback has been submitted successfully!'})
        
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred. Please try again.'})

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('admin_login.html')



@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))


def prepare_sentiment_wordclouds(feedbacks):
    """Prepare word cloud data for each sentiment"""
    sentiment_texts = {
        'Positive': [],
        'Negative': [],
        'Neutral': []
    }
    
    for feedback in feedbacks:
        sentiment = feedback.sentiment_label
        if sentiment in sentiment_texts:
            sentiment_texts[sentiment].append(feedback.feedback_text)
    
    wordcloud_data = {}
    for sentiment, texts in sentiment_texts.items():
        if texts:
            combined_text = ' '.join(texts)
            # Basic word processing
            words = re.findall(r'\b[a-zA-Z]{4,}\b', combined_text.lower())
            word_counts = Counter(words)
            # Get top 30 words for each sentiment
            top_words = word_counts.most_common(30)
            wordcloud_data[sentiment] = top_words
        else:
            wordcloud_data[sentiment] = []
    
    return wordcloud_data

@app.route('/admin')
def admin_dashboard():
    # Get feedback statistics
    feedbacks = Feedback.query.all()
    sentiment_counts = Counter([f.sentiment_label for f in feedbacks])
    
    # Get rating statistics
    ratings = Rating.query.all()
    rating_counts = Counter([r.rating_value for r in ratings])
    avg_rating = sum([r.rating_value for r in ratings]) / len(ratings) if ratings else 0
    
    # Prepare word cloud data for each sentiment
    wordcloud_data = prepare_sentiment_wordclouds(feedbacks)
    
    return render_template('admin_dashboard.html', 
                         feedbacks=feedbacks,
                         sentiment_counts=sentiment_counts,
                         rating_counts=rating_counts,
                         avg_rating=round(avg_rating, 2),
                         wordcloud_data=wordcloud_data)
    pass
@app.route('/admin/ratings')
def admin_ratings():
    ratings = Rating.query.order_by(Rating.date_submitted.desc()).all()
    rating_counts = Counter([r.rating_value for r in ratings])
    avg_rating = sum([r.rating_value for r in ratings]) / len(ratings) if ratings else 0
    
    return render_template('admin_ratings.html',
                         ratings=ratings,
                         rating_counts=rating_counts,
                         avg_rating=round(avg_rating, 2))

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False, host='0.0.0.0', port=5000)
