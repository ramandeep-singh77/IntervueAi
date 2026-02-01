"""
Session Manager
Manages interview session data and state
"""

from typing import Dict, Optional
import json
import os
from datetime import datetime, timedelta

class SessionManager:
    def __init__(self):
        self.sessions = {}  # In-memory storage for demo purposes
        self.session_timeout = timedelta(hours=2)  # Sessions expire after 2 hours
    
    def create_session(self, session_id: str, session_data: Dict) -> bool:
        """
        Create a new interview session
        
        Args:
            session_id: Unique session identifier
            session_data: Session data dictionary
            
        Returns:
            bool: True if session created successfully
        """
        try:
            # Add timestamp and metadata
            session_data.update({
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "status": "active"
            })
            
            self.sessions[session_id] = session_data
            return True
            
        except Exception as e:
            print(f"Error creating session {session_id}: {str(e)}")
            return False
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Retrieve session data
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dict or None: Session data if found and not expired
        """
        if session_id not in self.sessions:
            return None
        
        session_data = self.sessions[session_id]
        
        # Check if session has expired
        try:
            created_at = datetime.fromisoformat(session_data.get("created_at", ""))
            if datetime.now() - created_at > self.session_timeout:
                # Session expired, remove it
                del self.sessions[session_id]
                return None
        except (ValueError, TypeError):
            # Invalid timestamp, keep session but update timestamp
            session_data["created_at"] = datetime.now().isoformat()
        
        return session_data
    
    def update_session(self, session_id: str, session_data: Dict) -> bool:
        """
        Update existing session data
        
        Args:
            session_id: Session identifier
            session_data: Updated session data
            
        Returns:
            bool: True if updated successfully
        """
        if session_id not in self.sessions:
            return False
        
        try:
            # Update timestamp
            session_data["last_updated"] = datetime.now().isoformat()
            self.sessions[session_id] = session_data
            return True
            
        except Exception as e:
            print(f"Error updating session {session_id}: {str(e)}")
            return False
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            bool: True if deleted successfully
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def list_sessions(self) -> Dict[str, Dict]:
        """
        List all active sessions
        
        Returns:
            Dict: Dictionary of session_id -> session_data
        """
        # Clean up expired sessions first
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session_data in self.sessions.items():
            try:
                created_at = datetime.fromisoformat(session_data.get("created_at", ""))
                if current_time - created_at > self.session_timeout:
                    expired_sessions.append(session_id)
            except (ValueError, TypeError):
                continue
        
        # Remove expired sessions
        for session_id in expired_sessions:
            del self.sessions[session_id]
        
        return self.sessions.copy()
    
    def get_session_summary(self, session_id: str) -> Optional[Dict]:
        """
        Get a summary of session data (without full response details)
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dict or None: Session summary if found
        """
        session_data = self.get_session(session_id)
        if not session_data:
            return None
        
        # Create summary without heavy data
        summary = {
            "session_id": session_id,
            "role": session_data.get("role", "Unknown"),
            "experience_level": session_data.get("experience_level", "Unknown"),
            "created_at": session_data.get("created_at", ""),
            "last_updated": session_data.get("last_updated", ""),
            "status": session_data.get("status", "unknown"),
            "total_questions": len(session_data.get("questions", [])),
            "completed_responses": len(session_data.get("responses", [])),
            "current_question": session_data.get("current_question", 0)
        }
        
        return summary
    
    def update_session_status(self, session_id: str, status: str) -> bool:
        """
        Update session status
        
        Args:
            session_id: Session identifier
            status: New status (active, completed, paused, etc.)
            
        Returns:
            bool: True if updated successfully
        """
        if session_id not in self.sessions:
            return False
        
        try:
            self.sessions[session_id]["status"] = status
            self.sessions[session_id]["last_updated"] = datetime.now().isoformat()
            return True
        except Exception as e:
            print(f"Error updating session status {session_id}: {str(e)}")
            return False
    
    def add_response_to_session(self, session_id: str, response_data: Dict) -> bool:
        """
        Add a response to an existing session
        
        Args:
            session_id: Session identifier
            response_data: Response data to add
            
        Returns:
            bool: True if added successfully
        """
        session_data = self.get_session(session_id)
        if not session_data:
            return False
        
        try:
            # Initialize responses list if it doesn't exist
            if "responses" not in session_data:
                session_data["responses"] = []
            
            # Add timestamp to response
            response_data["timestamp"] = datetime.now().isoformat()
            
            # Add response
            session_data["responses"].append(response_data)
            
            # Update current question index
            session_data["current_question"] = len(session_data["responses"])
            
            # Update session
            return self.update_session(session_id, session_data)
            
        except Exception as e:
            print(f"Error adding response to session {session_id}: {str(e)}")
            return False
    
    def get_session_progress(self, session_id: str) -> Optional[Dict]:
        """
        Get session progress information
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dict or None: Progress information
        """
        session_data = self.get_session(session_id)
        if not session_data:
            return None
        
        total_questions = len(session_data.get("questions", []))
        completed_responses = len(session_data.get("responses", []))
        current_question = session_data.get("current_question", 0)
        
        progress_percentage = (completed_responses / total_questions * 100) if total_questions > 0 else 0
        
        return {
            "session_id": session_id,
            "total_questions": total_questions,
            "completed_responses": completed_responses,
            "current_question_index": current_question,
            "progress_percentage": round(progress_percentage, 1),
            "is_completed": completed_responses >= total_questions,
            "remaining_questions": max(0, total_questions - completed_responses)
        }
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions
        
        Returns:
            int: Number of sessions cleaned up
        """
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session_data in self.sessions.items():
            try:
                created_at = datetime.fromisoformat(session_data.get("created_at", ""))
                if current_time - created_at > self.session_timeout:
                    expired_sessions.append(session_id)
            except (ValueError, TypeError):
                # Invalid timestamp, consider it expired
                expired_sessions.append(session_id)
        
        # Remove expired sessions
        for session_id in expired_sessions:
            del self.sessions[session_id]
        
        return len(expired_sessions)
    
    def export_session_data(self, session_id: str) -> Optional[str]:
        """
        Export session data as JSON string
        
        Args:
            session_id: Session identifier
            
        Returns:
            str or None: JSON string of session data
        """
        session_data = self.get_session(session_id)
        if not session_data:
            return None
        
        try:
            return json.dumps(session_data, indent=2, default=str)
        except Exception as e:
            print(f"Error exporting session {session_id}: {str(e)}")
            return None