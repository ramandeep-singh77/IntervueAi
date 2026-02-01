import React, { createContext, useContext, useState, useEffect } from 'react';
import { MediaRecorderService } from '../services/mediaRecorder';

const MediaContext = createContext();

export const useMedia = () => {
  const context = useContext(MediaContext);
  if (!context) {
    throw new Error('useMedia must be used within a MediaProvider');
  }
  return context;
};

export const MediaProvider = ({ children }) => {
  const [mediaService] = useState(() => new MediaRecorderService());
  const [stream, setStream] = useState(null);
  const [permissions, setPermissions] = useState({
    camera: 'unknown',
    microphone: 'unknown'
  });
  const [devices, setDevices] = useState({
    audioInputs: [],
    videoInputs: []
  });

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (mediaService) {
        mediaService.cleanup();
      }
    };
  }, [mediaService]);

  const initializeMedia = async (constraints = {}) => {
    try {
      const mediaStream = await mediaService.initializeStream(constraints);
      setStream(mediaStream);
      return mediaStream;
    } catch (error) {
      console.error('Failed to initialize media:', error);
      throw error;
    }
  };

  const requestPermissions = async () => {
    try {
      // Request permissions
      const permissionResult = await MediaRecorderService.requestPermissions();
      setPermissions({
        camera: permissionResult.camera,
        microphone: permissionResult.microphone
      });

      if (!permissionResult.success) {
        throw new Error(permissionResult.error || 'Permission denied');
      }

      // Get available devices
      const availableDevices = await MediaRecorderService.getAvailableDevices();
      setDevices(availableDevices);

      return permissionResult;
    } catch (error) {
      setPermissions({
        camera: 'denied',
        microphone: 'denied'
      });
      throw error;
    }
  };

  const cleanup = () => {
    if (mediaService) {
      mediaService.cleanup();
    }
    setStream(null);
  };

  const value = {
    mediaService,
    stream,
    permissions,
    devices,
    initializeMedia,
    requestPermissions,
    cleanup,
    setStream,
    setPermissions,
    setDevices
  };

  return (
    <MediaContext.Provider value={value}>
      {children}
    </MediaContext.Provider>
  );
};

export default MediaContext;