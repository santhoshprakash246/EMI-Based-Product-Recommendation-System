"""
Deep Learning Model Implementations for EMI Affordability System
Multi-Task Neural Network, TabNet, and Hybrid approaches
"""

import tensorflow as tf
from tensorflow.keras import layers, Model, callbacks
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

# ============================================
# 1. MULTI-TASK DENSE NEURAL NETWORK
# ============================================

class MultiTaskAffordabilityNN:
    """
    Dense neural network for simultaneous classification (risk level)
    and regression (affordability score) prediction
    """
    
    def __init__(self, input_dim=25, seed=42):
        """Initialize the multi-task model"""
        self.input_dim = input_dim
        self.model = None
        self.scaler = StandardScaler()
        tf.random.set_seed(seed)
        
    def build_model(self):
        """
        Build multi-task learning architecture
        
        Returns:
            Model: Keras functional model
        """
        # Input layer
        inputs = layers.Input(shape=(self.input_dim,), name='input')
        
        # Shared embedding and normalization
        x = layers.Dense(128, activation='relu', name='dense_1')(inputs)
        x = layers.BatchNormalization(name='bn_1')(x)
        x = layers.Dropout(0.3, name='dropout_1')(x)
        
        # Shared hidden layers
        x = layers.Dense(64, activation='relu', name='dense_2')(x)
        x = layers.BatchNormalization(name='bn_2')(x)
        x = layers.Dropout(0.3, name='dropout_2')(x)
        
        x = layers.Dense(32, activation='relu', name='dense_3')(x)
        x = layers.BatchNormalization(name='bn_3')(x)
        x = layers.Dropout(0.2, name='dropout_3')(x)
        
        # Task 1: Classification (Risk Level)
        classification = layers.Dense(16, activation='relu', name='class_dense_1')(x)
        classification = layers.Dropout(0.2)(classification)
        classification_output = layers.Dense(
            3, 
            activation='softmax', 
            name='risk_level'
        )(classification)
        
        # Task 2: Regression (Affordability Score)
        regression = layers.Dense(16, activation='relu', name='reg_dense_1')(x)
        regression = layers.Dropout(0.2)(regression)
        regression_output = layers.Dense(
            1, 
            activation='sigmoid', 
            name='affordability_score'
        )(regression)
        
        # Create model
        model = Model(inputs=inputs, outputs=[classification_output, regression_output])
        
        return model
    
    def compile_model(self, learning_rate=0.001):
        """
        Compile the model
        
        Args:
            learning_rate (float): Learning rate for optimizer
        """
        self.model = self.build_model()
        
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
            loss={
                'risk_level': 'categorical_crossentropy',
                'affordability_score': 'mse'
            },
            loss_weights={
                'risk_level': 1.0,
                'affordability_score': 0.8
            },
            metrics={
                'risk_level': ['accuracy'],
                'affordability_score': ['mae', 'mse']
            }
        )
        
        print("✓ Model compiled successfully")
        print(self.model.summary())
    
    def train(self, X_train, y_class_train, y_reg_train, 
              X_val=None, y_class_val=None, y_reg_val=None,
              epochs=50, batch_size=32, verbose=1):
        """
        Train the model
        
        Args:
            X_train: Training features
            y_class_train: Classification targets (one-hot encoded)
            y_reg_train: Regression targets
            X_val: Validation features (optional)
            y_class_val: Validation classification targets
            y_reg_val: Validation regression targets
            epochs: Number of training epochs
            batch_size: Batch size
            verbose: Verbosity level
        
        Returns:
            history: Training history
        """
        # Prepare validation data
        validation_data = None
        if X_val is not None and y_class_val is not None and y_reg_val is not None:
            validation_data = (
                X_val,
                {'risk_level': y_class_val, 'affordability_score': y_reg_val}
            )
        
        # Callbacks
        early_stopping = callbacks.EarlyStopping(
            monitor='val_loss',
            patience=15,
            restore_best_weights=True,
            verbose=1
        )
        
        reduce_lr = callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6,
            verbose=1
        )
        
        # Train
        history = self.model.fit(
            X_train,
            {
                'risk_level': y_class_train,
                'affordability_score': y_reg_train
            },
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, reduce_lr],
            verbose=verbose
        )
        
        return history
    
    def predict(self, X):
        """
        Make predictions
        
        Args:
            X: Input features
        
        Returns:
            tuple: (risk_predictions, affordability_scores)
        """
        predictions = self.model.predict(X)
        risk_pred = predictions[0]
        affordability_pred = predictions[1]
        
        return risk_pred, affordability_pred
    
    def get_model(self):
        """Return the compiled model"""
        return self.model
    
    def save(self, filepath):
        """Save model weights"""
        self.model.save_weights(filepath)
        print(f"✓ Model saved to {filepath}")
    
    def load(self, filepath):
        """Load model weights"""
        if self.model is None:
            self.compile_model()
        self.model.load_weights(filepath)
        print(f"✓ Model loaded from {filepath}")


# ============================================
# 2. AUTOENCODER FOR FEATURE EXTRACTION
# ============================================

class FeatureExtractorAutoencoder:
    """
    Autoencoder for learning compressed feature representations
    Can be used with XGBoost or other models
    """
    
    def __init__(self, input_dim=25, encoding_dim=16, seed=42):
        """Initialize autoencoder"""
        self.input_dim = input_dim
        self.encoding_dim = encoding_dim
        self.autoencoder = None
        self.encoder = None
        tf.random.set_seed(seed)
    
    def build_model(self):
        """Build autoencoder architecture"""
        inputs = layers.Input(shape=(self.input_dim,))
        
        # Encoder
        encoded = layers.Dense(64, activation='relu')(inputs)
        encoded = layers.BatchNormalization()(encoded)
        encoded = layers.Dropout(0.2)(encoded)
        
        encoded = layers.Dense(32, activation='relu')(encoded)
        encoded = layers.BatchNormalization()(encoded)
        encoded = layers.Dropout(0.2)(encoded)
        
        encoded = layers.Dense(self.encoding_dim, activation='relu', name='encoding')(encoded)
        
        # Decoder
        decoded = layers.Dense(32, activation='relu')(encoded)
        decoded = layers.BatchNormalization()(decoded)
        decoded = layers.Dropout(0.2)(decoded)
        
        decoded = layers.Dense(64, activation='relu')(decoded)
        decoded = layers.BatchNormalization()(decoded)
        decoded = layers.Dropout(0.2)(decoded)
        
        decoded = layers.Dense(self.input_dim, activation='sigmoid')(decoded)
        
        # Full autoencoder
        self.autoencoder = Model(inputs, decoded)
        self.autoencoder.compile(optimizer='adam', loss='mse')
        
        # Encoder only
        self.encoder = Model(inputs, encoded)
        
        return self.autoencoder, self.encoder
    
    def train(self, X_train, X_val=None, epochs=50, batch_size=32, verbose=1):
        """Train autoencoder"""
        if self.autoencoder is None:
            self.build_model()
        
        history = self.autoencoder.fit(
            X_train, X_train,
            validation_data=(X_val, X_val) if X_val is not None else None,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[
                callbacks.EarlyStopping(monitor='loss', patience=10),
                callbacks.ReduceLROnPlateau(factor=0.5, patience=5)
            ],
            verbose=verbose
        )
        
        return history
    
    def extract_features(self, X):
        """Extract compressed features using encoder"""
        return self.encoder.predict(X)
    
    def save(self, filepath):
        """Save encoder"""
        self.encoder.save(filepath)
        print(f"✓ Encoder saved to {filepath}")
    
    def load(self, filepath):
        """Load encoder"""
        self.encoder = tf.keras.models.load_model(filepath)
        print(f"✓ Encoder loaded from {filepath}")


# ============================================
# 3. LSTM FOR TEMPORAL AFFORDABILITY
# ============================================

class TemporalAffordabilityLSTM:
    """
    LSTM model for predicting affordability based on transaction history
    Useful if you have sequential EMI transaction data
    """
    
    def __init__(self, input_dim=25, sequence_length=12, seed=42):
        """Initialize LSTM model"""
        self.input_dim = input_dim
        self.sequence_length = sequence_length
        self.model = None
        tf.random.set_seed(seed)
    
    def build_model(self):
        """Build LSTM architecture"""
        model = tf.keras.Sequential([
            layers.LSTM(64, activation='relu', return_sequences=True, 
                       input_shape=(self.sequence_length, self.input_dim)),
            layers.Dropout(0.2),
            
            layers.LSTM(32, activation='relu', return_sequences=True),
            layers.Dropout(0.2),
            
            layers.LSTM(16, activation='relu'),
            layers.Dropout(0.2),
            
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            
            layers.Dense(16, activation='relu'),
            
            # Multi-output
            layers.Dense(3, activation='softmax', name='risk_level'),  # Classification
            layers.Dense(1, activation='sigmoid', name='affordability_score')  # Regression
        ])
        
        return model
    
    def compile_model(self):
        """Compile LSTM model"""
        self.model = self.build_model()
        self.model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        return self.model
    
    def train(self, X_train, y_train, epochs=50, batch_size=32, verbose=1):
        """Train LSTM"""
        if self.model is None:
            self.compile_model()
        
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[
                callbacks.EarlyStopping(patience=10),
                callbacks.ReduceLROnPlateau(factor=0.5, patience=5)
            ],
            verbose=verbose
        )
        
        return history


# ============================================
# USAGE EXAMPLE
# ============================================

if __name__ == "__main__":
    # Example 1: Multi-Task NN
    print("=" * 60)
    print("Example 1: Multi-Task Neural Network")
    print("=" * 60)
    
    # Create sample data
    X_train = np.random.randn(400, 25)
    y_class_train = np.random.randint(0, 3, 400)
    y_reg_train = np.random.rand(400)
    
    X_val = np.random.randn(100, 25)
    y_class_val = np.random.randint(0, 3, 100)
    y_reg_val = np.random.rand(100)
    
    # Convert classification to one-hot
    y_class_train_onehot = tf.keras.utils.to_categorical(y_class_train, 3)
    y_class_val_onehot = tf.keras.utils.to_categorical(y_class_val, 3)
    
    # Create and train model
    mtnn = MultiTaskAffordabilityNN(input_dim=25)
    mtnn.compile_model(learning_rate=0.001)
    
    history = mtnn.train(
        X_train, y_class_train_onehot, y_reg_train,
        X_val, y_class_val_onehot, y_reg_val,
        epochs=20, batch_size=32
    )
    
    # Predict
    risk_pred, aff_pred = mtnn.predict(X_val)
    print(f"\nPredicted risk levels: {risk_pred[0]}")
    print(f"Predicted affordability: {aff_pred[0]}")
    
    # Example 2: Autoencoder
    print("\n" + "=" * 60)
    print("Example 2: Feature Extraction Autoencoder")
    print("=" * 60)
    
    ae = FeatureExtractorAutoencoder(input_dim=25, encoding_dim=16)
    ae.build_model()
    
    ae.train(X_train, X_val, epochs=20, batch_size=32)
    
    # Extract features
    features = ae.extract_features(X_train)
    print(f"Original shape: {X_train.shape}")
    print(f"Extracted features shape: {features.shape}")
    print("✓ Features can now be used with XGBoost or other models")
