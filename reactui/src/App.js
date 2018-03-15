import React, { Component } from 'react'
import { Link, Navbar } from './generic_components.jsx'
import * as class_page from './class_page.jsx'
import logo from './logo.svg'
import './App.css'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = { pageName: 'welcome' }
    this.set = (obj => this.setState(obj)).bind(this)
  }
  componentDidMount() {
    window.MathJax.Hub.Queue(['Typeset', window.MathJax.Hub, 'root']);
  }
  componentDidUpdate() {
    window.MathJax.Hub.Queue(['Typeset', window.MathJax.Hub, 'root']);
  }
  render() {
    const pageSelector = function(_this) {
      switch (_this.state.pageName) {
        case 'welcome':
          return (
            <div className="container">
              <div className="row">
                <div className="col-lg-12 text-left">
                  <h1 className="mt-5">Benvenuto</h1>
                  <p>
                    Da qui puoi accedere alle singole pagine di ogni classe dove troverai esercizi suddivisi per
                    tipologia.
                  </p>
                  <ul className="list-unstyled">
                    <li>
                      <Link text="Classe prima" lambda={() => _this.set({ pageName: 'classe_prima' })} />
                    </li>
                  </ul>
                  {/* <p class="lead">Complete with pre-defined file paths and responsive navigation!</p> */}
                  {/* <ul class="list-unstyled">
                    <li>Bootstrap 4.0.0</li>
                    <li>jQuery 3.3.0</li>
                  </ul> */}
                </div>
              </div>
            </div>
          )
          break
        case 'classe_prima':
          return class_page.classePrima(_this)
          break
        default:
          return (
            <div class="container">
              <div class="row">
                <div class="col-lg-12">
                  <h1 class="mt-5">Errore</h1>
                  <p>Per qualche motivo inspiegabile c'è stato un errore...</p>
                </div>
              </div>
            </div>
          )
      }
    }
    return (
      <div className="App">
        <Navbar
          className="navbar navbar-expand-lg navbar-dark bg-dark fixed-top"
          brand={
            <a className="navbar-brand" href="#">
              Yamath
            </a>
          }
        />
        {pageSelector(this)}
      </div>
    )
  }
}

export default App
