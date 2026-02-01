/**
 * Media Recording Service
 * Handles webcam and microphone recording functionality
 */

export class MediaRecorderService {
  constructor() {
    this.mediaRecorder = null;
    this.stream = null;
    this.chunks = [];
    this.isRecording = false;
    this.recordingType = null; // 'audio', 'video', or 'both'
  }

  /**
   * Initialize media stream with camera and microphone
   * @param {Object} constraints - Media constraints
   * @returns {Promise<MediaStream>} Media stream
   */
  async initializeStream(constraints = {}) {
    try {
      const defaultConstraints = {
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 },
          frameRate: { ideal: 30 },
          facingMode: 'user'
        },
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
          sampleRate: 44100
        }
      };

      const finalConstraints = { ...defaultConstraints, ...constraints };
      
      // Stop existing stream if any
      if (this.stream) {
        this.stream.getTracks().forEach(track => track.stop());
      }
      
      this.stream = await navigator.mediaDevices.getUserMedia(finalConstraints);
      
      console.log('Media stream initialized:', {
        video: this.stream.getVideoTracks().length > 0,
        audio: this.stream.getAudioTracks().length > 0
      });
      
      return this.stream;
    } catch (error) {
      console.error('Failed to initialize media stream:', error);
      throw new Error(`Camera/microphone access failed: ${error.message}`);
    }
  }

  /**
   * Start recording
   * @param {string} type - Recording type: 'audio', 'video', or 'both'
   * @param {Object} options - Recording options
   * @returns {Promise<void>}
   */
  async startRecording(type = 'both', options = {}) {
    if (!this.stream) {
      throw new Error('Media stream not initialized. Call initializeStream() first.');
    }

    if (this.isRecording) {
      throw new Error('Recording is already in progress');
    }

    try {
      this.recordingType = type;
      this.chunks = [];

      // Create appropriate stream based on recording type
      let recordingStream;
      if (type === 'audio') {
        recordingStream = new MediaStream(this.stream.getAudioTracks());
      } else if (type === 'video') {
        recordingStream = new MediaStream([
          ...this.stream.getVideoTracks(),
          ...this.stream.getAudioTracks()
        ]);
      } else {
        recordingStream = this.stream;
      }

      // Configure MediaRecorder options
      const defaultOptions = {
        mimeType: this.getSupportedMimeType(type),
        audioBitsPerSecond: 128000,
        videoBitsPerSecond: type === 'audio' ? undefined : 2500000
      };

      const finalOptions = { ...defaultOptions, ...options };

      this.mediaRecorder = new MediaRecorder(recordingStream, finalOptions);

      // Set up event handlers
      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          this.chunks.push(event.data);
        }
      };

      this.mediaRecorder.onstart = () => {
        console.log(`${type} recording started`);
        this.isRecording = true;
      };

      this.mediaRecorder.onstop = () => {
        console.log(`${type} recording stopped`);
        this.isRecording = false;
      };

      this.mediaRecorder.onerror = (event) => {
        console.error('MediaRecorder error:', event.error);
        this.isRecording = false;
      };

      // Start recording
      this.mediaRecorder.start(1000); // Collect data every second
      
    } catch (error) {
      console.error('Failed to start recording:', error);
      throw new Error(`Recording failed to start: ${error.message}`);
    }
  }

  /**
   * Stop recording and return blob
   * @returns {Promise<Blob>} Recorded data blob
   */
  async stopRecording() {
    if (!this.mediaRecorder || !this.isRecording) {
      throw new Error('No active recording to stop');
    }

    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        reject(new Error('Recording stop timeout'));
      }, 5000);

      this.mediaRecorder.onstop = () => {
        clearTimeout(timeout);
        
        if (this.chunks.length === 0) {
          reject(new Error('No recorded data available'));
          return;
        }

        const mimeType = this.getSupportedMimeType(this.recordingType);
        const blob = new Blob(this.chunks, { type: mimeType });
        
        console.log(`Recording stopped. Blob size: ${blob.size} bytes`);
        
        // Reset chunks for next recording
        this.chunks = [];
        this.isRecording = false;
        
        resolve(blob);
      };

      this.mediaRecorder.stop();
    });
  }

  /**
   * Pause recording
   */
  pauseRecording() {
    if (this.mediaRecorder && this.isRecording) {
      this.mediaRecorder.pause();
      console.log('Recording paused');
    }
  }

  /**
   * Resume recording
   */
  resumeRecording() {
    if (this.mediaRecorder && this.mediaRecorder.state === 'paused') {
      this.mediaRecorder.resume();
      console.log('Recording resumed');
    }
  }

  /**
   * Get supported MIME type for recording
   * @param {string} type - Recording type
   * @returns {string} Supported MIME type
   */
  getSupportedMimeType(type) {
    const types = {
      audio: [
        'audio/webm;codecs=opus',
        'audio/webm',
        'audio/mp4',
        'audio/wav'
      ],
      video: [
        'video/webm;codecs=vp9,opus',
        'video/webm;codecs=vp8,opus',
        'video/webm',
        'video/mp4'
      ],
      both: [
        'video/webm;codecs=vp9,opus',
        'video/webm;codecs=vp8,opus',
        'video/webm',
        'video/mp4'
      ]
    };

    const candidates = types[type] || types.both;
    
    for (const mimeType of candidates) {
      if (MediaRecorder.isTypeSupported(mimeType)) {
        console.log(`Using MIME type: ${mimeType}`);
        return mimeType;
      }
    }

    // Fallback
    const fallback = type === 'audio' ? 'audio/webm' : 'video/webm';
    console.warn(`No supported MIME type found, using fallback: ${fallback}`);
    return fallback;
  }

  /**
   * Get current recording state
   * @returns {Object} Recording state information
   */
  getRecordingState() {
    return {
      isRecording: this.isRecording,
      recordingType: this.recordingType,
      state: this.mediaRecorder?.state || 'inactive',
      hasStream: !!this.stream,
      streamActive: this.stream?.active || false
    };
  }

  /**
   * Get media stream for video preview
   * @returns {MediaStream|null} Current media stream
   */
  getStream() {
    return this.stream;
  }

  /**
   * Stop all media tracks and clean up
   */
  cleanup() {
    try {
      // Stop recording if active
      if (this.isRecording && this.mediaRecorder) {
        this.mediaRecorder.stop();
      }

      // Stop all media tracks
      if (this.stream) {
        this.stream.getTracks().forEach(track => {
          track.stop();
          console.log(`Stopped ${track.kind} track`);
        });
      }

      // Reset state
      this.mediaRecorder = null;
      this.stream = null;
      this.chunks = [];
      this.isRecording = false;
      this.recordingType = null;

      console.log('MediaRecorderService cleaned up');
    } catch (error) {
      console.error('Error during cleanup:', error);
    }
  }

  /**
   * Check browser compatibility
   * @returns {Object} Compatibility information
   */
  static checkCompatibility() {
    const compatibility = {
      mediaDevices: !!navigator.mediaDevices,
      getUserMedia: !!navigator.mediaDevices?.getUserMedia,
      mediaRecorder: !!window.MediaRecorder,
      webRTC: !!window.RTCPeerConnection
    };

    const isCompatible = Object.values(compatibility).every(Boolean);

    return {
      ...compatibility,
      isCompatible,
      issues: Object.entries(compatibility)
        .filter(([key, value]) => !value)
        .map(([key]) => key)
    };
  }

  /**
   * Get available media devices
   * @returns {Promise<Object>} Available devices
   */
  static async getAvailableDevices() {
    try {
      const devices = await navigator.mediaDevices.enumerateDevices();
      
      return {
        audioInputs: devices.filter(device => device.kind === 'audioinput'),
        videoInputs: devices.filter(device => device.kind === 'videoinput'),
        audioOutputs: devices.filter(device => device.kind === 'audiooutput')
      };
    } catch (error) {
      console.error('Failed to enumerate devices:', error);
      return {
        audioInputs: [],
        videoInputs: [],
        audioOutputs: []
      };
    }
  }

  /**
   * Request permissions for camera and microphone
   * @returns {Promise<Object>} Permission status
   */
  static async requestPermissions() {
    try {
      // Request permissions by attempting to get user media
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
      });

      // Stop the stream immediately as we only needed permissions
      stream.getTracks().forEach(track => track.stop());

      return {
        camera: 'granted',
        microphone: 'granted',
        success: true
      };
    } catch (error) {
      console.error('Permission request failed:', error);
      
      return {
        camera: error.name === 'NotAllowedError' ? 'denied' : 'error',
        microphone: error.name === 'NotAllowedError' ? 'denied' : 'error',
        success: false,
        error: error.message
      };
    }
  }
}