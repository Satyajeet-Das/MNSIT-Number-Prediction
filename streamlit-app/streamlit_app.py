import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64
import os

# Configure page
st.set_page_config(
    page_title="MNIST Digit Predictor - AI Neural Network",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom header styling */
    .custom-header {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.8);
    }
    
    .custom-header h1 {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }
    
    .custom-header p {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 300;
        color: #34495e;
        margin-top: 10px;
        opacity: 0.8;
    }
    
    .brain-icon {
        font-size: 3rem;
        background: linear-gradient(45deg, #3498db, #2c3e50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Canvas section styling */
    .canvas-section {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.8);
        margin-bottom: 2rem;
    }
    
    /* Result section styling */
    .result-section {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.8);
        text-align: center;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .predicted-digit {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    
    .confidence-info {
        margin-top: 1rem;
    }
    
    .confidence-label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #495057;
        margin-bottom: 10px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(52, 152, 219, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(52, 152, 219, 0.4);
    }
    
    /* Metric styling */
    .metric-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #3498db, #2ecc71, #27ae60);
    }
    
    /* Instructions styling */
    .instructions {
        background: rgba(52, 152, 219, 0.1);
        padding: 1rem;
        border-radius: 12px;
        border-left: 4px solid #3498db;
        margin-bottom: 1rem;
    }
    
    .instructions p {
        color: #2c3e50;
        margin: 0;
        font-weight: 500;
    }
    
    /* Error styling */
    .error-message {
        background: rgba(231, 76, 60, 0.1);
        padding: 1rem;
        border-radius: 12px;
        border-left: 4px solid #e74c3c;
        color: #e74c3c;
        margin: 1rem 0;
    }
    
    /* Success styling */
    .success-message {
        background: rgba(46, 204, 113, 0.1);
        padding: 1rem;
        border-radius: 12px;
        border-left: 4px solid #2ecc71;
        color: #27ae60;
        margin: 1rem 0;
    }

    /* Hide canvas toolbar */
    .streamlit-drawable-canvas > div > div:first-child {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Load model with caching
@st.cache_resource
def load_model():
    try:
        model_path = os.path.join('..', 'models', 'mnist_model.h5')
        model = tf.keras.models.load_model(model_path)
        return model, None
    except Exception as e:
        return None, str(e)

def process_canvas_image(canvas_result):
    """Process the canvas image for prediction"""
    if canvas_result.image_data is not None:
        # Convert to PIL Image
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        
        # Convert to grayscale
        img = img.convert('L')
        
        # Resize to 28x28
        img = img.resize((28, 28), Image.Resampling.LANCZOS)
        
        # Convert to numpy array and normalize
        img_array = np.array(img).reshape(1, 28, 28, 1)
        img_array = img_array.astype("float32") / 255.0
        
        # Invert colors (MNIST expects white digits on black background)
        img_array = 1.0 - img_array
        
        return img_array
    return None

def predict_digit(model, img_array):
    """Make prediction using the model"""
    try:
        predictions = model.predict(img_array, verbose=0)
        predicted_class = np.argmax(predictions, axis=1)[0]
        confidence = np.max(predictions)
        return predicted_class, confidence, predictions[0]
    except Exception as e:
        return None, None, str(e)

# Main app
def main():
    # Custom header
    st.markdown("""
    <div class="custom-header">
        <h1><span class="brain-icon">🧠</span> MNIST Digit Predictor</h1>
        <p>Draw a digit and let AI predict what number it is!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load model
    model, error = load_model()
    
    if error:
        st.markdown(f"""
        <div class="error-message">
            <strong>Error loading model:</strong> {error}
            <br>Please ensure 'mnist_model.h5' is in the same directory as this script.
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Create two columns
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="canvas-section">', unsafe_allow_html=True)
        st.markdown("### 🎨 Draw a Digit")
        
        # Instructions
        st.markdown("""
        <div class="instructions">
            <p>📝 Draw a single digit (0-9) in the canvas below. Make it large and centered for best results!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Drawing canvas
        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0)",  # Transparent fill
            stroke_width=20,
            stroke_color="black",
            background_color="white",
            background_image=None,
            update_streamlit=True,
            height=280,
            width=280,
            drawing_mode="freedraw",
            point_display_radius=0,
            key="canvas",
        )
        
        # Buttons
        col_predict, col_clear = st.columns(2)
        
        with col_predict:
            predict_btn = st.button("🔮 Predict Digit", type="primary", use_container_width=True)
        
        with col_clear:
            if st.button("🧹 Clear Canvas", use_container_width=True):
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.markdown("### 🤖 AI Prediction Results")
        
        if predict_btn:
            if canvas_result.image_data is not None:
                # Check if something is drawn
                img_array = process_canvas_image(canvas_result)
                
                if img_array is not None and np.sum(img_array) > 0.1:  # Check if there's content
                    with st.spinner("🧠 Analyzing your drawing..."):
                        predicted_class, confidence, all_predictions = predict_digit(model, img_array)
                    
                    if predicted_class is not None:
                        # Display prediction
                        st.markdown(f"""
                        <div style="text-align: center;">
                            <div class="predicted-digit">{predicted_class}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Confidence metrics
                        st.markdown('<div class="confidence-info">', unsafe_allow_html=True)
                        st.markdown('<div class="confidence-label">Confidence Level</div>', unsafe_allow_html=True)
                        
                        # Progress bar for confidence
                        st.progress(confidence, text=f"{confidence:.1%} confident")
                        
                        # Detailed metrics
                        col_metric1, col_metric2 = st.columns(2)
                        with col_metric1:
                            st.metric("Predicted Digit", predicted_class)
                        with col_metric2:
                            st.metric("Confidence", f"{confidence:.1%}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Show all predictions
                        with st.expander("📊 View All Predictions"):
                            prediction_data = []
                            for i, prob in enumerate(all_predictions):
                                prediction_data.append({
                                    "Digit": i,
                                    "Probability": f"{prob:.1%}",
                                    "Confidence": prob
                                })
                            
                            # Sort by confidence
                            prediction_data.sort(key=lambda x: x["Confidence"], reverse=True)
                            
                            for item in prediction_data[:3]:  # Show top 3
                                st.write(f"**{item['Digit']}**: {item['Probability']}")
                        
                        st.markdown("""
                        <div class="success-message">
                            ✅ Prediction completed successfully!
                        </div>
                        """, unsafe_allow_html=True)
                    
                    else:
                        st.markdown("""
                        <div class="error-message">
                            ❌ Prediction failed. Please try drawing again.
                        </div>
                        """, unsafe_allow_html=True)
                
                else:
                    st.markdown("""
                    <div class="error-message">
                        ✏️ Please draw a digit on the canvas first!
                    </div>
                    """, unsafe_allow_html=True)
            
            else:
                st.markdown("""
                <div class="error-message">
                    🎨 Canvas is empty. Please draw a digit first!
                </div>
                """, unsafe_allow_html=True)
        
        else:
            # Default state
            st.markdown("""
            <div style="text-align: center; color: #6c757d; padding: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                <p style="font-size: 1.1rem; line-height: 1.5;">
                    Draw a digit and click "Predict Digit" to see the AI's prediction!
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: rgba(44, 62, 80, 0.7); font-size: 0.9rem; padding: 1rem;">
        Powered by Neural Networks & TensorFlow | Built with Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
