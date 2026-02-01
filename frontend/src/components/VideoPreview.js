import React, { useRef, useEffect, useState } from 'react';
import { Camera, Play } from 'lucide-react';

const VideoPreview = ({ stream, className = "", showPlaceholder = true }) => {
  const videoRef = useRef(null);
  const [needsUserInteraction, setNeedsUserInteraction] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    const video = videoRef.current;
    if (!video || !stream) return;

    const handleLoadedMetadata = () => {
      // Try to play automatically first
      const playPromise = video.play();
      
      if (playPromise !== undefined) {
        playPromise
          .then(() => {
            console.log('Video playback started successfully');
            setIsPlaying(true);
            setNeedsUserInteraction(false);
          })
          .catch(error => {
            // If autoplay fails, show user interaction button
            if (error.name === 'NotAllowedError') {
              console.log('Autoplay prevented, user interaction required');
              setNeedsUserInteraction(true);
            } else if (error.name !== 'AbortError') {
              console.log('Video playback failed:', error.name, error.message);
            }
          });
      }
    };

    const handleError = (error) => {
      console.error('Video error:', error);
    };

    const handleAbort = () => {
      console.log('Video playback was aborted');
    };

    const handlePlay = () => {
      setIsPlaying(true);
      setNeedsUserInteraction(false);
    };

    const handlePause = () => {
      setIsPlaying(false);
    };

    // Set up the video stream
    video.srcObject = stream;
    video.addEventListener('loadedmetadata', handleLoadedMetadata);
    video.addEventListener('error', handleError);
    video.addEventListener('abort', handleAbort);
    video.addEventListener('play', handlePlay);
    video.addEventListener('pause', handlePause);

    // Cleanup function
    return () => {
      video.removeEventListener('loadedmetadata', handleLoadedMetadata);
      video.removeEventListener('error', handleError);
      video.removeEventListener('abort', handleAbort);
      video.removeEventListener('play', handlePlay);
      video.removeEventListener('pause', handlePause);
      
      // Pause the video before cleanup to prevent play() interruption
      if (!video.paused) {
        video.pause();
      }
      
      // Don't stop the stream here as it might be used elsewhere
      if (video.srcObject) {
        video.srcObject = null;
      }
    };
  }, [stream]);

  const handleUserPlay = () => {
    const video = videoRef.current;
    if (video) {
      video.play().catch(console.error);
    }
  };

  if (!stream && showPlaceholder) {
    return (
      <div className={`flex items-center justify-center text-gray-500 ${className}`}>
        <div className="text-center">
          <Camera className="w-12 h-12 mx-auto mb-2 opacity-50" />
          <p>Camera preview will appear here</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`relative ${className}`}>
      <video
        ref={videoRef}
        className="w-full h-full"
        muted
        playsInline
        style={{ objectFit: 'cover' }}
      />
      
      {needsUserInteraction && (
        <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <button
            onClick={handleUserPlay}
            className="flex items-center px-4 py-2 bg-white text-gray-900 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <Play className="w-5 h-5 mr-2" />
            Start Camera
          </button>
        </div>
      )}
    </div>
  );
};

export default VideoPreview;