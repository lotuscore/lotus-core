import React from 'react';
import ReactDOM from 'react-dom';
import Publisher from './index.js';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<Publisher />, div);
});
