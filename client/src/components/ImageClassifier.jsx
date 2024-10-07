import React, { useRef, useEffect } from 'react';
import * as tf from '@tensorflow/tfjs';

const ImageClassifier = ({ imageData, onClassification }) => {
  const canvasRef = useRef(null);
  const modelRef = useRef(null);

  useEffect(() => {
    const loadModel = async () => {
      modelRef.current = await tf.loadLayersModel('data/model.json');
    };

    loadModel();
  }, []);

  useEffect(() => {
    const classifyImage = async () => {
      if (modelRef.current && imageData && canvasRef.current) {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        const image = new Image();
        image.onload = async () => {
          ctx.drawImage(image, 0, 0, 28, 28);
          const imageData = ctx.getImageData(0, 0, 28, 28);
          const input = tf.tensor(Array.from(imageData.data), [1, 28, 28, 1]).div(255);
          const predictions = await modelRef.current.predict(input);
          const classNames = await fetchClassNames();
          const topK = await predictions.topk(10);
          const topKClasses = topK.indices.dataSync();
          const topKProbs = topK.values.dataSync();
          const results = topKClasses.map((classIndex, i) => ({
            className: classNames[classIndex],
            probability: topKProbs[i]
          }));
          onClassification(results);
        };
        image.src = imageData;
      }
    };

    classifyImage();
  }, [imageData, onClassification]);

  const fetchClassNames = async () => {
    const response = await fetch('data/class_names.txt');
    const text = await response.text();
    return text.split('\n');
  };

  return <canvas ref={canvasRef} width={28} height={28} style={{ display: 'none' }} />;
};

export default ImageClassifier;