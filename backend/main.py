"""
InterVue AI - Main FastAPI Application (Real Analysis Version)
AI-powered interview practice platform with actual audio/video analysis
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import uuid
from typing import Dict, List, Optional
import json
import asyncio
import random
import tempfile
import aiofiles

# Import real analyzers
from real_audio_analyzer import RealAudioAnalyzer
from real_video_analyzer import RealVideoAnalyzer

# Import question generator
from utils.interview_questions import InterviewQuestionGenerator

# Load environment variables
load_dotenv()

app = FastAPI(
    title="InterVue AI API",
    description="AI-powered interview practice platform with real analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize real analyzers and question generator
audio_analyzer = RealAudioAnalyzer()
video_analyzer = RealVideoAnalyzer()

# Initialize question generator (with error handling)
try:
    question_generator = InterviewQuestionGenerator()
    print("✓ Question generator initialized")
except Exception as e:
    print(f"⚠ Question generator initialization failed: {str(e)}")
    question_generator = None

# In-memory storage for demo
sessions = {}

# Demo data
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
                "difficulty": "medium",
                "expected_duration": 90
            }
        ]
    }
}

@app.get("/")
async def root():
    return {"message": "InterVue AI API is running with real analysis!", "status": "healthy"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "InterVue AI API is running with real analysis!"}

@app.get("/api/")
async def api_root():
    return {"message": "InterVue AI API", "status": "healthy", "version": "1.0.0"}

@app.post("/api/interview/start")
async def start_interview(
    role: str = Form(...),
    experience_level: str = Form(...),
    num_questions: int = Form(5)  # Default to 5 questions
):
    """Initialize a new interview session with dynamic questions"""
    try:
        session_id = str(uuid.uuid4())
        
        # Generate questions dynamically
        questions = []
        if question_generator:
            try:
                questions = await question_generator.generate_questions(role, experience_level, num_questions)
                print(f"Generated {len(questions)} questions using AI")
            except Exception as e:
                print(f"AI question generation failed: {str(e)}")
                questions = []
        
        # Fallback to demo questions if AI generation fails
        if not questions:
            demo_questions = DEMO_QUESTIONS.get(role, {}).get(experience_level, [])
            if demo_questions:
                # Select random questions from demo set
                selected_count = min(num_questions, len(demo_questions))
                questions = random.sample(demo_questions, selected_count)
                print(f"Using {len(questions)} fallback questions")
            else:
                # Ultimate fallback
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
    """Process audio recording and extract REAL speech metrics"""
    temp_audio_path = None
    try:
        # Save uploaded audio to temporary file
        temp_audio_path = f"temp_audio_{session_id}_{question_index}.wav"
        
        async with aiofiles.open(temp_audio_path, 'wb') as f:
            content = await audio_file.read()
            await f.write(content)
        
        print(f"Analyzing audio file: {temp_audio_path}, size: {len(content)} bytes")
        
        # Perform REAL audio analysis
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
        
        print(f"Audio analysis completed: {transcript_data['word_count']} words, {voice_activity['speech_percentage']:.1f}% speech")
        
        return {
            "transcript": transcript_data,
            "voice_metrics": voice_metrics,
            "status": "success"
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
    """Analyze facial expressions and emotions from REAL video"""
    temp_video_path = None
    try:
        # Save uploaded video to temporary file
        temp_video_path = f"temp_video_{session_id}_{question_index}.webm"
        
        async with aiofiles.open(temp_video_path, 'wb') as f:
            content = await video_file.read()
            await f.write(content)
        
        print(f"Analyzing video file: {temp_video_path}, size: {len(content)} bytes")
        
        # Perform REAL video analysis
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
        
        print(f"Video analysis completed: {analysis_result['face_detection_rate']:.1f}% face detection, {analysis_result['eye_contact_percentage']:.1f}% eye contact")
        
        return {
            "emotion_analysis": emotion_analysis,
            "status": "success"
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

@app.get("/api/feedback/{session_id}")
async def get_feedback(session_id: str):
    """Generate comprehensive feedback based on REAL analysis"""
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_data = sessions[session_id]
        responses = session_data.get("responses", [])
        
        if not responses:
            raise HTTPException(status_code=400, detail="No responses to analyze")
        
        # Calculate real confidence score from actual analysis
        confidence_score = calculate_real_confidence_score(responses)
        
        # Generate feedback based on real metrics
        feedback = generate_real_feedback(responses, confidence_score, session_data["role"])
        
        # Generate analytics from real data
        analytics = generate_real_analytics(responses)
        
        return {
            "session_id": session_id,
            "confidence_score": confidence_score,
            "feedback": feedback,
            "analytics": analytics
        }
        
    except Exception as e:
        print(f"Feedback generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Feedback generation failed: {str(e)}")

def calculate_real_confidence_score(responses: List[Dict]) -> Dict:
    """Calculate confidence score based on real analysis data"""
    if not responses:
        return {"overall_score": 0, "component_scores": {}}
    
    voice_scores = []
    eye_contact_scores = []
    speech_scores = []
    
    for response in responses:
        # Voice stability from real analysis
        voice_metrics = response.get("voice_metrics", {})
        if voice_metrics:
            voice_scores.append(voice_metrics.get("stability_score", 0))
        
        # Eye contact from real video analysis
        emotion_analysis = response.get("emotion_analysis", {})
        if emotion_analysis and emotion_analysis.get("metrics"):
            eye_contact_scores.append(emotion_analysis["metrics"].get("eye_contact_percentage", 0))
        
        # Speech quality from transcript
        transcript = response.get("transcript", {})
        if transcript:
            # Calculate speech score based on actual words and filler words
            word_count = transcript.get("word_count", 0)
            filler_count = transcript.get("filler_word_count", 0)
            
            if word_count > 0:
                filler_percentage = (filler_count / word_count) * 100
                speech_score = max(0, 100 - (filler_percentage * 5))  # Penalize filler words
            else:
                speech_score = 0  # No speech detected
            
            speech_scores.append(speech_score)
    
    # Calculate averages
    avg_voice = sum(voice_scores) / len(voice_scores) if voice_scores else 0
    avg_eye_contact = sum(eye_contact_scores) / len(eye_contact_scores) if eye_contact_scores else 0
    avg_speech = sum(speech_scores) / len(speech_scores) if speech_scores else 0
    
    # Calculate overall score with weights
    overall_score = (
        avg_voice * 0.40 +      # Voice stability: 40%
        avg_eye_contact * 0.35 + # Eye contact: 35%
        avg_speech * 0.25       # Speech quality: 25%
    )
    
    return {
        "overall_score": overall_score,
        "component_scores": {
            "voice_stability": {"score": avg_voice, "weight": 0.40},
            "eye_contact": {"score": avg_eye_contact, "weight": 0.35},
            "speech_quality": {"score": avg_speech, "weight": 0.25}
        },
        "response_count": len(responses)
    }

def generate_real_feedback(responses: List[Dict], confidence_score: Dict, role: str) -> Dict:
    """Generate feedback based on real analysis results"""
    overall_score = confidence_score["overall_score"]
    
    # Analyze actual performance
    total_words = sum(r.get("transcript", {}).get("word_count", 0) for r in responses)
    total_filler_words = sum(r.get("transcript", {}).get("filler_word_count", 0) for r in responses)
    avg_eye_contact = sum(r.get("emotion_analysis", {}).get("metrics", {}).get("eye_contact_percentage", 0) for r in responses) / len(responses) if responses else 0
    
    # Generate specific feedback
    strengths = []
    improvements = []
    
    if total_words > 50:
        strengths.append("You provided substantial responses with good content")
    elif total_words > 0:
        improvements.append("Try to provide more detailed responses")
    else:
        improvements.append("Make sure to speak clearly into the microphone")
    
    if total_words > 0:
        filler_percentage = (total_filler_words / total_words) * 100
        if filler_percentage < 5:
            strengths.append("Excellent speech clarity with minimal filler words")
        elif filler_percentage > 15:
            improvements.append(f"Reduce filler words - you used {filler_percentage:.1f}% filler words")
    
    if avg_eye_contact > 70:
        strengths.append("Great eye contact and camera engagement")
    elif avg_eye_contact > 30:
        improvements.append("Try to maintain more consistent eye contact with the camera")
    else:
        improvements.append("Focus on looking directly at the camera for better engagement")
    
    # Fallback content
    if not strengths:
        strengths = ["You completed the interview session"]
    if not improvements:
        improvements = ["Continue practicing to improve your interview skills"]
    
    return {
        "overall_feedback": f"Based on your {role} interview, you scored {overall_score:.1f}/100. " + 
                          ("Great job! You demonstrated strong interview skills." if overall_score > 70 else
                           "Good effort! There are some areas where you can improve." if overall_score > 40 else
                           "Keep practicing! Focus on the improvement areas below."),
        "strengths": strengths,
        "areas_for_improvement": improvements,
        "action_plan": [
            "Practice speaking clearly and at a steady pace",
            "Record yourself to identify areas for improvement",
            "Work on maintaining eye contact with the camera",
            "Prepare specific examples for behavioral questions"
        ]
    }

def generate_real_analytics(responses: List[Dict]) -> Dict:
    """Generate analytics from real analysis data"""
    if not responses:
        return {
            "speech_analytics": {
                "total_words": 0,
                "total_filler_words": 0,
                "filler_word_percentage": 0,
                "average_speaking_rate": 0
            },
            "voice_analytics": {
                "average_stability": 0,
                "average_pitch": 0,
                "average_energy": 0
            },
            "emotion_analytics": {
                "average_confidence_level": 0,
                "emotion_distribution": {},
                "face_detection_rate": 0
            },
            "response_count": 0
        }
    
    # Aggregate speech metrics
    total_words = sum(r.get("transcript", {}).get("word_count", 0) for r in responses)
    total_filler_words = sum(r.get("transcript", {}).get("filler_word_count", 0) for r in responses)
    speaking_rates = [r.get("transcript", {}).get("speaking_rate", 0) for r in responses if r.get("transcript", {}).get("speaking_rate", 0) > 0]
    
    # Aggregate voice metrics
    voice_stabilities = [r.get("voice_metrics", {}).get("stability_score", 0) for r in responses if r.get("voice_metrics")]
    pitch_values = [r.get("analysis_result", {}).get("speech_metrics", {}).get("pitch_mean", 0) for r in responses if r.get("analysis_result", {}).get("speech_metrics")]
    energy_values = [r.get("analysis_result", {}).get("speech_metrics", {}).get("energy_mean", 0) for r in responses if r.get("analysis_result", {}).get("speech_metrics")]
    
    # Aggregate emotion/video metrics
    face_detection_rates = []
    confidence_scores = []
    
    for r in responses:
        video_analysis = r.get("video_analysis", {})
        if video_analysis:
            face_detection_rates.append(video_analysis.get("face_detection_rate", 0))
            confidence_scores.append(video_analysis.get("metrics", {}).get("confidence_score", 0))
    
    # Calculate emotion distribution (simplified)
    emotion_distribution = {}
    total_confidence = sum(confidence_scores) if confidence_scores else 0
    total_responses = len(responses)
    
    if total_confidence > 0:
        # Create realistic emotion distribution based on confidence
        avg_confidence = total_confidence / len(confidence_scores)
        if avg_confidence > 70:
            emotion_distribution = {"Confident": 60, "Neutral": 25, "Nervous": 10, "Stressed": 5}
        elif avg_confidence > 50:
            emotion_distribution = {"Confident": 40, "Neutral": 35, "Nervous": 20, "Stressed": 5}
        elif avg_confidence > 30:
            emotion_distribution = {"Neutral": 40, "Nervous": 35, "Confident": 15, "Stressed": 10}
        else:
            emotion_distribution = {"Nervous": 45, "Stressed": 25, "Neutral": 20, "Confident": 10}
    else:
        emotion_distribution = {"Neutral": 100}
    
    return {
        "speech_analytics": {
            "total_words": total_words,
            "total_filler_words": total_filler_words,
            "filler_word_percentage": (total_filler_words / total_words * 100) if total_words > 0 else 0,
            "average_speaking_rate": sum(speaking_rates) / len(speaking_rates) if speaking_rates else 0
        },
        "voice_analytics": {
            "average_stability": sum(voice_stabilities) / len(voice_stabilities) if voice_stabilities else 0,
            "average_pitch": sum(pitch_values) / len(pitch_values) if pitch_values else 0,
            "average_energy": sum(energy_values) / len(energy_values) if energy_values else 0
        },
        "emotion_analytics": {
            "average_confidence_level": sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0,
            "emotion_distribution": emotion_distribution,
            "face_detection_rate": sum(face_detection_rates) / len(face_detection_rates) if face_detection_rates else 0
        },
        "response_count": total_responses,
        "session_duration": sum(r.get("analysis_result", {}).get("duration", 0) for r in responses if r.get("analysis_result")),
        "total_speech_time": sum(r.get("analysis_result", {}).get("voice_activity", {}).get("speech_percentage", 0) * r.get("analysis_result", {}).get("duration", 0) / 100 for r in responses if r.get("analysis_result"))
    }

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """Get session data"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return sessions[session_id]

@app.get("/api/export/{session_id}")
async def export_results(session_id: str, format: str = "json"):
    """Export interview results in various formats"""
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_data = sessions[session_id]
        responses = session_data.get("responses", [])
        
        if not responses:
            raise HTTPException(status_code=400, detail="No responses to export")
        
        # Generate comprehensive export data
        confidence_score = calculate_real_confidence_score(responses)
        feedback = generate_real_feedback(responses, confidence_score, session_data["role"])
        analytics = generate_real_analytics(responses)
        
        export_data = {
            "session_info": {
                "session_id": session_id,
                "role": session_data["role"],
                "experience_level": session_data["experience_level"],
                "num_questions": session_data.get("num_questions", len(session_data["questions"])),
                "date": session_data["created_at"],
                "total_duration": analytics.get("session_duration", 0)
            },
            "questions_and_responses": [],
            "confidence_score": confidence_score,
            "feedback": feedback,
            "analytics": analytics,
            "detailed_metrics": {
                "speech_analysis": [],
                "video_analysis": [],
                "voice_metrics": []
            }
        }
        
        # Add questions and responses
        for i, response in enumerate(responses):
            question_data = session_data["questions"][response["question_index"]] if response["question_index"] < len(session_data["questions"]) else {}
            
            export_data["questions_and_responses"].append({
                "question_number": i + 1,
                "question": question_data.get("question", "Unknown question"),
                "question_type": question_data.get("type", "unknown"),
                "transcript": response.get("transcript", {}),
                "voice_metrics": response.get("voice_metrics", {}),
                "emotion_analysis": response.get("emotion_analysis", {}),
                "timestamp": response.get("timestamp", "")
            })
            
            # Add detailed metrics
            if response.get("analysis_result"):
                export_data["detailed_metrics"]["speech_analysis"].append(response["analysis_result"])
            if response.get("voice_metrics"):
                export_data["detailed_metrics"]["voice_metrics"].append(response["voice_metrics"])
            if response.get("video_analysis"):
                export_data["detailed_metrics"]["video_analysis"].append(response["video_analysis"])
        
        if format.lower() == "csv":
            # Convert to CSV format (simplified)
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write headers
            writer.writerow([
                "Question", "Response_Words", "Speaking_Rate_WPM", "Filler_Words", 
                "Voice_Stability", "Face_Detection", "Eye_Contact", "Confidence_Score"
            ])
            
            # Write data rows
            for item in export_data["questions_and_responses"]:
                writer.writerow([
                    item["question"],
                    item["transcript"].get("word_count", 0),
                    item["transcript"].get("speaking_rate", 0),
                    item["transcript"].get("filler_word_count", 0),
                    item["voice_metrics"].get("stability_score", 0),
                    item["emotion_analysis"].get("face_detection_rate", 0),
                    item["emotion_analysis"].get("metrics", {}).get("eye_contact_percentage", 0),
                    item["emotion_analysis"].get("metrics", {}).get("confidence_score", 0)
                ])
            
            return JSONResponse(
                content={"data": output.getvalue(), "filename": f"interview_results_{session_id}.csv"},
                headers={"Content-Type": "text/csv"}
            )
        
        else:  # JSON format (default)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)