import os
import logging
from flask import Flask, render_template, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from ml_analyzer import MLAnalyzer

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "clariflo-dev-key-2025")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize ML analyzer
ml_analyzer = MLAnalyzer()

@app.route('/')
def index():
    """Main page with the analysis interface"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_post():
    """Analyze social media post for truthfulness"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'No text provided for analysis'
            }), 400
        
        text = data['text'].strip()
        
        if not text:
            return jsonify({
                'error': 'Empty text cannot be analyzed'
            }), 400
        
        if len(text) < 10:
            return jsonify({
                'error': 'Text too short for meaningful analysis (minimum 10 characters)'
            }), 400
        
        if len(text) > 5000:
            return jsonify({
                'error': 'Text too long for analysis (maximum 5000 characters)'
            }), 400
        
        # Perform ML analysis
        result = ml_analyzer.analyze_truthfulness(text)
        
        return jsonify(result)
        
    except Exception as e:
        app.logger.error(f"Error analyzing post: {str(e)}")
        return jsonify({
            'error': 'An error occurred during analysis. Please try again.'
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Clariflo.ai'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
