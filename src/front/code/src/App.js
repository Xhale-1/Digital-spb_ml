import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';

function App() {
  const [inputValue, setInputValue] = useState('');


const handleKeyDown = async (event) => {
  if (event.key == 'Enter') {
        const response = await fetch('/api/process_query', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ query: event.target.value }),
        });

        const data = await response.json();
        
        setInputValue(data.response);
      }
  };

  

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>Поиск:</p>
        <input
          type="text"
          className="input"
          //value={inputValue}
          //onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Введите текст и нажмите Enter"
        />
        <myelement>

        </myelement>
        <p>Ответ сервера: {inputValue}</p>
      </header>
    </div>
  );
}

export default App;