"""
DeepFace Emotion Analysis Service
Analyzes facial expressions and emotions from video frames
"""

import cv2
import numpy as np
from deepface import DeepFace
import os
import tempfile
from typing import Dict, List, Tuple
import asyncio
import json

class EmotionAnalysisService:
    def __init__(self):
        self.confidence_emotions = ["happy", "neutral"]
        self.nervous_emotions = ["fear", "surprise", "sad"]
        self.stressed_emotions = ["angry", "disgust"]
        
        # Initialize DeepFace (this will download models if needed)
        try:
            # Test DeepFace with a dummy image to ensure models are loaded
            dummy_img = np.zeros((224, 224, 3), dtype=np.uint8)
            DeepFace.analyze(dummy_img, actions=['emotion'], enforce_detection=False)
        except Exception as e:
            print(f"DeepFace initialization warning: {e}")
    
    async def analyze_video(self, video_path: str, sample_rate: int = 2) -> Dict:
        """
        Analyze emotions from video frames
        
        Args:
            video_path: Path to the video file
            sample_rate: Analyze every Nth frame (default: 2)
            
        Returns:
            Dict containing emotion analysis results
        """
        try:
            # Open video file
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            emotions_timeline = []
            face_detected_frames = 0
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Sample frames based on sample_rate
                if frame_count % sample_rate == 0:
                    timestamp = frame_count / fps if fps > 0 else 0
                    
                    try:
                        # Analyze frame for emotions
                        result = DeepFace.analyze(
                            frame, 
                            actions=['emotion'], 
                            enforce_detection=False,
                            silent=True
                        )
                        
                        # Handle both single face and multiple faces
                        if isinstance(result, list):
                            result = result[0] if result else {}
                        
                        if result and 'emotion' in result:
                            face_detected_frames += 1
                            emotions = result['emotion']
                            dominant_emotion = result.get('dominant_emotion', 'neutral')
                            
                            emotions_timeline.append({
                                "timestamp": timestamp,
                                "emotions": emotions,
                                "dominant_emotion": dominant_emotion,
                                "frame_number": frame_count
                            })
                    
                    except Exception as e:
                        # Frame analysis failed, continue with next frame
                        emotions_timeline.append({
                            "timestamp": timestamp,
                            "emotions": {},
                            "dominant_emotion": "unknown",
                            "frame_number": frame_count,
                            "error": str(e)
                        })
                
                frame_count += 1
            
            cap.release()
            
            # Calculate overall metrics
            metrics = self._calculate_emotion_metrics(emotions_timeline, duration)
            
            return {
                "duration": duration,
                "total_frames": total_frames,
                "analyzed_frames": len(emotions_timeline),
                "face_detected_frames": face_detected_frames,
                "face_detection_rate": face_detected_frames / len(emotions_timeline) if emotions_timeline else 0,
                "emotions_timeline": emotions_timeline,
                "metrics": metrics
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "duration": 0,
                "total_frames": 0,
                "analyzed_frames": 0,
                "face_detected_frames": 0,
                "face_detection_rate": 0,
                "emotions_timeline": [],
                "metrics": {}
            }
    
    def _calculate_emotion_metrics(self, emotions_timeline: List[Dict], duration: float) -> Dict:
        """Calculate overall emotion metrics from timeline"""
        if not emotions_timeline:
            return {
                "confidence_score": 0,
                "nervousness_score": 0,
                "stress_score": 0,
                "eye_contact_percentage": 0,
                "emotion_consistency": 0,
                "dominant_emotions": {}
            }
        
        # Filter out frames with errors or no emotions
        valid_frames = [frame for frame in emotions_timeline 
                       if frame.get("emotions") and "error" not in frame]
        
        if not valid_frames:
            return {
                "confidence_score": 0,
                "nervousness_score": 0,
                "stress_score": 0,
                "eye_contact_percentage": 0,
                "emotion_consistency": 0,
                "dominant_emotions": {}
            }
        
        # Calculate emotion scores
        confidence_scores = []
        nervousness_scores = []
        stress_scores = []
        dominant_emotion_counts = {}
        
        for frame in valid_frames:
            emotions = frame["emotions"]
            dominant = frame["dominant_emotion"]
            
            # Count dominant emotions
            dominant_emotion_counts[dominant] = dominant_emotion_counts.get(dominant, 0) + 1
            
            # Calculate confidence (happy + neutral emotions)
            confidence = sum(emotions.get(emotion, 0) for emotion in self.confidence_emotions)
            confidence_scores.append(confidence)
            
            # Calculate nervousness (fear + surprise + sad)
            nervousness = sum(emotions.get(emotion, 0) for emotion in self.nervous_emotions)
            nervousness_scores.append(nervousness)
            
            # Calculate stress (angry + disgust)
            stress = sum(emotions.get(emotion, 0) for emotion in self.stressed_emotions)
            stress_scores.append(stress)
        
        # Calculate averages
        avg_confidence = np.mean(confidence_scores) if confidence_scores else 0
        avg_nervousness = np.mean(nervousness_scores) if nervousness_scores else 0
        avg_stress = np.mean(stress_scores) if stress_scores else 0
        
        # Estimate eye contact (based on face detection consistency)
        face_detection_rate = len(valid_frames) / len(emotions_timeline)
        eye_contact_percentage = face_detection_rate * 100
        
        # Calculate emotion consistency (lower variance = more consistent)
        emotion_variance = np.var(confidence_scores) if len(confidence_scores) > 1 else 0
        emotion_consistency = max(0, 100 - emotion_variance)
        
        # Convert counts to percentages
        total_valid_frames = len(valid_frames)
        dominant_emotions_percentage = {
            emotion: (count / total_valid_frames * 100) 
            for emotion, count in dominant_emotion_counts.items()
        }
        
        return {
            "confidence_score": float(avg_confidence),
            "nervousness_score": float(avg_nervousness),
            "stress_score": float(avg_stress),
            "eye_contact_percentage": float(eye_contact_percentage),
            "emotion_consistency": float(emotion_consistency),
            "dominant_emotions": dominant_emotions_percentage,
            "total_valid_frames": total_valid_frames
        }
    
    def get_emotion_summary(self, emotion_data: Dict) -> Dict:
        """Get a human-readable summary of emotion analysis"""
        metrics = emotion_data.get("metrics", {})
        
        # Determine overall emotional state
        confidence = metrics.get("confidence_score", 0)
        nervousness = metrics.get("nervousness_score", 0)
        stress = metrics.get("stress_score", 0)
        
        if confidence > 60:
            overall_state = "confident"
        elif nervousness > 40:
            overall_state = "nervous"
        elif stress > 30:
            overall_state = "stressed"
        else:
            overall_state = "neutral"
        
        # Eye contact assessment
        eye_contact = metrics.get("eye_contact_percentage", 0)
        if eye_contact > 80:
            eye_contact_level = "excellent"
        elif eye_contact > 60:
            eye_contact_level = "good"
        elif eye_contact > 40:
            eye_contact_level = "moderate"
        else:
            eye_contact_level = "poor"
        
        return {
            "overall_emotional_state": overall_state,
            "eye_contact_level": eye_contact_level,
            "face_detection_rate": emotion_data.get("face_detection_rate", 0),
            "analysis_duration": emotion_data.get("duration", 0),
            "key_insights": self._generate_insights(metrics)
        }
    
    def _generate_insights(self, metrics: Dict) -> List[str]:
        """Generate actionable insights from emotion metrics"""
        insights = []
        
        confidence = metrics.get("confidence_score", 0)
        nervousness = metrics.get("nervousness_score", 0)
        stress = metrics.get("stress_score", 0)
        eye_contact = metrics.get("eye_contact_percentage", 0)
        consistency = metrics.get("emotion_consistency", 0)
        
        if confidence < 40:
            insights.append("Work on projecting more confidence through facial expressions")
        
        if nervousness > 30:
            insights.append("Practice relaxation techniques to reduce visible nervousness")
        
        if stress > 25:
            insights.append("Focus on stress management before interviews")
        
        if eye_contact < 60:
            insights.append("Improve eye contact by looking directly at the camera")
        
        if consistency < 70:
            insights.append("Work on maintaining consistent emotional expression")
        
        if not insights:
            insights.append("Great emotional control and presence!")
        
        return insights