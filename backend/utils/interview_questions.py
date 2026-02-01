"""
Interview Question Generator
Generates role-specific interview questions using Gemini AI
"""

import os
import google.generativeai as genai
from typing import List, Dict
import json
import random

class InterviewQuestionGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        try:
            self.model = genai.GenerativeModel('gemini-pro')
        except AttributeError:
            # Fallback for older versions
            self.model = genai
        
        # Fallback questions for each role and experience level
        self.fallback_questions = {
            "Software Engineer": {
                "Fresher": [
                    "Tell me about yourself and why you're interested in software engineering.",
                    "What programming languages are you most comfortable with and why?",
                    "Describe a challenging project you worked on during your studies.",
                    "How do you approach debugging when your code isn't working?",
                    "What do you know about our company and why do you want to work here?",
                    "Explain the difference between object-oriented and functional programming.",
                    "How do you stay updated with new programming technologies?",
                    "Describe a time when you had to learn a new technology quickly.",
                    "What is your favorite programming language and why?",
                    "How do you handle version control in your projects?",
                    "What are some best practices for writing clean code?",
                    "Describe your experience with databases and SQL.",
                    "How would you explain APIs to a non-technical person?",
                    "What motivates you to pursue a career in software development?",
                    "Describe a time when you collaborated on a coding project."
                ],
                "Experienced": [
                    "Walk me through your experience with software architecture and design patterns.",
                    "How do you handle code reviews and ensure code quality in a team environment?",
                    "Describe a time when you had to optimize application performance.",
                    "How do you stay updated with new technologies and programming trends?",
                    "Tell me about a challenging technical problem you solved recently."
                ]
            },
            "HR": {
                "Fresher": [
                    "Why are you interested in pursuing a career in Human Resources?",
                    "How would you handle a conflict between two team members?",
                    "What do you think are the most important qualities for an HR professional?",
                    "Describe a time when you had to communicate difficult information to someone.",
                    "How would you approach recruiting candidates for a technical role?"
                ],
                "Experienced": [
                    "How do you develop and implement HR policies that align with business objectives?",
                    "Describe your experience with performance management and employee development.",
                    "How do you handle sensitive employee relations issues?",
                    "What strategies do you use for talent retention and employee engagement?",
                    "Tell me about a time you had to manage organizational change."
                ]
            },
            "Data Analyst": {
                "Fresher": [
                    "What interests you about data analysis and why did you choose this field?",
                    "How would you explain a complex data finding to a non-technical stakeholder?",
                    "What tools and technologies have you used for data analysis?",
                    "Describe a data project you worked on and the insights you discovered.",
                    "How do you ensure data quality and accuracy in your analysis?"
                ],
                "Experienced": [
                    "How do you approach building predictive models and validating their accuracy?",
                    "Describe your experience with data visualization and storytelling with data.",
                    "How do you handle missing or inconsistent data in large datasets?",
                    "Tell me about a time when your analysis influenced a business decision.",
                    "What's your process for identifying trends and patterns in complex data?"
                ]
            }
        }
    
    async def generate_questions(self, role: str, experience_level: str, num_questions: int = 5) -> List[Dict]:
        """
        Generate interview questions for specific role and experience level
        
        Args:
            role: Interview role (Software Engineer, HR, Data Analyst)
            experience_level: Fresher or Experienced
            num_questions: Number of questions to generate
            
        Returns:
            List of question dictionaries with question text and metadata
        """
        try:
            # Try to generate questions using Gemini
            generated_questions = await self._generate_with_gemini(role, experience_level, num_questions)
            
            if generated_questions:
                return generated_questions
            else:
                # Fallback to predefined questions
                return self._get_fallback_questions(role, experience_level, num_questions)
                
        except Exception as e:
            print(f"Question generation error: {str(e)}")
            return self._get_fallback_questions(role, experience_level, num_questions)
    
    async def _generate_with_gemini(self, role: str, experience_level: str, num_questions: int) -> List[Dict]:
        """Generate questions using Gemini AI"""
        prompt = f"""
        Generate {num_questions} interview questions for a {experience_level} {role} position.
        
        Requirements:
        - Questions should be appropriate for {experience_level} level candidates
        - Mix of behavioral, technical, and situational questions
        - Questions should be realistic and commonly asked in {role} interviews
        - Avoid overly complex or niche questions
        - Each question should be clear and concise
        
        For {experience_level} level:
        {"- Focus on foundational knowledge, learning ability, and potential" if experience_level == "Fresher" else "- Focus on experience, leadership, complex problem-solving, and strategic thinking"}
        
        Return the response as a JSON array where each question is an object with:
        - "question": the question text
        - "type": "behavioral", "technical", or "situational"
        - "difficulty": "easy", "medium", or "hard"
        - "expected_duration": estimated answer time in seconds (30-120)
        
        Example format:
        [
            {{
                "question": "Tell me about yourself and your interest in this role.",
                "type": "behavioral",
                "difficulty": "easy",
                "expected_duration": 60
            }}
        ]
        """
        
        try:
            if hasattr(self.model, 'generate_content'):
                response = self.model.generate_content(prompt)
            else:
                # Fallback for older API
                response = genai.generate_text(prompt=prompt)
                response.text = response.result if hasattr(response, 'result') else str(response)
            
            # Try to parse JSON response
            try:
                questions_data = json.loads(response.text.strip())
                
                # Validate the structure
                if isinstance(questions_data, list) and len(questions_data) > 0:
                    validated_questions = []
                    for i, q in enumerate(questions_data):
                        if isinstance(q, dict) and "question" in q:
                            validated_questions.append({
                                "id": i + 1,
                                "question": q.get("question", ""),
                                "type": q.get("type", "behavioral"),
                                "difficulty": q.get("difficulty", "medium"),
                                "expected_duration": q.get("expected_duration", 60),
                                "role": role,
                                "experience_level": experience_level
                            })
                    
                    return validated_questions if validated_questions else None
                
            except json.JSONDecodeError:
                # Try to extract questions from text format
                return self._parse_text_questions(response.text, role, experience_level)
                
        except Exception as e:
            print(f"Gemini question generation failed: {str(e)}")
            return None
    
    def _parse_text_questions(self, text: str, role: str, experience_level: str) -> List[Dict]:
        """Parse questions from plain text response"""
        lines = text.strip().split('\n')
        questions = []
        question_id = 1
        
        for line in lines:
            line = line.strip()
            
            # Look for lines that seem like questions
            if line and (line.endswith('?') or 
                        line.startswith(('1.', '2.', '3.', '4.', '5.', '-', '•', '*')) or
                        any(word in line.lower() for word in ['tell me', 'describe', 'how do you', 'what', 'why', 'when'])):
                
                # Clean up the question text
                question_text = line
                for prefix in ['1.', '2.', '3.', '4.', '5.', '-', '•', '*']:
                    if question_text.startswith(prefix):
                        question_text = question_text[len(prefix):].strip()
                        break
                
                if question_text and len(question_text) > 10:  # Reasonable question length
                    questions.append({
                        "id": question_id,
                        "question": question_text,
                        "type": self._classify_question_type(question_text),
                        "difficulty": "medium",
                        "expected_duration": 60,
                        "role": role,
                        "experience_level": experience_level
                    })
                    question_id += 1
        
        return questions if questions else None
    
    def _classify_question_type(self, question: str) -> str:
        """Classify question type based on content"""
        question_lower = question.lower()
        
        behavioral_keywords = ['tell me about', 'describe a time', 'give me an example', 'how did you handle']
        technical_keywords = ['how do you', 'what is', 'explain', 'implement', 'design', 'code', 'algorithm']
        situational_keywords = ['what would you do', 'how would you', 'if you were', 'imagine']
        
        if any(keyword in question_lower for keyword in behavioral_keywords):
            return "behavioral"
        elif any(keyword in question_lower for keyword in technical_keywords):
            return "technical"
        elif any(keyword in question_lower for keyword in situational_keywords):
            return "situational"
        else:
            return "behavioral"  # Default
    
    def _get_fallback_questions(self, role: str, experience_level: str, num_questions: int) -> List[Dict]:
        """Get fallback questions from predefined sets with randomization for variety"""
        if role not in self.fallback_questions:
            role = "Software Engineer"  # Default role
        
        if experience_level not in self.fallback_questions[role]:
            experience_level = "Fresher"  # Default experience level
        
        available_questions = self.fallback_questions[role][experience_level]
        
        # Add some randomization to make questions feel fresh
        import time
        import hashlib
        
        # Create a seed based on current time to ensure different questions each time
        seed = int(time.time()) % 1000
        random.seed(seed)
        
        # Shuffle the available questions
        shuffled_questions = available_questions.copy()
        random.shuffle(shuffled_questions)
        
        # Select questions (ensure we don't exceed available questions)
        selected_questions = shuffled_questions[:min(num_questions, len(shuffled_questions))]
        
        # If we need more questions, cycle through the list
        while len(selected_questions) < num_questions:
            remaining_needed = num_questions - len(selected_questions)
            additional_questions = shuffled_questions[:remaining_needed]
            selected_questions.extend(additional_questions)
        
        # Format as question objects with some variation
        formatted_questions = []
        for i, question in enumerate(selected_questions):
            formatted_questions.append({
                "id": i + 1,
                "question": question,
                "type": self._classify_question_type(question),
                "difficulty": random.choice(["easy", "medium", "hard"]) if experience_level == "Experienced" else random.choice(["easy", "medium"]),
                "expected_duration": random.randint(45, 120),
                "role": role,
                "experience_level": experience_level,
                "source": "fallback_randomized"
            })
        
        print(f"✓ Generated {len(formatted_questions)} randomized fallback questions for {role} ({experience_level})")
        return formatted_questions
    
    def get_available_roles(self) -> List[str]:
        """Get list of available interview roles"""
        return list(self.fallback_questions.keys())
    
    def get_experience_levels(self) -> List[str]:
        """Get list of available experience levels"""
        return ["Fresher", "Experienced"]
    
    async def generate_follow_up_question(self, original_question: str, user_response: str, role: str) -> str:
        """Generate a follow-up question based on user's response"""
        prompt = f"""
        Based on this {role} interview question and the candidate's response, generate a relevant follow-up question.
        
        Original Question: {original_question}
        Candidate's Response: {user_response}
        
        Generate a follow-up question that:
        - Digs deeper into their response
        - Tests their knowledge or experience further
        - Is appropriate for the {role} role
        - Is concise and clear
        
        Return only the follow-up question text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            follow_up = response.text.strip()
            
            # Ensure it's a question
            if not follow_up.endswith('?'):
                follow_up += '?'
            
            return follow_up
            
        except Exception as e:
            # Fallback follow-up questions
            generic_follow_ups = [
                "Can you give me a specific example of that?",
                "How did you measure the success of that approach?",
                "What would you do differently if you faced that situation again?",
                "What challenges did you encounter and how did you overcome them?"
            ]
            return random.choice(generic_follow_ups)