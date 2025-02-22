import React, { useState } from 'react';
import speechUtils from '../utils/speechUtils';

function SpeechControls({ text, language = 'en' }) {
  const [isSpeaking, setIsSpeaking] = useState(false);

  const handleSpeak = () => {
    if (isSpeaking) {
      speechUtils.stopSpeaking();
      setIsSpeaking(false);
    } else {
      speechUtils.speak(text, language);
      setIsSpeaking(true);
    }
  };

  return (
    <button 
      onClick={handleSpeak}
      className="speech-control-btn"
      style={{
        padding: '8px 16px',
        borderRadius: '20px',
        border: 'none',
        backgroundColor: '#007bff',
        color: 'white',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        gap: '8px'
      }}
    >
      {isSpeaking ? "🔇 Stop" : "🔊 Listen"} 
      {language === 'hi' ? "(हिंदी)" : "(English)"}
    </button>
  );
}

export default SpeechControls; 