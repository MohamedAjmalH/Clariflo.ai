# Clariflo.ai - Social Media Truth Analyzer

## Overview

Clariflo.ai is a web-based application that uses machine learning to analyze social media posts and determine their truthfulness. The system provides users with an interface to input social media content and receive AI-powered analysis with confidence scores and detailed insights about the credibility of the information.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
The application uses a traditional server-rendered web architecture with Flask templates. The frontend consists of:

- **Template Engine**: Jinja2 templates for server-side rendering
- **Styling Framework**: Bootstrap 5 with dark theme for responsive design
- **JavaScript**: Vanilla JavaScript for client-side interactions and form validation
- **UI Components**: Custom CSS with gradient backgrounds and enhanced card styling for a modern look

### Backend Architecture
The backend is built using Flask with a modular design:

- **Web Framework**: Flask with Werkzeug proxy fix for deployment compatibility
- **Application Structure**: Separation of concerns with dedicated modules for ML analysis
- **Request Handling**: RESTful API endpoint for post analysis with JSON responses
- **Input Validation**: Multiple layers of validation including text length limits (10-5000 characters)

### Machine Learning Pipeline
The core ML functionality is encapsulated in a dedicated analyzer module:

- **Text Processing**: NLTK-based preprocessing with tokenization, stemming, and stopword removal
- **Feature Extraction**: TF-IDF vectorization for text feature representation
- **Classification Model**: Logistic regression for truthfulness prediction
- **Pattern Matching**: Rule-based detection of suspicious and credible patterns in text
- **Confidence Scoring**: Numerical confidence metrics for analysis results

### Data Processing Strategy
The system employs a hybrid approach combining statistical ML with rule-based analysis:

- **Preprocessing Pipeline**: Text normalization, special character handling, and linguistic feature extraction
- **Feature Engineering**: TF-IDF features combined with pattern-based indicators
- **Suspicious Pattern Detection**: Regex-based identification of misleading language patterns
- **Credibility Indicators**: Recognition of academic and journalistic language markers

## External Dependencies

### Python Libraries
- **Flask**: Web framework for HTTP request handling and templating
- **scikit-learn**: Machine learning pipeline including TF-IDF vectorization and logistic regression
- **NLTK**: Natural language processing for tokenization, stemming, and stopword removal
- **NumPy**: Numerical computing support for ML operations
- **Werkzeug**: WSGI utilities and middleware for production deployment

### Frontend Dependencies
- **Bootstrap 5**: CSS framework for responsive design and component styling
- **Font Awesome**: Icon library for UI enhancement
- **Custom CSS**: Application-specific styling with dark theme implementation

### Development Tools
- **Python 3.x**: Runtime environment
- **Flask development server**: Local development and debugging
- **Logging**: Built-in Python logging for debugging and monitoring

### NLTK Data Requirements
The application automatically downloads required NLTK datasets:
- **Punkt tokenizer**: Sentence and word tokenization models
- **Stopwords corpus**: Common word filtering for text preprocessing
- **Porter stemmer**: Word stemming for feature normalization

The architecture is designed for easy deployment on cloud platforms with minimal configuration, using environment variables for sensitive settings and automatic dependency management.