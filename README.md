# Clariflo.ai - Social Media Truth Analyzer

A web-based AI application that analyzes social media posts to determine their truthfulness using machine learning and natural language processing.

## 🚀 Features

- **Real-time Analysis**: Instant truthfulness detection for social media content
- **Confidence Scoring**: Detailed confidence metrics with explanations
- **Pattern Recognition**: Advanced detection of suspicious vs credible language patterns
- **User-Friendly Interface**: Clean, responsive design with intuitive controls
- **Detailed Insights**: Comprehensive breakdown of analysis factors

## 🛠️ Technologies Used

- **Backend**: Python, Flask
- **Machine Learning**: scikit-learn, NLTK, NumPy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Text Processing**: Natural Language Processing with pattern matching
- **Deployment**: Gunicorn WSGI server

## 📋 How It Works

1. **Input**: User pastes social media post content
2. **Processing**: AI analyzes text using:
   - Pattern recognition for suspicious/credible indicators
   - Linguistic feature extraction
   - Statistical text analysis
3. **Output**: Truthfulness classification with confidence score and detailed explanation

## 🎯 Classification System

- **True**: High confidence in content reliability (65+ score)
- **False**: High confidence content is misleading (35- score)  
- **Uncertain**: Mixed indicators requiring further verification

## 🔧 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/clariflo-ai.git
cd clariflo-ai

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

The application will be available at `http://localhost:5000`

## 📦 Dependencies

```
flask
scikit-learn
nltk
numpy
gunicorn
werkzeug
```

## 🎨 Design

Modern, responsive interface with:
- Custom gradient color scheme
- Interactive analysis feedback
- Progress visualization
- Mobile-friendly design

## ⚠️ Important Notice

This tool provides AI-powered analysis for educational and research purposes. Results should be used as guidance only and not as definitive truth verification. Always verify information through multiple reliable sources.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for improvements.

## 📄 License

This project is open source and available under the MIT License.

---

Built with ❤️ using Python and Flask