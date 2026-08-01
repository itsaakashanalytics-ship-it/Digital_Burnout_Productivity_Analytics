"""
ML model management module
Handles loading, caching, and making predictions with trained models
"""

import streamlit as st
import pickle
import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Tuple, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelManager:
    """Manages ML model loading and predictions"""
    
    def __init__(self, models_dir: str = "./models"):
        """Initialize model manager"""
        self.models_dir = Path(models_dir)
        self.burnout_model = None
        self.productivity_model = None
        self.model_metadata = {}
    
    @st.cache_resource
    def load_models(self):
        """Load pickled models from disk"""
        try:
            burnout_path = self.models_dir / "logistic_burnout_model.pkl"
            productivity_path = self.models_dir / "linear_productivity_model.pkl"
            
            if burnout_path.exists():
                with open(burnout_path, 'rb') as f:
                    self.burnout_model = pickle.load(f)
                logger.info("Burnout model loaded successfully")
            else:
                logger.warning(f"Burnout model not found at {burnout_path}")
            
            if productivity_path.exists():
                with open(productivity_path, 'rb') as f:
                    self.productivity_model = pickle.load(f)
                logger.info("Productivity model loaded successfully")
            else:
                logger.warning(f"Productivity model not found at {productivity_path}")
            
            return self.burnout_model is not None and self.productivity_model is not None
        
        except Exception as e:
            logger.error(f"Failed to load models: {str(e)}")
            return False
    
    def predict_burnout_risk(self, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict burnout risk probability
        Returns: (predictions, probabilities)
        """
        try:
            if self.burnout_model is None:
                raise ValueError("Burnout model not loaded")
            
            predictions = self.burnout_model.predict(X)
            probabilities = self.burnout_model.predict_proba(X)[:, 1]
            
            return predictions, probabilities
        except Exception as e:
            logger.error(f"Burnout prediction failed: {str(e)}")
            raise
    
    def predict_productivity_score(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict productivity score
        Returns: predicted scores (0-100)
        """
        try:
            if self.productivity_model is None:
                raise ValueError("Productivity model not loaded")
            
            predictions = self.productivity_model.predict(X)
            # Clip to valid range [0, 100]
            predictions = np.clip(predictions, 0, 100)
            
            return predictions
        except Exception as e:
            logger.error(f"Productivity prediction failed: {str(e)}")
            raise
    
    def get_model_info(self) -> dict:
        """Get metadata about loaded models"""
        info = {
            "burnout_model_loaded": self.burnout_model is not None,
            "productivity_model_loaded": self.productivity_model is not None,
            "burnout_model_type": type(self.burnout_model).__name__ if self.burnout_model else "Not loaded",
            "productivity_model_type": type(self.productivity_model).__name__ if self.productivity_model else "Not loaded"
        }
        return info

@st.cache_resource
def initialize_models(models_dir: str = "./models") -> ModelManager:
    """Initialize and cache model manager"""
    manager = ModelManager(models_dir)
    manager.load_models()
    return manager

def get_burnout_risk_category(risk_score: float) -> str:
    """Categorize burnout risk score"""
    if risk_score >= 80:
        return "Critical"
    elif risk_score >= 60:
        return "High"
    elif risk_score >= 40:
        return "Medium"
    else:
        return "Low"

def get_productivity_category(score: float) -> str:
    """Categorize productivity score"""
    if score >= 80:
        return "High"
    elif score >= 60:
        return "Medium"
    else:
        return "Low"

def format_prediction_result(burnout_score: float, productivity_score: float) -> dict:
    """Format prediction results for display"""
    return {
        "burnout_risk_score": round(burnout_score, 2),
        "burnout_category": get_burnout_risk_category(burnout_score),
        "productivity_score": round(productivity_score, 2),
        "productivity_category": get_productivity_category(productivity_score),
        "risk_level": "⚠️ High Risk" if burnout_score >= 60 else "✅ Acceptable",
        "productivity_level": "⭐ High" if productivity_score >= 80 else "⚠️ Moderate" if productivity_score >= 60 else "❌ Low"
    }

# Feature importance from training
FEATURE_IMPORTANCE = {
    "burnout": {
        "Daily Screen Time": -0.32,
        "Burnout Risk": -0.48,
        "Deep Work Hours": 0.52,
        "Focus Sessions": 0.45,
        "Stress Level": -0.40,
        "Sleep Hours": 0.38,
        "Distraction Frequency": -0.35,
        "Motivation Level": 0.42,
    },
    "productivity": {
        "Deep Work Hours": 0.52,
        "Focus Sessions": 0.45,
        "Burnout Risk": -0.48,
        "Daily Screen Time": -0.32,
        "Distraction Frequency": -0.35,
        "Motivation Level": 0.42,
        "Sleep Hours": 0.38,
        "App Switch Frequency": -0.32,
    }
}

def get_improvement_recommendations(burnout_score: float, productivity_score: float) -> list:
    """Generate personalized recommendations based on scores"""
    recommendations = []
    
    if burnout_score >= 70:
        recommendations.append({
            "priority": "🔴 High",
            "action": "Reduce Daily Screen Time",
            "detail": "Implement 50-minute work blocks with 10-minute breaks"
        })
        recommendations.append({
            "priority": "🔴 High",
            "action": "Schedule Recovery Time",
            "detail": "Block out 2 hours weekly for personal recovery and wellness"
        })
    
    if productivity_score < 60:
        recommendations.append({
            "priority": "🟡 Medium",
            "action": "Increase Deep Work Hours",
            "detail": "Schedule 2-3 focus sessions (90 min each) daily without interruptions"
        })
        recommendations.append({
            "priority": "🟡 Medium",
            "action": "Reduce Context Switching",
            "detail": "Batch similar tasks and limit app switching to focused periods"
        })
    
    if burnout_score >= 70 and productivity_score >= 80:
        recommendations.append({
            "priority": "🟡 Medium",
            "action": "Sustain Balance",
            "detail": "Maintain current schedules while monitoring burnout signals"
        })
    
    if burnout_score < 50 and productivity_score >= 80:
        recommendations.append({
            "priority": "🟢 Low",
            "action": "Maintain Current Pattern",
            "detail": "Current work-life balance is working well - continue current approach"
        })
    
    return recommendations[:3]  # Return top 3 recommendations
