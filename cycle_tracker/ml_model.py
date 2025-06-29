"""
ml_model.py

Provides utility functions for loading the trained CycleAware ML model and
predicting menstrual phases based on athlete features.

Workflow:
    - Loads scaler, PCA, and classifier objects from a pickled .pkl file.
    - Uses these for preprocessing and predicting the menstrual phase.
"""

import pickle  # (kept if needed for future use)
import numpy as np
import joblib

# Load the trained scaler, PCA, and classifier objects
# Ensure path uses forward slashes or raw strings for cross-platform compatibility
scaler, pca, clf = joblib.load(r"cycle_tracker/cycleaware_model.pkl").values()

def predict_phase(features):
    """
    Predicts the menstrual phase given input athlete features.

    Args:
        features (list or np.ndarray): List or 1D array of numerical features
                                       for prediction. Must match model expectations.

    Returns:
        int: Predicted menstrual phase encoded as an integer label.
    """
    features = np.array(features).reshape(1, -1)  # Ensure features are 2D for model
    features_scaled = scaler.transform(features)  # Apply the same scaling as during training
    features_pca = pca.transform(features_scaled)  # Reduce dimensions for classifier
    
    return int(clf.predict(features_pca)[0])  # Return predicted phase as integer
