import { useEffect, useState } from 'react';
import SpeechControls from '../components/SpeechControls';

function YourPage() {
  const [pageText, setPageText] = useState('');

  useEffect(() => {
    // Get all text content from the main content area
    const content = document.querySelector('main')?.textContent || 
                   document.body.textContent;
    setPageText(content);
  }, []);

  return (
    <div>
      <h1>Your Content</h1>
      <p>Some text content here...</p>
      
      <div className="speech-controls-container">
        <SpeechControls 
          text="Your text content here" 
          language="en" 
        />
        <SpeechControls 
          text="आपका हिंदी टेक्स्ट यहां" 
          language="hi" 
        />
      </div>
      <div style={{ position: 'fixed', bottom: '20px', right: '20px', zIndex: 1000 }}>
        <SpeechControls 
          text={pageText} 
          language="en" 
        />
      </div>
    </div>
  );
}

export default YourPage; 