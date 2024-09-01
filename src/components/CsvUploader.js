// src/CsvUploader.js
import React, { useState, useRef } from 'react';
// import Papa from 'papaparse';
import '../css/CsvUploader.css'; // Import the CSS file for styling
import { useDispatch } from 'react-redux';
import { useSelector } from 'react-redux';
import  {actionCreators} from '../states/index';
import { TailSpin } from "react-loader-spinner";
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Toast from './Toast';
import { toastOptions } from '../helpers/helper';

const CsvUploader = () => {
  const [error, setError] = useState(null);
  const inputRef = useRef(null);
  const [loading, setLoading] = useState(false);
  

  const dispach = useDispatch();
  const tableData = useSelector(state => state.tableData)
  const filters = useSelector(state => state.filters)

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      // Clear previous data and error
      setError(null);

      try {
        setLoading(true);
        // Prepare FormData to send file
        const formData = new FormData();
        formData.append('file', file);

        // Call the FastAPI endpoint
        const response = await fetch('http://127.0.0.1:8000/uploadfile/', {
          method: 'POST',
          body: formData,
        });

        // if (!response.ok) {
        //   throw new Error('Network response was not ok');
        // }

        // Parse JSON response
        const result = await response.json();

        // Set data from response
        if (result.data) {
        dispach(actionCreators.setTableDataAction(JSON.parse(result.data)))
        setLoading(false)
        }
        else{
          console.log(result)
          toast.error(result.detail, toastOptions);
          setLoading(false);
        }
      } catch (err) {
        toast.error(err.message, toastOptions);
        setLoading(false);
      }
    }
  };

  const downloadCSV = () => {
    const csv = convertToCSV(tableData);
    if (!csv) return;

    // Create a Blob from the CSV string
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');

    // Create a link to download the Blob
    if (link.download !== undefined) {
      // Support for modern browsers
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', 'data.csv');
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  // Convert JSON data to CSV format
  const convertToCSV = (data) => {
    if (!data || data.length === 0) return '';

    const headers = Object.keys(data[0]);
    const rows = data.map(row =>
      headers.map(header => JSON.stringify(row[header] || '')).join(',')
    );

    return [headers.join(','), ...rows].join('\n');
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      // Print the input value to the console
      // console.log('Input text:', inputRef.current.value);

      dispach(actionCreators.addFilterAction(inputRef.current.value))

      // Clear the input field
      inputRef.current.value = '';

      // Optionally prevent the default action
      event.preventDefault();
    }
  };

  const removeFilter = (filter) => {
    dispach(actionCreators.removeFilterAction(filter))
  }

    // Determine placeholder text based on tableData
    const inputPlaceholder = tableData === false
    ? 'Upload a CSV file to enable filtering...'
    : 'Type to filter...';

  return (
    <div className="csv-uploader">
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
      <input
        type="file"
        accept=".csv"
        onChange={handleFileUpload}
        className="file-input"
      />
      {tableData.length > 0 && ( <button className="download-button" style={{ marginLeft: "auto" }} onClick={downloadCSV}>Download</button> )}
    </div>
      <div className="filter-section">
        <label htmlFor="filter-input" className="filter-label">Enter your query to filter:</label>
        <input
          type="text"
          id="filter-input"
          ref={inputRef}
          onKeyDown={handleKeyDown}
          placeholder={inputPlaceholder}
          className="filter-input"
          disabled={tableData === false} // Disable input when tableData is empty
        />
      </div>
      {loading && (
        <div className="loader-container">
          <TailSpin color="#4CAF50" height={80} width={80} />
        </div>
      )}
      {error && <p className="error-message">Error: {error}</p>}
      {filters && filters.length > 0 && (
        <div className="filter-section">
          {filters.map((filter, index) => (
            <div key={index} className='filter-item'>
              <p>{filter}</p>
              <button className="cross-button" onClick={() => removeFilter(filter)}>&times;</button>
            </div>
          ))}
        </div>
      )}
      {tableData.length > 0 && (
        <div className='table'>
          <table className="csv-table">
            <thead>
              <tr>
                {Object.keys(tableData[0]).map((key) => (
                  <th key={key} className="table-header">{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {tableData.map((row, index) => (
                <tr key={index}>
                  {Object.keys(row).map((key) => (
                    <td key={key} className="table-cell">{row[key]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <div>
        <Toast />
      </div>
    </div>
  );
};

export default CsvUploader;
