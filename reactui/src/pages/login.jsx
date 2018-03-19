import React, { Component } from 'react'
import { api } from '../fetch.jsx'
import { Form, Input } from '../generic_components.jsx'

export function LoginPage(props) {
  const app = props.app
  const pageState = props.pageState || app.state.pageState || {}
  const username = props.pageState && props.pageState.loginForm && props.pageState.loginForm.username
  const password = props.pageState && props.pageState.loginForm && props.pageState.loginForm.password
  return (
    <div className="container">
      <div className='row'>
        <div className='col-lg-12'>
        <h1 className='mt-5'>Benvenut@ eternauta</h1>
      <div>
        <p>Prima di procedere, inserisci nome utente e password:</p>
        <Form
          lambda={() => {
            api(
              '/api/login',
              {
                username: username,
                password: password,
              },
              {
                username: 'mockUser',
                fasthash: '0',
                isadmin: false,
              },
            ).then(res => {
              if (!res.erroneous) {
                app.set({ userState: Object.assign(res, { isSignedin: true, pageName: 'main' }) })
              } else {
                app.set({ userState: {} })
              }
            })
          }}
        >
          <div className="form-group">
            <label>Username</label>
            <Input
              name="username"
              className="form-control"
              type="text"
              value={username}
              lambda={event => {
                const value = event.target.value
                const new_pageState = Object.assign(pageState, { loginForm: { username: value, password: password } })
                console.log('from', event, 'gonna set', new_pageState)
                app.set({ pageState: new_pageState })
              }}
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <Input
              name="password"
              className="form-control"
              type="password"
              value={password}
              lambda={event => {
                const value = event.target.value
                const new_pageState = Object.assign(pageState, { loginForm: { username: username, password: value } })
                app.set({ pageState: new_pageState })
              }}
            />
          </div>
          <Input name="submit" className="btn btn-primary" type="submit" value="Accedi" />
        </Form>
      </div>
    </div>
    </div>
    </div>
  )
}
