import './App.css'
import { Route, Routes } from 'react-router-dom';
import { BrowserRouter } from 'react-router-dom';
import About from './components/About/About';
import Contact from './components/Contact/Contact';
import Header from './components/Home/Header';
import Navbar from './components/Navbar/Navbar';
import SignIn from './components/Signin/Signin';

const App = () => {
  return (
    <>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Header />} />
          <Route path="/about" element={<Header />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/signin" element={<SignIn />} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
