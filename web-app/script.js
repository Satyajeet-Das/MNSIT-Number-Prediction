const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const canvasContainer = document.querySelector('.canvas-container');
const resultElement = document.getElementById('result');
let drawing = false;
let hasDrawn = false;

// Initialize canvas with white background
ctx.fillStyle = 'white';
ctx.fillRect(0, 0, canvas.width, canvas.height);

// Set drawing style
ctx.strokeStyle = 'black';
ctx.lineWidth = 20;
ctx.lineCap = 'round';
ctx.lineJoin = 'round';

// Mouse events for drawing
canvas.addEventListener('mousedown', (event) => {
    drawing = true;
    hasDrawn = true;
    canvasContainer.classList.add('canvas-has-content');
    ctx.beginPath();
    ctx.moveTo(event.offsetX, event.offsetY);
});

canvas.addEventListener('mouseup', () => {
    drawing = false;
});

canvas.addEventListener('mousemove', (event) => {
    if (drawing) {
        ctx.lineTo(event.offsetX, event.offsetY);
        ctx.stroke();
    }
});

// Touch events for mobile
canvas.addEventListener('touchstart', (event) => {
    event.preventDefault();
    const touch = event.touches[0];
    const rect = canvas.getBoundingClientRect();
    const x = touch.clientX - rect.left;
    const y = touch.clientY - rect.top;
    
    drawing = true;
    hasDrawn = true;
    canvasContainer.classList.add('canvas-has-content');
    ctx.beginPath();
    ctx.moveTo(x, y);
});

canvas.addEventListener('touchend', (event) => {
    event.preventDefault();
    drawing = false;
});

canvas.addEventListener('touchmove', (event) => {
    event.preventDefault();
    if (drawing) {
        const touch = event.touches[0];
        const rect = canvas.getBoundingClientRect();
        const x = touch.clientX - rect.left;
        const y = touch.clientY - rect.top;
        
        ctx.lineTo(x, y);
        ctx.stroke();
    }
});

// Clear canvas functionality
function clearCanvas() {
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    hasDrawn = false;
    canvasContainer.classList.remove('canvas-has-content');
    
    // Reset result to placeholder
    resultElement.innerHTML = `
        <div class="result-placeholder">
            <i class="fas fa-robot"></i>
            <span>Draw a digit and click "Predict Number" to see the AI's prediction!</span>
        </div>
    `;
}

// Add event listeners for buttons
document.getElementById('clear-btn').addEventListener('click', clearCanvas);

// Show loading state
function showLoading() {
    resultElement.innerHTML = `
        <div class="loading">
            <i class="fas fa-spinner"></i>
            <span>Analyzing your drawing...</span>
        </div>
    `;
}

// Show error state
function showError(message) {
    resultElement.innerHTML = `
        <div class="error">
            <i class="fas fa-exclamation-triangle"></i>
            <div>
                <h3>Oops! Something went wrong</h3>
                <p>${message}</p>
            </div>
        </div>
    `;
}

// Show prediction result
function showResult(predictedClass, confidence) {
    const confidencePercent = (confidence * 100).toFixed(1);
    
    resultElement.innerHTML = `
        <div class="result-content">
            <h2 class="predicted-digit">${predictedClass}</h2>
            <div class="confidence-info">
                <div class="confidence-label">Confidence Level</div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: ${confidencePercent}%"></div>
                </div>
                <div class="confidence-text">${confidencePercent}% confident</div>
            </div>
        </div>
    `;
}

// Prediction functionality
document.getElementById('predict-btn').addEventListener('click', async (event) => {
    event.preventDefault();
    
    if (!hasDrawn) {
        showError('Please draw a digit on the canvas first!');
        return;
    }
    
    showLoading();
    
    try {
        const dataUrl = canvas.toDataURL('image/png');
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: dataUrl })
        });
        
        const result = await response.json();
        
        if (result.error) {
            showError(result.error);
        } else {
            showResult(result.class, result.confidence);
        }
    } catch (error) {
        showError(`Network Error: ${error.message}. Make sure the server is running on port 8000.`);
    }
});
