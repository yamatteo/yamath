import React, { Component } from 'react'
import { Link, Navbar } from './generic_components.jsx'
import { PageSelector } from './pages/selector.jsx'
import logo from './logo.svg'
import './App.css'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = { pageState: { pageName: 'classe_prima' } }
    // this.set = (obj => this.setState(obj)).bind(this)
    // this.path_set = function set(path, value, prevState) {
    // // console.log('path_set', path, value);
    // const array = path.split('/')
    // const nextStateByArray = function(prevState, array, value) {
    //   // console.log('prevState', prevState)
    //   // console.log('array', array);
    //   let nextState = JSON.parse(JSON.stringify(prevState))
    //   if (array.length == 1) {
    //     nextState[array[0]] = value
    //   } else {
    //     const subState = prevState[array[0]] || {}
    //     nextState[array[0]] = nextStateByArray(subState, array.slice(1), value)
    //   }
    //   // console.log('retrning', nextState);
    //   return nextState
    // }
    //   const state = prevState || this.state
    //   const nextState = nextStateByArray(state, array, value)
    //   this.setState(nextState)
    //   return nextState
    // }.bind(this)
    this.arraySetState = this.arraySetState.bind(this)
    this.handleKeyPress = this.handleKeyPress.bind(this)
  }
  arraySetState(array, value, prevState) {
    const _array_set_state = function(array, value, prevState) {
      const nextState = JSON.parse(JSON.stringify(prevState))
      if (array.length == 1) {
        nextState[array[0]] = value
      } else {
        const subState = prevState[array[0]] || {}
        nextState[array[0]] = _array_set_state(array.slice(1), value, subState)
      }
      return nextState
    }
    let nextState = {}
    if (prevState == undefined) {
      nextState = _array_set_state(array, value, this.state)
    } else {
      nextState = _array_set_state(array, value, prevState)
    }
    this.setState(nextState)
    return new Promise((resolve, reject) => resolve(nextState))
  }
  componentDidMount() {
    try {
      window.MathJax.Hub.Queue(['Typeset', window.MathJax.Hub, 'root'])
    } catch (e) {
      ;
    }
    document.addEventListener('keydown', this.handleKeyPress, false)
  }
  componentDidUpdate() {
    try {
      window.MathJax.Hub.Queue(['Typeset', window.MathJax.Hub, 'root'])
    } catch (e) {
      ;
    }
  }
  handleKeyPress(event) {
    if (event.key == 'Insert') {
      if (this.state.experimental) {
        this.setState({ experimental: false })
      } else {
        this.setState({ experimental: true })
      }
    }
  }
  render() {
    return (
      <div className="App">
        <Navbar
          className="navbar navbar-expand navbar-dark bg-dark"
          // className="navbar navbar-expand-lg navbar-dark bg-dark fixed-top"
          brand={
            <Link
              className="navbar-brand"
              lambda={() => this.arraySetState(['pageState'], { pageName: 'welcome' })}
              text={this.state.experimental ? 'Xper' : 'Yamath'}
            />
          }
        >
          {/* {this.state.experimental && (
            <Link
              className="nav-link"
              lambda={() => this.setState({ pageName: 'question', questionId: '5ab13d73ce616410a749cd06' })}
              text="question"
            />
          )} */}
        </Navbar>
        <PageSelector app={this} />
      </div>
    )
  }
}

export default App
