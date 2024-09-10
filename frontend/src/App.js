// src/App.js
import React, { useState, useEffect } from 'react';
import CsvUploader from './components/CsvUploader';
import ThemeToggleButton from './components/ToggleButton';
import './App.css'; // Import the CSS file for overall app styling

const App = () => {
  const [isNightMode, setIsNightMode] = useState(() => 
    localStorage.getItem('nightMode') === 'true'
  );

  useEffect(() => {
    document.body.className = isNightMode ? 'night-mode' : 'light-mode';
    localStorage.setItem('nightMode', isNightMode);
  }, [isNightMode]);

  const toggleTheme = () => {
    setIsNightMode(prevMode => !prevMode);
  };

  return (
    <div className="app-container">
      <div className="header-container">
        <h1 className="app-title">Filter Your CSV On Your Choice</h1>
        <div className="theme-toggle-button">
          <ThemeToggleButton toggleTheme={toggleTheme} isNightMode={isNightMode} />
        </div>
      </div>
      <CsvUploader />
    </div>
  );
};

export default App;
