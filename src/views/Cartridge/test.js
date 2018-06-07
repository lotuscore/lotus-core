import React from 'react';
import ReactDOM from 'react-dom';
import Cartridge from './index.js';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<Cartridge />, div);
});
