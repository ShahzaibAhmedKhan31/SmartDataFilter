// src/components/ThemeToggleButton.js
import React from 'react';
import '../css/ThemeToggleButton.css'; // Import the CSS file for styling

const ThemeToggleButton = ({ toggleTheme, isNightMode }) => {
  return (
    <div className="theme-toggle-container">
      <input 
        type="checkbox" 
        className="theme-toggle-checkbox" 
        id="theme-toggle"
        checked={isNightMode}
        onChange={toggleTheme}
      />
      <label className="theme-toggle-label" htmlFor="theme-toggle">
        <span className="theme-toggle-slider"></span>
      </label>
    </div>
  );
};

export default ThemeToggleButton;
