import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { Auth0Provider } from "@auth0/auth0-react";
import Wrapper from './wrapper'

ReactDOM.render(
  <Auth0Provider
    domain="dev-artsite.eu.auth0.com"
    clientId="RhpGUoMtR5bfQWFNJ19u7TfB63Le8o3d"
    redirectUri={window.location.origin}
    audience="https://dev-artsite.eu.auth0.com/api/v2/"
    scope="read:current_user update:current_user_metadata"
  >
    <React.StrictMode>
      <Wrapper>
        <App />
      </Wrapper>
    </React.StrictMode>
  </Auth0Provider>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
