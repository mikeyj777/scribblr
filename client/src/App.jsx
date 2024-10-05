import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import DrawingCanvas from './components/DrawingCanvas';
import Gallery from './components/Gallery';
import NameInput from './components/NameInput';

const App = () => {
  const [name, setName] = useState('');
  const [drawings, setDrawings] = useState([]);

  useEffect(() => {
    if (name) {
      fetchDrawings();
    }
  }, [name]);

  const fetchDrawings = async () => {
    try {
      const response = await axios.get(`/api/drawings/${name}`);
      setDrawings(response.data);
    } catch (error) {
      console.error('Error fetching drawings:', error);
    }
  };

  const handleNameSubmit = async (submittedName) => {
    try {
      await axios.post('/api/users', { name: submittedName });
      setName(submittedName);
    } catch (error) {
      console.error('Error creating user:', error);
    }
  };

  const handleDrawingSubmit = async (dataURL) => {
    const blob = await (await fetch(dataURL)).blob();
    const formData = new FormData();
    formData.append('image', blob, 'drawing.jpg');
    formData.append('name', name);
    try {
      const response = await axios.post('/api/drawings', formData);
      alert(`Top predictions: ${response.data.map((p) => p[0]).join(', ')}`);
      fetchDrawings();
    } catch (error) {
      console.error('Error saving drawing:', error);
    }
  };

  return (
    <div>
      <h1>Drawing App</h1>
      <NameInput onSubmit={handleNameSubmit} />
      <DrawingCanvas onSubmit={handleDrawingSubmit} />
      <Gallery drawings={drawings} />
    </div>
  );
};

export default App;