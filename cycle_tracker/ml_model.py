import pickle
import numpy as np
import joblib


# Save the trained objects correctly

# Load the ML model properly

scaler, pca, clf = joblib.load("cycle_tracker\cycleaware_model.pkl").values() # This should work now

#

def predict_phase(features):
    """
    Takes input features as a list and returns the predicted phase.
    """
    features = np.array(features).reshape(1, -1)  # Ensure correct shape
    features_scaled = scaler.transform(features)
    features_pca = pca.transform(features_scaled)
    
    return int(clf.predict(features_pca)[0])  # Return the phase prediction