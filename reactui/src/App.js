import React, { Component } from 'react'
import { Link, Navbar } from './generic_components.jsx'
import { PageSelector } from './pages/selector.jsx'
import logo from './logo.svg'
import './App.css'


class App extends Component {
  constructor(props) {
    super(props)
    this.state = { pageName: 'welcome' }
    this.set = (obj => this.setState(obj)).bind(this)
    this.path_set = (function set(path, value) {
      console.log('path_set', path, value);
      const array = path.split('/')
      const nextStateByArray = function(prevState, array, value) {
        console.log('prevState', prevState)
        console.log('array', array);
        let nextState = JSON.parse(JSON.stringify(prevState))
        if (array.length==1) {
          nextState[array[0]] = value
        } else {
          const subState = prevState[array[0]] || {}
          nextState[array[0]] = nextStateByArray(subState, array.slice(1), value)
        }
        return nextState
      }
      this.setState(nextStateByArray(this.state, array, value))
    }).bind(this)
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
            <Link className='navbar-brand' lambda={() => this.set({pageName:'welcome'})} text={ this.state.experimental ? 'Xper' :'Yamath'}/>
          }
        >
          { this.state.experimental && (
            <Link className='nav-link' lambda={() => this.set({pageName: 'question', questionId:'5ab13d73ce616410a749cd06'})} text='question'/>
          )}
        </Navbar>
        <PageSelector app={this}/>
      </div>
    )
  }
}

export default App
