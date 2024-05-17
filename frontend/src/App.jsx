import './App.css'
// import { Route, Routes } from 'react-router-dom';
// import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import About from './components/About/About';
import Contact from './components/Contact/Contact';
import Header from './components/Home/Header'
import Navbar from './components/Navbar/Navbar'

function App() {

return(
  <>
  <Navbar/>
  <Header/>
  </>
)
//   return <Router>
//     <Navbar />
//     <Header />
// {/*     
//   <Switch>
//     <Route exact path="/" component={Home} />
//     <Route path="/About/About" component={About} />
//   </Switch>
//   </Router> */}
}

export default App
