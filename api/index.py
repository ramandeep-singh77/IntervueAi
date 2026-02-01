from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uuid
import random
import json

app = FastAPI(title="InterVue AI API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
sessions = {}

# Demo questions
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
            }
        ],
        "Experienced": [
            {
                "id": 1,
                "question": "How do you develop and implement HR policies that align with business objectives?",
                "type": "technical",
                "difficulty": "hard",
                "expected_duration": 120
            }
        ]
    }
}

@app.get("/")
def root():
    return {"message": "InterVue AI API is running!", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": "serverless"}

@app.post("/interview/start")
def start_interview(
    role: str = Form(...),
    experience_level: str = Form(...),
    num_questions: int = Form(5)
):
    try:
        session_id = str(uuid.uuid4())
        
        # Get demo questions
        demo_questions = DEMO_QUESTIONS.get(role, {}).get(experience_level, [])
        if not demo_questions:
            demo_questions = DEMO_QUESTIONS["Software Engineer"]["Fresher"]
        
        selected_count = min(num_questions, len(demo_questions))
        questions = demo_questions[:selected_count]
        
        # Create session
        session_data = {
            "session_id": session_id,
            "role": role,
            "experience_level": experience_level,
            "questions": questions,
            "responses": []
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
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/audio")
def analyze_audio(
    session_id: str = Form(...),
    question_index: int = Form(...),
    audio_file: UploadFile = File(...)
):
    try:
        word_count = random.randint(15, 80)
        filler_count = random.randint(0, 8)
        
        return {
            "transcript": {
                "transcript": f"Demo analysis: detected {word_count} words in your response.",
                "word_count": word_count,
                "speaking_rate": random.randint(120, 180),
                "filler_words": ["um", "uh"],
                "filler_word_count": filler_count,
                "confidence": 0.85
            },
            "voice_metrics": {
                "stability_score": random.randint(70, 90),
                "clarity_score": random.randint(75, 95),
                "pitch_analysis": {"mean_pitch": 150, "pitch_stability": 80},
                "energy_analysis": {"mean_energy": 0.6, "energy_stability": 75},
                "voice_activity": {"speech_percentage": random.randint(70, 95)}
            },
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/video")
def analyze_video(
    session_id: str = Form(...),
    question_index: int = Form(...),
    video_file: UploadFile = File(...)
):
    try:
        face_detection_rate = random.randint(70, 95)
        eye_contact_percentage = random.randint(60, 85)
        
        return {
            "emotion_analysis": {
                "duration": 30,
                "total_frames": 300,
                "analyzed_frames": 60,
                "face_detected_frames": int(60 * face_detection_rate / 100),
                "face_detection_rate": face_detection_rate / 100,
                "metrics": {
                    "confidence_score": random.randint(65, 90),
                    "nervousness_score": random.randint(10, 35),
                    "eye_contact_percentage": eye_contact_percentage,
                    "face_detection_rate": face_detection_rate
                }
            },
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feedback/{session_id}")
def get_feedback(session_id: str):
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_data = sessions[session_id]
        overall_score = random.randint(65, 85)
        
        return {
            "session_id": session_id,
            "confidence_score": {
                "overall_score": overall_score,
                "component_scores": {
                    "voice_stability": {"score": random.randint(60, 90), "weight": 0.40},
                    "eye_contact": {"score": random.randint(50, 85), "weight": 0.35},
                    "speech_quality": {"score": random.randint(70, 95), "weight": 0.25}
                }
            },
            "feedback": {
                "overall_feedback": f"You scored {overall_score}/100 in your {session_data['role']} interview. Good effort!",
                "strengths": [
                    "Clear communication style",
                    "Good engagement with questions"
                ],
                "areas_for_improvement": [
                    "Practice maintaining eye contact",
                    "Work on reducing filler words"
                ],
                "action_plan": [
                    "Practice speaking clearly",
                    "Record yourself for improvement",
                    "Prepare specific examples"
                ]
            },
            "analytics": {
                "speech_analytics": {
                    "total_words": random.randint(200, 500),
                    "total_filler_words": random.randint(5, 25),
                    "filler_word_percentage": random.randint(2, 8),
                    "average_speaking_rate": random.randint(140, 180)
                },
                "voice_analytics": {
                    "average_stability": random.randint(70, 90),
                    "average_pitch": random.randint(120, 200),
                    "average_energy": round(random.uniform(0.3, 0.8), 2)
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
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session/{session_id}")
def get_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]

@app.get("/export/{session_id}")
def export_results(session_id: str, format: str = "json"):
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_data = sessions[session_id]
        
        export_data = {
            "session_info": {
                "session_id": session_id,
                "role": session_data["role"],
                "experience_level": session_data["experience_level"],
                "num_questions": len(session_data["questions"])
            },
            "questions": session_data["questions"],
            "summary": "Demo export for serverless deployment"
        }
        
        return {
            "data": export_data,
            "filename": f"interview_results_{session_id}.json",
            "format": "json"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/roles")
def get_available_roles():
    return {"roles": ["Software Engineer", "HR", "Data Analyst", "Product Manager"]}

@app.get("/experience-levels")
def get_experience_levels():
    return {"levels": ["Fresher", "Experienced"]}

# Vercel handler
handler = app