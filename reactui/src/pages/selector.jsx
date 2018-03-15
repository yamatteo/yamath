import React, { Component } from 'react'
import { LoginPage } from './login.jsx'
import { WelcomePage } from './welcome.jsx'
import { ClassePrima } from './classe_prima.jsx'
import { ClasseSeconda } from './classe_seconda.jsx'
import { ClasseTerza } from './classe_terza.jsx'
import { ClasseQuarta } from './classe_quarta.jsx'
import { ClasseQuinta } from './classe_quinta.jsx'

export function PageSelector(props) {
  const app = props.app
  const set = props.set || (props.app && props.app.set)
  const pageName = props.pageName || (props.app && props.app.state && props.app.state.pageName)
  const dict = {
    welcome: <WelcomePage set={set}/>,
    login: <LoginPage set={set}/>,
    classe_prima: <ClassePrima app={app}/>,
    classe_seconda: <ClasseSeconda app={app}/>,
    classe_terza: <ClasseTerza app={app}/>,
    classe_quarta: <ClasseQuarta app={app}/>,
    classe_quinta: <ClasseQuinta app={app}/>,
  }
  try {
    if (! dict[pageName] ) { throw 'KeyError' }
    return dict[pageName]
  } catch (e) {
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
