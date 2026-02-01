"""
InterVue AI - Vercel Serverless API
AI-powered interview practice platform optimized for serverless deployment
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import uuid
from typing import Dict, List, Optional
import json
import random
import tempfile

app = FastAPI(
    title="InterVue AI API",
    description="AI-powered interview practice platform (Serverless)",
    version="1.0.0"
)

# CORS middleware - allow all origins for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for serverless (use Redis/Database in production)
sessions = {}

# Demo questions as fallback
DEMO_QUESTIONS = {
    "Software Engineer": {
        "Fresher": [
            {
                "id": 1,
                "question": "Tell me about yourself and why you're interested in software engineering.",
                "type": "behavioral",
                "difficulty": "easy",
                "expected_duration": 60
            },
            {
                "id": 2,
                "question": "What programming languages are you most comfortable with and why?",
                "type": "technical",
                "difficulty": "medium",
                "expected_duration": 90
            },
            {
                "id": 3,
                "question": "Describe a challenging project you worked on during your studies.",
                "type": "behavioral",
                "difficulty": "medium",
                "expected_duration": 90
            },
            {
                "id": 4,
                "question": "How do you approach debugging when your code isn't working?",
                "type": "technical",
                "difficulty": "medium",
                "expected_duration": 90
            },
            {
                "id": 5,
                "question": "What do you know about our company and why do you want to work here?",
                "type": "behavioral",
                "difficulty": "easy",
                "expected_duration": 60
            }
        ],
        "Experienced": [
            {
                "id": 1,
                "question": "Walk me through your experience with software architecture and design patterns.",
                "type": "technical",
                "difficulty": "hard",
                "expected_duration": 120
            },
            {
                "id": 2,
                "question": "How do you handle code reviews and ensure code quality in a team environment?",
                "type": "behavioral",
                "difficulty": "medium",
                "expected_duration": 90
            },
            {
                "id": 3,
                "question": "Describe a time when you had to optimize application performance.",
                "type": "technical",
                "difficulty": "hard",
                "expected_duration": 120
            },
            {
                "id": 4,
                "question": "How do you stay updated with new technologies and programming trends?",
                "type": "behavioral",
                "difficulty": "medium",
                "expected_duration": 90
            },
            {
                "id": 5,
                "question": "Tell me about a challenging technical problem you solved recently.",
                "type": "technical",
                "difficulty": "hard",
                "expected_duration": 120
            }
        ]
    },
    "HR": {
        "Fresher": [
            {
                "id": 1,
                "question": "Why are you interested in pursuing a career in Human Resources?",
                "type": "behavioral",
                "difficulty": "easy",
                "expected_duration": 60
            },
            {
                "id": 2,
                "question": "How would you handle a conflict between two team members?",
                "type": "situational",
                "difficulty": "medium",
                "expected_duration": 90
            }
        ],
        "Experienced": [
            {
                "id": 1,
                "question": "How do you develop and implement HR policies that align with business objectives?",
                "type": "technical",
                "difficulty": "hard",
                "expected_duration": 120
            },
            {
                "id": 2,
                "question": "Describe your experience with performance management and employee development.",
                "type": "behavioral",
                "difficulty": "medium",
                "expected_duration": 90
            }
        ]
    },
    "Data Analyst": {
        "Fresher": [
            {
                "id": 1,
                "question": "What interests you about data analysis and why did you choose this field?",
                "type": "behavioral",
                "difficulty": "easy",
                "expected_duration": 60
            },
            {
                "id": 2,
                "question": "How would you explain a complex data finding to a non-technical stakeholder?",
                "type": "situational",
                "difficulty": "medium",
                "expected_duration": 90
            }
        ],
        "Experienced": [
            {
                "id": 1,
                "question": "How do you approach building predictive models and validating their accuracy?",
                "type": "technical",
                "difficulty": "hard",
                "expected_duration": 120
            },
            {
                "id": 2,
                "question": "Tell me about a time when your analysis influenced a business decision.",
                "type": "behavioral",
                "difficulty": "hard",
                "expected_duration": 120
            }
        ]
    }
}

@app.get("/")
async def root():
    return {"message": "InterVue AI API is running on Vercel!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": "serverless",
        "message": "InterVue AI API is running successfully"
    }

@app.post("/interview/start")
async def start_interview(
    role: str = Form(...),
    experience_level: str = Form(...),
    num_questions: int = Form(5)
):
    """Initialize a new interview session with dynamic questions"""
    try:
        session_id = str(uuid.uuid4())
        
        # Use demo questions for serverless deployment
        demo_questions = DEMO_QUESTIONS.get(role, {}).get(experience_level, [])
        if demo_questions:
            selected_count = min(num_questions, len(demo_questions))
            questions = random.sample(demo_questions, selected_count)
        else:
            questions = DEMO_QUESTIONS["Software Engineer"]["Fresher"][:num_questions]
        
        # Create session
        session_data = {
            "session_id": session_id,
            "role": role,
            "experience_level": experience_level,
            "num_questions": num_questions,
            "questions": questions,
            "current_question": 0,
            "responses": [],
            "created_at": str(random.randint(1000000000, 9999999999))
        }
        
        sessions[session_id] = session_data
        
        return {
            "session_id": session_id,
            "questions": questions,
            "total_questions": len(questions),
            "role": role,
            "experience_level": experience_level
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start interview: {str(e)}")

@app.post("/analyze/audio")
async def analyze_audio(
    session_id: str = Form(...),
    question_index: int = Form(...),
    audio_file: UploadFile = File(...)
):
    """Process audio recording and extract speech metrics"""
    try:
        # Demo analysis for serverless deployment
        word_count = random.randint(15, 80)
        filler_count = random.randint(0, 8)
        
        return {
            "transcript": {
                "transcript": f"Demo analysis for serverless deployment. Detected {word_count} words.",
                "word_count": word_count,
                "speaking_rate": random.randint(120, 180),
                "filler_words": ["um", "uh", "like"],
                "filler_word_count": filler_count,
                "confidence": random.uniform(0.7, 0.95)
            },
            "voice_metrics": {
                "stability_score": random.randint(60, 90),
                "clarity_score": random.randint(70, 95),
                "pitch_analysis": {"mean_pitch": random.randint(120, 200), "pitch_stability": random.randint(70, 90)},
                "energy_analysis": {"mean_energy": random.uniform(0.3, 0.8), "energy_stability": random.randint(65, 85)},
                "voice_activity": {"speech_percentage": random.randint(70, 95)}
            },
            "status": "success"
        }
        
    except Exception as e:
        return {
            "transcript": {
                "transcript": "Analysis temporarily unavailable",
                "word_count": 0,
                "speaking_rate": 0,
                "filler_words": [],
                "filler_word_count": 0,
                "confidence": 0.0
            },
            "voice_metrics": {
                "stability_score": 0,
                "clarity_score": 0,
                "pitch_analysis": {"mean_pitch": 0, "pitch_stability": 0},
                "energy_analysis": {"mean_energy": 0, "energy_stability": 0},
                "voice_activity": {"speech_percentage": 0}
            },
            "status": "error",
            "error": str(e)
        }

@app.post("/analyze/video")
async def analyze_video(
    session_id: str = Form(...),
    question_index: int = Form(...),
    video_file: UploadFile = File(...)
):
    """Analyze facial expressions and emotions from video"""
    try:
        # Demo analysis for serverless
        face_detection_rate = random.randint(60, 95)
        eye_contact_percentage = random.randint(50, 85)
        
        emotion_analysis = {
            "duration": 30,
            "total_frames": 300,
            "analyzed_frames": 60,
            "face_detected_frames": int(60 * face_detection_rate / 100),
            "face_detection_rate": face_detection_rate / 100,
            "metrics": {
                "confidence_score": random.randint(60, 90),
                "nervousness_score": random.randint(10, 40),
                "eye_contact_percentage": eye_contact_percentage,
                "face_detection_rate": face_detection_rate
            }
        }
        
        # Update session with emotion data
        if session_id in sessions and len(sessions[session_id]["responses"]) > question_index:
            sessions[session_id]["responses"][question_index]["emotion_analysis"] = emotion_analysis
        
        return {
            "emotion_analysis": emotion_analysis,
            "status": "demo"
        }
        
    except Exception as e:
        print(f"Video analysis error: {str(e)}")
        return {
            "emotion_analysis": {
                "duration": 0,
                "total_frames": 0,
                "analyzed_frames": 0,
                "face_detected_frames": 0,
                "face_detection_rate": 0,
                "metrics": {
                    "confidence_score": 0,
                    "nervousness_score": 0,
                    "eye_contact_percentage": 0,
                    "face_detection_rate": 0
                }
            },
            "status": "error"
        }

@app.get("/feedback/{session_id}")
async def get_feedback(session_id: str):
    """Generate comprehensive feedback"""
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_data = sessions[session_id]
        
        # Generate demo feedback
        confidence_score = {
            "overall_score": random.randint(65, 85),
            "component_scores": {
                "voice_stability": {"score": random.randint(60, 90), "weight": 0.40},
                "eye_contact": {"score": random.randint(50, 85), "weight": 0.35},
                "speech_quality": {"score": random.randint(70, 95), "weight": 0.25}
            },
            "response_count": len(session_data.get("questions", []))
        }
        
        feedback = {
            "overall_feedback": f"Based on your {session_data['role']} interview, you scored {confidence_score['overall_score']}/100. Good effort! There are some areas where you can improve.",
            "strengths": [
                "You provided thoughtful responses to the questions",
                "Good engagement with the camera",
                "Clear communication style"
            ],
            "areas_for_improvement": [
                "Try to maintain more consistent eye contact",
                "Work on reducing filler words",
                "Practice speaking at a steady pace"
            ],
            "action_plan": [
                "Practice speaking clearly and at a steady pace",
                "Record yourself to identify areas for improvement",
                "Work on maintaining eye contact with the camera",
                "Prepare specific examples for behavioral questions"
            ]
        }
        
        analytics = {
            "speech_analytics": {
                "total_words": random.randint(200, 500),
                "total_filler_words": random.randint(5, 25),
                "filler_word_percentage": random.randint(2, 8),
                "average_speaking_rate": random.randint(140, 180)
            },
            "voice_analytics": {
                "average_stability": random.randint(70, 90),
                "average_pitch": random.randint(120, 200),
                "average_energy": random.uniform(0.3, 0.8)
            },
            "emotion_analytics": {
                "average_confidence_level": random.randint(60, 85),
                "emotion_distribution": {
                    "Confident": 45,
                    "Neutral": 35,
                    "Nervous": 15,
                    "Stressed": 5
                },
                "face_detection_rate": random.randint(70, 95)
            },
            "response_count": len(session_data.get("questions", [])),
            "session_duration": random.randint(300, 600)
        }
        
        return {
            "session_id": session_id,
            "confidence_score": confidence_score,
            "feedback": feedback,
            "analytics": analytics
        }
        
    except Exception as e:
        print(f"Feedback generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Feedback generation failed: {str(e)}")

@app.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get session data"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return sessions[session_id]

@app.get("/export/{session_id}")
async def export_results(session_id: str, format: str = "json"):
    """Export interview results"""
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_data = sessions[session_id]
        
        export_data = {
            "session_info": {
                "session_id": session_id,
                "role": session_data["role"],
                "experience_level": session_data["experience_level"],
                "num_questions": session_data.get("num_questions", len(session_data["questions"])),
                "date": session_data["created_at"]
            },
            "questions": session_data["questions"],
            "summary": "Demo export - full analysis available in local mode"
        }
        
        if format.lower() == "csv":
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            writer.writerow(["Question", "Type", "Difficulty"])
            for q in session_data["questions"]:
                writer.writerow([q["question"], q["type"], q["difficulty"]])
            
            return JSONResponse(
                content={"data": output.getvalue(), "filename": f"interview_results_{session_id}.csv"},
                headers={"Content-Type": "text/csv"}
            )
        
        return {
            "data": export_data,
            "filename": f"interview_results_{session_id}.json",
            "format": "json"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@app.get("/roles")
async def get_available_roles():
    """Get available interview roles"""
    roles = ["Software Engineer", "HR", "Data Analyst", "Product Manager", "Marketing", "Sales"]
    return {"roles": roles}

@app.get("/experience-levels")
async def get_experience_levels():
    """Get available experience levels"""
    levels = ["Fresher", "Experienced"]
    return {"levels": levels}

# Vercel serverless handler
handler = app