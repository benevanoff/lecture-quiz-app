import './App.css'
import { BrowserRouter } from 'react-router-dom';
import About from './components/About/About';
import Contact from './components/Contact/Contact';
import Header from './components/Home/Header'
import Navbar from './components/Navbar/Navbar'

function App() {
  return (<>

    <BrowserRouter>
    <Navbar />
    <br />
    <Header />
        <Route path="/about" component={About} />
        <Route path="/contact" component={Contact} />
    </BrowserRouter>

  </>)
}

export default App
