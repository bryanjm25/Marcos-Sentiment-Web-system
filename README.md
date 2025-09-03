# Marcos Jr. Sentiment Analysis System

A comprehensive web-based platform for analyzing public sentiment regarding Philippine President Ferdinand "Bongbong" Marcos Jr. This system leverages advanced machine learning techniques to provide real-time insights into public opinion through feedback analysis and rating systems.

## Features

### 🏠 Homepage
- **Feedback Submission**: Users can submit their thoughts and opinions about President Marcos Jr.
- **5-Star Rating System**: Optional rating mechanism for comprehensive feedback
- **Real-time Sentiment Analysis**: Instant AI-powered sentiment classification
- **Success Notifications**: User-friendly feedback confirmation

### 🔐 Admin Panel
- **Secure Authentication**: Login system with username: `admin` and password: `admin123`
- **Comprehensive Dashboard**: 
  - Sentiment distribution analytics (Positive, Negative, Neutral)
  - Interactive charts and visualizations
  - Word cloud generation from feedback text
  - Recent feedback details with confidence scores
- **Rating Analytics**: 
  - Detailed 5-star rating breakdown
  - Average rating calculations
  - Rating distribution charts

### ℹ️ About Page
- **System Overview**: Detailed information about the platform
- **Technical Features**: Complete feature breakdown
- **Technology Stack**: Backend and frontend technologies used
- **Privacy & Security**: Data protection information

## Technology Stack

### Backend
- **Python Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Database (easily replaceable with PostgreSQL/MySQL)
- **Scikit-learn**: Machine learning models
- **Pickle**: Model serialization

### Frontend
- **HTML5 & CSS3**: Modern web standards
- **Bootstrap 5**: Responsive framework
- **JavaScript ES6+**: Interactive functionality
- **Chart.js**: Data visualizations
- **Font Awesome**: Icons

### Machine Learning
- **Pre-trained Models**: Sentiment analysis using your existing pkl files:
  - `model.pkl`: Main sentiment classification model
  - `vectorizer.pkl`: Text vectorization
  - `scaler.pkl`: Feature scaling
  - `encoder.pkl`: Label encoding

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone/Download the Project
```bash
# Navigate to your project directory
cd /path/to/MArcos
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Place Your ML Models
Ensure your trained models are in the root directory:
- `model.pkl`
- `vectorizer.pkl`
- `scaler.pkl`
- `encoder.pkl`

**Note**: If these files are not available, the system will use dummy models for testing purposes.

### Step 5: Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## Usage

### For Users
1. **Visit Homepage**: Navigate to `http://localhost:5000`
2. **Submit Feedback**: Enter your thoughts about President Marcos Jr.
3. **Rate Experience**: Optionally provide a 1-5 star rating
4. **Receive Confirmation**: Get instant feedback submission confirmation

### For Administrators
1. **Access Admin**: Go to `http://localhost:5000/admin/login`
2. **Login Credentials**:
   - Username: `admin`
   - Password: `admin123`
3. **View Analytics**: Access comprehensive sentiment and rating analytics
4. **Monitor Feedback**: Review all submitted feedback with sentiment labels

## Project Structure
```
MArcos/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── model.pkl             # Sentiment analysis model (your file)
├── vectorizer.pkl        # Text vectorizer (your file)
├── scaler.pkl            # Feature scaler (your file)
├── encoder.pkl           # Label encoder (your file)
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── admin_login.html  # Admin login
│   ├── admin_dashboard.html # Admin dashboard
│   ├── admin_ratings.html   # Rating analytics
│   ├── about.html        # About page
│   ├── 404.html          # Error pages
│   └── 500.html
└── static/               # Static files
    ├── css/
    │   └── style.css     # Custom styles
    └── js/
        └── main.js       # JavaScript functionality
```

## Database Schema

### Feedback Table
- `id`: Primary key
- `feedback_text`: User feedback content
- `sentiment_label`: AI-predicted sentiment (Positive/Negative/Neutral)
- `confidence_score`: Prediction confidence (0-1)
- `date_submitted`: Timestamp

### Rating Table
- `id`: Primary key
- `rating_value`: Star rating (1-5)
- `date_submitted`: Timestamp

## Security Features

- **Session Management**: Secure admin authentication
- **Input Validation**: Form data sanitization
- **Error Handling**: Comprehensive error management
- **CSRF Protection**: Built-in Flask security
- **Anonymous Feedback**: No personal data collection

## Customization

### Changing Admin Credentials
Edit the admin login route in `app.py`:
```python
if username == 'your_username' and password == 'your_password':
```

### Database Configuration
To use PostgreSQL or MySQL, update the database URI in `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/dbname'
```

### Styling Customization
Modify `static/css/style.css` to customize the appearance.

## Deployment

### Production Deployment
1. **Set Environment Variables**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secure-secret-key
   ```

2. **Use Production Server**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Database Migration**: For production, consider using PostgreSQL or MySQL.

## Troubleshooting

### Common Issues

**Models Not Loading**:
- Ensure all `.pkl` files are in the root directory
- Check file permissions
- Verify model compatibility with current scikit-learn version

**Database Errors**:
- Delete `sentiment_analysis.db` to reset database
- Check write permissions in project directory

**Port Already in Use**:
- Change port in `app.py`: `app.run(port=5001)`
- Or kill existing process using the port

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is created for educational and research purposes. Please ensure compliance with local laws and regulations when collecting and analyzing public sentiment data.

## Support

For technical support or questions:
- Check the troubleshooting section
- Review the code documentation
- Contact the development team through the admin panel

---

**Last Updated**: 2024
**Version**: 1.0.0
