import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DrawingCanvas from './components/DrawingCanvas';
import Gallery from './components/Gallery';
import NameInput from './components/NameInput';
import ImageClassifier from './components/ImageClassifier';
import { SERVER_HOST } from './utils/config';

const App = () => {
  const [userId, setUserId] = useState('');
  const [drawings, setDrawings] = useState([]);
  const [selectedDrawing, setSelectedDrawing] = useState(null);
  const [imageData, setImageData] = useState(null);
  const [classifications, setClassifications] = useState([]);

  useEffect(() => {
    if (userId) {
      fetchDrawings();
    }
  }, [userId]);

  const fetchDrawings = async () => {
    try {
      const response = await axios.get(`${SERVER_HOST}/api/drawings/${userId}`);
      setDrawings(response.data);
      console.log('Fetched drawings:', response.data);
    } catch (error) {
      console.error('Error fetching drawings:', error);
    }
  };

  const handleNameSubmit = async (submittedName) => {
    try {
      const response = await axios.post(`${SERVER_HOST}/api/users`, { name: submittedName });
      setUserId(response.data.id);
      console.log('Created user:', response.data);
    } catch (error) {
      console.error('Error creating user:', error);
    }
  };

  const handleDrawingSubmit = async (dataURL) => {
    setImageData(dataURL);
  };

  const handleClassification = (results) => {
    setClassifications(results);
  };

  const handleDrawingSelect = (drawing) => {
    setSelectedDrawing(drawing);
  };

  const handleStartOver = () => {
    setSelectedDrawing(null);
    setImageData(null);
    setClassifications([]);
  };

  return (
    <div className="app">
      <h1>Drawing App</h1>
      {!userId ? (
        <NameInput onSubmit={handleNameSubmit} />
      ) : (
        <>
          <div className="drawing-container">
            <DrawingCanvas onSubmit={handleDrawingSubmit} onStartOver={handleStartOver} />
          </div>
          <div className="gallery-container">
            <Gallery
              drawings={drawings}
              selectedDrawing={selectedDrawing}
              onDrawingSelect={handleDrawingSelect}
            />
          </div>
          <ImageClassifier imageData={imageData} onClassification={handleClassification} />
          {classifications.length > 0 && (
            <div className="classification-results">
              <h3>Classification Results:</h3>
              <ul>
                {classifications.map((result, index) => (
                  <li key={index}>
                    {result.className}: {(result.probability * 100).toFixed(2)}%
                  </li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default App;