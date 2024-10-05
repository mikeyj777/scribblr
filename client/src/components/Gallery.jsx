import React from 'react';

const Gallery = ({ drawings, selectedDrawing, onDrawingSelect }) => {
  return (
    <div className="gallery">
      <h2>Your Drawings:</h2>
      <div className="thumbnail-carousel">
        {drawings.map((drawing) => (
          <div
            key={drawing.id}
            className={`thumbnail ${selectedDrawing?.id === drawing.id ? 'selected' : ''}`}
            onClick={() => onDrawingSelect(drawing)}
          >
            <img src={`/${drawing.image_path}`} alt="Drawing thumbnail" />
          </div>
        ))}
      </div>
      {selectedDrawing && (
        <div className="selected-drawing">
          <img src={`/${selectedDrawing.image_path}`} alt="Selected drawing" />
          <div className="predictions">
            <h3>Predictions:</h3>
            <ul>
              {selectedDrawing.predictions.map((prediction, index) => (
                <li key={index}>{prediction[0]}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default Gallery;