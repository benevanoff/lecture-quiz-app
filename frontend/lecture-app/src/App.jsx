import './App.css'

import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './components/HeaderForHome';
import About from './components/About';
import Contact from './components/Contact';
import Header from './components/HeaderForHome/header'
import Navbar from './components/Navbar/Navbar'

function App() {
  return (<>
    <Navbar />
    <br />
    <Header />

    <Router>
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/about" component={About} />
        <Route path="/contact" component={Contact} />
      </Switch>
    </Router>

  </>)
}

export default App
