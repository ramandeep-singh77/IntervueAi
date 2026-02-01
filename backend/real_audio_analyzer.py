"""
Real Audio Analysis Module
Analyzes actual audio recordings for speech patterns, silence, and voice characteristics
"""

import librosa
import numpy as np
import soundfile as sf
import speech_recognition as sr
import os
import subprocess
from typing import Dict, List, Tuple
import tempfile

# Conditional imports for serverless compatibility
try:
    from pydub import AudioSegment
    from pydub.utils import which
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("Warning: pydub not available, using basic audio processing")

class RealAudioAnalyzer:
    def __init__(self):
        self.sample_rate = 16000  # Standard for speech recognition
        self.frame_duration = 30  # ms
        self.energy_threshold = 0.01  # Energy threshold for voice activity detection
        
        # Check if ffmpeg is available for format conversion
        self.has_ffmpeg = which("ffmpeg") is not None or os.path.exists("ffmpeg.exe") if PYDUB_AVAILABLE else False
        if self.has_ffmpeg:
            print("✓ FFmpeg found - WebM conversion available")
        else:
            print("⚠ FFmpeg not found - using basic audio processing")
            
        # Set ffmpeg path for pydub if local ffmpeg.exe exists
        if PYDUB_AVAILABLE and os.path.exists("ffmpeg.exe"):
            AudioSegment.converter = os.path.abspath("ffmpeg.exe")
            AudioSegment.ffmpeg = os.path.abspath("ffmpeg.exe")
            AudioSegment.ffprobe = os.path.abspath("ffmpeg.exe")
        
    def _convert_audio_format(self, input_path: str) -> str:
        """Convert audio file to WAV format if needed"""
        try:
            # Check if file is already WAV
            if input_path.lower().endswith('.wav'):
                return input_path
            
            print(f"Converting audio format: {input_path}")
            
            # Create temporary WAV file
            temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_wav.close()
            
            # Method 1: Try direct ffmpeg conversion (if available)
            if self.has_ffmpeg and os.path.exists("ffmpeg.exe"):
                try:
                    print("Using direct ffmpeg conversion...")
                    cmd = [
                        "ffmpeg.exe",
                        "-i", input_path,
                        "-ar", str(self.sample_rate),  # Set sample rate to 16kHz
                        "-ac", "1",  # Convert to mono
                        "-y",  # Overwrite output file
                        temp_wav.name
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print(f"✓ FFmpeg conversion successful: {temp_wav.name}")
                        return temp_wav.name
                    else:
                        print(f"FFmpeg conversion failed: {result.stderr}")
                        
                except Exception as e:
                    print(f"FFmpeg subprocess failed: {str(e)}")
            
            # Method 2: Try pydub (if available)
            if PYDUB_AVAILABLE:
                try:
                    print("Trying pydub conversion...")
                    if input_path.lower().endswith('.webm'):
                        audio = AudioSegment.from_file(input_path, format="webm")
                    else:
                        audio = AudioSegment.from_file(input_path)
                    
                    # Convert to mono and set sample rate
                    audio = audio.set_channels(1)  # Mono
                    audio = audio.set_frame_rate(self.sample_rate)  # 16kHz
                    
                    # Export as WAV
                    audio.export(temp_wav.name, format="wav")
                    print(f"✓ Pydub conversion successful: {temp_wav.name}")
                    
                    return temp_wav.name
                    
                except Exception as e:
                    print(f"Pydub conversion failed: {str(e)}")
            
            # Method 3: Try direct librosa load with audioread
            try:
                print("Trying direct librosa load...")
                audio_data, sr = librosa.load(input_path, sr=self.sample_rate)
                
                # Save as WAV
                sf.write(temp_wav.name, audio_data, self.sample_rate)
                print(f"✓ Direct librosa conversion successful: {temp_wav.name}")
                
                return temp_wav.name
                
            except Exception as e2:
                print(f"Direct librosa load failed: {str(e2)}")
                # Return original file as last resort
                return input_path
            
        except Exception as e:
            print(f"All audio conversion methods failed: {str(e)}")
            # If conversion fails, try to use original file
            return input_path

    def analyze_audio_file(self, audio_file_path: str) -> Dict:
        """
        Analyze actual audio file for real speech metrics
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Dict containing real analysis results
        """
        converted_path = None
        try:
            print(f"Loading audio file: {audio_file_path}")
            
            # Convert audio format if needed
            try:
                converted_path = self._convert_audio_format(audio_file_path)
            except Exception as e:
                print(f"Format conversion failed, using original: {str(e)}")
                converted_path = audio_file_path
            
            # Load audio file
            audio_data, original_sr = librosa.load(converted_path, sr=None)
            
            print(f"Audio loaded: {len(audio_data)} samples at {original_sr}Hz")
            
            if len(audio_data) == 0:
                print("Audio file is empty")
                return self._empty_analysis()
            
            # Resample to 16kHz for speech processing
            if original_sr != self.sample_rate:
                print(f"Resampling from {original_sr}Hz to {self.sample_rate}Hz")
                audio_data = librosa.resample(audio_data, orig_sr=original_sr, target_sr=self.sample_rate)
            
            duration = len(audio_data) / self.sample_rate
            print(f"Audio duration: {duration:.2f}s")
            
            # Check audio levels
            max_amplitude = np.max(np.abs(audio_data))
            rms_level = np.sqrt(np.mean(audio_data ** 2))
            print(f"Audio levels - Max: {max_amplitude:.4f}, RMS: {rms_level:.4f}")
            
            # Perform various analyses
            transcript_data = self._transcribe_audio(audio_data)
            voice_activity = self._detect_voice_activity(audio_data)
            speech_metrics = self._analyze_speech_patterns(audio_data, voice_activity)
            audio_quality = self._analyze_audio_quality(audio_data)
            
            result = {
                "duration": duration,
                "transcript": transcript_data,
                "voice_activity": voice_activity,
                "speech_metrics": speech_metrics,
                "audio_quality": audio_quality,
                "has_speech": voice_activity["speech_percentage"] > 5.0  # At least 5% speech
            }
            
            print(f"Analysis complete - Words: {transcript_data['word_count']}, Speech: {voice_activity['speech_percentage']:.1f}%")
            return result
            
        except Exception as e:
            print(f"Audio analysis error: {str(e)}")
            import traceback
            traceback.print_exc()
            return self._empty_analysis()
        finally:
            # Clean up converted file if it was created
            if converted_path and converted_path != audio_file_path:
                try:
                    os.unlink(converted_path)
                except:
                    pass
    
    def _transcribe_audio(self, audio_data: np.ndarray) -> Dict:
        """Transcribe audio using speech recognition"""
        try:
            # Save audio to temporary WAV file for speech recognition
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                sf.write(temp_file.name, audio_data, self.sample_rate)
                temp_path = temp_file.name
            
            print(f"Transcribing audio: {len(audio_data)} samples, {len(audio_data)/self.sample_rate:.2f}s duration")
            
            # Use speech recognition
            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_path) as source:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.record(source)
            
            try:
                # Try to recognize speech
                print("Attempting speech recognition...")
                text = recognizer.recognize_google(audio)
                print(f"Speech recognized: '{text}'")
                
                words = text.split()
                word_count = len(words)
                
                # Calculate speaking rate (WPM)
                duration_minutes = len(audio_data) / self.sample_rate / 60.0
                speaking_rate = word_count / duration_minutes if duration_minutes > 0 else 0
                
                # Detect filler words
                filler_words = self._detect_filler_words(words)
                
                result = {
                    "transcript": text,
                    "word_count": word_count,
                    "speaking_rate": speaking_rate,
                    "filler_words": filler_words,
                    "filler_word_count": len(filler_words),
                    "confidence": 0.8  # Approximate confidence
                }
                
            except sr.UnknownValueError:
                # No speech detected
                print("No speech could be recognized")
                result = {
                    "transcript": "",
                    "word_count": 0,
                    "speaking_rate": 0,
                    "filler_words": [],
                    "filler_word_count": 0,
                    "confidence": 0.0
                }
            except sr.RequestError as e:
                print(f"Speech recognition service error: {e}")
                result = {
                    "transcript": "",
                    "word_count": 0,
                    "speaking_rate": 0,
                    "filler_words": [],
                    "filler_word_count": 0,
                    "confidence": 0.0
                }
            
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass
            return result
            
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "transcript": "",
                "word_count": 0,
                "speaking_rate": 0,
                "filler_words": [],
                "filler_word_count": 0,
                "confidence": 0.0
            }
    
    def _detect_voice_activity(self, audio_data: np.ndarray) -> Dict:
        """Detect voice activity in audio using energy-based detection"""
        try:
            # Frame size for analysis (30ms at 16kHz = 480 samples)
            frame_size = int(self.sample_rate * self.frame_duration / 1000)
            
            # Pad audio to make it divisible by frame_size
            padding = frame_size - (len(audio_data) % frame_size)
            if padding != frame_size:
                audio_data = np.pad(audio_data, (0, padding), 'constant')
            
            # Analyze frames using energy-based detection
            total_frames = len(audio_data) // frame_size
            speech_frames = 0
            
            for i in range(total_frames):
                start = i * frame_size
                end = start + frame_size
                frame = audio_data[start:end]
                
                # Calculate RMS energy
                rms_energy = np.sqrt(np.mean(frame ** 2))
                
                # Check if energy exceeds threshold (indicates speech)
                if rms_energy > self.energy_threshold:
                    speech_frames += 1
            
            speech_percentage = (speech_frames / total_frames * 100) if total_frames > 0 else 0
            
            return {
                "total_frames": total_frames,
                "speech_frames": speech_frames,
                "speech_percentage": speech_percentage,
                "silence_percentage": 100 - speech_percentage
            }
            
        except Exception as e:
            print(f"Voice activity detection error: {str(e)}")
            return {
                "total_frames": 0,
                "speech_frames": 0,
                "speech_percentage": 0,
                "silence_percentage": 100
            }
    
    def _analyze_speech_patterns(self, audio_data: np.ndarray, voice_activity: Dict) -> Dict:
        """Analyze speech patterns and characteristics"""
        try:
            # Extract features only if there's speech
            if voice_activity["speech_percentage"] < 1.0:
                return {
                    "pitch_mean": 0,
                    "pitch_std": 0,
                    "energy_mean": 0,
                    "energy_std": 0,
                    "stability_score": 0
                }
            
            # Extract pitch (fundamental frequency)
            pitches, magnitudes = librosa.piptrack(y=audio_data, sr=self.sample_rate)
            
            # Get pitch values where magnitude is high
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 50 and pitch < 500:  # Human speech range
                    pitch_values.append(pitch)
            
            # Calculate pitch statistics
            if len(pitch_values) > 0:
                pitch_mean = np.mean(pitch_values)
                pitch_std = np.std(pitch_values)
            else:
                pitch_mean = 0
                pitch_std = 0
            
            # Calculate energy (RMS)
            rms = librosa.feature.rms(y=audio_data)[0]
            energy_mean = np.mean(rms)
            energy_std = np.std(rms)
            
            # Calculate stability score based on consistency
            pitch_stability = 100 - min(100, (pitch_std / pitch_mean * 100)) if pitch_mean > 0 else 0
            energy_stability = 100 - min(100, (energy_std / energy_mean * 100)) if energy_mean > 0 else 0
            
            stability_score = (pitch_stability + energy_stability) / 2
            
            return {
                "pitch_mean": float(pitch_mean),
                "pitch_std": float(pitch_std),
                "energy_mean": float(energy_mean),
                "energy_std": float(energy_std),
                "stability_score": float(stability_score)
            }
            
        except Exception as e:
            print(f"Speech pattern analysis error: {str(e)}")
            return {
                "pitch_mean": 0,
                "pitch_std": 0,
                "energy_mean": 0,
                "energy_std": 0,
                "stability_score": 0
            }
    
    def _analyze_audio_quality(self, audio_data: np.ndarray) -> Dict:
        """Analyze audio quality metrics"""
        try:
            # Signal-to-noise ratio approximation
            signal_power = np.mean(audio_data ** 2)
            
            # Estimate noise from quiet segments
            rms = librosa.feature.rms(y=audio_data)[0]
            noise_threshold = np.percentile(rms, 10)  # Bottom 10% as noise
            noise_power = noise_threshold ** 2
            
            snr = 10 * np.log10(signal_power / noise_power) if noise_power > 0 else 20
            
            # Clipping detection
            clipping_percentage = np.sum(np.abs(audio_data) > 0.95) / len(audio_data) * 100
            
            # Dynamic range
            dynamic_range = np.max(np.abs(audio_data)) - np.min(np.abs(audio_data))
            
            return {
                "snr": float(snr),
                "clipping_percentage": float(clipping_percentage),
                "dynamic_range": float(dynamic_range),
                "quality_score": float(max(0, min(100, snr * 5)))  # Scale SNR to 0-100
            }
            
        except Exception as e:
            print(f"Audio quality analysis error: {str(e)}")
            return {
                "snr": 0,
                "clipping_percentage": 0,
                "dynamic_range": 0,
                "quality_score": 0
            }
    
    def _detect_filler_words(self, words: List[str]) -> List[str]:
        """Detect filler words in transcript"""
        filler_patterns = [
            "um", "uh", "like", "you know", "so", "well", 
            "actually", "basically", "literally", "right",
            "okay", "alright", "yeah", "yes", "no", "hmm"
        ]
        
        filler_words = []
        for word in words:
            if word.lower().strip('.,!?') in filler_patterns:
                filler_words.append(word.lower())
        
        return filler_words
    
    def _empty_analysis(self) -> Dict:
        """Return empty analysis result"""
        return {
            "duration": 0,
            "transcript": {
                "transcript": "",
                "word_count": 0,
                "speaking_rate": 0,
                "filler_words": [],
                "filler_word_count": 0,
                "confidence": 0.0
            },
            "voice_activity": {
                "total_frames": 0,
                "speech_frames": 0,
                "speech_percentage": 0,
                "silence_percentage": 100
            },
            "speech_metrics": {
                "pitch_mean": 0,
                "pitch_std": 0,
                "energy_mean": 0,
                "energy_std": 0,
                "stability_score": 0
            },
            "audio_quality": {
                "snr": 0,
                "clipping_percentage": 0,
                "dynamic_range": 0,
                "quality_score": 0
            },
            "has_speech": False
        }