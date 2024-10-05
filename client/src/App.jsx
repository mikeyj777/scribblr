import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DrawingCanvas from './components/DrawingCanvas';
import Gallery from './components/Gallery';
import NameInput from './components/NameInput';
import { SERVER_HOST } from './utils/config';

const App = () => {
  const [userId, setUserId] = useState('');
  const [drawings, setDrawings] = useState([]);
  const [selectedDrawing, setSelectedDrawing] = useState(null);

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
    const blob = await (await fetch(dataURL)).blob();
    const formData = new FormData();
    formData.append('image', blob, 'drawing.jpg');
    formData.append('userId', userId);
    try {
      const response = await axios.post(`${SERVER_HOST}/api/drawings`, formData);
      const newDrawing = {
        id: response.data.id,
        image_path: response.data.image_path,
        predictions: response.data.predictions,
      };
      setDrawings([...drawings, newDrawing]);
      setSelectedDrawing(newDrawing);
    } catch (error) {
      console.error('Error saving drawing:', error);
    }
  };

  const handleDrawingSelect = (drawing) => {
    setSelectedDrawing(drawing);
  };

  const handleStartOver = () => {
    setSelectedDrawing(null);
  };

  return (
    <div className="app">
      <h1 className="app-title">Drawing App</h1>
      {!userId ? (
        <NameInput onSubmit={handleNameSubmit} />
      ) : (
        <div className="app-content">
          <div className="drawing-section">
            <DrawingCanvas onSubmit={handleDrawingSubmit} onStartOver={handleStartOver} />
          </div>
          <div className="gallery-section">
            <Gallery
              drawings={drawings}
              selectedDrawing={selectedDrawing}
              onDrawingSelect={handleDrawingSelect}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default App;