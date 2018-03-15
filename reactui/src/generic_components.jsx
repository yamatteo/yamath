import React, { Component } from 'react'

export function Button(props) {
  const className = props.className !== undefined ? props.className : 'btn btn-primary'
  const text = props.text !== undefined ? props.text : 'Click me'
  const onClick = (() => {
    if (props.lambda) {
      return props.lambda
    } else if (props.action && props.dispatch) {
      return () => props.dispatch(props.action)
    } else {
      return () => alert('Button was clicked (no action)')
    }
  })()
  return (
    <button
      className={className}
      onClick={event => {
        event.preventDefault()
        onClick()
      }}
    >
      {text}
    </button>
  )
}
export function ButtonGroup(props) {
  const array = (function() {
    try {
      return props.values.split(' ')
    } catch (e) {
      return ['No values']
    }
  })()
  const selectedValue = props.selectedValue
  const className = props.className
  const actionGenerator = props.actionGenerator
  const lambdaGenerator = props.lambdaGenerator
  const dispatch = props.dispatch
  if (actionGenerator && dispatch && !lambdaGenerator) {
    return (
      <div className="btn-group" role="group">
        {array.map(value => (
          <Button
            key={value}
            className={className + (selectedValue === value ? ' active' : '')}
            text={value}
            action={actionGenerator(value)}
            dispatch={dispatch}
          />
        ))}
      </div>
    )
  } else if (!actionGenerator && lambdaGenerator) {
    return (
      <div className="btn-gro
            up" role="group">
        {array.map(value => (
          <Button
            key={value}
            className={className + (selectedValue === value ? ' active' : '')}
            text={value}
            lambda={lambdaGenerator(value)}
          />
        ))}
      </div>
    )
  }
}
export function Form(props) {
  const className = props.className
  const action = props.action
  const dispatch = props.dispatch
  const lambda = props.lambda
  const onSubmit = (function() {
    if (action && dispatch && !lambda) {
      return event => {
        event.preventDefault()
        dispatch(action())
      }
    } else if (!action && lambda) {
      return event => {
        event.preventDefault()
        lambda()
      }
    } else {
      return event => {
        alert('Form submitted with no action')
      }
    }
  })()
  const children = props.children instanceof Array ? props.children : [props.children]
  return (
    <form className={className} onSubmit={onSubmit}>
      {children.map(item => item)}
    </form>
  )
}
export function Input(props) {
  const className = props.className
  const type = props.type || 'text'
  const name = props.name
  const value = props.value
  const placeholder = props.placeholder || props.name
  const actionGenerator = props.actionGenerator
  const dispatch = props.dispatch
  const lambdaGenerator = props.lambdaGenerator
  const onChange = (function() {
    if (actionGenerator && dispatch && !lambdaGenerator) {
      return event => dispatch(actionGenerator(event.target.value, name))
    } else if (!actionGenerator && lambdaGenerator !== undefined) {
      return event => {
        lambdaGenerator(event, name)()
      }
    } else {
      return event => {
        alert('Value changed with no action')
      }
    }
  })()
  return (
    <input className={className} name={name} type={type} value={value} placeholder={placeholder} onChange={onChange} />
  )
}
export function Link(props) {
  const className = props.className
  const text = props.text || 'Link (missing text)'
  const onClick = (() => {
    if (props.lambda && !props.action) {
      return props.lambda
    } else if (!props.lambda && props.action && props.dispatch) {
      return () => props.dispatch(props.action)
    } else {
      return () => alert('Link was clicked (no action)')
    }
  })()
  return (
    <a
      className={className}
      href="#"
      onClick={event => {
        event.preventDefault()
        onClick()
      }}
    >
      {text}
    </a>
  )
}
export function Navbar(props) {
  const className = (() => {
    if (props.className) {
      return props.className
    }
    let name = 'navbar navbar-expand'
    if (props.extraClassName !== undefined) {
      name += ' '
      name += props.extraClassName
    }
    return name
  })()
  const children = props.children instanceof Array ? props.children : [props.children]
  const brand = props.brand
  const links = children
  const rightAligned = (props.rightAligned instanceof Array ? props.rightAligned : [props.rightAligned])
  // const buttons = children.filter(child => child.type.name === "Button");
  // console.log("className", className);
  // console.log("Navbar children", props.children);
  return (
    <nav className={className}>
      <div className="container">
        {brand}
        <button
          className="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarResponsive"
          aria-controls="navbarResponsive"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>
        <div className="collapse navbar-collapse">
          <ul className="navbar-nav mr-auto">{links.map(link => <li className="nav-item">{link}</li>)}</ul>
        </div>
        <div className="collapse navbar-collapse">
          <ul className="navbar-nav ml-auto">{rightAligned.map(link => <li className="nav-item">{link}</li>)}</ul>
        </div>
      </div>
    </nav>
  )
}
export function Title(props) {
  return (
    <div className="jumbotron">
      <div className="container">
        <h1 className="display-3">{props.title}</h1>
      </div>
    </div>
  )
}
