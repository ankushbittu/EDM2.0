import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load the pre-trained model
model_path = "C:/Users/HP BITTU/Downloads/final_model.keras"
model = load_model(model_path)

# Load Haar Cascade for face detection
face_cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(face_cascade_path)

# Preprocess the image (resize, convert to grayscale, normalize)
def detect_emotion(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image using Haar Cascade
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5)

    emotions = []

    # If faces are found, loop over each face and make predictions
    for (x, y, w, h) in faces:
        # Extract the region of interest (the face)
        face = gray_image[y:y+h, x:x+w]

        # Resize the face to 48x48 (or the required size)
        resized_face = cv2.resize(face, (48, 48))

        # Normalize pixel values to be between 0 and 1
        normalized_face = resized_face / 255.0

        # Add an extra dimension to match the expected input shape (batch size, height, width, channels)
        face_array = np.expand_dims(normalized_face, axis=0)  # Add batch dimension
        face_array = np.expand_dims(face_array, axis=-1)  # Add channel dimension for grayscale

        # Make predictions on the face
        predictions = model.predict(face_array)

        # Convert each probability to percentage
        percentages = predictions * 100

        # Define the emotion labels (assuming the model is trained on FER-2013 or a similar dataset)
        emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

        # Print prediction percentages for each emotion
        print("Prediction percentages for the detected face:")
        for i, emotion in enumerate(emotion_labels):
            print(f"{emotion}: {percentages[0][i]:.2f}%")

        # Find the emotion with the highest probability
        predicted_emotion_index = np.argmax(predictions)
        predicted_emotion = emotion_labels[predicted_emotion_index]

        # Print the predicted emotion
        
    return predicted_emotion

