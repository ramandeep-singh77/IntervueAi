/**
 * Session Storage Utilities
 * Handles storing and retrieving session data without MediaStream objects
 */

const SESSION_KEY_PREFIX = 'intervue_session_';

export const sessionStorage = {
  /**
   * Store session data (excluding non-serializable objects)
   */
  setSessionData: (sessionId, data) => {
    try {
      // Create a clean copy without MediaStream or other non-serializable objects
      const cleanData = {
        session_id: data.session_id,
        role: data.role,
        experience_level: data.experience_level,
        questions: data.questions,
        current_question: data.current_question,
        responses: data.responses || [],
        created_at: data.created_at
      };
      
      const key = SESSION_KEY_PREFIX + sessionId;
      localStorage.setItem(key, JSON.stringify(cleanData));
      return true;
    } catch (error) {
      console.error('Failed to store session data:', error);
      return false;
    }
  },

  /**
   * Retrieve session data
   */
  getSessionData: (sessionId) => {
    try {
      const key = SESSION_KEY_PREFIX + sessionId;
      const data = localStorage.getItem(key);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('Failed to retrieve session data:', error);
      return null;
    }
  },

  /**
   * Remove session data
   */
  removeSessionData: (sessionId) => {
    try {
      const key = SESSION_KEY_PREFIX + sessionId;
      localStorage.removeItem(key);
      return true;
    } catch (error) {
      console.error('Failed to remove session data:', error);
      return false;
    }
  },

  /**
   * Clear all session data
   */
  clearAllSessions: () => {
    try {
      const keys = Object.keys(localStorage);
      keys.forEach(key => {
        if (key.startsWith(SESSION_KEY_PREFIX)) {
          localStorage.removeItem(key);
        }
      });
      return true;
    } catch (error) {
      console.error('Failed to clear session data:', error);
      return false;
    }
  }
};

export default sessionStorage;