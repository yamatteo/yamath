import React, { Component } from 'react'
import { Link, Navbar } from './generic_components.jsx'
import { PageSelector } from './pages/selector.jsx'
import * as class_page from './class_page.jsx'
import logo from './logo.svg'
import './App.css'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = { pageName: 'welcome' }
    this.set = (obj => this.setState(obj)).bind(this)
    this.handleKeyPress = this.handleKeyPress.bind(this)
  }
  componentDidMount() {
    window.MathJax.Hub.Queue(['Typeset', window.MathJax.Hub, 'root']);
    document.addEventListener("keydown", this.handleKeyPress, false);
  }
  componentDidUpdate() {
    window.MathJax.Hub.Queue(['Typeset', window.MathJax.Hub, 'root']);
  }
  handleKeyPress(event) {
    if(event.key == 'Insert'){
      if (this.state.experimental) {
        this.set({experimental: false})
      } else {
        this.set({experimental: true})
      }
    }
  }
  render() {
    return (
      <div className="App">
        <Navbar
          className="navbar navbar-expand-lg navbar-dark bg-dark fixed-top"
          brand={
            <Link className='navbar-brand' lambda={() => this.set({pageName:'welcome'})} text='Yamath'/>
          }
        />
        <PageSelector app={this}/>
      </div>
    )
  }
}

export default App
