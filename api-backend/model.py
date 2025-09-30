from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import base64
from PIL import Image
import io
import os

#Loading the trained model
model_path = os.path.join('..', 'models', 'mnist_model.h5')
model = load_model(model_path)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ImageData(BaseModel):
    image: str  # Base64 encoded image data

@app.post("/predict")
def predict(data: ImageData):
    try:
        # Extract base64 data from data URL
        image_data = data.image.split(',')[1]  # Remove "data:image/png;base64," prefix
        
        # Decode base64 to image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        image.save("original_image.png")  # Save original image for debugging

        
        # Convert to grayscale and resize to 28x28
        image = image.convert('L')
        image = image.resize((28, 28))
        
        # Convert to numpy array and normalize
        image_array = np.array(image).reshape(1, 28, 28, 1)
        image_array = image_array.astype("float32") / 255.0
        
        # Invert colors (MNIST expects white digits on black background)
        image_array = 1.0 - image_array

        # Save image array locally for testing in image format
        image = Image.fromarray((image_array[0] * 255).astype(np.uint8).squeeze(), mode='L')
        image.save("uploaded_image.png")
        # np.save("uploaded_image.npy", image_array)

        # Make a prediction
        predictions = model.predict(image_array)
        predicted_class = np.argmax(predictions, axis=1)
        print(f"Predicted class: {predicted_class[0]}, Confidence: {np.max(predictions)}")
        return {
            "class": int(predicted_class[0]), 
            "confidence": float(np.max(predictions)), 
            "predictions": predictions.tolist()
        }
    except Exception as e:
        return {"error": str(e)}

# To run the app, use the command: uvicorn model:app --reload
# Running on localhost:8000

