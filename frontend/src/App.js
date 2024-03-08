import logo from './logo.svg';
import './App.css';

import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [learningRate, setLearningRate] = useState('');
  const [optimizer, setOptimizer] = useState('');
  const [file, setFile] = useState(null);
  const [selectedNode, setSelectedNode] = useState('');

  const handleTrainClick = async () => {
    try {
      const formData = new FormData();
      formData.append('learning_rate', learningRate);
      formData.append('optimizer', optimizer);
      formData.append('file', file);
      formData.append('selected_node', selectedNode);

      await axios.post('http://ipaddress:80/start_train', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    } catch (error) {
      console.error('Error starting training:', error);
    }
  };

  return (
    <div className="container">
      <h1>Peer-AI Project</h1>
      <p>
        Peer-AI is a Distributed Training Framework for ML models. This framework leverages the
        power of peer-to-peer (P2P) networks to distribute the computational load, enabling efficient,
        secure, and collaborative model training across a distributed network of participants in the
        P2P Network. Our primary focus is training ML models in the P2P network based on
        the D2D communications based on URLLC and Enhanced Mobile Broadband (eMBB) 5G
        Networks specializing in edge devices.
      </p>
      <div className="form-group">
        <label htmlFor="file">Upload base.py:</label>
        <input
          type="file"
          id="file"
          accept=".py"
          onChange={(e) => setFile(e.target.files[0])}
        />
      </div>
      <div className="form-group">
        <label htmlFor="learningRate">Learning Rate:</label>
        <input
          type="text"
          id="learningRate"
          value={learningRate}
          onChange={(e) => setLearningRate(e.target.value)}
        />
      </div>
      <div className="form-group">
        <label htmlFor="optimizer">Optimizer:</label>
        <select
          id="optimizer"
          value={optimizer}
          onChange={(e) => setOptimizer(e.target.value)}
        >
          <option value="">Select Optimizer</option>
          <option value="sgd">SGD</option>
          <option value="adgrad">Adgrad</option>
        </select>
      </div>
      <div className="form-group">
        <label>Select Training Node:</label>
        <select
          value={selectedNode}
          onChange={(e) => setSelectedNode(e.target.value)}
        >
          <option value="">Select Training Node</option>
          <option value="1">Train Node 1</option>
          <option value="2">Train Node 2</option>
          <option value="3">Train Node 3</option>
          <option value="4">Train Node 4</option>
        </select>
      </div>
      <button onClick={handleTrainClick}>Train</button>
    </div>
  );
};

export default App;

