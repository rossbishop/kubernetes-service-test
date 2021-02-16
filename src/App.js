import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import LoginButton from './loginbutton' 
import LogoutButton from './logout';
import { useAuth0 } from '@auth0/auth0-react';

function App() {
  const { getAccessTokenSilently } = useAuth0();
  const [currentTime, setCurrentTime] = useState(0);
  const [accessToken, setAccessToken] = useState();
  const [privateData, setPrivateData] = useState();

  useEffect(() => {
    fetch('/api/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });

    (async() => {
      try {
        const tempAccessToken = await getAccessTokenSilently({
          audience: `https://dev-artsite.eu.auth0.com/api/v2/`,
          scope: "read:current_user",
        });
        setAccessToken(tempAccessToken);
      }
      catch (e) {
        console.log(e.message);
      }
    })()

  }, []);

  useEffect(() => {
    if(accessToken != null){
      (async() => {
        try {
          const tempPrivateData = await fetch('/api/private', {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
          setPrivateData(tempPrivateData);
        }
        catch (e) {
          console.log(e.message);
        }
      })()
    }
  }, [accessToken])

  return (
    <div className="App">
      <header className="App-header">

      <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>

        <p>The current time is {currentTime}.</p>
        {/* {privateData && 
          <p>Private data: {privateData}</p>
        } */}
        <LogoutButton/>
        <LoginButton/>

      </header>
    </div>
  );
}

export default App;