"""
Voice Analysis Service
Analyzes audio for pitch stability, energy, speaking rate, and vocal characteristics
"""

import librosa
import numpy as np
import scipy.stats
from typing import Dict, List, Tuple
import soundfile as sf

class VoiceAnalyzer:
    def __init__(self):
        self.sample_rate = 22050
        self.hop_length = 512
        self.frame_length = 2048
    
    def analyze_audio(self, audio_file_path: str) -> Dict:
        """
        Comprehensive voice analysis of audio file
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Dict containing voice analysis metrics
        """
        try:
            # Load audio file
            y, sr = librosa.load(audio_file_path, sr=self.sample_rate)
            duration = len(y) / sr
            
            if len(y) == 0:
                return self._empty_analysis_result()
            
            # Extract various audio features
            pitch_analysis = self._analyze_pitch(y, sr)
            energy_analysis = self._analyze_energy(y, sr)
            spectral_analysis = self._analyze_spectral_features(y, sr)
            rhythm_analysis = self._analyze_rhythm(y, sr)
            voice_quality = self._analyze_voice_quality(y, sr)
            
            # Calculate composite scores
            stability_score = self._calculate_stability_score(pitch_analysis, energy_analysis)
            clarity_score = self._calculate_clarity_score(spectral_analysis, voice_quality)
            
            return {
                "duration": duration,
                "pitch_analysis": pitch_analysis,
                "energy_analysis": energy_analysis,
                "spectral_analysis": spectral_analysis,
                "rhythm_analysis": rhythm_analysis,
                "voice_quality": voice_quality,
                "stability_score": stability_score,
                "clarity_score": clarity_score,
                "overall_score": (stability_score + clarity_score) / 2
            }
            
        except Exception as e:
            return {
                "error": str(e),
                **self._empty_analysis_result()
            }
    
    def _analyze_pitch(self, y: np.ndarray, sr: int) -> Dict:
        """Analyze pitch characteristics"""
        try:
            # Extract pitch using librosa
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr, hop_length=self.hop_length)
            
            # Get fundamental frequency over time
            f0 = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    f0.append(pitch)
            
            if not f0:
                return {
                    "mean_pitch": 0,
                    "pitch_variance": 0,
                    "pitch_stability": 0,
                    "pitch_range": 0,
                    "voiced_frames": 0
                }
            
            f0 = np.array(f0)
            
            # Calculate pitch statistics
            mean_pitch = np.mean(f0)
            pitch_variance = np.var(f0)
            pitch_std = np.std(f0)
            pitch_range = np.max(f0) - np.min(f0)
            
            # Pitch stability (inverse of coefficient of variation)
            pitch_stability = 100 - min(100, (pitch_std / mean_pitch * 100)) if mean_pitch > 0 else 0
            
            return {
                "mean_pitch": float(mean_pitch),
                "pitch_variance": float(pitch_variance),
                "pitch_stability": float(pitch_stability),
                "pitch_range": float(pitch_range),
                "voiced_frames": len(f0),
                "pitch_std": float(pitch_std)
            }
            
        except Exception as e:
            return {
                "mean_pitch": 0,
                "pitch_variance": 0,
                "pitch_stability": 0,
                "pitch_range": 0,
                "voiced_frames": 0,
                "error": str(e)
            }
    
    def _analyze_energy(self, y: np.ndarray, sr: int) -> Dict:
        """Analyze energy and volume characteristics"""
        try:
            # RMS energy
            rms = librosa.feature.rms(y=y, hop_length=self.hop_length)[0]
            
            # Zero crossing rate (indicator of voiced vs unvoiced)
            zcr = librosa.feature.zero_crossing_rate(y, hop_length=self.hop_length)[0]
            
            # Calculate energy statistics
            mean_energy = np.mean(rms)
            energy_variance = np.var(rms)
            energy_std = np.std(rms)
            
            # Energy stability
            energy_stability = 100 - min(100, (energy_std / mean_energy * 100)) if mean_energy > 0 else 0
            
            # Dynamic range
            dynamic_range = np.max(rms) - np.min(rms)
            
            return {
                "mean_energy": float(mean_energy),
                "energy_variance": float(energy_variance),
                "energy_stability": float(energy_stability),
                "dynamic_range": float(dynamic_range),
                "mean_zcr": float(np.mean(zcr)),
                "energy_std": float(energy_std)
            }
            
        except Exception as e:
            return {
                "mean_energy": 0,
                "energy_variance": 0,
                "energy_stability": 0,
                "dynamic_range": 0,
                "mean_zcr": 0,
                "error": str(e)
            }
    
    def _analyze_spectral_features(self, y: np.ndarray, sr: int) -> Dict:
        """Analyze spectral characteristics"""
        try:
            # Spectral centroid (brightness)
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=self.hop_length)[0]
            
            # Spectral rolloff
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, hop_length=self.hop_length)[0]
            
            # Spectral bandwidth
            spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr, hop_length=self.hop_length)[0]
            
            # MFCC features (first 13 coefficients)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=self.hop_length)
            
            return {
                "mean_spectral_centroid": float(np.mean(spectral_centroids)),
                "mean_spectral_rolloff": float(np.mean(spectral_rolloff)),
                "mean_spectral_bandwidth": float(np.mean(spectral_bandwidth)),
                "mfcc_mean": [float(np.mean(mfcc)) for mfcc in mfccs],
                "spectral_centroid_std": float(np.std(spectral_centroids)),
                "spectral_rolloff_std": float(np.std(spectral_rolloff))
            }
            
        except Exception as e:
            return {
                "mean_spectral_centroid": 0,
                "mean_spectral_rolloff": 0,
                "mean_spectral_bandwidth": 0,
                "mfcc_mean": [0] * 13,
                "spectral_centroid_std": 0,
                "spectral_rolloff_std": 0,
                "error": str(e)
            }
    
    def _analyze_rhythm(self, y: np.ndarray, sr: int) -> Dict:
        """Analyze rhythm and tempo characteristics"""
        try:
            # Tempo estimation
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=self.hop_length)
            
            # Onset detection
            onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=self.hop_length)
            onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=self.hop_length)
            
            # Calculate rhythm regularity
            if len(onset_times) > 1:
                onset_intervals = np.diff(onset_times)
                rhythm_regularity = 100 - min(100, np.std(onset_intervals) * 100)
            else:
                rhythm_regularity = 0
            
            return {
                "tempo": float(tempo),
                "beat_count": len(beats),
                "onset_count": len(onset_times),
                "rhythm_regularity": float(rhythm_regularity),
                "average_onset_interval": float(np.mean(np.diff(onset_times))) if len(onset_times) > 1 else 0
            }
            
        except Exception as e:
            return {
                "tempo": 0,
                "beat_count": 0,
                "onset_count": 0,
                "rhythm_regularity": 0,
                "average_onset_interval": 0,
                "error": str(e)
            }
    
    def _analyze_voice_quality(self, y: np.ndarray, sr: int) -> Dict:
        """Analyze voice quality indicators"""
        try:
            # Harmonic-percussive separation
            y_harmonic, y_percussive = librosa.effects.hpss(y)
            
            # Calculate harmonic-to-noise ratio approximation
            harmonic_energy = np.sum(y_harmonic ** 2)
            percussive_energy = np.sum(y_percussive ** 2)
            
            if percussive_energy > 0:
                hnr_approx = 10 * np.log10(harmonic_energy / percussive_energy)
            else:
                hnr_approx = 20  # High HNR if no percussive component
            
            # Jitter approximation (pitch period variation)
            # This is a simplified version - real jitter requires more sophisticated analysis
            rms = librosa.feature.rms(y=y, hop_length=self.hop_length)[0]
            jitter_approx = np.std(rms) / np.mean(rms) if np.mean(rms) > 0 else 0
            
            return {
                "harmonic_to_noise_ratio": float(hnr_approx),
                "jitter_approximation": float(jitter_approx),
                "harmonic_energy": float(harmonic_energy),
                "percussive_energy": float(percussive_energy),
                "voice_quality_score": float(max(0, min(100, hnr_approx * 5)))  # Scale to 0-100
            }
            
        except Exception as e:
            return {
                "harmonic_to_noise_ratio": 0,
                "jitter_approximation": 0,
                "harmonic_energy": 0,
                "percussive_energy": 0,
                "voice_quality_score": 0,
                "error": str(e)
            }
    
    def _calculate_stability_score(self, pitch_analysis: Dict, energy_analysis: Dict) -> float:
        """Calculate overall voice stability score"""
        pitch_stability = pitch_analysis.get("pitch_stability", 0)
        energy_stability = energy_analysis.get("energy_stability", 0)
        
        # Weighted average (pitch is more important for perceived stability)
        stability_score = (pitch_stability * 0.7) + (energy_stability * 0.3)
        return float(stability_score)
    
    def _calculate_clarity_score(self, spectral_analysis: Dict, voice_quality: Dict) -> float:
        """Calculate voice clarity score"""
        voice_quality_score = voice_quality.get("voice_quality_score", 0)
        
        # Normalize spectral centroid (higher values indicate clearer speech)
        spectral_centroid = spectral_analysis.get("mean_spectral_centroid", 0)
        normalized_centroid = min(100, spectral_centroid / 50)  # Rough normalization
        
        # Combine voice quality and spectral clarity
        clarity_score = (voice_quality_score * 0.6) + (normalized_centroid * 0.4)
        return float(clarity_score)
    
    def _empty_analysis_result(self) -> Dict:
        """Return empty analysis result structure"""
        return {
            "duration": 0,
            "pitch_analysis": {},
            "energy_analysis": {},
            "spectral_analysis": {},
            "rhythm_analysis": {},
            "voice_quality": {},
            "stability_score": 0,
            "clarity_score": 0,
            "overall_score": 0
        }
    
    def get_voice_insights(self, analysis_result: Dict) -> List[str]:
        """Generate actionable insights from voice analysis"""
        insights = []
        
        stability_score = analysis_result.get("stability_score", 0)
        clarity_score = analysis_result.get("clarity_score", 0)
        pitch_analysis = analysis_result.get("pitch_analysis", {})
        energy_analysis = analysis_result.get("energy_analysis", {})
        
        if stability_score < 60:
            insights.append("Work on maintaining consistent pitch and volume")
        
        if clarity_score < 60:
            insights.append("Focus on clear articulation and voice projection")
        
        pitch_stability = pitch_analysis.get("pitch_stability", 0)
        if pitch_stability < 50:
            insights.append("Practice controlling pitch variations for more confident delivery")
        
        energy_stability = energy_analysis.get("energy_stability", 0)
        if energy_stability < 50:
            insights.append("Work on maintaining consistent energy levels throughout your response")
        
        if not insights:
            insights.append("Excellent voice control and clarity!")
        
        return insights