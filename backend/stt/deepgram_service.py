"""
Deepgram Speech-to-Text Service
Converts audio recordings to text with timestamps
"""

import os
import asyncio
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
from typing import Dict, List, Optional
import json

class DeepgramSTTService:
    def __init__(self):
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPGRAM_API_KEY environment variable is required")
        
        self.client = DeepgramClient(self.api_key)
    
    async def transcribe_audio(self, audio_file_path: str) -> Dict:
        """
        Transcribe audio file to text with word-level timestamps
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Dict containing transcript, confidence, and word timestamps
        """
        try:
            # Read audio file
            with open(audio_file_path, "rb") as audio_file:
                buffer_data = audio_file.read()
            
            payload: FileSource = {
                "buffer": buffer_data,
            }
            
            # Configure transcription options
            options = PrerecordedOptions(
                model="nova-2",
                smart_format=True,
                punctuate=True,
                diarize=False,
                language="en-US",
                utterances=True,
                utt_split=0.8,
                dictation=True
            )
            
            # Make the transcription request
            response = self.client.listen.prerecorded.v("1").transcribe_file(
                payload, options
            )
            
            # Extract transcript and metadata
            result = response.to_dict()
            
            if not result.get("results", {}).get("channels", []):
                return {
                    "transcript": "",
                    "confidence": 0.0,
                    "word_count": 0,
                    "duration": 0.0,
                    "words": [],
                    "filler_words": []
                }
            
            channel = result["results"]["channels"][0]
            alternatives = channel.get("alternatives", [])
            
            if not alternatives:
                return {
                    "transcript": "",
                    "confidence": 0.0,
                    "word_count": 0,
                    "duration": 0.0,
                    "words": [],
                    "filler_words": []
                }
            
            best_alternative = alternatives[0]
            transcript = best_alternative.get("transcript", "")
            confidence = best_alternative.get("confidence", 0.0)
            
            # Extract word-level information
            words = best_alternative.get("words", [])
            word_count = len([w for w in words if w.get("word", "").strip()])
            
            # Calculate duration
            duration = 0.0
            if words:
                duration = words[-1].get("end", 0.0) - words[0].get("start", 0.0)
            
            # Detect filler words
            filler_words = self._detect_filler_words(words)
            
            return {
                "transcript": transcript,
                "confidence": confidence,
                "word_count": word_count,
                "duration": duration,
                "words": words,
                "filler_words": filler_words,
                "speaking_rate": self._calculate_speaking_rate(word_count, duration)
            }
            
        except Exception as e:
            print(f"Deepgram transcription error: {str(e)}")
            return {
                "transcript": "",
                "confidence": 0.0,
                "word_count": 0,
                "duration": 0.0,
                "words": [],
                "filler_words": [],
                "error": str(e)
            }
    
    def _detect_filler_words(self, words: List[Dict]) -> List[Dict]:
        """Detect filler words in the transcript"""
        filler_patterns = [
            "um", "uh", "like", "you know", "so", "well", 
            "actually", "basically", "literally", "right",
            "okay", "alright", "yeah", "yes", "no"
        ]
        
        filler_words = []
        for word_info in words:
            word = word_info.get("word", "").lower().strip()
            if word in filler_patterns:
                filler_words.append({
                    "word": word,
                    "start": word_info.get("start", 0),
                    "end": word_info.get("end", 0),
                    "confidence": word_info.get("confidence", 0)
                })
        
        return filler_words
    
    def _calculate_speaking_rate(self, word_count: int, duration: float) -> float:
        """Calculate words per minute (WPM)"""
        if duration <= 0:
            return 0.0
        
        # Convert duration from seconds to minutes
        duration_minutes = duration / 60.0
        return word_count / duration_minutes if duration_minutes > 0 else 0.0
    
    def get_transcript_statistics(self, transcript_data: Dict) -> Dict:
        """Get detailed statistics from transcript data"""
        words = transcript_data.get("words", [])
        filler_words = transcript_data.get("filler_words", [])
        
        # Calculate pauses (gaps between words > 0.5 seconds)
        pauses = []
        for i in range(len(words) - 1):
            current_end = words[i].get("end", 0)
            next_start = words[i + 1].get("start", 0)
            gap = next_start - current_end
            
            if gap > 0.5:  # Pause longer than 0.5 seconds
                pauses.append({
                    "start": current_end,
                    "end": next_start,
                    "duration": gap
                })
        
        return {
            "total_words": len(words),
            "filler_word_count": len(filler_words),
            "filler_word_percentage": (len(filler_words) / len(words) * 100) if words else 0,
            "pause_count": len(pauses),
            "total_pause_duration": sum(p["duration"] for p in pauses),
            "average_pause_duration": sum(p["duration"] for p in pauses) / len(pauses) if pauses else 0,
            "speaking_rate": transcript_data.get("speaking_rate", 0),
            "confidence": transcript_data.get("confidence", 0)
        }