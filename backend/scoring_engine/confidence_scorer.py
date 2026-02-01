"""
Confidence Scoring Engine
Calculates overall confidence score based on multiple factors
"""

import numpy as np
from typing import Dict, List, Optional

class ConfidenceScorer:
    def __init__(self):
        # Scoring weights as specified in requirements
        self.weights = {
            "voice_stability": 0.40,    # 40%
            "eye_contact": 0.25,        # 25%
            "emotion_consistency": 0.20, # 20%
            "filler_word_frequency": 0.15 # 15%
        }
    
    def calculate_score(self, responses: List[Dict]) -> Dict:
        """
        Calculate comprehensive confidence score from interview responses
        
        Args:
            responses: List of response data containing audio, video, and transcript analysis
            
        Returns:
            Dict containing overall score and component breakdowns
        """
        if not responses:
            return self._empty_score_result()
        
        # Extract component scores from all responses
        voice_scores = []
        eye_contact_scores = []
        emotion_scores = []
        filler_word_scores = []
        
        for response in responses:
            # Voice stability score
            voice_metrics = response.get("voice_metrics", {})
            voice_score = self._calculate_voice_stability_score(voice_metrics)
            voice_scores.append(voice_score)
            
            # Eye contact score
            emotion_analysis = response.get("emotion_analysis", {})
            eye_contact_score = self._calculate_eye_contact_score(emotion_analysis)
            eye_contact_scores.append(eye_contact_score)
            
            # Emotion consistency score
            emotion_score = self._calculate_emotion_consistency_score(emotion_analysis)
            emotion_scores.append(emotion_score)
            
            # Filler word frequency score
            transcript_data = response.get("transcript", {})
            filler_score = self._calculate_filler_word_score(transcript_data)
            filler_word_scores.append(filler_score)
        
        # Calculate average scores across all responses
        avg_voice_stability = np.mean(voice_scores) if voice_scores else 0
        avg_eye_contact = np.mean(eye_contact_scores) if eye_contact_scores else 0
        avg_emotion_consistency = np.mean(emotion_scores) if emotion_scores else 0
        avg_filler_word = np.mean(filler_word_scores) if filler_word_scores else 0
        
        # Calculate weighted overall score
        overall_score = (
            avg_voice_stability * self.weights["voice_stability"] +
            avg_eye_contact * self.weights["eye_contact"] +
            avg_emotion_consistency * self.weights["emotion_consistency"] +
            avg_filler_word * self.weights["filler_word_frequency"]
        )
        
        return {
            "overall_score": float(overall_score),
            "component_scores": {
                "voice_stability": {
                    "score": float(avg_voice_stability),
                    "weight": self.weights["voice_stability"],
                    "weighted_contribution": float(avg_voice_stability * self.weights["voice_stability"])
                },
                "eye_contact": {
                    "score": float(avg_eye_contact),
                    "weight": self.weights["eye_contact"],
                    "weighted_contribution": float(avg_eye_contact * self.weights["eye_contact"])
                },
                "emotion_consistency": {
                    "score": float(avg_emotion_consistency),
                    "weight": self.weights["emotion_consistency"],
                    "weighted_contribution": float(avg_emotion_consistency * self.weights["emotion_consistency"])
                },
                "filler_word_frequency": {
                    "score": float(avg_filler_word),
                    "weight": self.weights["filler_word_frequency"],
                    "weighted_contribution": float(avg_filler_word * self.weights["filler_word_frequency"])
                }
            },
            "response_count": len(responses),
            "score_interpretation": self._interpret_score(overall_score)
        }
    
    def _calculate_voice_stability_score(self, voice_metrics: Dict) -> float:
        """Calculate voice stability score from voice analysis"""
        if not voice_metrics:
            return 0.0
        
        # Get stability score from voice analyzer
        stability_score = voice_metrics.get("stability_score", 0)
        clarity_score = voice_metrics.get("clarity_score", 0)
        
        # Combine stability and clarity (stability is more important)
        voice_score = (stability_score * 0.7) + (clarity_score * 0.3)
        
        return min(100.0, max(0.0, voice_score))
    
    def _calculate_eye_contact_score(self, emotion_analysis: Dict) -> float:
        """Calculate eye contact score from emotion analysis"""
        if not emotion_analysis:
            return 0.0
        
        metrics = emotion_analysis.get("metrics", {})
        eye_contact_percentage = metrics.get("eye_contact_percentage", 0)
        
        # Eye contact score is directly the percentage
        return min(100.0, max(0.0, eye_contact_percentage))
    
    def _calculate_emotion_consistency_score(self, emotion_analysis: Dict) -> float:
        """Calculate emotion consistency score"""
        if not emotion_analysis:
            return 0.0
        
        metrics = emotion_analysis.get("metrics", {})
        
        # Get confidence and consistency metrics
        confidence_score = metrics.get("confidence_score", 0)
        emotion_consistency = metrics.get("emotion_consistency", 0)
        nervousness_score = metrics.get("nervousness_score", 0)
        stress_score = metrics.get("stress_score", 0)
        
        # Calculate composite emotion score
        # Higher confidence and consistency = better score
        # Higher nervousness and stress = lower score
        positive_emotions = confidence_score + emotion_consistency
        negative_emotions = nervousness_score + stress_score
        
        # Normalize to 0-100 scale
        emotion_score = max(0, min(100, positive_emotions - (negative_emotions * 0.5)))
        
        return float(emotion_score)
    
    def _calculate_filler_word_score(self, transcript_data: Dict) -> float:
        """Calculate filler word frequency score"""
        if not transcript_data:
            return 100.0  # No transcript = assume no filler words
        
        # Get filler word statistics
        filler_words = transcript_data.get("filler_words", [])
        total_words = transcript_data.get("word_count", 0)
        
        if total_words == 0:
            return 100.0
        
        # Calculate filler word percentage
        filler_percentage = (len(filler_words) / total_words) * 100
        
        # Convert to score (lower filler percentage = higher score)
        # 0% filler words = 100 points
        # 10% filler words = 50 points
        # 20%+ filler words = 0 points
        filler_score = max(0, 100 - (filler_percentage * 5))
        
        return float(filler_score)
    
    def get_detailed_metrics(self, responses: List[Dict]) -> Dict:
        """Get detailed analytics for dashboard display"""
        if not responses:
            return {}
        
        # Aggregate metrics across all responses
        all_voice_metrics = []
        all_emotion_timelines = []
        all_transcript_stats = []
        
        for response in responses:
            voice_metrics = response.get("voice_metrics", {})
            emotion_analysis = response.get("emotion_analysis", {})
            transcript_data = response.get("transcript", {})
            
            if voice_metrics:
                all_voice_metrics.append(voice_metrics)
            
            if emotion_analysis and emotion_analysis.get("emotions_timeline"):
                all_emotion_timelines.extend(emotion_analysis["emotions_timeline"])
            
            if transcript_data:
                all_transcript_stats.append(transcript_data)
        
        # Calculate aggregate statistics
        analytics = {
            "voice_analytics": self._aggregate_voice_metrics(all_voice_metrics),
            "emotion_analytics": self._aggregate_emotion_metrics(all_emotion_timelines),
            "speech_analytics": self._aggregate_speech_metrics(all_transcript_stats),
            "response_count": len(responses)
        }
        
        return analytics
    
    def _aggregate_voice_metrics(self, voice_metrics_list: List[Dict]) -> Dict:
        """Aggregate voice metrics across responses"""
        if not voice_metrics_list:
            return {}
        
        # Extract stability and clarity scores
        stability_scores = [vm.get("stability_score", 0) for vm in voice_metrics_list]
        clarity_scores = [vm.get("clarity_score", 0) for vm in voice_metrics_list]
        
        # Extract pitch analysis
        pitch_stabilities = []
        for vm in voice_metrics_list:
            pitch_analysis = vm.get("pitch_analysis", {})
            if pitch_analysis:
                pitch_stabilities.append(pitch_analysis.get("pitch_stability", 0))
        
        return {
            "average_stability": float(np.mean(stability_scores)) if stability_scores else 0,
            "average_clarity": float(np.mean(clarity_scores)) if clarity_scores else 0,
            "average_pitch_stability": float(np.mean(pitch_stabilities)) if pitch_stabilities else 0,
            "stability_trend": stability_scores,
            "clarity_trend": clarity_scores
        }
    
    def _aggregate_emotion_metrics(self, emotion_timeline: List[Dict]) -> Dict:
        """Aggregate emotion metrics across all frames"""
        if not emotion_timeline:
            return {}
        
        # Count dominant emotions
        emotion_counts = {}
        confidence_levels = []
        
        for frame in emotion_timeline:
            dominant = frame.get("dominant_emotion", "unknown")
            if dominant != "unknown":
                emotion_counts[dominant] = emotion_counts.get(dominant, 0) + 1
            
            # Extract confidence-related emotions
            emotions = frame.get("emotions", {})
            if emotions:
                confidence_level = emotions.get("happy", 0) + emotions.get("neutral", 0)
                confidence_levels.append(confidence_level)
        
        # Calculate percentages
        total_frames = len([f for f in emotion_timeline if f.get("dominant_emotion") != "unknown"])
        emotion_percentages = {}
        if total_frames > 0:
            for emotion, count in emotion_counts.items():
                emotion_percentages[emotion] = (count / total_frames) * 100
        
        return {
            "emotion_distribution": emotion_percentages,
            "average_confidence_level": float(np.mean(confidence_levels)) if confidence_levels else 0,
            "total_analyzed_frames": total_frames,
            "confidence_timeline": confidence_levels
        }
    
    def _aggregate_speech_metrics(self, transcript_stats: List[Dict]) -> Dict:
        """Aggregate speech metrics across responses"""
        if not transcript_stats:
            return {}
        
        # Extract speaking rates and filler word counts
        speaking_rates = []
        filler_word_counts = []
        total_words = []
        
        for stats in transcript_stats:
            if stats.get("speaking_rate"):
                speaking_rates.append(stats["speaking_rate"])
            
            filler_words = stats.get("filler_words", [])
            filler_word_counts.append(len(filler_words))
            
            word_count = stats.get("word_count", 0)
            total_words.append(word_count)
        
        # Calculate averages
        avg_speaking_rate = np.mean(speaking_rates) if speaking_rates else 0
        total_filler_words = sum(filler_word_counts)
        total_word_count = sum(total_words)
        filler_percentage = (total_filler_words / total_word_count * 100) if total_word_count > 0 else 0
        
        return {
            "average_speaking_rate": float(avg_speaking_rate),
            "total_filler_words": total_filler_words,
            "filler_word_percentage": float(filler_percentage),
            "total_words": total_word_count,
            "speaking_rate_trend": speaking_rates
        }
    
    def _interpret_score(self, score: float) -> Dict:
        """Interpret the overall confidence score"""
        if score >= 85:
            level = "Excellent"
            description = "Outstanding confidence and communication skills"
        elif score >= 70:
            level = "Good"
            description = "Strong confidence with minor areas for improvement"
        elif score >= 55:
            level = "Average"
            description = "Moderate confidence, several areas for development"
        elif score >= 40:
            level = "Below Average"
            description = "Low confidence, significant improvement needed"
        else:
            level = "Poor"
            description = "Very low confidence, major development required"
        
        return {
            "level": level,
            "description": description,
            "score_range": self._get_score_range(score)
        }
    
    def _get_score_range(self, score: float) -> str:
        """Get score range for display"""
        if score >= 85:
            return "85-100"
        elif score >= 70:
            return "70-84"
        elif score >= 55:
            return "55-69"
        elif score >= 40:
            return "40-54"
        else:
            return "0-39"
    
    def _empty_score_result(self) -> Dict:
        """Return empty score result"""
        return {
            "overall_score": 0.0,
            "component_scores": {
                "voice_stability": {"score": 0.0, "weight": 0.40, "weighted_contribution": 0.0},
                "eye_contact": {"score": 0.0, "weight": 0.25, "weighted_contribution": 0.0},
                "emotion_consistency": {"score": 0.0, "weight": 0.20, "weighted_contribution": 0.0},
                "filler_word_frequency": {"score": 0.0, "weight": 0.15, "weighted_contribution": 0.0}
            },
            "response_count": 0,
            "score_interpretation": {
                "level": "No Data",
                "description": "No responses to analyze",
                "score_range": "0"
            }
        }