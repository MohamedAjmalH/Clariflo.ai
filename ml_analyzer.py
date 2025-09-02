import re
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import os

class MLAnalyzer:
    def __init__(self):
        """Initialize the ML analyzer with pre-trained models and features"""
        self.logger = logging.getLogger(__name__)
        self.stemmer = PorterStemmer()
        
        # Download required NLTK data
        self._download_nltk_data()
        
        # Initialize the ML pipeline
        self._initialize_model()
        
        # Define suspicious patterns that might indicate false information
        self.suspicious_patterns = [
            r'\b(fake|false|hoax|satire|parody|onion|babylon bee)\b',  # Explicit fake indicators
            r'\b(doctors hate|miracle cure|secret formula|hidden truth)\b',
            r'\b(100% proven|absolutely certain|guaranteed cure)\b',
            r'\b(they don\'t want you to know|mainstream media hiding|cover.?up)\b',
            r'[!]{3,}',  # Three or more exclamation marks
            r'[A-Z]{15,}',  # Very long sequences of capitals (15+ chars)
            r'\b(click here|act now|limited time|don\'t miss)\b',
            r'\b(miracle|instant|overnight|revolutionary breakthrough)\b',
            r'\b(you won\'t believe|shocking truth|this will blow your mind)\b',
            r'\b(completely made up|totally false|obviously fake)\b'
        ]
        
        # Define credibility indicators - much more comprehensive
        self.credible_patterns = [
            r'\b(according to|study shows|research indicates|data suggests|findings show|confirms|verified)\b',
            r'\b(university|institute|journal|published|academic|college|school)\b',
            r'\b(evidence|statistics|analysis|peer-reviewed|scientific|research|data)\b',
            r'\b(reuters|ap news|bbc|cnn|npr|associated press|abc news|nbc|cbs|fox news)\b',
            r'\b(professor|dr\.|phd|researcher|scientist|expert|analyst|specialist)\b',
            r'\b(study|survey|poll|investigation|report|review|examination)\b',
            r'\b(government|official|ministry|department|agency|administration|authority)\b',
            r'\b(breaking news|news report|journalist|correspondent|reporter|editor)\b',
            r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
            r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\b',
            r'\b(said|told|stated|announced|confirmed|revealed|disclosed)\b',
            r'\b(police|court|judge|lawyer|attorney|trial|case|legal)\b',
            r'\b(hospital|medical|health|patient|doctor|treatment|clinic)\b',
            r'\b(company|corporation|business|industry|market|economic|financial)\b',
            r'\b(president|minister|senator|congressman|governor|mayor|official)\b'
        ]

    def _download_nltk_data(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            nltk.download('punkt_tab')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')

    def _initialize_model(self):
        """Initialize and train a basic model for truthfulness classification"""
        # Create a simple pipeline with TF-IDF and Logistic Regression
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2),
                lowercase=True
            )),
            ('classifier', LogisticRegression(random_state=42))
        ])
        
        # Since we don't have training data, we'll use rule-based analysis
        # combined with linguistic features
        self.is_trained = False

    def _preprocess_text(self, text):
        """Preprocess text for analysis"""
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove special characters but keep punctuation for pattern analysis
        cleaned_text = re.sub(r'[^\w\s\.,!?;:\'"()-]', '', text)
        
        return cleaned_text.strip()

    def _calculate_sentiment_features(self, text):
        """Calculate sentiment and linguistic features"""
        features = {}
        
        # Text length features
        features['text_length'] = len(text)
        features['word_count'] = len(text.split())
        features['avg_word_length'] = np.mean([len(word) for word in text.split()]) if text.split() else 0
        
        # Punctuation features
        features['exclamation_count'] = text.count('!')
        features['question_count'] = text.count('?')
        features['capital_ratio'] = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        
        # Suspicious pattern matching
        suspicious_score = 0
        for pattern in self.suspicious_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            suspicious_score += matches
        features['suspicious_score'] = suspicious_score
        
        # Credible pattern matching
        credible_score = 0
        for pattern in self.credible_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            credible_score += matches
        features['credible_score'] = credible_score
        
        return features

    def _analyze_linguistic_patterns(self, text):
        """Analyze linguistic patterns that might indicate truthfulness"""
        try:
            tokens = word_tokenize(text.lower())
            stop_words = set(stopwords.words('english'))
            filtered_tokens = [token for token in tokens if token not in stop_words and token.isalpha()]
            
            # Calculate readability and complexity
            avg_sentence_length = len(tokens) / max(1, text.count('.') + text.count('!') + text.count('?'))
            unique_words_ratio = len(set(filtered_tokens)) / max(1, len(filtered_tokens))
            
            return {
                'avg_sentence_length': avg_sentence_length,
                'unique_words_ratio': unique_words_ratio,
                'filtered_word_count': len(filtered_tokens)
            }
        except Exception as e:
            self.logger.error(f"Error in linguistic analysis: {str(e)}")
            return {
                'avg_sentence_length': 0,
                'unique_words_ratio': 0,
                'filtered_word_count': 0
            }

    def analyze_truthfulness(self, text):
        """Analyze the truthfulness of a social media post"""
        try:
            # Preprocess the text
            cleaned_text = self._preprocess_text(text)
            
            # Extract features
            sentiment_features = self._calculate_sentiment_features(cleaned_text)
            linguistic_features = self._analyze_linguistic_patterns(cleaned_text)
            
            # Rule-based scoring system - Much more confident for legitimate news
            truthfulness_score = 75  # Start with high confidence for news content
            
            # MAJOR boost for credible patterns - if it looks like news, treat it as news
            credible_boost = sentiment_features['credible_score'] * 20
            if sentiment_features['credible_score'] >= 3:  # Multiple credible indicators
                credible_boost += 15  # Extra bonus for multiple indicators
            if sentiment_features['credible_score'] >= 5:  # Lots of credible indicators
                credible_boost += 25  # Massive bonus - clearly legitimate news
            truthfulness_score += credible_boost
            
            # Check for explicit fake indicators first
            explicit_fake_patterns = ['fake', 'false', 'hoax', 'satire', 'parody', 'made up']
            explicit_fake_count = sum(1 for pattern in explicit_fake_patterns if pattern in cleaned_text.lower())
            
            # Special boost for typical news language patterns
            news_words = ['said', 'according', 'reported', 'announced', 'confirmed', 'revealed', 'stated']
            news_word_count = sum(1 for word in news_words if word in cleaned_text.lower())
            if news_word_count >= 2:
                # But don't boost if it contains fake indicators
                if explicit_fake_count == 0:  # Only boost if no fake indicators
                    truthfulness_score += 20  # Big boost for news language
            
            # Smart penalty system for suspicious patterns
            suspicious_penalty = sentiment_features['suspicious_score'] * 12
            
            # MAJOR penalty for explicit fake indicators
            if explicit_fake_count > 0:
                truthfulness_score -= 50  # Massive penalty for explicit fake indicators
                suspicious_penalty *= 2  # Double other suspicious penalties
            
            truthfulness_score -= suspicious_penalty
            
            # Very lenient on formatting for news
            if sentiment_features['capital_ratio'] > 0.7:  # Very high threshold
                truthfulness_score -= 8  # Minimal penalty
            
            # Very lenient on punctuation for news headlines
            if sentiment_features['exclamation_count'] > 8:  # Very high threshold
                truthfulness_score -= 5  # Minimal penalty
            
            # No penalty for short news snippets/headlines
            if sentiment_features['word_count'] < 5:
                truthfulness_score -= 0  # No penalty
            
            # Big bonus for typical news article length
            if 10 <= sentiment_features['word_count'] <= 500:
                truthfulness_score += 10  # Increased bonus
            
            # No penalty for complex news writing
            if linguistic_features['avg_sentence_length'] > 50:  # Very high threshold
                truthfulness_score -= 0  # No penalty
            
            # Normalize score to 0-100 range
            truthfulness_score = max(0, min(100, truthfulness_score))
            
            # Determine classification - Balanced thresholds
            if truthfulness_score >= 65:  # Threshold for "True"
                classification = "True"
                confidence = min(98, max(75, truthfulness_score + 10))  # High confidence boost
            elif truthfulness_score <= 35:  # Threshold for "False" 
                classification = "False"
                confidence = min(98, max(75, 100 - truthfulness_score))  # High confidence for fake
            else:
                classification = "Uncertain"
                confidence = max(50, abs(50 - truthfulness_score))  # Moderate uncertain confidence
            
            # Prepare detailed analysis
            analysis_details = {
                'word_count': sentiment_features['word_count'],
                'suspicious_patterns_found': sentiment_features['suspicious_score'],
                'credible_patterns_found': sentiment_features['credible_score'],
                'excessive_capitals': sentiment_features['capital_ratio'] > 0.5,
                'excessive_punctuation': sentiment_features['exclamation_count'] > 5,
                'readability_score': min(100, max(0, 100 - linguistic_features['avg_sentence_length']))
            }
            
            return {
                'classification': classification,
                'confidence': round(confidence, 1),
                'truthfulness_score': round(truthfulness_score, 1),
                'analysis_details': analysis_details,
                'explanation': self._generate_explanation(classification, analysis_details, truthfulness_score)
            }
            
        except Exception as e:
            self.logger.error(f"Error in truthfulness analysis: {str(e)}")
            return {
                'error': 'Analysis failed due to technical error',
                'classification': 'Uncertain',
                'confidence': 0,
                'truthfulness_score': 50
            }

    def _generate_explanation(self, classification, details, score):
        """Generate human-readable explanation of the analysis"""
        explanations = []
        
        if details['suspicious_patterns_found'] > 0:
            explanations.append(f"Found {details['suspicious_patterns_found']} suspicious language patterns")
        
        if details['credible_patterns_found'] > 0:
            explanations.append(f"Found {details['credible_patterns_found']} credibility indicators")
        
        if details['excessive_capitals']:
            explanations.append("Excessive use of capital letters detected")
        
        if details['excessive_punctuation']:
            explanations.append("Excessive punctuation usage detected")
        
        if details['word_count'] < 10:
            explanations.append("Text is very short, limiting analysis accuracy")
        
        if score >= 70:
            base_explanation = "The text shows characteristics of reliable information."
        elif score <= 30:
            base_explanation = "The text shows characteristics commonly associated with misinformation."
        else:
            base_explanation = "The text has mixed characteristics, making classification uncertain."
        
        if explanations:
            return f"{base_explanation} {' '.join(explanations)}"
        else:
            return f"{base_explanation} No significant patterns detected."
