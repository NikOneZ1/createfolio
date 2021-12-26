import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router , Routes, Route } from 'react-router-dom';

import Home from "./Pages/Home"
import Portfolio from "./Pages/Portfolio"

function App() {
  return (
      <div className='App'>
          <Router>
              <Routes>
                  <Route path="/" element={<Home/>} />
                  <Route path="/portfolio/:link" element={<Portfolio/>}/>
              </Routes>
          </Router>
      </div>
  );
}

export default App;
