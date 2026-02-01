"""
Answer Rating Service
Provides AI-powered rating and feedback for individual interview answers using Gemini AI
"""

import os
import google.generativeai as genai
from typing import Dict, List, Optional
import json

class AnswerRatingService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        try:
            self.model = genai.GenerativeModel('gemini-pro')
        except AttributeError:
            # Fallback for older versions of google-generativeai
            self.model = genai
        
        # Rating criteria for different question types
        self.rating_criteria = {
            "behavioral": {
                "structure": "Clear STAR method (Situation, Task, Action, Result)",
                "specificity": "Specific examples and concrete details",
                "relevance": "Relevance to the question and role",
                "impact": "Demonstrated impact and learning",
                "communication": "Clear and organized communication"
            },
            "technical": {
                "accuracy": "Technical accuracy and correctness",
                "depth": "Depth of technical knowledge",
                "explanation": "Ability to explain complex concepts clearly",
                "problem_solving": "Problem-solving approach and methodology",
                "best_practices": "Awareness of best practices and standards"
            },
            "situational": {
                "approach": "Logical and structured approach to the situation",
                "consideration": "Consideration of multiple perspectives and factors",
                "decision_making": "Sound decision-making process",
                "communication": "Clear communication of thought process",
                "adaptability": "Flexibility and adaptability in approach"
            }
        }
    
    async def rate_answer(
        self, 
        question: str, 
        answer: str, 
        question_type: str, 
        role: str, 
        experience_level: str,
        transcript_data: Optional[Dict] = None,
        voice_metrics: Optional[Dict] = None,
        emotion_analysis: Optional[Dict] = None
    ) -> Dict:
        """
        Rate an interview answer using AI analysis
        
        Args:
            question: The interview question asked
            answer: The candidate's answer (transcript)
            question_type: Type of question (behavioral, technical, situational)
            role: Interview role
            experience_level: Candidate's experience level
            transcript_data: Audio analysis data (optional)
            voice_metrics: Voice quality metrics (optional)
            emotion_analysis: Video emotion analysis (optional)
            
        Returns:
            Dict containing rating, feedback, and improvement suggestions
        """
        try:
            # Generate comprehensive rating
            content_rating = await self._rate_answer_content(
                question, answer, question_type, role, experience_level
            )
            
            # Generate delivery rating if metrics available
            delivery_rating = await self._rate_answer_delivery(
                answer, transcript_data, voice_metrics, emotion_analysis
            )
            
            # Calculate overall rating
            overall_rating = self._calculate_overall_rating(content_rating, delivery_rating)
            
            # Generate specific feedback
            feedback = await self._generate_answer_feedback(
                question, answer, question_type, role, content_rating, delivery_rating
            )
            
            # Generate improvement suggestions
            improvements = await self._generate_improvement_suggestions(
                question, answer, question_type, role, content_rating, delivery_rating
            )
            
            return {
                "overall_rating": overall_rating,
                "content_rating": content_rating,
                "delivery_rating": delivery_rating,
                "feedback": feedback,
                "improvements": improvements,
                "question_type": question_type,
                "role": role,
                "experience_level": experience_level
            }
            
        except Exception as e:
            print(f"Answer rating error: {str(e)}")
            return self._generate_fallback_rating(question, answer, question_type)
    
    async def _rate_answer_content(
        self, 
        question: str, 
        answer: str, 
        question_type: str, 
        role: str, 
        experience_level: str
    ) -> Dict:
        """Rate the content quality of the answer"""
        
        criteria = self.rating_criteria.get(question_type, self.rating_criteria["behavioral"])
        criteria_text = "\n".join([f"- {key}: {value}" for key, value in criteria.items()])
        
        prompt = f"""
        You are an expert interview coach evaluating a {experience_level} {role} candidate's answer.
        
        Question: {question}
        Question Type: {question_type}
        Candidate's Answer: {answer}
        
        Evaluation Criteria for {question_type} questions:
        {criteria_text}
        
        Rate the answer on a scale of 1-10 for each criterion and provide an overall content score.
        Consider the candidate's experience level ({experience_level}) in your evaluation.
        
        For {experience_level} candidates:
        {"- Focus on potential, learning ability, and foundational knowledge" if experience_level == "Fresher" else "- Expect advanced expertise, leadership examples, and strategic thinking"}
        
        Return your evaluation as JSON in this format:
        {{
            "overall_score": 7.5,
            "criterion_scores": {{
                "structure": 8,
                "specificity": 7,
                "relevance": 8,
                "impact": 7,
                "communication": 8
            }},
            "strengths": ["Clear structure", "Good specific example"],
            "weaknesses": ["Could provide more quantifiable results", "Missing some technical depth"],
            "score_explanation": "Good answer with clear structure and relevant example, but could benefit from more specific metrics and deeper technical insight."
        }}
        """
        
        try:
            if hasattr(self.model, 'generate_content'):
                response = self.model.generate_content(prompt)
                response_text = response.text
            else:
                # Fallback for older API
                response = genai.generate_text(prompt=prompt)
                response_text = response.result if hasattr(response, 'result') else str(response)
            
            rating_data = json.loads(response_text.strip())
            
            # Validate and clean the response
            if isinstance(rating_data, dict) and "overall_score" in rating_data:
                return {
                    "overall_score": min(10, max(1, rating_data.get("overall_score", 5))),
                    "criterion_scores": rating_data.get("criterion_scores", {}),
                    "strengths": rating_data.get("strengths", []),
                    "weaknesses": rating_data.get("weaknesses", []),
                    "score_explanation": rating_data.get("score_explanation", "")
                }
            else:
                raise ValueError("Invalid response format")
                
        except Exception as e:
            print(f"Content rating error: {str(e)}")
            # Fallback rating based on answer length and basic analysis
            word_count = len(answer.split())
            
            if word_count < 20:
                score = 4.0
                explanation = "Answer is too brief and lacks detail."
            elif word_count < 50:
                score = 6.0
                explanation = "Answer provides some information but could be more comprehensive."
            elif word_count < 100:
                score = 7.5
                explanation = "Good answer length with adequate detail."
            else:
                score = 8.0
                explanation = "Comprehensive answer with good detail."
            
            return {
                "overall_score": score,
                "criterion_scores": {},
                "strengths": ["Provided a response"],
                "weaknesses": ["Could be more detailed"] if word_count < 50 else [],
                "score_explanation": explanation
            }
    
    async def _rate_answer_delivery(
        self,
        answer: str,
        transcript_data: Optional[Dict],
        voice_metrics: Optional[Dict],
        emotion_analysis: Optional[Dict]
    ) -> Dict:
        """Rate the delivery quality of the answer"""
        
        if not any([transcript_data, voice_metrics, emotion_analysis]):
            return {
                "overall_score": 7.0,
                "delivery_aspects": {
                    "clarity": 7.0,
                    "confidence": 7.0,
                    "pace": 7.0,
                    "engagement": 7.0
                },
                "explanation": "Delivery metrics not available for detailed analysis."
            }
        
        # Analyze available metrics
        delivery_scores = {}
        
        # Voice clarity and pace
        if transcript_data:
            word_count = transcript_data.get("word_count", 0)
            speaking_rate = transcript_data.get("speaking_rate", 150)
            filler_count = transcript_data.get("filler_word_count", 0)
            
            # Rate speaking pace (optimal: 140-180 WPM)
            if 140 <= speaking_rate <= 180:
                pace_score = 9.0
            elif 120 <= speaking_rate <= 200:
                pace_score = 7.5
            else:
                pace_score = 6.0
            
            # Rate clarity based on filler words
            if word_count > 0:
                filler_percentage = (filler_count / word_count) * 100
                if filler_percentage < 2:
                    clarity_score = 9.0
                elif filler_percentage < 5:
                    clarity_score = 7.5
                elif filler_percentage < 10:
                    clarity_score = 6.0
                else:
                    clarity_score = 4.0
            else:
                clarity_score = 5.0
            
            delivery_scores["pace"] = pace_score
            delivery_scores["clarity"] = clarity_score
        
        # Voice confidence
        if voice_metrics:
            stability = voice_metrics.get("stability_score", 70)
            voice_clarity = voice_metrics.get("clarity_score", 70)
            
            confidence_score = (stability + voice_clarity) / 20  # Convert to 1-10 scale
            delivery_scores["confidence"] = min(10, max(1, confidence_score))
        
        # Engagement from emotion analysis
        if emotion_analysis:
            metrics = emotion_analysis.get("metrics", {})
            eye_contact = metrics.get("eye_contact_percentage", 70)
            confidence_level = metrics.get("confidence_score", 70)
            
            engagement_score = (eye_contact + confidence_level) / 20  # Convert to 1-10 scale
            delivery_scores["engagement"] = min(10, max(1, engagement_score))
        
        # Calculate overall delivery score
        if delivery_scores:
            overall_delivery = sum(delivery_scores.values()) / len(delivery_scores)
        else:
            overall_delivery = 7.0
        
        return {
            "overall_score": round(overall_delivery, 1),
            "delivery_aspects": delivery_scores,
            "explanation": self._generate_delivery_explanation(delivery_scores)
        }
    
    def _generate_delivery_explanation(self, delivery_scores: Dict) -> str:
        """Generate explanation for delivery rating"""
        explanations = []
        
        for aspect, score in delivery_scores.items():
            if score >= 8.5:
                explanations.append(f"Excellent {aspect}")
            elif score >= 7.0:
                explanations.append(f"Good {aspect}")
            elif score >= 5.5:
                explanations.append(f"Average {aspect}")
            else:
                explanations.append(f"Needs improvement in {aspect}")
        
        return ". ".join(explanations) + "."
    
    def _calculate_overall_rating(self, content_rating: Dict, delivery_rating: Dict) -> Dict:
        """Calculate overall rating combining content and delivery"""
        
        content_score = content_rating.get("overall_score", 7.0)
        delivery_score = delivery_rating.get("overall_score", 7.0)
        
        # Weight content more heavily (70% content, 30% delivery)
        overall_score = (content_score * 0.7) + (delivery_score * 0.3)
        
        # Determine rating level
        if overall_score >= 9.0:
            level = "Excellent"
            description = "Outstanding answer with excellent content and delivery"
        elif overall_score >= 8.0:
            level = "Very Good"
            description = "Strong answer with good content and solid delivery"
        elif overall_score >= 7.0:
            level = "Good"
            description = "Good answer with adequate content and delivery"
        elif overall_score >= 6.0:
            level = "Fair"
            description = "Acceptable answer but with room for improvement"
        elif overall_score >= 5.0:
            level = "Below Average"
            description = "Answer needs significant improvement in content or delivery"
        else:
            level = "Poor"
            description = "Answer requires major improvement in both content and delivery"
        
        return {
            "score": round(overall_score, 1),
            "level": level,
            "description": description,
            "content_weight": 0.7,
            "delivery_weight": 0.3
        }
    
    async def _generate_answer_feedback(
        self,
        question: str,
        answer: str,
        question_type: str,
        role: str,
        content_rating: Dict,
        delivery_rating: Dict
    ) -> str:
        """Generate specific feedback for the answer"""
        
        prompt = f"""
        Provide constructive feedback for this {role} interview answer:
        
        Question: {question}
        Answer: {answer}
        
        Content Rating: {content_rating['overall_score']}/10
        Content Strengths: {', '.join(content_rating.get('strengths', []))}
        Content Weaknesses: {', '.join(content_rating.get('weaknesses', []))}
        
        Delivery Rating: {delivery_rating['overall_score']}/10
        
        Write 2-3 sentences of specific, actionable feedback that:
        - Acknowledges what they did well
        - Identifies specific areas for improvement
        - Provides encouragement and motivation
        - Is professional and supportive in tone
        
        Focus on being constructive and helpful rather than critical.
        """
        
        try:
            if hasattr(self.model, 'generate_content'):
                response = self.model.generate_content(prompt)
                return response.text.strip()
            else:
                # Fallback for older API
                response = genai.generate_text(prompt=prompt)
                return response.result if hasattr(response, 'result') else str(response).strip()
        except Exception as e:
            # Fallback feedback
            content_score = content_rating.get("overall_score", 7.0)
            if content_score >= 8.0:
                return f"Great answer! You provided good detail and structure. To make it even stronger, consider adding more specific examples or quantifiable results."
            elif content_score >= 6.0:
                return f"Good response with relevant information. To improve, try to be more specific with examples and ensure your answer directly addresses all parts of the question."
            else:
                return f"Your answer shows understanding of the topic. To strengthen future responses, provide more detailed examples and structure your answer more clearly."
    
    async def _generate_improvement_suggestions(
        self,
        question: str,
        answer: str,
        question_type: str,
        role: str,
        content_rating: Dict,
        delivery_rating: Dict
    ) -> List[str]:
        """Generate specific improvement suggestions"""
        
        suggestions = []
        
        # Content-based suggestions
        content_score = content_rating.get("overall_score", 7.0)
        weaknesses = content_rating.get("weaknesses", [])
        
        if content_score < 7.0:
            suggestions.append("Structure your answer more clearly with a beginning, middle, and end")
            suggestions.append("Provide more specific examples and concrete details")
        
        if "quantifiable" in str(weaknesses).lower():
            suggestions.append("Include specific numbers, metrics, or measurable outcomes")
        
        if "technical" in str(weaknesses).lower() and "technical" in question_type.lower():
            suggestions.append("Demonstrate deeper technical knowledge and explain your reasoning")
        
        # Delivery-based suggestions
        delivery_score = delivery_rating.get("overall_score", 7.0)
        delivery_aspects = delivery_rating.get("delivery_aspects", {})
        
        if delivery_aspects.get("pace", 7.0) < 6.0:
            suggestions.append("Practice speaking at a more natural pace - not too fast or too slow")
        
        if delivery_aspects.get("clarity", 7.0) < 6.0:
            suggestions.append("Reduce filler words by pausing briefly instead of saying 'um' or 'uh'")
        
        if delivery_aspects.get("confidence", 7.0) < 6.0:
            suggestions.append("Work on voice confidence through practice and preparation")
        
        if delivery_aspects.get("engagement", 7.0) < 6.0:
            suggestions.append("Maintain better eye contact and show more engagement")
        
        # Question-type specific suggestions
        if question_type == "behavioral" and content_score < 7.0:
            suggestions.append("Use the STAR method: Situation, Task, Action, Result")
        elif question_type == "technical" and content_score < 7.0:
            suggestions.append("Break down complex technical concepts into simpler explanations")
        elif question_type == "situational" and content_score < 7.0:
            suggestions.append("Walk through your thought process step by step")
        
        # Limit to top 4 suggestions
        return suggestions[:4] if suggestions else ["Keep practicing and stay confident!"]
    
    def _generate_fallback_rating(self, question: str, answer: str, question_type: str) -> Dict:
        """Generate fallback rating when AI analysis fails"""
        
        word_count = len(answer.split())
        
        # Basic scoring based on answer length and completeness
        if word_count < 10:
            score = 3.0
            level = "Poor"
        elif word_count < 30:
            score = 5.0
            level = "Below Average"
        elif word_count < 60:
            score = 6.5
            level = "Fair"
        elif word_count < 100:
            score = 7.5
            level = "Good"
        else:
            score = 8.0
            level = "Very Good"
        
        return {
            "overall_rating": {
                "score": score,
                "level": level,
                "description": f"{level} answer based on length and completeness"
            },
            "content_rating": {
                "overall_score": score,
                "strengths": ["Provided a response"],
                "weaknesses": ["Could be more detailed"] if word_count < 50 else [],
                "score_explanation": f"Answer contains {word_count} words"
            },
            "delivery_rating": {
                "overall_score": 7.0,
                "explanation": "Delivery analysis not available"
            },
            "feedback": f"Your answer shows effort. To improve, try to provide more specific examples and structure your response more clearly.",
            "improvements": [
                "Provide more specific examples",
                "Structure your answer clearly",
                "Practice speaking with confidence"
            ],
            "question_type": question_type
        }