import './App.css';
import React, { useState } from 'react';

function App() {
  const [inputValue, setInputValue] = useState('0');


// const handleKeyDown = async (event) => {
  // if (event.key == 'Enter') {
  //       const response = await fetch('/api/process_query', {
  //         method: 'POST',
  //         headers: {
  //           'Content-Type': 'application/json',
  //         },
  //         body: JSON.stringify({ query: event.target.value }),
  //       });

  //       const data = await response.json();
        
  //       setInputValue(data.response);
  //     }
  //   sendSeachRequest()
  // };

  
// Функцию sendSeachRequest нужно вынести за пределы return
const sendSeachRequest = async (event) => {
  if (event.key == 'Enter') {
    try {

        const response = await fetch('/api/query', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ query: event.target.value }),
        });

        const data = await response.json();
        const json = data;
        setInputValue(data.response);
      
      document.getElementById('demo').outerHTML = '<table id="demo"></table>';
      
      for (var i = 0; i < json.response.length; i++) {
        console.log(json.response[i]); 
        console.log(i); 
        const new_row = document.createElement("tr");
        document.getElementById('demo').appendChild(new_row);
        const new_line = document.createElement("th");
        new_line.innerHTML = json.response[i];
        new_row.appendChild(new_line);
      }
    } catch (error) {
       console.error('Error:', error);
    }
  };
}
  

  // return (
    // <div className="App">
    //   <header className="App-header">
    //     <img src={logo} className="App-logo" alt="logo" />
    //     <p>Поиск:</p>
    //     <input
    //       type="text"
    //       className="input"
    //       //value={inputValue}
    //       //onChange={(e) => setInputValue(e.target.value)}
    //       onKeyDown={handleKeyDown}
    //       placeholder="Введите текст и нажмите Enter"
    //     />

    //     <table id="resp_list">

    //     </table>
    //     <myelement>

    //     </myelement>
    //     <p>Ответ сервера: {inputValue}</p>
    //   </header>
    // </div>

    return (
      // <div className="App">
      //   <head>
      //     <meta charSet="UTF-8" />
      //     <title>Welcome Page</title>
      //   </head>
        <div>
          <h1>Welcome!</h1>
          <p>Welcome to our simple Flask app.</p>
    
          <div id="searchbar">
            <div id="searchbar_inside">
              <p id="textentry_label">Введите адрес</p>
              <div id="tentry_area"> 
                <button 
                  type="button" 
                  //onClick={() => sendSeachRequest(document.getElementById('textentry').value)}
                >
                  🔎
                </button>
    
                <input 
                  id="textentry"
                  type="text"
                  name="name"
                  required
                  maxLength="128" 
                  // onChange = {(e)=>setInputValue(e.target.value)}
                  onKeyDown={sendSeachRequest}
                />
              </div>
                {inputValue}
              <div>

              </div>
    
              <p id="demo"></p>
            </div>
          </div>
          
          <p><a href="/about">About this site</a></p>
        </div>

    );
    
    
}

export default App;