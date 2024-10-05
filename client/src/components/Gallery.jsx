import React from 'react';

const Gallery = ({ drawings }) => {
  return (
    <div>
      <h2>Your Drawings:</h2>
      <div className="gallery">
        {drawings.map((drawing) => (
          <div key={drawing.id} className="drawing">
            <img src={`/${drawing.image_path}`} alt="Drawing" />
            <div className="predictions">
              <h3>Predictions:</h3>
              <ul>
                {drawing.predictions.map((p, i) => (
                  <li key={i}>{p[0]}</li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Gallery;