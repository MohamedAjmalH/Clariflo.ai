// Clariflo.ai - Main JavaScript functionality

class ClarifloAnalyzer {
    constructor() {
        this.isAnalyzing = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateCharacterCount();
    }

    setupEventListeners() {
        // Form submission
        const form = document.getElementById('analysisForm');
        form.addEventListener('submit', (e) => this.handleFormSubmission(e));

        // Character counter
        const textArea = document.getElementById('postText');
        textArea.addEventListener('input', () => this.updateCharacterCount());

        // Real-time validation
        textArea.addEventListener('input', () => this.validateInput());
    }

    updateCharacterCount() {
        const textArea = document.getElementById('postText');
        const charCount = document.getElementById('charCount');
        const currentLength = textArea.value.length;
        
        charCount.textContent = currentLength;
        
        // Change color based on character count
        if (currentLength > 4500) {
            charCount.style.color = '#dc3545'; // Red
        } else if (currentLength > 4000) {
            charCount.style.color = '#ffc107'; // Yellow
        } else {
            charCount.style.color = '#6c757d'; // Default
        }
    }

    validateInput() {
        const textArea = document.getElementById('postText');
        const analyzeBtn = document.getElementById('analyzeBtn');
        const text = textArea.value.trim();

        // Enable/disable button based on input
        if (text.length >= 10 && text.length <= 5000) {
            analyzeBtn.disabled = false;
            textArea.classList.remove('is-invalid');
        } else {
            analyzeBtn.disabled = true;
            if (text.length > 0 && (text.length < 10 || text.length > 5000)) {
                textArea.classList.add('is-invalid');
            }
        }
    }

    async handleFormSubmission(e) {
        e.preventDefault();
        
        if (this.isAnalyzing) {
            return;
        }

        const textArea = document.getElementById('postText');
        const text = textArea.value.trim();

        // Validate input
        if (!this.validateInputText(text)) {
            return;
        }

        try {
            this.setLoadingState(true);
            this.hideResults();
            
            const result = await this.analyzeText(text);
            
            if (result.error) {
                this.showError(result.error);
            } else {
                this.displayResults(result);
            }
            
        } catch (error) {
            console.error('Analysis error:', error);
            this.showError('Failed to analyze the text. Please check your connection and try again.');
        } finally {
            this.setLoadingState(false);
        }
    }

    validateInputText(text) {
        if (!text) {
            this.showError('Please enter some text to analyze.');
            return false;
        }

        if (text.length < 10) {
            this.showError('Text is too short. Please provide at least 10 characters for meaningful analysis.');
            return false;
        }

        if (text.length > 5000) {
            this.showError('Text is too long. Please limit your input to 5000 characters.');
            return false;
        }

        return true;
    }

    async analyzeText(text) {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Analysis failed');
        }

        return await response.json();
    }

    displayResults(result) {
        this.hideError();
        
        // Update main result
        this.updateClassificationBadge(result.classification);
        this.updateConfidenceScore(result.confidence);
        this.updateTruthfulnessBar(result.truthfulness_score, result.classification);
        
        // Update detailed analysis
        this.updateDetailedAnalysis(result.analysis_details);
        
        // Update explanation
        document.getElementById('explanation').textContent = result.explanation;
        
        // Show results with animation
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    updateClassificationBadge(classification) {
        const badge = document.getElementById('classificationBadge');
        badge.textContent = classification;
        
        // Remove existing classes
        badge.className = 'badge fs-4 px-4 py-2';
        
        // Add appropriate class based on classification
        switch (classification.toLowerCase()) {
            case 'true':
                badge.classList.add('bg-success');
                break;
            case 'false':
                badge.classList.add('bg-danger');
                break;
            case 'uncertain':
                badge.classList.add('bg-warning', 'text-dark');
                break;
            default:
                badge.classList.add('bg-secondary');
        }
    }

    updateConfidenceScore(confidence) {
        const confidenceElement = document.getElementById('confidenceScore');
        confidenceElement.textContent = `${confidence}%`;
        
        // Animate the number
        this.animateNumber(confidenceElement, 0, confidence, 1000);
    }

    updateTruthfulnessBar(score, classification) {
        const bar = document.getElementById('truthfulnessBar');
        const scoreElement = document.getElementById('truthfulnessScore');
        
        // Remove existing classes
        bar.className = 'progress-bar';
        
        // Add appropriate class based on score
        if (score >= 70) {
            bar.classList.add('bg-success');
        } else if (score <= 30) {
            bar.classList.add('bg-danger');
        } else {
            bar.classList.add('bg-warning');
        }
        
        // Animate the progress bar
        setTimeout(() => {
            bar.style.width = `${score}%`;
            scoreElement.textContent = `${score}%`;
        }, 100);
    }

    updateDetailedAnalysis(details) {
        document.getElementById('wordCount').textContent = details.word_count;
        document.getElementById('suspiciousPatterns').textContent = details.suspicious_patterns_found;
        document.getElementById('credibleIndicators').textContent = details.credible_patterns_found;
        document.getElementById('excessiveCapitals').textContent = details.excessive_capitals ? 'Yes' : 'No';
        document.getElementById('readabilityScore').textContent = `${details.readability_score}%`;
        document.getElementById('excessivePunctuation').textContent = details.excessive_punctuation ? 'Yes' : 'No';
        
        // Add color coding for indicators
        this.colorCodeIndicator('suspiciousPatterns', details.suspicious_patterns_found, true);
        this.colorCodeIndicator('credibleIndicators', details.credible_patterns_found, false);
        this.colorCodeBooleanIndicator('excessiveCapitals', details.excessive_capitals);
        this.colorCodeBooleanIndicator('excessivePunctuation', details.excessive_punctuation);
    }

    colorCodeIndicator(elementId, value, isNegative) {
        const element = document.getElementById(elementId);
        element.className = 'fw-bold';
        
        if (value > 0) {
            if (isNegative) {
                element.classList.add('text-danger');
            } else {
                element.classList.add('text-success');
            }
        } else {
            element.classList.add('text-muted');
        }
    }

    colorCodeBooleanIndicator(elementId, value) {
        const element = document.getElementById(elementId);
        element.className = 'fw-bold';
        
        if (value) {
            element.classList.add('text-danger');
        } else {
            element.classList.add('text-success');
        }
    }

    animateNumber(element, start, end, duration) {
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = Math.round(start + (end - start) * progress);
            element.textContent = `${current}%`;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }

    setLoadingState(loading) {
        this.isAnalyzing = loading;
        const analyzeBtn = document.getElementById('analyzeBtn');
        const textArea = document.getElementById('postText');
        
        if (loading) {
            analyzeBtn.disabled = true;
            analyzeBtn.innerHTML = `
                <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Analyzing...
            `;
            textArea.disabled = true;
            document.body.classList.add('loading');
        } else {
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = `
                <i class="fas fa-brain me-2"></i>
                Analyze Truthfulness
            `;
            textArea.disabled = false;
            document.body.classList.remove('loading');
            this.validateInput(); // Re-validate in case input changed during loading
        }
    }

    showError(message) {
        this.hideResults();
        const errorSection = document.getElementById('errorSection');
        const errorMessage = document.getElementById('errorMessage');
        
        errorMessage.textContent = message;
        errorSection.style.display = 'block';
        errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    hideError() {
        const errorSection = document.getElementById('errorSection');
        errorSection.style.display = 'none';
    }

    hideResults() {
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.style.display = 'none';
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ClarifloAnalyzer();
});

// Add some utility functions for enhanced user experience
document.addEventListener('DOMContentLoaded', () => {
    // Add smooth scrolling for all internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add copy functionality for results (if needed in future)
    const addCopyFunctionality = () => {
        // This can be extended to add copy buttons for results
        console.log('Copy functionality ready for future implementation');
    };

    addCopyFunctionality();

    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const form = document.getElementById('analysisForm');
            if (form) {
                form.dispatchEvent(new Event('submit', { cancelable: true }));
            }
        }
    });
});
