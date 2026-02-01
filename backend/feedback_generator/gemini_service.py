"""
Gemini AI Feedback Generator
Generates personalized feedback and improvement suggestions
"""

import os
import google.generativeai as genai
from typing import Dict, List
import json

class FeedbackGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Feedback templates and guidelines
        self.feedback_tone_guidelines = """
        Generate feedback that is:
        - Supportive and encouraging
        - Constructive and actionable
        - Non-judgmental and professional
        - Specific with concrete examples
        - Balanced (highlight strengths and areas for improvement)
        """
    
    async def generate_feedback(self, responses: List[Dict], confidence_score: Dict, interview_role: str) -> Dict:
        """
        Generate comprehensive AI feedback based on interview performance
        
        Args:
            responses: List of interview responses with analysis data
            confidence_score: Overall confidence scoring results
            interview_role: The role being interviewed for
            
        Returns:
            Dict containing structured feedback
        """
        try:
            # Prepare analysis summary for Gemini
            analysis_summary = self._prepare_analysis_summary(responses, confidence_score)
            
            # Generate different types of feedback
            overall_feedback = await self._generate_overall_feedback(analysis_summary, interview_role)
            specific_improvements = await self._generate_specific_improvements(analysis_summary, interview_role)
            strengths = await self._identify_strengths(analysis_summary, interview_role)
            action_plan = await self._generate_action_plan(analysis_summary, interview_role)
            
            return {
                "overall_feedback": overall_feedback,
                "strengths": strengths,
                "areas_for_improvement": specific_improvements,
                "action_plan": action_plan,
                "confidence_level": confidence_score.get("score_interpretation", {}).get("level", "Unknown"),
                "personalized_tips": await self._generate_personalized_tips(analysis_summary, interview_role)
            }
            
        except Exception as e:
            return {
                "overall_feedback": "Unable to generate detailed feedback at this time.",
                "strengths": ["Completed the interview session"],
                "areas_for_improvement": ["Continue practicing interview skills"],
                "action_plan": ["Schedule regular practice sessions", "Record yourself to review performance"],
                "confidence_level": "Unknown",
                "personalized_tips": ["Keep practicing and stay confident!"],
                "error": str(e)
            }
    
    def _prepare_analysis_summary(self, responses: List[Dict], confidence_score: Dict) -> Dict:
        """Prepare a structured summary of analysis results for Gemini"""
        summary = {
            "overall_confidence_score": confidence_score.get("overall_score", 0),
            "confidence_level": confidence_score.get("score_interpretation", {}).get("level", "Unknown"),
            "component_scores": confidence_score.get("component_scores", {}),
            "response_count": len(responses),
            "performance_metrics": {}
        }
        
        # Aggregate key metrics
        total_filler_words = 0
        total_words = 0
        speaking_rates = []
        emotion_summaries = []
        voice_stability_scores = []
        
        for response in responses:
            # Transcript analysis
            transcript = response.get("transcript", {})
            if transcript:
                filler_words = transcript.get("filler_words", [])
                total_filler_words += len(filler_words)
                total_words += transcript.get("word_count", 0)
                
                if transcript.get("speaking_rate"):
                    speaking_rates.append(transcript["speaking_rate"])
            
            # Voice analysis
            voice_metrics = response.get("voice_metrics", {})
            if voice_metrics:
                voice_stability_scores.append(voice_metrics.get("stability_score", 0))
            
            # Emotion analysis
            emotion_analysis = response.get("emotion_analysis", {})
            if emotion_analysis:
                metrics = emotion_analysis.get("metrics", {})
                emotion_summaries.append({
                    "confidence_score": metrics.get("confidence_score", 0),
                    "nervousness_score": metrics.get("nervousness_score", 0),
                    "eye_contact_percentage": metrics.get("eye_contact_percentage", 0)
                })
        
        # Calculate averages
        summary["performance_metrics"] = {
            "filler_word_percentage": (total_filler_words / total_words * 100) if total_words > 0 else 0,
            "average_speaking_rate": sum(speaking_rates) / len(speaking_rates) if speaking_rates else 0,
            "average_voice_stability": sum(voice_stability_scores) / len(voice_stability_scores) if voice_stability_scores else 0,
            "average_eye_contact": sum(e["eye_contact_percentage"] for e in emotion_summaries) / len(emotion_summaries) if emotion_summaries else 0,
            "average_emotional_confidence": sum(e["confidence_score"] for e in emotion_summaries) / len(emotion_summaries) if emotion_summaries else 0
        }
        
        return summary
    
    async def _generate_overall_feedback(self, analysis_summary: Dict, interview_role: str) -> str:
        """Generate overall performance feedback"""
        prompt = f"""
        {self.feedback_tone_guidelines}
        
        You are an expert interview coach providing feedback for a {interview_role} interview practice session.
        
        Performance Summary:
        - Overall Confidence Score: {analysis_summary['overall_confidence_score']:.1f}/100
        - Confidence Level: {analysis_summary['confidence_level']}
        - Number of Questions Answered: {analysis_summary['response_count']}
        
        Key Metrics:
        - Voice Stability: {analysis_summary['performance_metrics']['average_voice_stability']:.1f}/100
        - Eye Contact: {analysis_summary['performance_metrics']['average_eye_contact']:.1f}%
        - Speaking Rate: {analysis_summary['performance_metrics']['average_speaking_rate']:.1f} WPM
        - Filler Words: {analysis_summary['performance_metrics']['filler_word_percentage']:.1f}%
        
        Provide a comprehensive 3-4 sentence overall feedback that:
        1. Acknowledges their effort and participation
        2. Highlights their current confidence level
        3. Gives an encouraging assessment of their performance
        4. Sets a positive tone for improvement
        
        Keep it supportive, professional, and motivating.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Great job completing the interview practice session! Your confidence level shows {analysis_summary['confidence_level'].lower()} performance with room for growth. Keep practicing to build your interview skills and confidence."
    
    async def _generate_specific_improvements(self, analysis_summary: Dict, interview_role: str) -> List[str]:
        """Generate specific areas for improvement"""
        prompt = f"""
        {self.feedback_tone_guidelines}
        
        Based on this {interview_role} interview analysis, identify 3-5 specific areas for improvement:
        
        Performance Data:
        - Voice Stability: {analysis_summary['performance_metrics']['average_voice_stability']:.1f}/100
        - Eye Contact: {analysis_summary['performance_metrics']['average_eye_contact']:.1f}%
        - Filler Words: {analysis_summary['performance_metrics']['filler_word_percentage']:.1f}%
        - Speaking Rate: {analysis_summary['performance_metrics']['average_speaking_rate']:.1f} WPM
        
        Component Scores:
        {json.dumps(analysis_summary['component_scores'], indent=2)}
        
        For each improvement area, provide:
        - A clear, actionable suggestion
        - Specific to the metrics shown
        - Encouraging and constructive tone
        - Relevant to {interview_role} interviews
        
        Return as a JSON array of strings, each being one improvement suggestion.
        Example: ["Work on maintaining steadier eye contact with the camera", "Practice reducing filler words like 'um' and 'uh'"]
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Try to parse as JSON, fallback to manual parsing
            try:
                improvements = json.loads(response.text.strip())
                return improvements if isinstance(improvements, list) else []
            except:
                # Manual parsing if JSON fails
                lines = response.text.strip().split('\n')
                improvements = []
                for line in lines:
                    line = line.strip()
                    if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                        improvements.append(line[1:].strip())
                    elif line and not line.startswith('[') and not line.startswith(']'):
                        improvements.append(line)
                return improvements[:5]  # Limit to 5 items
        except Exception as e:
            # Fallback improvements based on scores
            improvements = []
            metrics = analysis_summary['performance_metrics']
            
            if metrics['average_voice_stability'] < 70:
                improvements.append("Practice speaking with more consistent pitch and volume")
            
            if metrics['average_eye_contact'] < 60:
                improvements.append("Improve eye contact by looking directly at the camera")
            
            if metrics['filler_word_percentage'] > 5:
                improvements.append("Reduce filler words by pausing instead of saying 'um' or 'uh'")
            
            if metrics['average_speaking_rate'] < 120 or metrics['average_speaking_rate'] > 180:
                improvements.append("Adjust speaking pace for clearer communication")
            
            return improvements if improvements else ["Continue practicing interview skills regularly"]
    
    async def _identify_strengths(self, analysis_summary: Dict, interview_role: str) -> List[str]:
        """Identify and highlight strengths"""
        prompt = f"""
        {self.feedback_tone_guidelines}
        
        Identify 2-4 strengths from this {interview_role} interview performance:
        
        Performance Data:
        - Overall Score: {analysis_summary['overall_confidence_score']:.1f}/100
        - Voice Stability: {analysis_summary['performance_metrics']['average_voice_stability']:.1f}/100
        - Eye Contact: {analysis_summary['performance_metrics']['average_eye_contact']:.1f}%
        - Filler Words: {analysis_summary['performance_metrics']['filler_word_percentage']:.1f}%
        - Speaking Rate: {analysis_summary['performance_metrics']['average_speaking_rate']:.1f} WPM
        
        Focus on positive aspects and what they did well. Be specific and encouraging.
        Return as a JSON array of strings.
        Example: ["Maintained good speaking pace throughout the interview", "Showed confidence in voice delivery"]
        """
        
        try:
            response = self.model.generate_content(prompt)
            try:
                strengths = json.loads(response.text.strip())
                return strengths if isinstance(strengths, list) else []
            except:
                # Manual parsing
                lines = response.text.strip().split('\n')
                strengths = []
                for line in lines:
                    line = line.strip()
                    if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                        strengths.append(line[1:].strip())
                    elif line and not line.startswith('[') and not line.startswith(']'):
                        strengths.append(line)
                return strengths[:4]
        except Exception as e:
            # Fallback strengths
            strengths = ["Completed the full interview session"]
            metrics = analysis_summary['performance_metrics']
            
            if metrics['average_voice_stability'] > 70:
                strengths.append("Demonstrated good voice control and stability")
            
            if metrics['average_eye_contact'] > 70:
                strengths.append("Maintained good eye contact throughout")
            
            if metrics['filler_word_percentage'] < 3:
                strengths.append("Spoke clearly with minimal filler words")
            
            return strengths
    
    async def _generate_action_plan(self, analysis_summary: Dict, interview_role: str) -> List[str]:
        """Generate actionable improvement plan"""
        prompt = f"""
        Create a 4-5 step action plan for improving {interview_role} interview performance:
        
        Current Performance:
        - Confidence Score: {analysis_summary['overall_confidence_score']:.1f}/100
        - Key areas needing work based on component scores:
        {json.dumps(analysis_summary['component_scores'], indent=2)}
        
        Create specific, actionable steps they can take to improve. Make them practical and achievable.
        Return as a JSON array of strings.
        Example: ["Practice answering common questions in front of a mirror", "Record yourself speaking to identify filler words"]
        """
        
        try:
            response = self.model.generate_content(prompt)
            try:
                action_plan = json.loads(response.text.strip())
                return action_plan if isinstance(action_plan, list) else []
            except:
                # Manual parsing
                lines = response.text.strip().split('\n')
                action_plan = []
                for line in lines:
                    line = line.strip()
                    if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                        action_plan.append(line[1:].strip())
                    elif line and not line.startswith('[') and not line.startswith(']'):
                        action_plan.append(line)
                return action_plan[:5]
        except Exception as e:
            # Fallback action plan
            return [
                "Practice answering common interview questions daily",
                "Record yourself to review body language and speech patterns",
                "Work on maintaining eye contact with the camera",
                "Practice speaking without filler words",
                "Schedule regular mock interview sessions"
            ]
    
    async def _generate_personalized_tips(self, analysis_summary: Dict, interview_role: str) -> List[str]:
        """Generate personalized tips based on specific performance"""
        confidence_level = analysis_summary['confidence_level'].lower()
        metrics = analysis_summary['performance_metrics']
        
        tips = []
        
        # Voice-related tips
        if metrics['average_voice_stability'] < 60:
            tips.append("Practice deep breathing exercises before interviews to stabilize your voice")
        
        # Eye contact tips
        if metrics['average_eye_contact'] < 50:
            tips.append("Place a small arrow or dot near your camera to remind yourself to look directly at it")
        
        # Speaking rate tips
        if metrics['average_speaking_rate'] < 100:
            tips.append("You speak quite slowly - try to increase your pace slightly for more dynamic delivery")
        elif metrics['average_speaking_rate'] > 200:
            tips.append("You speak quite quickly - practice slowing down for clearer communication")
        
        # Filler word tips
        if metrics['filler_word_percentage'] > 8:
            tips.append("Practice pausing silently instead of using filler words - silence is better than 'um'")
        
        # Role-specific tips
        if interview_role.lower() in ['software engineer', 'developer', 'programmer']:
            tips.append("For technical roles, practice explaining complex concepts in simple terms")
        elif interview_role.lower() in ['hr', 'human resources']:
            tips.append("Focus on demonstrating empathy and communication skills in your responses")
        elif interview_role.lower() in ['data analyst', 'analyst']:
            tips.append("Practice presenting data insights clearly and concisely")
        
        # Confidence-level specific tips
        if confidence_level in ['poor', 'below average']:
            tips.append("Start with easier questions and gradually work up to more challenging ones")
        elif confidence_level in ['excellent', 'good']:
            tips.append("You're doing great! Focus on fine-tuning your delivery for even better impact")
        
        return tips[:4]  # Limit to 4 tips