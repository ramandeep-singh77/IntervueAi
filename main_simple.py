"""
InterVue AI - Simplified Railway Deployment
Minimal version to ensure deployment works
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys
import uuid
import random
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="InterVue AI",
    description="AI-powered interview practice platform",
    version="1.0.0"
)

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
DEMO_QUESTIONS = [
    {
        "id": 1,
        "question": "Tell me about yourself and why you're interested in this role.",
        "type": "behavioral",
        "difficulty": "easy",
        "expected_duration": 60
    },
    {
        "id": 2,
        "question": "What are your greatest strengths and how do they apply to this position?",
        "type": "behavioral",
        "difficulty": "medium",
        "expected_duration": 90
    },
    {
        "id": 3,
        "question": "Describe a challenging situation you faced and how you handled it.",
        "type": "behavioral",
        "difficulty": "medium",
        "expected_duration": 90
    },
    {
        "id": 4,
        "question": "Where do you see yourself in 5 years?",
        "type": "behavioral",
        "difficulty": "easy",
        "expected_duration": 60
    },
    {
        "id": 5,
        "question": "Why should we hire you for this position?",
        "type": "behavioral",
        "difficulty": "medium",
        "expected_duration": 90
    }
]

# API Routes
@app.get("/")
async def root():
    return {"message": "InterVue AI is running on Railway!", "status": "healthy", "environment": "railway"}

@app.get("/api/")
async def api_root():
    return {"message": "InterVue AI API", "status": "healthy", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": "railway",
        "version": "1.0.0",
        "message": "InterVue AI is running successfully"
    }

@app.post("/api/interview/start")
async def start_interview(
    role: str = Form(...),
    experience_level: str = Form(...),
    num_questions: int = Form(5)
):
    """Start a new interview session"""
    try:
        session_id = str(uuid.uuid4())
        
        # Use demo questions
        selected_questions = random.sample(DEMO_QUESTIONS, min(num_questions, len(DEMO_QUESTIONS)))
        
        # Create session
        session_data = {
            "session_id": session_id,
            "role": role,
            "experience_level": experience_level,
            "num_questions": num_questions,
            "questions": selected_questions,
            "current_question": 0,
            "responses": [],
            "created_at": str(uuid.uuid4())
        }
        
        sessions[session_id] = session_data
        
        return {
            "session_id": session_id,
            "questions": selected_questions,
            "total_questions": len(selected_questions),
            "role": role,
            "experience_level": experience_level
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start interview: {str(e)}")

@app.post("/api/analyze/audio")
async def analyze_audio(
    session_id: str = Form(...),
    question_index: int = Form(...),
    audio_file: UploadFile = File(...)
):
    """Analyze audio recording - demo version"""
    try:
        # Demo analysis
        word_count = random.randint(15, 80)
        filler_count = random.randint(0, 8)
        
        return {
            "transcript": {
                "transcript": f"Demo analysis: detected {word_count} words in your response.",
                "word_count": word_count,
                "speaking_rate": random.randint(120, 180),
                "filler_words": ["um", "uh", "like"],
                "filler_word_count": filler_count,
                "confidence": round(random.uniform(0.7, 0.95), 2)
            },
            "voice_metrics": {
                "stability_score": random.randint(70, 90),
                "clarity_score": random.randint(75, 95),
                "pitch_analysis": {"mean_pitch": random.randint(120, 200), "pitch_stability": random.randint(70, 90)},
                "energy_analysis": {"mean_energy": round(random.uniform(0.3, 0.8), 2), "energy_stability": random.randint(65, 85)},
                "voice_activity": {"speech_percentage": random.randint(70, 95)}
            },
            "status": "demo"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio analysis failed: {str(e)}")

@app.post("/api/analyze/video")
async def analyze_video(
    session_id: str = Form(...),
    question_index: int = Form(...),
    video_file: UploadFile = File(...)
):
    """Analyze video recording - demo version"""
    try:
        # Demo analysis
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
            "status": "demo"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video analysis failed: {str(e)}")

@app.get("/api/feedback/{session_id}")
async def get_feedback(session_id: str):
    """Generate feedback"""
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_data = sessions[session_id]
        overall_score = random.randint(65, 85)
        
        return {
            "session_id": session_id,
            "confidence_score": {"overall_score": overall_score},
            "feedback": {
                "overall_feedback": f"Based on your {session_data['role']} interview, you scored {overall_score}/100.",
                "strengths": ["Good participation", "Completed all questions"],
                "areas_for_improvement": ["Practice more", "Improve confidence"],
                "action_plan": ["Regular practice", "Focus on weak areas"]
            },
            "analytics": {
                "speech_analytics": {"total_words": 250, "average_speaking_rate": 150},
                "response_count": len(session_data.get("responses", []))
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback generation failed: {str(e)}")

@app.get("/api/roles")
async def get_available_roles():
    """Get available interview roles"""
    roles = ["Software Engineer", "HR", "Data Analyst", "Product Manager", "Marketing", "Sales"]
    return {"roles": roles}

@app.get("/api/experience-levels")
async def get_experience_levels():
    """Get available experience levels"""
    levels = ["Fresher", "Experienced"]
    return {"levels": levels}

# Serve React frontend if build exists
frontend_build_path = Path("frontend/build")
if frontend_build_path.exists() and (frontend_build_path / "index.html").exists():
    print("✅ Frontend build found - serving React app")
    
    # Mount static files
    static_path = frontend_build_path / "static"
    if static_path.exists():
        app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    
    @app.get("/{path:path}")
    async def serve_frontend(path: str):
        # Don't serve frontend for API routes
        if path.startswith("api"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # Serve specific files if they exist
        file_path = frontend_build_path / path
        if file_path.is_file():
            return FileResponse(str(file_path))
        
        # For all other routes, serve index.html (React Router)
        return FileResponse(str(frontend_build_path / "index.html"))
else:
    print("⚠️ Frontend build not found - API only mode")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting InterVue AI on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)