import React from 'react';
import ReactDOM from 'react-dom/client';
import './styling/designs/shard.css';
import './styling/themes/romanticxxx/romanticxxx.css';
import './index.css';
import AppView from './components/AppViews/BasicSinglePageAppView';
import reportWebVitals from './miscellaneous/reportWebVitals';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <AppView />
    </LocalizationProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
