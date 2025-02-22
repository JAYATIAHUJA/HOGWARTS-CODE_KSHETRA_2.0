const speechUtils = {
  // Speech synthesis instance
  synth: typeof window !== 'undefined' ? window.speechSynthesis : null,
  
  // Speaking state
  isSpeaking: false,
  
  // Stop any ongoing speech
  stopSpeaking() {
    if (this.synth) {
      this.synth.cancel();
      this.isSpeaking = false;
    }
  },

  // Get available voice for a language
  getVoice(language) {
    if (!this.synth) return null;
    const voices = this.synth.getVoices();
    
    // Try to find a voice that matches the language code
    return voices.find(voice => voice.lang.startsWith(language)) ||
           // Fallback to any available voice
           voices[0];
  },

  speak(text, language = 'en') {
    this.stopSpeaking();
    
    if (!this.synth) {
      console.error('Speech synthesis not supported');
      return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = language === 'hi' ? 'hi-IN' : 'en-US';
    
    // Wait for voices to load if necessary
    const voices = this.synth.getVoices();
    if (voices.length === 0) {
      this.synth.addEventListener('voiceschanged', () => {
        utterance.voice = this.getVoice(utterance.lang);
        this.synth.speak(utterance);
      }, { once: true });
    } else {
      utterance.voice = this.getVoice(utterance.lang);
      this.synth.speak(utterance);
    }

    this.isSpeaking = true;
    
    utterance.onend = () => {
      this.isSpeaking = false;
    };

    utterance.onerror = (event) => {
      console.error('Speech synthesis error:', event);
      this.isSpeaking = false;
    };
  },

  // Speak text in Hindi using a third-party service
  // You'll need to sign up for an API key
  async speakHindi(text) {
    this.stopSpeaking();
    
    try {
      // Example using Google Cloud Text-to-Speech API
      const response = await fetch('YOUR_TTS_API_ENDPOINT', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer YOUR_API_KEY'
        },
        body: JSON.stringify({
          text: text,
          language: 'hi-IN',
          voice: 'hi-IN-Standard-A'
        })
      });
      
      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      
      this.isSpeaking = true;
      audio.play();
      
      audio.onended = () => {
        this.isSpeaking = false;
        URL.revokeObjectURL(audioUrl);
      };
    } catch (error) {
      console.error('Error playing Hindi speech:', error);
      this.isSpeaking = false;
    }
  }
};

export default speechUtils; 