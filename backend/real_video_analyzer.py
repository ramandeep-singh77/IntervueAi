"""
Real Video Analysis Module
Analyzes actual video recordings for face detection, eye contact, and basic emotion indicators
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple
import os

class RealVideoAnalyzer:
    def __init__(self):
        # Load OpenCV face detection models
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
    def analyze_video_file(self, video_file_path: str) -> Dict:
        """
        Analyze actual video file for face detection and eye contact
        
        Args:
            video_file_path: Path to the video file
            
        Returns:
            Dict containing real video analysis results
        """
        try:
            # Open video file
            cap = cv2.VideoCapture(video_file_path)
            
            if not cap.isOpened():
                return self._empty_analysis()
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            # Analysis variables
            frames_analyzed = 0
            frames_with_face = 0
            frames_with_eyes = 0
            face_positions = []
            face_sizes = []
            
            # Sample every 5th frame for performance
            frame_skip = 5
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Skip frames for performance
                if frame_count % frame_skip != 0:
                    continue
                
                frames_analyzed += 1
                
                # Analyze this frame
                face_data = self._analyze_frame(frame)
                
                if face_data["has_face"]:
                    frames_with_face += 1
                    face_positions.append(face_data["face_center"])
                    face_sizes.append(face_data["face_size"])
                    
                    if face_data["has_eyes"]:
                        frames_with_eyes += 1
            
            cap.release()
            
            # Calculate metrics
            face_detection_rate = (frames_with_face / frames_analyzed * 100) if frames_analyzed > 0 else 0
            eye_contact_percentage = (frames_with_eyes / frames_analyzed * 100) if frames_analyzed > 0 else 0
            
            # Analyze face position consistency (stability)
            position_stability = self._calculate_position_stability(face_positions)
            
            # Analyze face size consistency (distance from camera)
            size_consistency = self._calculate_size_consistency(face_sizes)
            
            return {
                "duration": duration,
                "total_frames": total_frames,
                "frames_analyzed": frames_analyzed,
                "frames_with_face": frames_with_face,
                "frames_with_eyes": frames_with_eyes,
                "face_detection_rate": face_detection_rate,
                "eye_contact_percentage": eye_contact_percentage,
                "position_stability": position_stability,
                "size_consistency": size_consistency,
                "has_face": face_detection_rate > 10.0,  # At least 10% face detection
                "metrics": {
                    "confidence_score": self._calculate_confidence_score(face_detection_rate, eye_contact_percentage, position_stability),
                    "nervousness_score": self._calculate_nervousness_score(position_stability, size_consistency),
                    "eye_contact_percentage": eye_contact_percentage,
                    "face_detection_rate": face_detection_rate
                }
            }
            
        except Exception as e:
            print(f"Video analysis error: {str(e)}")
            return self._empty_analysis()
    
    def _analyze_frame(self, frame: np.ndarray) -> Dict:
        """Analyze a single frame for face and eye detection"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                return {
                    "has_face": False,
                    "has_eyes": False,
                    "face_center": None,
                    "face_size": 0
                }
            
            # Use the largest face (closest to camera)
            largest_face = max(faces, key=lambda f: f[2] * f[3])
            x, y, w, h = largest_face
            
            # Calculate face center and size
            face_center = (x + w//2, y + h//2)
            face_size = w * h
            
            # Extract face region for eye detection
            face_roi = gray[y:y+h, x:x+w]
            
            # Detect eyes in face region
            eyes = self.eye_cascade.detectMultiScale(face_roi, 1.1, 3)
            has_eyes = len(eyes) >= 2  # Need at least 2 eyes for good eye contact
            
            return {
                "has_face": True,
                "has_eyes": has_eyes,
                "face_center": face_center,
                "face_size": face_size
            }
            
        except Exception as e:
            print(f"Frame analysis error: {str(e)}")
            return {
                "has_face": False,
                "has_eyes": False,
                "face_center": None,
                "face_size": 0
            }
    
    def _calculate_position_stability(self, face_positions: List[Tuple]) -> float:
        """Calculate how stable the face position is (less movement = more confident)"""
        if len(face_positions) < 2:
            return 0.0
        
        try:
            # Calculate movement between consecutive frames
            movements = []
            for i in range(1, len(face_positions)):
                prev_pos = face_positions[i-1]
                curr_pos = face_positions[i]
                
                # Calculate Euclidean distance
                movement = np.sqrt((curr_pos[0] - prev_pos[0])**2 + (curr_pos[1] - prev_pos[1])**2)
                movements.append(movement)
            
            # Lower average movement = higher stability
            avg_movement = np.mean(movements)
            
            # Convert to 0-100 scale (lower movement = higher score)
            stability = max(0, 100 - (avg_movement / 10))  # Normalize by dividing by 10
            
            return float(stability)
            
        except Exception as e:
            print(f"Position stability calculation error: {str(e)}")
            return 0.0
    
    def _calculate_size_consistency(self, face_sizes: List[float]) -> float:
        """Calculate how consistent the face size is (consistent distance from camera)"""
        if len(face_sizes) < 2:
            return 0.0
        
        try:
            # Calculate coefficient of variation
            mean_size = np.mean(face_sizes)
            std_size = np.std(face_sizes)
            
            if mean_size == 0:
                return 0.0
            
            cv = std_size / mean_size
            
            # Convert to 0-100 scale (lower variation = higher consistency)
            consistency = max(0, 100 - (cv * 100))
            
            return float(consistency)
            
        except Exception as e:
            print(f"Size consistency calculation error: {str(e)}")
            return 0.0
    
    def _calculate_confidence_score(self, face_detection_rate: float, eye_contact_percentage: float, position_stability: float) -> float:
        """Calculate overall confidence score based on video metrics"""
        # Weighted combination of factors
        confidence = (
            face_detection_rate * 0.3 +  # 30% - being visible
            eye_contact_percentage * 0.5 +  # 50% - eye contact
            position_stability * 0.2  # 20% - stability
        )
        
        return float(min(100, max(0, confidence)))
    
    def _calculate_nervousness_score(self, position_stability: float, size_consistency: float) -> float:
        """Calculate nervousness score based on movement and inconsistency"""
        # Higher movement and inconsistency = higher nervousness
        nervousness = (
            (100 - position_stability) * 0.6 +  # 60% - movement
            (100 - size_consistency) * 0.4  # 40% - distance changes
        )
        
        return float(min(100, max(0, nervousness)))
    
    def _empty_analysis(self) -> Dict:
        """Return empty analysis result"""
        return {
            "duration": 0,
            "total_frames": 0,
            "frames_analyzed": 0,
            "frames_with_face": 0,
            "frames_with_eyes": 0,
            "face_detection_rate": 0,
            "eye_contact_percentage": 0,
            "position_stability": 0,
            "size_consistency": 0,
            "has_face": False,
            "metrics": {
                "confidence_score": 0,
                "nervousness_score": 0,
                "eye_contact_percentage": 0,
                "face_detection_rate": 0
            }
        }