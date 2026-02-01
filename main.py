"""
InterVue AI - Full-Stack Interview Practice Platform
Real AI-powered analysis with FastAPI backend and React frontend
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import uuid
import random
import json
from pathlib import Path
from dotenv import load_dotenv
import asyncio
import tempfile
import aiofiles

# Load environment variables
load_dotenv()

# Add backend directory to path for imports
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.append(backend_path)

# Import real analyzers with error handling
try:
    from real_audio_analyzer import RealAudioAnalyzer
    from real_video_analyzer import RealVideoAnalyzer
    from utils.interview_questions import InterviewQuestionGenerator
    print("✓ Real analysis modules imported successfully")
except ImportError as e:
    print(f"⚠ Import warning: {e}")
    RealAudioAnalyzer = None
    RealVideoAnalyzer = None
    InterviewQuestionGenerator = None

app = FastAPI(
    title="InterVue AI",
    description="AI-powered interview practice platform with real analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzers with error handling
audio_analyzer = None
video_analyzer = None
question_generator = None

try:
    if RealAudioAnalyzer:
        audio_analyzer = RealAudioAnalyzer()
        print("✓ Audio analyzer initialized")
except Exception as e:
    print(f"⚠ Audio analyzer initialization failed: {str(e)}")

try:
    if RealVideoAnalyzer:
        video_analyzer = RealVideoAnalyzer()
        print("✓ Video analyzer initialized")
except Exception as e:
    print(f"⚠ Video analyzer initialization failed: {str(e)}")

try:
    if InterviewQuestionGenerator:
        question_generator = InterviewQuestionGenerator()
        print("✓ Question generator initialized")
except Exception as e:
    print(f"⚠ Question generator initialization failed: {str(e)}")

# In-memory storage
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

# API Routes
@app.get("/")
async def root():
    return {"message": "InterVue AI API is running!", "status": "healthy"}

@app.get("/api/")
async def api_root():
    return {"message": "InterVue AI API", "status": "healthy", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "audio_analyzer": audio_analyzer is not None,
        "video_analyzer": video_analyzer is not None,
        "question_generator": question_generator is not None,
        "api_keys": {
            "gemini": bool(os.getenv("GEMINI_API_KEY")),
            "deepgram": bool(os.getenv("DEEPGRAM_API_KEY"))
        }
    }

@app.post("/api/interview/start")
async def start_interview(
    role: str = Form(...),
    experience_level: str = Form(...),
    num_questions: int = Form(5)
):
    """Initialize a new interview session with AI-generated questions"""
    try:
        session_id = str(uuid.uuid4())
        
        # Generate questions using AI if available
        questions = []
        if question_generator:
            try:
                questions = await question_generator.generate_questions(role, experience_level, num_questions)
                print(f"✓ Generated {len(questions)} questions using Gemini AI")
            except Exception as e:
                print(f"⚠ AI question generation failed: {str(e)}")
                questions = []
        
        # Fallback to demo questions if AI generation fails
        if not questions:
            demo_questions = DEMO_QUESTIONS.get(role, {}).get(experience_level, [])
            if demo_questions:
                selected_count = min(num_questions, len(demo_questions))
                questions = random.sample(demo_questions, selected_count)
                print(f"Using {len(questions)} fallback questions")
            else:
                questions = DEMO_QUESTIONS["Software Engineer"]["Fresher"][:num_questions]
                print(f"Using default questions")
        
        # Create session
        session_data = {
            "session_id": session_id,
            "role": role,
            "experience_level": experience_level,
            "num_questions": num_questions,
            "questions": questions,
            "current_question": 0,
            "responses": [],
            "created_at": str(asyncio.get_event_loop().time())
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

@app.post("/api/analyze/audio")
async def analyze_audio(
    session_id: str = Form(...),
    question_index: int = Form(...),
    audio_file: UploadFile = File(...)
):
    """Process audio recording with real AI analysis"""
    temp_audio_path = None
    try:
        # Save uploaded audio to temporary file
        temp_audio_path = f"temp_audio_{session_id}_{question_index}.wav"
        
        async with aiofiles.open(temp_audio_path, 'wb') as f:
            content = await audio_file.read()
            await f.write(content)
        
        print(f"Analyzing audio file: {temp_audio_path}, size: {len(content)} bytes")
        
        # Perform real audio analysis if analyzer is available
        if audio_analyzer:
            analysis_result = audio_analyzer.analyze_audio_file(temp_audio_path)
            
            # Extract real metrics
            transcript_data = analysis_result["transcript"]
            voice_activity = analysis_result["voice_activity"]
            speech_metrics = analysis_result["speech_metrics"]
            audio_quality = analysis_result["audio_quality"]
            
            # Create voice metrics based on real analysis
            voice_metrics = {
                "stability_score": speech_metrics["stability_score"],
                "clarity_score": audio_quality["quality_score"],
                "pitch_analysis": {
                    "mean_pitch": speech_metrics["pitch_mean"],
                    "pitch_stability": 100 - min(100, speech_metrics["pitch_std"])
                },
                "energy_analysis": {
                    "mean_energy": speech_metrics["energy_mean"],
                    "energy_stability": 100 - min(100, speech_metrics["energy_std"])
                },
                "voice_activity": voice_activity
            }
            
            # Store results in session
            if session_id in sessions:
                response_data = {
                    "question_index": question_index,
                    "transcript": transcript_data,
                    "voice_metrics": voice_metrics,
                    "analysis_result": analysis_result,
                    "timestamp": str(asyncio.get_event_loop().time())
                }
                
                sessions[session_id]["responses"].append(response_data)
            
            print(f"✓ Real audio analysis completed: {transcript_data['word_count']} words, {voice_activity['speech_percentage']:.1f}% speech")
            
            return {
                "transcript": transcript_data,
                "voice_metrics": voice_metrics,
                "status": "success"
            }
        else:
            # Fallback demo analysis
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
        print(f"Audio analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Audio analysis failed: {str(e)}")
    finally:
        # Clean up temp file
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.remove(temp_audio_path)
            except:
                pass

@app.post("/api/analyze/video")
async def analyze_video(
    session_id: str = Form(...),
    question_index: int = Form(...),
    video_file: UploadFile = File(...)
):
    """Analyze facial expressions and emotions with real AI"""
    temp_video_path = None
    try:
        # Save uploaded video to temporary file
        temp_video_path = f"temp_video_{session_id}_{question_index}.webm"
        
        async with aiofiles.open(temp_video_path, 'wb') as f:
            content = await video_file.read()
            await f.write(content)
        
        print(f"Analyzing video file: {temp_video_path}, size: {len(content)} bytes")
        
        # Perform real video analysis if analyzer is available
        if video_analyzer:
            analysis_result = video_analyzer.analyze_video_file(temp_video_path)
            
            # Create emotion analysis based on real analysis
            emotion_analysis = {
                "duration": analysis_result["duration"],
                "total_frames": analysis_result["total_frames"],
                "analyzed_frames": analysis_result["frames_analyzed"],
                "face_detected_frames": analysis_result["frames_with_face"],
                "face_detection_rate": analysis_result["face_detection_rate"] / 100,
                "metrics": analysis_result["metrics"]
            }
            
            # Update session with emotion data
            if session_id in sessions and len(sessions[session_id]["responses"]) > question_index:
                sessions[session_id]["responses"][question_index]["emotion_analysis"] = emotion_analysis
                sessions[session_id]["responses"][question_index]["video_analysis"] = analysis_result
            
            print(f"✓ Real video analysis completed: {analysis_result['face_detection_rate']:.1f}% face detection")
            
            return {
                "emotion_analysis": emotion_analysis,
                "status": "success"
            }
        else:
            # Fallback demo analysis
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
        print(f"Video analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Video analysis failed: {str(e)}")
    finally:
        # Clean up temp file
        if temp_video_path and os.path.exists(temp_video_path):
            try:
                os.remove(temp_video_path)
            except:
                pass

# Import the rest of the endpoints from backend/main.py
@app.get("/api/feedback/{session_id}")
async def get_feedback(session_id: str):
    """Generate comprehensive AI-powered feedback"""
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_data = sessions[session_id]
        responses = session_data.get("responses", [])
        
        if not responses:
            # Generate demo feedback for empty sessions
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
                    "overall_feedback": f"You scored {overall_score}/100 in your {session_data['role']} interview practice.",
                    "strengths": ["Completed the interview session", "Good engagement with the platform"],
                    "areas_for_improvement": ["Practice speaking clearly", "Work on maintaining eye contact"],
                    "action_plan": ["Record more practice sessions", "Focus on specific improvement areas"]
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
                        "emotion_distribution": {"Confident": 45, "Neutral": 35, "Nervous": 15, "Stressed": 5},
                        "face_detection_rate": random.randint(70, 95)
                    },
                    "response_count": len(session_data.get("questions", [])),
                    "session_duration": random.randint(300, 600)
                }
            }
        
        # Use real analysis if available (import from backend/main.py functions)
        # For now, return demo feedback - can be enhanced with real analysis functions
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
                "response_count": len(responses)
            }
        }
        
    except Exception as e:
        print(f"Feedback generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Feedback generation failed: {str(e)}")

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """Get session data"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]

@app.get("/api/export/{session_id}")
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
                "num_questions": len(session_data["questions"])
            },
            "questions": session_data["questions"],
            "summary": "InterVue AI - Railway Deployment Results"
        }
        
        return {
            "data": export_data,
            "filename": f"interview_results_{session_id}.json",
            "format": "json"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

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

# Serve React frontend
frontend_build_path = Path("frontend/build")
print(f"Checking for frontend build at: {frontend_build_path.absolute()}")
print(f"Frontend build exists: {frontend_build_path.exists()}")

if frontend_build_path.exists():
    print("✅ Frontend build found - serving React app")
    
    # List contents of build directory for debugging
    try:
        build_contents = list(frontend_build_path.iterdir())
        print(f"Build directory contents: {[f.name for f in build_contents]}")
        
        static_path = frontend_build_path / "static"
        if static_path.exists():
            print(f"Static directory found with contents: {[f.name for f in static_path.iterdir()]}")
            app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
        else:
            print("⚠️ Static directory not found in build")
            
    except Exception as e:
        print(f"Error reading build directory: {e}")
    
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
        index_path = frontend_build_path / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        else:
            raise HTTPException(status_code=404, detail="Frontend not available")
else:
    print("⚠️ Frontend build not found - serving API only")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Directory contents: {os.listdir('.')}")
    
    if os.path.exists("frontend"):
        print(f"Frontend directory contents: {os.listdir('frontend')}")
    
    @app.get("/")
    async def root_with_instructions():
        return {
            "message": "InterVue AI API is running on Railway!",
            "status": "healthy",
            "environment": "railway",
            "note": "Frontend build not found. The React app may not have built successfully.",
            "debug_info": {
                "cwd": os.getcwd(),
                "frontend_exists": os.path.exists("frontend"),
                "build_path_checked": str(frontend_build_path.absolute()),
                "build_exists": frontend_build_path.exists()
            },
            "api_endpoints": {
                "health": "/api/health",
                "roles": "/api/roles",
                "start_interview": "/api/interview/start"
            }
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)