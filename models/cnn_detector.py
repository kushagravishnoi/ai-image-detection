"""
Custom CNN Model for Image Detection
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

class CNNDetector:
    """
    Custom Convolutional Neural Network for detecting AI-generated images
    """
    
    def __init__(self, input_shape=(224, 224, 3)):
        """
        Initialize CNN detector
        
        Args:
            input_shape: Input image shape (height, width, channels)
        """
        self.input_shape = input_shape
        self.model = None
    
    def build_model(self):
        """
        Build CNN model architecture
        """
        model = keras.Sequential([
            # Block 1
            layers.Conv2D(32, (3, 3), activation='relu', padding='same', 
                         input_shape=self.input_shape, name='conv1_1'),
            layers.Conv2D(32, (3, 3), activation='relu', padding='same', name='conv1_2'),
            layers.MaxPooling2D((2, 2), name='pool1'),
            layers.Dropout(0.25),
            
            # Block 2
            layers.Conv2D(64, (3, 3), activation='relu', padding='same', name='conv2_1'),
            layers.Conv2D(64, (3, 3), activation='relu', padding='same', name='conv2_2'),
            layers.MaxPooling2D((2, 2), name='pool2'),
            layers.Dropout(0.25),
            
            # Block 3
            layers.Conv2D(128, (3, 3), activation='relu', padding='same', name='conv3_1'),
            layers.Conv2D(128, (3, 3), activation='relu', padding='same', name='conv3_2'),
            layers.MaxPooling2D((2, 2), name='pool3'),
            layers.Dropout(0.25),
            
            # Block 4
            layers.Conv2D(256, (3, 3), activation='relu', padding='same', name='conv4_1'),
            layers.Conv2D(256, (3, 3), activation='relu', padding='same', name='conv4_2'),
            layers.MaxPooling2D((2, 2), name='pool4'),
            layers.Dropout(0.25),
            
            # Flatten and Dense
            layers.Flatten(),
            layers.Dense(512, activation='relu', name='fc1'),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu', name='fc2'),
            layers.Dropout(0.5),
            
            # Output layer (Binary classification)
            layers.Dense(1, activation='sigmoid', name='output')
        ])
        
        self.model = model
        return model
    
    def compile_model(self, learning_rate=0.001):
        """
        Compile the model
        """
        optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
        self.model.compile(
            optimizer=optimizer,
            loss='binary_crossentropy',
            metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
        )
    
    def predict(self, image):
        """
        Predict if image is real or fake
        
        Args:
            image: Input image (numpy array)
        
        Returns:
            Confidence score (0-1) and prediction (0=real, 1=fake)
        """
        if self.model is None:
            raise ValueError('Model not built. Call build_model() first.')
        
        # Expand dims if single image
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)
        
        prediction = self.model.predict(image, verbose=0)
        return prediction[0][0]
    
    def get_summary(self):
        """
        Get model summary
        """
        if self.model is None:
            raise ValueError('Model not built. Call build_model() first.')
        return self.model.summary()
