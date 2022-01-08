import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router , Routes, Route } from 'react-router-dom';

import Home from "./Pages/Home";
import Portfolio from "./Pages/Portfolio";
import Login from "./Pages/Login";
import Registration from './Pages/Registration';
import Profile from './Pages/Profile';

function App() {
  return (
      <div className='App'>
          <Router>
              <Routes>
                  <Route path="/" element={<Home/>} />
                  <Route path="/portfolio/:link" element={<Portfolio/>}/>
                  <Route path="/login" element={<Login/>}/>
                  <Route path="/registration" element={<Registration/>}/>
                  <Route path='/profile' element={<Profile/>}/>
              </Routes>
          </Router>
      </div>
  );
}

export default App;
